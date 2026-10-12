"""
Day 2 batch scorer -- JUDGES' TOOL (no Neo4j, no LLM, no internet).

Reads each team's PATTERN REGISTRY and the DATASET it was given (ORD, HR, RISK, PAY, CLN), runs that dataset's hidden
and public packs through day2_offline_check.py, and prints one row per team in the column order of the
'Batch Test Results' tab of day2_judging_scorecard.xlsx.

Accepts, for each team, either:
  * the submitted notebook (.ipynb)          -- reads PATTERNS and DATASET_ID safely (never runs the notebook)
  * a text file with the pasted output of the submission-summary cell (.txt)
    -- reads its  REGISTRY_JSON: [...]  line and its  DATASET_ID: XXX  line

The dataset is taken from the notebook's DATASET_ID. If it is missing, it is inferred from the records in the file.
Override with  --dataset ORD  (applies to every file in that run).

Checks it makes for you:
  * RECORDS MATCH: how many of the dataset's records are really in the notebook (a team that edited the data is flagged)
  * COPYING: pairs of teams whose pattern rationales ("why" text) are near-identical

Usage:
    python day2_score_submissions.py team_*.ipynb
    python day2_score_submissions.py --name "Team Phoenix" phoenix.ipynb
    python day2_score_submissions.py --dataset PAY notes_for_team7.txt
Outputs:
    * a readable report per team (dataset, what each pattern is, what failed)
    * batch_results_B.tsv  -- paste into the Batch Test Results tab at cell B5  (name .. H9)
    * batch_results_P.tsv  -- paste into the same tab at cell P5               (HP1 .. HP4)
      (two pastes, so the automatic % columns in between are not overwritten)
      The team name column carries the dataset in square brackets, e.g.  "Phoenix [ORD]".
"""
import ast, difflib, importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("day2_offline_check", os.path.join(HERE, "day2_offline_check.py"))
CK = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(CK)


def _source(cell):
    return "".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]


def read_notebook(path):
    nb = json.load(open(path, encoding="utf-8"))
    code = [_source(c) for c in nb["cells"] if c["cell_type"] == "code"]
    return code, "\n".join(code)


def registry_from_notebook(path):
    code, _ = read_notebook(path)
    for src in code:
        if "PATTERNS" not in src:
            continue
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "PATTERNS" for t in node.targets):
                value = ast.literal_eval(node.value)       # literals only: nothing from the notebook is executed
                return [{"name": p["name"], "regex": p["regex"], "kind": p.get("kind"), "why": p.get("why", "")} for p in value]
    raise ValueError("no PATTERNS = [...] list found")


def registry_from_text(path):
    for line in open(path, encoding="utf-8"):
        if line.strip().startswith("REGISTRY_JSON:"):
            return json.loads(line.split("REGISTRY_JSON:", 1)[1])
    raise ValueError("no REGISTRY_JSON: line found (the pasted output must include it; or give the notebook itself)")


def dataset_from_file(path):
    """Returns (dataset_id or None, how)."""
    if path.endswith(".ipynb"):
        _, blob = read_notebook(path)
        m = re.search(r"^DATASET_ID\s*=\s*[\"'](\w+)[\"']", blob, re.M)
    else:
        blob = open(path, encoding="utf-8").read()
        m = re.search(r"^DATASET_ID:\s*(\w+)", blob, re.M)
    if m and m.group(1).upper() in CK.DATASET_IDS:
        return m.group(1).upper(), "DATASET_ID in file"
    best, best_n = None, 0                      # fall back: which dataset's records are in the file?
    for did in CK.DATASET_IDS:
        ds = CK.load_dataset(did)
        n = sum(1 for t in ds.texts[:40] if t in blob)
        if n > best_n:
            best, best_n = did, n
    return (best, f"inferred from records ({best_n}/40 sampled)") if best_n >= 10 else (None, "not found")


def records_match(path, ds):
    if not path.endswith(".ipynb"):
        return None
    _, blob = read_notebook(path)
    # records appear as Python string literals; compare on repr-free text by checking each record is present in either quoting
    found = sum(1 for t in ds.texts if (t in blob) or (repr(t)[1:-1] in blob) or (t.replace("'", "\\'") in blob) or (t.replace('"', '\\"') in blob))
    return found, len(ds.texts)


def matches(regex):
    out = set()
    for i, t in enumerate(CK.TEXTS):
        for m in re.finditer(regex, t):
            out.add((i, m.group(1)))
    return out


def classify(pattern, refs):
    """What does this regex actually match? Compared with the reference patterns on the data."""
    mine = matches(pattern["regex"])
    if not mine:
        return "matches nothing", None
    best, best_frac = None, 0.0
    for name, (kind, rx) in refs.items():
        ref = matches(rx)
        frac = len(mine & ref) / len(mine)
        if frac > best_frac:
            best, best_frac = name, frac
    if best and best_frac >= 0.5:
        return f"{refs[best][0]}: {best}", best
    return "OTHER (review by hand)", None


