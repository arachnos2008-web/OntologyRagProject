# IEEE-CIS Amrita — Agentic AI + Knowledge Grounding Workshop
**Oct 14–15, 2026 · 40–50 students (about 10–12 teams of 4–5)**

---

## Day 1 — Oct 14, 8:30 AM–1:30 PM

Students bring a laptop, a Google account and **their own LLM API key from any provider**. Each team also gets a graph store: a free **Neo4j Aura** instance, or lookup tables (see the Student Setup Guide).

| Time | Activity | Format |
|---|---|---|
| 8:30–8:45 | **Opening hook:** an AI agent confidently states a false fact by merging two unrelated records | Demo |
| 8:45–9:15 | **Embeddings and similarity search** | Demo (Week 1 notebook) |
| 9:15–9:45 | **RAG pipeline and where it breaks:** the exact conflated answer | Demo (Week 2 notebook) |
| 9:45–10:15 | **Grounding the agent:** same query, graph-backed, now correct | Demo (Week 3 notebook) |
| 10:15–10:30 | Break | Teams create their Aura instance (or choose lookup tables) |
| 10:30–12:30 | **Hands-on lab.** Open `day2_starter_notebook.ipynb` in Colab and: (1) plug in your own LLM key by editing the `call_llm` cell; (2) connect the graph store; (3) run the starter top to bottom; (4) add the **Alumnus** pattern and watch public question PP3 flip from "no recorded link" to "connected" | Guided, mentors roaming |
| 12:30–12:45 | Buffer for stragglers | Mentors |
| 12:45–1:15 | **Day 2 problem statement, rubric, submission deadline, team formation** | You present |
| 1:15–1:30 | Build-window logistics, Q&A | |

---

## Day 2 — Oct 15, 2:00–3:30 PM (demo and judging only)

All building happens between the two days.

### Problem: "Complete the grounding"
*Build an agent that tells the truth about what it doesn't know.*

**Scenario.** Campus operations and student services: 179 records, 14 categories. Different departments describe different events in similar words. Some records name a person, club or ticket (`Student S001`, `Club RC-1`, `HMT-58`); where that ID repeats, it *is* the same event. The task is to tell the two cases apart.

**Given to each team (`day2_starter_notebook.ipynb`).** Retrieval, a plain baseline RAG, graph building from a **pattern registry**, and a grounded answer step. The registry holds **one** pattern: the Student ID regex.

**Build window — each team**
1. Decides which other strings identify one event (**Kind 1**: person IDs, club codes, ticket numbers) and which are incidental fields reused across unrelated events (**Kind 2**: room, block, amount, semester).
2. Adds its patterns to the registry, each with an example and a reason, and lists the lookalikes it **rejected** and why.
3. Runs the **public pack** (8 adversarial + 3 positive-control questions) against baseline and grounded, and fills in an outcomes table: did the baseline fabricate, was the grounded answer correct, and why.
4. States **one failure it still has**.

**Extra work for every team.** Run on its own LLM provider (edit `call_llm`). A team that cannot use Neo4j replaces the graph with **lookup tables** that keep the same `graph_check` contract.

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

- **Tier 1, batch (before 2:00 PM, 70% of the rubric).** Save each team's registry as JSON and run `python day2_offline_check.py team_registry.json`. It reproduces the hidden-pack verdicts from the registry alone, with no Neo4j, LLM or provider, so it works for every team whatever graph store or LLM they used. Enter the marks in `day2_judging_scorecard.xlsx`; borderline teams are also run live.
- **Tier 2, live checkpoint (30%, about 3 min per team).** The team shows its registry and outcomes table and explains one row you choose.

| Time | Activity |
|---|---|
| 2:00–2:10 | Instructions, demo order |
| 2:10–~3:00 | Live checkpoints, ~3 min per team |
| 3:00–3:20 | Judges' deliberation (co-judges score independently, then reconcile) |
| 3:20–3:30 | Results and wrap |

### Before the event
- Run the public and hidden packs once against the starter's baseline with a real key and Aura instance, to see how often the baseline fabricates. Notebooks were verified with mock services only.
- Confirm the submission mechanism and co-judges.
