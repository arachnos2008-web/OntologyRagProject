"""
Appends the HIDDEN question pack to a team's submitted notebook so you can run it live.
JUDGES' TOOL. Never share the output with teams.

Usage:
    python day2_add_hidden_pack.py team_1_ananya.ipynb            # writes team_1_ananya_HIDDEN.ipynb
Then open the new notebook (Colab or Jupyter), set the LLM key / Neo4j secrets as the team did,
and Run all. The last two cells run the 9 hidden adversarial and 4 hidden positive questions.
Needs:  pip install nbformat
"""
import os, sys, pprint, runpy
import nbformat
from nbformat.v4 import new_markdown_cell as md, new_code_cell as code

HERE = os.path.dirname(os.path.abspath(__file__))
G = runpy.run_path(os.path.join(HERE, "day2_dataset_generator.py"))

HIDDEN_CELL = ("HIDDEN_ADVERSARIAL = " + pprint.pformat(G["HIDDEN_ADVERSARIAL"], width=100, sort_dicts=False)
               + "\n\nHIDDEN_POSITIVE = " + pprint.pformat(G["HIDDEN_POSITIVE"], width=100, sort_dicts=False)
               + '\n\nprint(f"Hidden pack: {len(HIDDEN_ADVERSARIAL)} adversarial + {len(HIDDEN_POSITIVE)} positive-control questions")')

NOTE = """## JUDGES: hidden pack (appended)

For each question read three lines: the baseline answer, the grounded answer, and the graph verdict (PASS/FAIL).
Score the question **1** if the team's grounded answer is right: for an adversarial question it says there is no recorded link; for a positive control it says the records are connected and names what they share. Score **0** otherwise.
Usually this equals the graph verdict. If the wording contradicts the verdict (for example the graph says NOT CONNECTED but the answer still asserts a link), score by the answer and note it."""


def main(path):
    nb = nbformat.read(path, as_version=4)
    nb.cells += [md(NOTE), code(HIDDEN_CELL),
                 code("hid_adv = run_pack(HIDDEN_ADVERSARIAL)"),
                 code("hid_pos = run_pack(HIDDEN_POSITIVE)")]
    out = os.path.splitext(path)[0] + "_HIDDEN.ipynb"
    nbformat.write(nb, out)
    print("Wrote", out)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__); sys.exit(1)
    main(sys.argv[1])
