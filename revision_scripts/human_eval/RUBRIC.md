# Human Evaluation Rubric — Incident Report Quality

Each rater scores every report on three dimensions, 1–5, using only the
report text and the alert evidence shown in the sheet. Raters must not look
up the community's ground-truth label or which model produced the report
(the sheet is blinded; the key stays with the study lead).

## D1 — Technical accuracy
Does the report's description of the attack match the behaviour visible in
the alert evidence?

- **5** — The described behaviour matches the evidence completely; nothing contradicts it.
- **4** — Matches, with one minor overstatement or omission.
- **3** — Broadly plausible but the attack type could equally be something else given the evidence.
- **2** — The described attack type conflicts with a clear signal in the evidence.
- **1** — The description is unrelated to the evidence.

## D2 — Evidence support
Are the specific claims in the summary and evidence fields traceable to the
alert data, with no fabricated details?

- **5** — Every specific claim (ports, counts, timing, protocols) appears in the alert evidence.
- **4** — All claims traceable; one vague or unverifiable phrase.
- **3** — Mostly traceable, but at least one specific detail is not in the evidence.
- **2** — Several untraceable or invented details.
- **1** — The evidence field is generic boilerplate or contradicts the alerts.

## D3 — Actionability
Is the recommended next step something a SOC analyst could act on for this
specific incident?

- **5** — Specific, appropriate to the described attack, and executable as written.
- **4** — Appropriate but partially generic.
- **3** — Generic advice that would fit almost any incident.
- **2** — Vague to the point of being unusable, or mismatched to the incident.
- **1** — Missing, circular, or harmful.

## Procedure

1. The study lead runs `generate_annotation_sheet.py`, which produces
   `annotation_sheet.csv` (blinded, shuffled) and `annotation_key.csv`
   (model + ground truth per row; not shown to raters).
2. Each rater fills `d1_accuracy`, `d2_evidence`, `d3_actionability`
   in their own copy of the sheet, independently, without discussion.
3. `compute_kappa.py rater1.csv rater2.csv` reports Cohen's Kappa
   (unweighted and linear-weighted) per dimension plus mean scores per
   model (joined from the key).
4. Report in the thesis: number of reports, number of raters, per-dimension
   means with the kappa agreement, and 2–3 quoted examples of disagreement.

A kappa of 0.61–0.80 is conventionally "substantial" agreement; below 0.40,
revise the rubric anchors and re-rate rather than reporting the numbers.
