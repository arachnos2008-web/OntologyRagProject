"""
Day 2 offline structural checker -- JUDGES' TOOL (no Neo4j, no LLM, no internet).

Given a team's PATTERN REGISTRY (the list of regexes they adopted) and the DATASET they were given,
this rebuilds the same entity graph the starter notebook builds and answers, for every question in the
hidden and public packs: "would the grounding check call these two records CONNECTED?"

  adversarial question  -> PASS if the two trap records are NOT connected
  positive control      -> PASS if the two shared records ARE connected

Datasets live in day2_datasets/ds_<ID>.py:  ORD, HR, RISK, PAY, CLN (the five team starters) and CAMPUS (reference).

Usage:
    python day2_offline_check.py                              # built-in sample registries for every dataset
    python day2_offline_check.py team_registry.json --dataset ORD   # JSON list of {"name":..., "regex":...}
"""
import re, sys, json, os, importlib.util
from collections import defaultdict, deque

HERE = os.path.dirname(os.path.abspath(__file__))
DS_DIR = os.path.join(HERE, "day2_datasets")
DATASET_IDS = ["ORD", "HR", "RISK", "PAY", "CLN", "CAMPUS"]
MAX_HOPS = 6   # matches shortestPath((a)-[*..6]-(b)) in the notebooks

DS = None      # the active dataset (a module); set with set_dataset()
G = {}         # active packs, keyed PUBLIC_ADVERSARIAL / PUBLIC_POSITIVE / HIDDEN_ADVERSARIAL / HIDDEN_POSITIVE
TEXTS, K1, K2 = [], {}, {}


def load_dataset(did):
    did = did.upper()
    path = os.path.join(DS_DIR, f"ds_{did}.py")
    if not os.path.exists(path):
        raise SystemExit(f"Unknown dataset {did!r}. Known: {', '.join(DATASET_IDS)}")
    spec = importlib.util.spec_from_file_location(f"ds_{did}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def set_dataset(did):
    """Select the dataset all other functions use. Returns the dataset module."""
    global DS, TEXTS, K1, K2
    DS = load_dataset(did)
    TEXTS, K1, K2 = DS.texts, DS.KIND1_PATTERNS, DS.KIND2_PATTERNS
    G.clear()
    for k in ("PUBLIC_ADVERSARIAL", "PUBLIC_POSITIVE", "HIDDEN_ADVERSARIAL", "HIDDEN_POSITIVE"):
        G[k] = getattr(DS, k)
    return DS


def build_graph(patterns):
    """patterns: list of {"name": str, "regex": str}. Returns adjacency over Event/Entity nodes."""
    adj = defaultdict(set)
    for i, text in enumerate(TEXTS):
        ev = ("Event", i)
        adj[ev]
        for p in patterns:
            for m in re.finditer(p["regex"], text):
                ent = (p["name"], m.group(1))
                adj[ev].add(ent)
                adj[ent].add(ev)
    return adj


def hops(adj, a, b):
    if a == b:
        return 0
    seen, q = {a}, deque([(a, 0)])
    while q:
        node, d = q.popleft()
        if d >= MAX_HOPS:
            continue
        for nb in adj[node]:
            if nb == b:
                return d + 1
            if nb not in seen:
                seen.add(nb)
                q.append((nb, d + 1))
    return None


def connected(adj, text_a, text_b):
    return hops(adj, ("Event", TEXTS.index(text_a)), ("Event", TEXTS.index(text_b))) is not None


def evaluate(patterns, pack, records_key):
    adj = build_graph(patterns)
    rows = []
    for t in pack:
        a, b = t[records_key]
        conn = connected(adj, a, b)
        passed = conn if t["expect_connected"] else (not conn)
        rows.append({"id": t["id"], "connected": conn, "pass": passed, "kind2": t.get("kind2_trap") or t.get("kind", "") or ""})
    return rows


def pct(rows):
    return round(100 * sum(r["pass"] for r in rows) / len(rows)) if rows else 0


def report(name, patterns):
    ha = evaluate(patterns, G["HIDDEN_ADVERSARIAL"], "trap_records")
    hp = evaluate(patterns, G["HIDDEN_POSITIVE"], "shared_records")
    pa = evaluate(patterns, G["PUBLIC_ADVERSARIAL"], "trap_records")
    pp = evaluate(patterns, G["PUBLIC_POSITIVE"], "shared_records")
    names = {p["name"] for p in patterns}
    k1_cov = sorted(n for n in K1 if n in names)
    k2_used = sorted(n for n in K2 if n in names)
    print(f"\n=== {name}  [dataset {DS.META['id']}] ===")
    print(f" patterns adopted: {sorted(names)}")
    print(f" Kind 1 covered ({len(k1_cov)}/{len(K1)}): {k1_cov} | Kind 2 adopted: {k2_used or 'none'}")
    for label, rows in (("HIDDEN adversarial", ha), ("HIDDEN positive", hp), ("PUBLIC adversarial", pa), ("PUBLIC positive", pp)):
        marks = " ".join(f"{r['id']}:{'1' if r['pass'] else '0'}" for r in rows)
        print(f" {label:19s} {pct(rows):3d}%  {marks}")
        for r in rows:
            if not r["pass"]:
                what = "falsely CONNECTED" if r["connected"] else "NOT connected (missed link)"
                print(f"     fail {r['id']}: {what}  [{r['kind2']}]")
    return {"hidden_adv": ha, "hidden_pos": hp, "public_adv": pa, "public_pos": pp,
            "k1_cov": k1_cov, "k2_used": k2_used}


def sample_registries():
    """Generic samples for the active dataset: starter only, full reference, over-eager (adds every Kind 2)."""
    kinds1 = list(K1)
    return {
        "Starter as shipped (given family only)": [{"name": DS.GIVEN, "regex": K1[DS.GIVEN]}],
        "Full reference (all Kind 1, no Kind 2)": [{"name": n, "regex": K1[n]} for n in kinds1],
        "Over-eager (given + a ticket + every Kind 2)": [{"name": DS.GIVEN, "regex": K1[DS.GIVEN]}, {"name": kinds1[-1], "regex": K1[kinds1[-1]]}]
                                                      + [{"name": k, "regex": r} for k, r in K2.items()],
    }


# ---- campus-only samples used in the earlier rehearsal (kept so old commands still work)
CAMPUS_SAMPLES = {
    "Ananya  (Student + Alumnus + Club + Ticket)": ("Student", "Alumnus", "Club", "Ticket"),
    "Rahul   (Student + Ticket + Room + Amount + Block + Semester)": ("Student", "Ticket", "Room", "Amount", "Block", "Semester"),
    "Priya   (Student + Alumnus)": ("Student", "Alumnus"),
    "Meera   (Student + Club + Ticket; lookup table, no Neo4j)": ("Student", "Club", "Ticket"),
}

if __name__ == "__main__":
    args = sys.argv[1:]
    did = "CAMPUS"
    if "--dataset" in args:
        i = args.index("--dataset")
        did = args[i + 1]
        del args[i:i + 2]
    set_dataset(did)
    if args:
        reg = json.load(open(args[0]))
        report(os.path.basename(args[0]), reg)
    else:
        for d in ([did] if "--dataset" in sys.argv else DATASET_IDS):
            set_dataset(d)
            for name, reg in sample_registries().items():
                report(name, reg)
            if d == "CAMPUS":
                allp = {**K1, **K2}
                for name, names in CAMPUS_SAMPLES.items():
                    report(name, [{"name": n, "regex": allp[n]} for n in names])
