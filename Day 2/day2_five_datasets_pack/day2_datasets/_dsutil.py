"""Helpers shared by the dataset files (judges' side). Each ds_<ID>.py exports:
META, CATEGORIES, KIND1_PATTERNS, KIND2_PATTERNS, K1_INFO, REJECTED, GIVEN, GUIDED,
texts, labels, PUBLIC_ADVERSARIAL, PUBLIC_POSITIVE, HIDDEN_ADVERSARIAL, HIDDEN_POSITIVE."""

def flatten(categories):
    texts, labels = [], []
    for cat, sents in categories.items():
        for s in sents:
            texts.append(s)
            labels.append(cat)
    assert len(set(texts)) == len(texts), "duplicate record text: " + str([t for t in texts if texts.count(t) > 1][:3])
    return texts, labels

def finder(texts):
    def f(sub):
        hits = [t for t in texts if sub in t]
        assert len(hits) == 1, f"{sub!r} matched {len(hits)} records"
        return hits[0]
    return f

def adv(f, id, kind, question, subs, must, k2=None):
    d = {"id": id, "question": question, "trap_records": [f(s) for s in subs],
         "correct_answer_must_state": must, "expect_connected": False}
    if k2 is None:
        d["kind"] = kind
    else:
        d["kind2_trap"] = k2
    return d

def pos(f, id, question, ident, subs, must):
    return {"id": id, "question": question, "shared_identifier": ident,
            "shared_records": [f(s) for s in subs],
            "correct_answer_must_state": must, "expect_connected": True}