def score_team(registry):
    K1, K2, GIVEN = CK.K1, CK.K2, CK.DS.GIVEN
    refs = {**{n: ("Kind 1", r) for n, r in K1.items()}, **{n: ("Kind 2", r) for n, r in K2.items()}}
    rows = {}
    for key, pack, rk in (("ha", CK.G["HIDDEN_ADVERSARIAL"], "trap_records"), ("hp", CK.G["HIDDEN_POSITIVE"], "shared_records"),
                          ("pa", CK.G["PUBLIC_ADVERSARIAL"], "trap_records"), ("pp", CK.G["PUBLIC_POSITIVE"], "shared_records")):
        rows[key] = CK.evaluate(registry, pack, rk)
    cls = [(p["name"], *classify(p, refs)) for p in registry]
    k1_added = sorted({ref for _, _, ref in cls if ref in K1 and ref != GIVEN})
    k2_used = sorted({ref for _, _, ref in cls if ref in K2})
    other = [n for n, label, ref in cls if label.startswith("OTHER")]
    return rows, cls, k1_added, k2_used, other


def main(argv):
    args, name_override, ds_override = [], None, None
    it = iter(argv)
    for a in it:
        if a == "--name":
            name_override = next(it)
        elif a == "--dataset":
            ds_override = next(it).upper()
        else:
            args.append(a)
    if not args:
        print(__doc__)
        return 1
    tsv_b, tsv_p, whys = [], [], []
    for path in args:
        name = name_override or re.sub(r"^team_\d+_", "", os.path.splitext(os.path.basename(path))[0]).replace("_", " ").title()
        try:
            reg = registry_from_notebook(path) if path.endswith(".ipynb") else registry_from_text(path)
            for p in reg:
                re.compile(p["regex"])
        except Exception as e:
            print(f"\n=== {name}: COULD NOT READ REGISTRY ({type(e).__name__}: {e}) ===")
            continue
        did, how = (ds_override, "--dataset flag") if ds_override else dataset_from_file(path)
        if not did:
            print(f"\n=== {name}: DATASET NOT FOUND in {os.path.basename(path)}. Re-run with  --dataset ORD|HR|RISK|PAY|CLN ===")
            continue
        ds = CK.set_dataset(did)
        rows, cls, k1_added, k2_used, other = score_team(reg)
        print(f"\n=== {name} ({os.path.basename(path)}) | dataset {did}: {ds.META['name']} ({how}) ===")
        rm = records_match(path, ds)
        if rm:
            flag = "" if rm[0] >= rm[1] - 2 else "   <-- WARNING: records differ from the issued dataset; check by hand"
            print(f"  records in notebook matching dataset {did}: {rm[0]}/{rm[1]}{flag}")
        for pname, label, _ in cls:
            print(f"  pattern {pname:<12} -> {label}")
        print(f"  Kind 1 added beyond {ds.GIVEN}: {len(k1_added)} {k1_added}")
        print(f"  Kind 2 adopted: {len(k2_used) + len(other)} {k2_used}" + (f"  + UNRECOGNISED {other}: judge by hand" if other else ""))
        for label, key in (("HIDDEN adversarial", "ha"), ("HIDDEN positive", "hp"), ("PUBLIC adversarial", "pa"), ("PUBLIC positive", "pp")):
            r = rows[key]
            marks = " ".join(f"{x['id']}:{1 if x['pass'] else 0}" for x in r)
            print(f"  {label:<19} {CK.pct(r):>3}%  {marks}")
            for x in r:
                if not x["pass"]:
                    print(f"      fail {x['id']}: " + ("falsely CONNECTED" if x["connected"] else "NOT connected (missed link)"))
        h = [1 if x["pass"] else 0 for x in rows["ha"]]
        hp = [1 if x["pass"] else 0 for x in rows["hp"]]
        patterns = ", ".join(p["name"] for p in reg)
        tsv_b.append("\t".join([f"{name} [{did}]", patterns, str(len(k1_added)), str(len(k2_used) + len(other))] + [str(x) for x in h]))
        tsv_p.append("\t".join(str(x) for x in hp))
        whys.append((f"{name} [{did}]", " ".join(p.get("why", "") for p in reg).strip()))
    if tsv_b:
        ob, op = (os.path.join(os.getcwd(), f) for f in ("batch_results_B.tsv", "batch_results_P.tsv"))
        open(ob, "w", encoding="utf-8").write("\n".join(tsv_b) + "\n")
        open(op, "w", encoding="utf-8").write("\n".join(tsv_p) + "\n")
        print(f"\nWrote {ob}\n  -> paste into 'Batch Test Results' at cell B5:  Team Name | Patterns | Kind 1 added | Kind 2 adopted | H1..H9")
        print(f"Wrote {op}\n  -> paste into the same tab at cell P5:  HP1..HP4")
        print("(Team # in column A and the auto % columns stay as they are. Add judge name and notes by hand.)")
    pairs = []
    for i in range(len(whys)):
        for j in range(i + 1, len(whys)):
            a, b = whys[i][1], whys[j][1]
            if len(a) > 80 and len(b) > 80:
                r = difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()
                if r >= 0.85:
                    pairs.append((r, whys[i][0], whys[j][0]))
    print("\n=== COPYING CHECK (pattern rationales) ===")
    if pairs:
        for r, a, b in sorted(pairs, reverse=True):
            print(f"  {a}  ~  {b}: {r:.0%} similar rationale text -> read both before scoring the rationale")
    else:
        print("  no pair of rationales is more than 85% similar")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
