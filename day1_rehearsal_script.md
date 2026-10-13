# Day 1 Rehearsal Script — Run This Before Oct 14

Goal: verify every live demo works end to end on a fresh Colab runtime, so nothing breaks live in front of 50+ students.

**Track to test:** Colab free tier, `all-MiniLM-L6-v2` for embeddings, your notebooks (Weeks 1-3 pattern) for RAG/Graph RAG, and the campus reference solution (`day2_reference_solution.ipynb`) for the walkthrough.

Times below are minutes from 9:00 AM. The first 15 minutes are the confidence-check warm-up (the concept map page), so the demos start at 0:15.

Run the *entire* rehearsal once from a cold start. Note timing and any errors per step.

---

## Segment 1 (0:15–0:30) — Opening hook: the false-narrative demo

**What to rehearse:** your Week 2 "stock replenishment" failure case, live, cold-started (i.e., run it as if you've never run it before — this is exactly how it'll feel live on Oct 14).

Checklist:
- [ ] Colab notebook opens and runs top-to-bottom with zero manual fixes
- [ ] The exact conflated answer ("...shipped to the customer's warehouse yesterday...") reproduces — LLM outputs aren't always identical run-to-run, so if you get a different (but still wrong-in-spirit) answer, that's fine; if it suddenly answers *correctly*, you need a backup failure example ready (see below)
- [ ] Time yourself: this should take under 3 minutes end-to-end including narration

**Backup plan if the LLM "accidentally" gets it right this time:** LLM outputs aren't deterministic. Have a **second pre-recorded example** ready (screenshot or short video of a previous run) so the hook never depends on live reproducibility. Rehearse pulling this up smoothly, not scrambling for it.

---

## Segment 2 (0:30–1:00) — Embeddings & similarity (Week 1 material)

**What to rehearse:** the cosine similarity demo + the `[7]`/`[8]` misranking finding from your own Day 1.

Checklist:
- [ ] `sentence-transformers` model download completes within a reasonable time on fresh Colab (first run downloads ~90MB — test on venue Wi-Fi speed if possible, or pre-download and cache in the notebook you'll share)
- [ ] The misranking example reproduces clearly enough to explain in under 2 minutes without over-explaining the math

**Simplify for a room, not a 1:1 tutorial:** you don't need the full cosine-similarity-by-hand walkthrough here — one clean example (correct match) and one clean counter-example (near-miss) is enough. Rehearse the *shortened* version, not the full Week 1 depth.

---

## Segment 3 (1:00–1:30) — RAG pipeline + the break (Week 2 material)

**What to rehearse:** retrieval + generation, then the deliberate break — in your Colab notebook.

Checklist:
- [ ] `.env`/API key loads correctly on a **fresh Colab runtime**
- [ ] Rehearse what happens if the API call is slow/rate-limited live — have a pre-run output ready to show if the live call hangs more than ~10 seconds


---

## Segment 4 (1:30–2:00) — The fix: Graph RAG (Week 3 material)

**What to rehearse:** the Neo4j Aura connection + the `connected_order: None` proof — from the Colab notebook.

Checklist:
- [ ] **Aura Free instance status** — confirm it's not paused (Aura Free auto-pauses after inactivity; verify it's "Running" the morning of, not the night before)
- [ ] Driver connection succeeds on a fresh Colab run (you already hit a `ServiceUnavailable` mid-session once — rehearse the fix: `driver.close()` + recreate, so if it happens live you're not debugging cold)
- [ ] Confirm the two-cluster graph visualization renders correctly in the Aura Console query view you'll be screen-sharing

---

## Segment 5 (2:15–3:30) — Reference solution walkthrough

You take the class through `day2_reference_solution.ipynb` (the campus example dataset, which no team uses). Students follow on screen and do not build. Do not use the five `reference_<code>.ipynb` files here: they solve the teams' own datasets.

Run order to rehearse: registry and its reasons, the Kind 2 candidates that are rejected, the public pack, the `OUTCOMES` table, the remaining failure.

Checklist:
- [ ] Time the notebook from a cold start on a fresh Colab runtime, with its saved output cleared. The walkthrough has 75 minutes, so each step should take 10 to 15 minutes of talking, not running
- [ ] With a **fresh Aura Free account**, confirm the graph-building cell finishes and prints per-pattern link counts (or use the no-Neo4j version if you would rather not depend on Aura live)
- [ ] Before the guided step, PP3 shows "NOT connected" in `run_pack(PUBLIC_POSITIVE)`; after adding the Alumnus pattern and re-running the graph cell, it shows "CONNECTED via Alumnus A002". Rehearse this flip with `day2_starter_notebook.ipynb` before you open the reference solution: it is the moment students see why a pattern matters
- [ ] Have a saved run of the whole notebook ready in case the LLM or Aura is slow or down on the day
- [ ] Prepare the `OUTCOMES` explanation slide: the three fields (`baseline_fabricated`, `grounded_correct`, `explanation`), one good and one weak explanation side by side. A student tester found this the least clear part of the task
- [ ] **Pilot the baseline:** run the public and hidden packs through `baseline_rag_answer` and note how often it actually fabricates. On the five datasets it ranged from 0 to 4 wrong "yes" answers out of 8 on the public pack, so frame "baseline fails, graph works" with care
- [ ] If using a shared/pooled API key: have a few people (or scripted parallel calls) hit the same key at once and confirm it does not rate-limit into failure

---

## What to log after each rehearsal run

For every segment: timing (actual vs. planned), any error encountered, and anything that behaved differently from the plan. This log is what turns into your final go/no-go call the day before the event — send it to me and we'll adjust the schedule/checklist together.
