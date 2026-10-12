# Day 2 Judging Runbook — from submission deadline to winners

**Setting:** submissions due **12:00 PM, Oct 15**. Session **2:00–3:30 PM**. About **25 teams**, spread over **five datasets** (ORD, HR, RISK, PAY, CLN), roughly five teams each. You have two hours before the session, then 90 minutes with the teams.

**Files you need in one folder:** `day2_score_submissions.py`, `day2_offline_check.py`, the `day2_datasets/` folder (it holds all five hidden packs), `day2_add_hidden_pack.py` (optional), `day2_judging_scorecard.xlsx`, and the teams' notebooks. The reference solutions in `day2_reference_solutions/` are for your own checking.

**Why five datasets can be scored together:** every dataset has the same structure (12 categories, about 140 records, four Kind 1 families with the first one given, four Kind 2 traps, 8 + 3 public and 9 + 4 hidden questions). A 9/9 on ORD means the same thing as a 9/9 on CLN, so percentages and pattern scores are directly comparable. The scorecard needs no change; the scoring script puts each team's dataset in square brackets after its name.

---

## Before the deadline (Oct 14 evening – Oct 15 morning)

1. Pilot once with a real key. For each of the five datasets, run the baseline on the hidden pack so you know how often it fabricates: `python day2_add_hidden_pack.py day2_starters/starter_ORD_orders_inventory_delivery_no_neo4j.ipynb --baseline-only`, open the `_HIDDEN` file, add your key, Run all. The five datasets may behave differently; this is the only way to know.
2. Make a submissions folder and confirm how teams will send notebooks (drive folder, form, or email).
3. Copy `day2_judging_scorecard.xlsx` to a fresh file and delete the four REHEARSAL rows (Ananya, Rahul, Priya, Meera) in *Batch Test Results* and *My Independent Scoring*. The sheet has room for 30 teams.
4. Decide your late-submission rule and tell the teams (for example: scored, with a note; or not scored on the batch part).
5. Decide how you will run the live checkpoints with 25 teams (see "Session" below) and book a co-judge if you can.

## 12:00 PM — Deadline passes

6. Snapshot the folder: download every notebook into one folder. Anything after this timestamp is late.
7. Rename files as `team_<n>_<name>.ipynb` so names come out right in the reports.
8. In the scorecard, enter the team numbers in the *Batch Test Results* tab (column A). The names arrive with the paste in step 11.

## 12:10–12:30 — Tier 1, batch marks (about 20 min)

9. Run `python day2_score_submissions.py team_*.ipynb`. It finds each team's dataset by itself.
10. Read the report. For each team check:
    - the **dataset line** (the right dataset for that team; the RECORDS line must read all records matched, otherwise the team edited the data, so open the notebook),
    - any pattern marked **UNRECOGNISED** (judge it by hand),
    - any **COULD NOT READ REGISTRY** or **DATASET NOT FOUND** (open the notebook; for the second, re-run that file with `--dataset ORD`, `HR`, `RISK`, `PAY` or `CLN`),
    - the failures listed under each pack,
    - the **COPYING CHECK** at the end: pairs of teams whose rationale text is more than 85% alike. Read both rationales before you score them.
11. Paste `batch_results_B.tsv` at cell **B5** and `batch_results_P.tsv` at cell **P5** of *Batch Test Results*. The two percentage columns calculate themselves.
12. Open each notebook and check the **Runs end-to-end** status: does it show saved output from top to bottom with no error cells? Note a 100 or 0 for each team; you enter it later.

## 12:30–1:35 — Tier 1, rationale and outcomes (25 teams: split the reading)

With 25 teams you cannot read everything yourself in the time. Split the notebooks with a co-judge, or read in full only the teams that are not clearly at the top or bottom of the batch ranking.

13. For each team read the pattern register and the rejected list in the summary output. Score rationale quality 0–30 (A adopted patterns, B rejected lookalikes, C understanding of the two kinds; the breakdown is in the *How to Use* tab) in the *Pattern Score* tab, column G. About 2 minutes per team.
14. Read each team's OUTCOMES table and remaining-failure note (about 1 minute per team). Compare their public-pack claims with the script's public marks; any disagreement is a flag for the checkpoint.
15. Give a provisional **Explaining outcomes** score (0–100) in *My Independent Scoring* and refine it after the live checkpoint. Criteria: all 11 public questions covered, causes correctly attributed (pattern vs retrieval), the baseline-fabricated column filled in from real answers, one honest and specific remaining failure.

## 1:35–1:50 — Optional live runs (only where it matters, maximum 2–3 teams)

16. Pick teams that are within a few points of a rank boundary, or whose public result doesn't match the script's prediction.
17. Run `python day2_add_hidden_pack.py team_x.ipynb`, open `team_x_HIDDEN.ipynb`, add the key and Run all. (It picks the team's dataset by itself.)
18. Read the grounded answers. Change an H or HP cell only if the answer contradicts the structural mark. Note why.

## 1:50 — Prepare the checkpoint

19. Look at the provisional ranking in *My Independent Scoring* (column J).
20. For each team choose one question and write it in column K, usually a row where the outcomes table disagrees with the marks, or "Why did you not include <X>?" for a team that missed a Kind 1 pattern (the dataset's own words: "Why is Driver missing?", "Why not Lab?").

## 2:00 PM — Session

21. Open with housekeeping: order of teams, what you will ask, how long each team gets.
22. **Time budget.** 25 teams do not fit at 3 minutes each in the 50 minutes from 2:10 to 3:00. Pick one:
    - **Two judge tables in parallel** (best): about 13 + 12 teams at 3 minutes is about 40 minutes.
    - **Solo judge:** 2 minutes per team (30 seconds to show the registry and outcomes table, one question, score), 50 minutes in all, no slack.
    - **Shortlist:** full 3-minute checkpoints for the top 10 by batch ranking plus any flagged team; the others keep their provisional Explaining outcomes score and get Live demo clarity from their notebook.

## 2:10–3:00 — Tier 2, live checkpoints

For each team:
23. They show the registry and the outcomes table.
24. Ask your chosen question. Record their answer briefly in column L and your notes in column M.
25. Score **Explaining outcomes** (final), **Runs end-to-end** (0 or 100) and **Live demo clarity** (0–100: states the answer clearly, cites record IDs, explains one row).
26. Do not discuss scores with the teams during the session.

## 3:00–3:20 — Deliberation

27. If you have co-judges, each keeps their own scorecard. Compare the *Weighted Total* column. Discuss any team where the two totals differ by more than about 10 points; the usual causes are the rationale score and Explaining outcomes.
28. Agree the top three. For a tie, use this order: higher no-fabrication % first, then Explaining outcomes, then Pattern Score.
29. Check the top teams' totals once more against their notes before you commit. If two top teams are on different datasets, look at the dataset only to be sure neither pack was unusually kind; the structures are identical, so scores stand.

## 3:20–3:30 — Declare the winners

30. Announce the top three overall with one sentence each on why they won, naming the rubric criteria rather than the scores (for example "the only registry that linked what is the same event and refused what is merely similar"). Optionally add a mention for the best team on each dataset.
31. Close with the lesson: too few patterns misses real links, too many invents false ones.

## After the session

32. Save the final scorecard, `batch_results_*.tsv` and the script reports.
33. Optionally send each team its own report: the patterns found, the marks, and what it missed. The script output is already in that form.
34. Note anything to change next time (questions that nobody failed, steps that took too long, whether any dataset turned out easier).
