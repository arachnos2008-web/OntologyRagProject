"""Dataset CAMPUS -- the original Day 2 dataset (campus operations & student services), exposed in the same shape as the
other datasets. Used for the sample submissions and as the Day 1 reference. JUDGES ONLY: contains the hidden pack."""
import os, runpy
_g = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "day2_dataset_generator.py"))
META = dict(id="CAMPUS", name="Campus operations & student services (reference)", domain="campus operations and student services",
            blurb="The reference dataset used in the sample submissions.")
CATEGORIES = _g["campus_categories"]; texts = _g["campus_texts"]; labels = _g["campus_labels"]
KNOWN_OVERLAP_PAIRS = _g["KNOWN_OVERLAP_PAIRS"]
KIND1_PATTERNS = _g["KIND1_PATTERNS"]; KIND2_PATTERNS = _g["KIND2_PATTERNS"]
GIVEN, GUIDED = "Student", "Alumnus"
for _n in ("PUBLIC_ADVERSARIAL", "PUBLIC_POSITIVE", "HIDDEN_ADVERSARIAL", "HIDDEN_POSITIVE"):
    globals()[_n] = _g[_n]
