# day2_datasets — JUDGES ONLY (contains every hidden pack)

Do not publish this folder, the reference solutions, `day2_offline_check.py`, `day2_score_submissions.py`,
`day2_add_hidden_pack.py` or the scorecard in a repository teams can read.

| Code | Dataset | Records | Given | Guided (PP3) | Other Kind 1 | Kind 2 traps (hidden H7/H8/H9; public P5/P6/P7) |
|---|---|---|---|---|---|---|
| ORD | Order / inventory / delivery | 142 | Order | Customer | Driver, Return (RMA-nnnn) | H7 Dock 9, H8 500 units, H9 holiday season; P5 Dock 4, P6 Zone B, P7 240 units |
| HR | Employee / contractor / manager | 141 | Employee | Contractor | Manager, Case (HRC-nnnn) | H7 Floor 8, H8 3000 dollars, H9 Q3 appraisal; P5 Floor 5, P6 Grade L3, P7 800 dollars |
| RISK | Risk / incident / problem | 141 | Incident | Problem | Risk (R-nn), Change (CHG-nnnn) | H7 Rack 22, H8 450 users, H9 month-end close; P5 Rack 14, P6 Severity 2, P7 300 users |
| PAY | Payment / shipment / invoice | 138 | Invoice | Shipment | Payment (PMT), PO (PO-nnnn) | H7 Port Rotterdam, H8 8500 euros, H9 quarter-end settlement; P5 Port Chennai, P6 net 30 terms, P7 12000 euros |
| CLN | Patient / prescription / clinician | 141 | Patient | Prescription | Clinician (DRnn), Lab (LAB-nnnn) | H7 Ward 3, H8 250 mg, H9 evening clinic; P5 Ward 6, P6 Wing B, P7 500 mg |
| CAMPUS | Campus operations (reference, Day 1 demo, sample submissions) | 179 | Student | Alumnus | Club, Ticket | H7 Room 118, H8 46000, H9 spring semester; P5 Room 214, P6 Block C, P7 500 rupees |

Each `ds_<CODE>.py` exports the records, the reference regexes (`KIND1_PATTERNS`, `KIND2_PATTERNS`), `K1_INFO`/`REJECTED`
(used by the reference solutions) and the four packs. Every pack question names its two records, so the structural verdict needs no LLM.

Every dataset has the identical structure (12 categories except CAMPUS, 4 Kind 1 families, 4 Kind 2 traps, 8+3 public and 9+4 hidden
questions), checked by the offline checker: given pattern only = hidden positives 1/4; all Kind 1 = 100%; adding each Kind 2 pattern breaks exactly
its own trap questions (H7/P5 place, P6 block-or-level, H8/P7 amount, H9 period).
