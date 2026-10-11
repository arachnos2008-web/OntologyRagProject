"""
Day 2 batch scorer -- JUDGES' TOOL (no Neo4j, no LLM, no internet).

Reads each team's PATTERN REGISTRY, runs the hidden and public packs through
day2_offline_check.py, and prints one row per team in the column order of the
'Batch Test Results' tab of day2_judging_scorecard.xlsx.

Accepts, for each team, either:
  * the submitted notebook (.ipynb)          -- reads the PATTERNS list safely (never runs the notebook)
  * a text file with the pasted output of the submission-summary cell (.txt)
    -- reads its  REGISTRY_JSON: [...]  line

Usage:
    python day2_score_submissions.py team_1_ananya.ipynb team_2_rahul.ipynb notes_for_team3.txt
    python day2_score_submissions.py --name "Team Phoenix" phoenix.ipynb
Outputs:
    * a readable report per team (what each pattern is, what failed)
    * batch_results_B.tsv  -- paste into the Batch Test Results tab at cell B5  (name .. H9)
    * batch_results_P.tsv  -- paste into the same tab at cell P5               (HP1 .. HP4)
      (two pastes, so the automatic % columns in between are not overwritten)
"""
import ast, json, os, re, sys, runpy

HERE = os.path.dirname(os.path.abspath(__file__))
CK = runpy.run_path(os.path.join(HERE, "day2_offline_check.py"))
G, K1, K2 = CK["G"], CK["K1"], CK["K2"]
TEXTS = G["campus_texts"]
REFS = {**{n: ("Kind 1", r) for n, r in K1.items()}, **{n: ("Kind 2", r) for n, r in K2.items()}}


def registry_from_notebook(path):
    nb = json.load(open(path, encoding="utf-8"))
    for cell in nb["cells"]:
        if cell["cell_type"] != "code":
            continue
        src = "".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]
        if "PATTERNS" not in src:
            continue
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "PATTERNS" for t in node.targets):
                value = ast.literal_eval(node.value)       # literals only: nothing from the notebook is executed
                return [{"name": p["name"], "regex": p["regex"], "kind": p.get("kind")} for p in value]
    raise ValueError("no PATTERNS = [...] list found")


def registry_from_text(path):
    for line in open(path, encoding="utf-8"):
        if line.strip().startswith("REGISTRY_JSON:"):
            return json.loads(line.split("REGISTRY_JSON:", 1)[1])
    raise ValueError("no REGISTRY_JSON: line found (the pasted output must include it; "
                     "or give the notebook itself)")


def matches(regex):
    out = set()
    for i, t in enumerate(TEXTS):
        for m in re.finditer(regex, t):
            out.add((i, m.group(1)))
    return out


def classify(pattern):
    """What does this regex actually match? Compared with the reference patterns on the data."""
    mine = matches(pattern["regex"])
    if not mine:
        return "matches nothing", None
    best, best_frac = None, 0.0
    for name, (kind, rx) in REFS.items():
        ref = matches(rx)
        frac = len(mine & ref) / len(mine)
        if frac > best_frac:
            best, best_frac = name, frac
    if best and best_frac >= 0.5:
        return f"{REFS[best][0]}: {best}", best
    return "OTHER (review by hand)", None


def score_team(name, registry):
    rows = {}
    for key, pack, rk in (("ha", G["HIDDEN_ADVERSARIAL"], "trap_records"), ("hp", G["HIDDEN_POSITIVE"], "shared_records"),
                          ("pa", G["PUBLIC_ADVERSARIAL"], "trap_records"), ("pp", G["PUBLIC_POSITIVE"], "shared_records")):
        rows[key] = CK["evaluate"](registry, pack, rk)
    cls = [(p["name"], *classify(p)) for p in registry]
    k1_added = sorted({ref for _, _, ref in cls if ref in K1 and ref != "Student"})
    k2_used = sorted({ref for _, _, ref in cls if ref in K2})
    other = [n for n, label, ref in cls if label.startswith("OTHER")]
    return rows, cls, k1_added, k2_used, other


def main(argv):
    args, name_override = [], None
    it = iter(argv)
    for a in it:
        if a == "--name":
            name_override = next(it)
        else:
            args.append(a)
    if not args:
        print(__doc__)
        return 1
    tsv_b, tsv_p = [], []
    for path in args:
        name = name_override or re.sub(r"^team_\d+_", "", os.path.splitext(os.path.basename(path))[0]).replace("_", " ").title()
        try:
            reg = registry_from_notebook(path) if path.endswith(".ipynb") else registry_from_text(path)
            for p in reg:
                re.compile(p["regex"])
        except Exception as e:
            print(f"\n=== {name}: COULD NOT READ REGISTRY ({type(e).__name__}: {e}) ===")
            continue
        rows, cls, k1_added, k2_used, other = score_team(name, reg)
        print(f"\n=== {name} ({os.path.basename(path)}) ===")
        for pname, label, _ in cls:
            print(f"  pattern {pname:<12} -> {label}")
        print(f"  Kind 1 added beyond Student: {len(k1_added)} {k1_added}")
        print(f"  Kind 2 adopted: {len(k2_used) + len(other)} {k2_used}" + (f"  + UNRECOGNISED {other}: judge by hand" if other else ""))
        for label, key in (("HIDDEN adversarial", "ha"), ("HIDDEN positive", "hp"), ("PUBLIC adversarial", "pa"), ("PUBLIC positive", "pp")):
            r = rows[key]
            marks = " ".join(f"{x['id']}:{1 if x['pass'] else 0}" for x in r)
            print(f"  {label:<19} {CK['pct'](r):>3}%  {marks}")
            for x in r:
                if not x["pass"]:
                    print(f"      fail {x['id']}: " + ("falsely CONNECTED" if x["connected"] else "NOT connected (missed link)"))
        h = [1 if x["pass"] else 0 for x in rows["ha"]]
        hp = [1 if x["pass"] else 0 for x in rows["hp"]]
        patterns = ", ".join(p["name"] for p in reg)
        tsv_b.append("\t".join([name, patterns, str(len(k1_added)), str(len(k2_used) + len(other))] + [str(x) for x in h]))
        tsv_p.append("\t".join(str(x) for x in hp))
    if tsv_b:
        ob, op = (os.path.join(os.getcwd(), f) for f in ("batch_results_B.tsv", "batch_results_P.tsv"))
        open(ob, "w", encoding="utf-8").write("\n".join(tsv_b) + "\n")
        open(op, "w", encoding="utf-8").write("\n".join(tsv_p) + "\n")
        print(f"\nWrote {ob}\n  -> paste into 'Batch Test Results' at cell B5:  Team Name | Patterns | Kind 1 added | Kind 2 adopted | H1..H9")
        print(f"Wrote {op}\n  -> paste into the same tab at cell P5:  HP1..HP4")
        print("(Team # in column A and the auto % columns stay as they are. Add judge name and notes by hand.)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
