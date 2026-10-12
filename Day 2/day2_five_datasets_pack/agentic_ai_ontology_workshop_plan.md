# IEEE-CIS Amrita — Agentic AI + Knowledge Grounding Workshop
**Oct 14–15, 2026 · about 25 teams, five datasets (about five teams on each)**

---

## Day 1 — Oct 14, 8:30 AM–1:30 PM

Students bring a laptop, a Google account and **their own LLM API key from any provider**. Each team picks **one of five starter notebooks**, one per dataset (table below), and uses either a free **Neo4j Aura** instance (`starter_<code>.ipynb`, for example `starter_ORD.ipynb`) or, if Aura is not possible, the **no-Neo4j** version of the same starter (`starter_<code>_no_neo4j.ipynb`), which keeps the graph in ready-made lookup tables. The two versions differ only in the graph store. The five datasets differ only in their subject matter, records and questions: the registry task, the structure and the judging are identical. Cap each dataset at about five teams (a sign-up sheet at team formation) and seat teams on the same dataset apart.

| Time | Activity | Format |
|---|---|---|
| 8:30–8:45 | **Opening hook:** an AI agent confidently states a false fact by merging two unrelated records | Demo |
| 8:45–9:15 | **Embeddings and similarity search** | Demo (Week 1 notebook) |
| 9:15–9:45 | **RAG pipeline and where it breaks:** the exact conflated answer | Demo (Week 2 notebook) |
| 9:45–10:15 | **Grounding the agent:** same query, graph-backed, now correct | Demo (Week 3 notebook) |
| 10:15–10:30 | Break | Teams create their Aura instance, or pick the no-Neo4j starter |
| 10:30–12:30 | **Hands-on lab.** Open your dataset's starter in Colab and: (1) plug in your own LLM key by editing the `call_llm` cell; (2) connect Neo4j (skip this with the no-Neo4j version); (3) run the starter top to bottom; (4) add the dataset's guided pattern (table below) and watch public question PP3 flip from "no recorded link" to "connected" | Guided, mentors roaming |
| 12:30–12:45 | Buffer for stragglers | Mentors |
| 12:45–1:15 | **Day 2 problem statement, rubric, submission deadline, team formation** | You present |
| 1:15–1:30 | Build-window logistics, Q&A | |

---

## Day 2 — Oct 15, 2:00–3:30 PM (demo and judging only)

All building happens between the two days.

### Problem: "Complete the grounding"
*Build an agent that tells the truth about what it doesn't know.*

**Scenario.** Each team works on one of five operational datasets of about 140 records in 12 categories. Different departments describe different events in similar words. Some records carry an identifier (an order number, a patient ID, an invoice number...); where that ID repeats, it *is* the same event. The task is to tell the two cases apart.

| Code | Dataset | Given pattern | Guided in the lab (PP3) |
|---|---|---|---|
| ORD | Order / inventory / delivery | Order | Customer |
| HR | Employee / contractor / manager | Employee | Contractor |
| RISK | Risk / incident / problem | Incident | Problem |
| PAY | Payment / shipment / invoice | Invoice | Shipment |
| CLN | Patient / prescription / clinician | Patient | Prescription |

All five have the same shape, so scores are comparable: four Kind 1 families (one given, three to find), four Kind 2 traps, a public pack of 8 adversarial and 3 positive questions and a hidden pack of 9 and 4. The public and hidden questions, the identifiers and the regexes all differ between datasets, so a registry copied from a team on another dataset does not work. The campus dataset (Student / Alumnus / Club / Ticket) stays as the Day 1 demonstration and the reference.

**Given to each team (its dataset's starter).** Retrieval, a plain baseline RAG, graph building from a **pattern registry**, and a grounded answer step. The registry holds **one** pattern: the dataset's first ID regex (the "given pattern" in the table).

**Build window — each team**
1. Decides which other strings identify one event (**Kind 1**: person, case, order or document IDs) and which are incidental fields reused across unrelated events (**Kind 2**: a place, a level or block, an amount or count, a period).
2. Adds its patterns to the registry, each with an example and a reason, and lists the lookalikes it **rejected** and why.
3. Runs the **public pack** (8 adversarial + 3 positive-control questions) against baseline and grounded, and fills in an outcomes table: did the baseline fabricate, was the grounded answer correct, and why.
4. States **one failure it still has**.

**Extra work for every team.** Run on its own LLM provider (edit `call_llm`). Teams without Neo4j use the no-Neo4j version of their starter; nobody builds lookup tables, so everyone's effort goes into the registry.

**Deliverable.** The notebook, run top to bottom on a fresh runtime, with the registry, outcomes table and remaining-failure note filled in. **Deadline: 2 hours before the Day 2 session** (e.g., 12:00 PM).

**The lesson.** Too few patterns misses real links; too many invents false ones. Scoring well means understanding what makes an identifier an identifier.

### Rubric

| Criterion | Weight | Scored by |
|---|---|---|
| No fabricated connections | 30% | Hidden adversarial pack (9 questions), pass/fail each |
| Affirms real links | 20% | Hidden positive controls (4), pass/fail each |
| Pattern choices and rationale | 20% | Kind 1 coverage (40) + Kind 2 restraint (30) + rationale (30) |
| Explaining outcomes | 20% | Outcomes table complete, causes correct, one honest remaining failure |
| Runs end-to-end | 5% | Binary, fresh runtime |
| Live demo clarity | 5% | States the answer, cites record IDs, explains one row |

### Judging (two tiers)

- **Tier 1, batch (before 2:00 PM, 70% of the rubric).** Run `python day2_score_submissions.py team_*.ipynb` on the teams' submitted notebooks. It reads each registry and each team's dataset (without running the notebook), reproduces that dataset's hidden-pack verdicts from the registry alone, checks the records were not edited, and flags near-identical rationales between teams. No Neo4j, LLM or provider is needed, so it works for every team whichever starter and LLM they used. Enter the marks in `day2_judging_scorecard.xlsx`; borderline teams are also run live.
- **Tier 2, live checkpoint (30%, about 3 min per team).** The team shows its registry and outcomes table and explains one row you choose.

| Time | Activity |
|---|---|
| 2:00–2:10 | Instructions, demo order |
| 2:10–~3:00 | Live checkpoints: 25 teams, so two judge tables or ~2 min per team (see the runbook) |
| 3:00–3:20 | Judges' deliberation (co-judges score independently, then reconcile) |
| 3:20–3:30 | Results and wrap |

### Before the event
- Run the hidden pack once against each of the five starters' baselines with a real key (`day2_add_hidden_pack.py ... --baseline-only`), and one starter end-to-end with an Aura instance, to see how often the baseline fabricates. Notebooks were verified with mock services only.
- Confirm the submission mechanism and co-judges.
