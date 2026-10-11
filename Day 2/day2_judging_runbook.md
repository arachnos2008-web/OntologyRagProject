# Day 2 Judging Runbook — from submission deadline to winners

**Setting:** submissions due **12:00 PM, Oct 15**. Session **2:00–3:30 PM**. About 10–12 teams. You have two hours before the session, then 90 minutes with the teams.

**Files you need in one folder:** `day2_score_submissions.py`, `day2_offline_check.py`, `day2_dataset_generator.py`, `day2_add_hidden_pack.py` (optional), `day2_judging_scorecard.xlsx`, and the teams' notebooks.

---

## Before the deadline (Oct 14 evening – Oct 15 morning)

1. Pilot once with a real key: run the public and hidden packs against the starter's baseline, so you know how often it fabricates.
2. Make a submissions folder and confirm how teams will send notebooks (drive folder, form, or email).
3. Copy `day2_judging_scorecard.xlsx` to a fresh file and delete the four REHEARSAL rows (Ananya, Rahul, Priya, Meera) in *Batch Test Results* and *My Independent Scoring*.
4. Decide your late-submission rule and tell the teams (for example: scored, with a note; or not scored on the batch part).

## 12:00 PM — Deadline passes

5. Snapshot the folder: download every notebook into one folder. Anything after this timestamp is late.
6. Rename files as `team_<n>_<name>.ipynb` so names come out right in the reports.
7. In the scorecard, enter the team numbers and names in the *Batch Test Results* tab (columns A and B).

## 12:10–12:30 — Tier 1, batch marks (about 20 min)

8. Run `python day2_score_submissions.py team_*.ipynb`.
9. Read the report. For each team check three things: any pattern marked **UNRECOGNISED** (judge it by hand), any **COULD NOT READ REGISTRY** (the registry cell is broken; open the notebook), and the failures listed under each pack.
10. Paste `batch_results_B.tsv` at cell **B5** and `batch_results_P.tsv` at cell **P5** of *Batch Test Results*. The two percentage columns calculate themselves.
11. Open each notebook and check the **Runs end-to-end** status: does it show saved output from top to bottom with no error cells? Note a 100 or 0 for each team; you enter it later.

## 12:30–1:10 — Tier 1, pattern rationale (about 2–3 min per team)

12. For each team read the pattern register and the rejected list in the summary output.
13. Score rationale quality 0–30 (A adopted patterns, B rejected lookalikes, C understanding of the two kinds; the breakdown is in the *How to Use* tab). Enter it in the *Pattern Score* tab, column G. The pattern score (0–100) then calculates itself.

## 1:10–1:35 — Outcomes review, provisional

14. Read each team's OUTCOMES table and remaining-failure note.
15. Compare their public-pack claims with the script's public marks. Any disagreement is a flag for the checkpoint.
16. Give a provisional **Explaining outcomes** score (0–100) in *My Independent Scoring* and refine it after the live checkpoint. Criteria: all 11 public questions covered, causes correctly attributed (pattern vs retrieval), the baseline-fabricated column filled in from real answers, one honest and specific remaining failure.

## 1:35–1:50 — Optional live runs (only where it matters, maximum 2–3 teams)

17. Pick teams that are within a few points of a rank boundary, or whose public result doesn't match the script's prediction.
18. Run `python day2_add_hidden_pack.py team_x.ipynb`, open `team_x_HIDDEN.ipynb`, add the key and Run all.
19. Read the grounded answers. Change an H or HP cell only if the answer contradicts the structural mark. Note why.

## 1:50 — Prepare the checkpoint

20. Look at the provisional ranking in *My Independent Scoring* (column J).
21. For each team choose one question and write it in column K, usually a row where the outcomes table disagrees with the marks, or "Why did you not include <X>?" for a team that missed a Kind 1 pattern.

## 2:00 PM — Session

22. Open with housekeeping: order of teams, 3 minutes each, what you will ask.

## 2:10–3:00 — Tier 2, live checkpoints (about 3 min per team)

For each team:
23. They show the registry and the outcomes table (30 s).
24. Ask your chosen question (about 1.5 min). Record their answer briefly in column L and your notes in column M.
25. Score **Explaining outcomes** (final), **Runs end-to-end** (0 or 100) and **Live demo clarity** (0–100: states the answer clearly, cites record IDs, explains one row).
26. Do not discuss scores with the teams during the session.

## 3:00–3:20 — Deliberation

27. If you have co-judges, each keeps their own scorecard. Compare the *Weighted Total* column. Discuss any team where the two totals differ by more than about 10 points; the usual causes are the rationale score and Explaining outcomes.
28. Agree the top three. For a tie, use this order: higher no-fabrication % first, then Explaining outcomes, then Pattern Score.
29. Check the top teams' totals once more against their notes before you commit.

## 3:20–3:30 — Declare the winners

30. Announce the top three with one sentence each on why they won, naming the rubric criteria rather than the scores (for example "the only registry that linked what is the same event and refused what is merely similar").
31. Close with the lesson: too few patterns misses real links, too many invents false ones.

## After the session

32. Save the final scorecard, `batch_results_*.tsv` and the script reports.
33. Optionally send each team its own report: the patterns found, the marks, and what it missed. The script output is already in that form.
34. Note anything to change next time (questions that nobody failed, steps that took too long).
