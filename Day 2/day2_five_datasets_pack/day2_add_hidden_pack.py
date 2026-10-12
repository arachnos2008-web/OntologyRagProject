"""
Appends the HIDDEN question pack to a team's submitted notebook so you can run it live.
JUDGES' TOOL. Never share the output with teams.

The dataset is read from the notebook's DATASET_ID (ORD, HR, RISK, PAY, CLN); add  --dataset ORD  to override.

Usage:
    python day2_add_hidden_pack.py team_1_ananya.ipynb            # writes team_1_ananya_HIDDEN.ipynb
    python day2_add_hidden_pack.py day2_starters/starter_ORD_orders_inventory_delivery_no_neo4j.ipynb --baseline-only
        # pilot: runs ONLY the plain baseline on the hidden pack (no graph needed), to see how often it fabricates
Then open the new notebook (Colab or Jupyter), set the LLM key / Neo4j secrets as the team did,
and Run all. The last two cells run the 9 hidden adversarial and 4 hidden positive questions.
Needs:  pip install nbformat
"""
import os, re, sys, pprint, importlib.util
import nbformat
from nbformat.v4 import new_markdown_cell as md, new_code_cell as code

HERE = os.path.dirname(os.path.abspath(__file__))
IDS = ["ORD", "HR", "RISK", "PAY", "CLN", "CAMPUS"]


def load_dataset(did):
    spec = importlib.util.spec_from_file_location(f"ds_{did}", os.path.join(HERE, "day2_datasets", f"ds_{did}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def detect_dataset(nb):
    blob = "\n".join(c.source for c in nb.cells if c.cell_type == "code")
    m = re.search(r"^DATASET_ID\s*=\s*[\"'](\w+)[\"']", blob, re.M)
    if m and m.group(1).upper() in IDS:
        return m.group(1).upper()
    for did in IDS:                                  # older notebooks: recognise the campus records
        ds = load_dataset(did)
        if sum(1 for t in ds.texts[:30] if t in blob) >= 10:
            return did
    raise SystemExit("Could not tell which dataset this notebook uses. Re-run with  --dataset ORD|HR|RISK|PAY|CLN")


def hidden_cell(ds):
    return ("HIDDEN_ADVERSARIAL = " + pprint.pformat(ds.HIDDEN_ADVERSARIAL, width=100, sort_dicts=False)
            + "\n\nHIDDEN_POSITIVE = " + pprint.pformat(ds.HIDDEN_POSITIVE, width=100, sort_dicts=False)
            + '\n\nprint(f"Hidden pack: {len(HIDDEN_ADVERSARIAL)} adversarial + {len(HIDDEN_POSITIVE)} positive-control questions")')

NOTE = """## JUDGES: hidden pack (appended)

For each question read three lines: the baseline answer, the grounded answer, and the graph verdict (PASS/FAIL).
Score the question **1** if the team's grounded answer is right: for an adversarial question it says there is no recorded link; for a positive control it says the records are connected and names what they share. Score **0** otherwise.
Usually this equals the graph verdict. If the wording contradicts the verdict (for example the graph says NOT CONNECTED but the answer still asserts a link), score by the answer and note it."""


BASELINE_NOTE = """## PILOT: baseline on the hidden pack (appended)

Reads each baseline answer next to what a correct answer must say. Count an adversarial question as **fabricated** if the baseline asserts a link
that the records do not support; count a positive control as **missed** if it denies a link that exists.
This shows how often the starter's baseline fails visibly, which is what the Day 2 contrast depends on."""

BASELINE_RUN = """def run_baseline_only(pack, label):
    print(f"==== {label} ====")
    for t in pack:
        ans = baseline_rag_answer(t["question"])
        print(f"[{t['id']}] {t['question']}")
        print("   Baseline :", ans["answer"][:400].replace("\\n", " "))
        print("   Must say :", t["correct_answer_must_state"][:220])
        print("   Expected :", "CONNECTED" if t["expect_connected"] else "NOT connected")
        print()

run_baseline_only(HIDDEN_ADVERSARIAL, "HIDDEN adversarial: did the baseline fabricate a link?")
run_baseline_only(HIDDEN_POSITIVE, "HIDDEN positive controls: did the baseline deny a real link?")"""


def main(path, baseline_only=False, dataset=None):
    nb = nbformat.read(path, as_version=4)
    did = dataset or detect_dataset(nb)
    ds = load_dataset(did)
    print("Dataset:", did, "-", ds.META["name"])
    HIDDEN_CELL = hidden_cell(ds)
    if baseline_only:
        nb.cells += [md(BASELINE_NOTE), code(HIDDEN_CELL), code(BASELINE_RUN)]
    else:
        nb.cells += [md(NOTE), code(HIDDEN_CELL),
                     code("hid_adv = run_pack(HIDDEN_ADVERSARIAL)"),
                     code("hid_pos = run_pack(HIDDEN_POSITIVE)")]
    out = os.path.splitext(path)[0] + "_HIDDEN.ipynb"
    nbformat.write(nb, out)
    print("Wrote", out)


if __name__ == "__main__":
    argv = sys.argv[1:]
    ds_override = None
    if "--dataset" in argv:
        i = argv.index("--dataset")
        ds_override = argv[i + 1].upper()
        del argv[i:i + 2]
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__); sys.exit(1)
    main(args[0], baseline_only="--baseline-only" in sys.argv, dataset=ds_override)
