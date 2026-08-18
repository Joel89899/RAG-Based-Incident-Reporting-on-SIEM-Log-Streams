# Defence Notes — Joel Isaria Mwende

**From Fragmented Alerts to Actionable Intelligence**
30-minute slot. Target: ~22 minutes talking, ~8 minutes questions.

---

## The one sentence to never lose

> The knowledge graph does not tell the retriever what the answer is.
> It tells the retriever what the answer **cannot** be.

If you forget everything else, say that. Every result in the thesis supports it.

---

## Numbers you must know cold

| Number | What it is |
|---|---|
| **14,182** | alerts, CIC-IDS working set |
| **54 / 18** | communities formed / scoreable |
| **691** | ATT&CK techniques in the retrieval corpus |
| **0.837** | clustering label purity (CIC-IDS) |
| **0.833 vs 0.556** | exact match, grounded vs LLM-only baseline (Mistral) |
| **0.400 vs 0.200** | macro-F1, same comparison |
| **77.8%** | majority-class ceiling |
| **+0.43** | DARPA macro-F1 gain, all three models |
| **22 / 22** | scoped rerank correct, when the technique was reachable |
| **0.0 / 0.056 / 0.0** | exact match with the constraint removed |

Do not memorise more than this. Everything else is on a slide or in a backup.

---

## Timing plan

| Section | Slides | Minutes |
|---|---|---|
| Motivation and questions | 3–6 | 4 |
| The pipeline | 7–12 | 6 |
| Setup | 13–15 | 3 |
| Results | 16–22 | 7 |
| Limitations and conclusions | 23–27 | 3 |

**Discipline:** the six pipeline slides are where defences overrun. Give each about
a minute. If you are past 12 minutes when you reach slide 13, skip the Stage 1
example sentence and compress Stages 2–3 to one line.

---

# Part 1 — Motivation and Questions (slides 3–6, ~4 min)

## Slide 3 — The problem

A SOC receives more alerts each day than its analysts can read. Over 10,000 a
day is routine and up to 70% are false positives. Skilled analysts are scarce,
so triage stops at the top of the queue and the rest go unexamined.

**Land this line:** alert fatigue is a structural mismatch between machine
generation speed and human reading speed. It is not a discipline problem, so
you cannot fix it by asking analysts to work harder.

## Slide 4 — Three gaps

1. **Grouping.** Attacks unfold across many alerts over hours or days. Most
   tools classify each alert alone and lose the narrative thread.
2. **Verifiability.** Reports get scored by text similarity or expert opinion,
   never against authoritative threat knowledge. So you cannot tell whether a
   report is correct or merely fluent.
3. **Privacy.** Most systems send logs to a cloud API. Defence, healthcare and
   critical infrastructure cannot do that. The environments that need this most
   are the ones excluded.

**Say:** this thesis addresses all three in one pipeline.

## Slide 5 — Research questions

Read them, do not elaborate. They map one-to-one onto the results section, and
you will answer them explicitly on the Conclusions slide.

## Slide 6 — Where this sits

Six dimensions. No prior system in the review combined all six. The two rarest
in prior work are local deployment with KG-scoped retrieval, and multi-model
comparison under fixed conditions.

**If asked "is that fair to prior work?":** the table reports what each paper
claims, thirteen systems, and each row is cited. Nobody is being penalised for
not attempting something they never set out to do.

---

# Part 2 — The Pipeline (slides 7–12, ~6 min)

## Slide 7 — The pipeline (the anchor slide)

Walk the diagram once, top to bottom, and point at two things only:

- **The shaded box** over Stages 1–4: fully unsupervised. No label touches the
  alert text, the embeddings, the clustering or the extraction. Labels enter
  only at scoring.
- **The blue arrow** from Stage 5 into Stage 6: the graph decides which
  techniques retrieval is allowed to return. That arrow is the contribution.

**Do not** narrate all seven stages here. You are about to do that anyway.

## Slide 8 — Stage 1, alerts become sentences

A fixed hand-written template, no LLM. Chosen deliberately: an LLM would be
non-deterministic, so the same flow could produce different text on different
runs and the embeddings would stop being comparable.

**The point to make:** the class label is deliberately excluded from the
sentence. If it were in there, the "unsupervised" claim would be false.

## Slide 9 — Stages 2–3, embed then group

Each sentence becomes a 384-dimensional vector with all-MiniLM-L6-v2, and
communities form by greedy cosine threshold directly on the embeddings.

**Why not Louvain** (expect this): Louvain needs an explicit graph and puts
every alert in exactly one community. A port scan that precedes both a
brute-force attempt and a C2 callback belongs to two attack chains, and Louvain
would force a choice. Clustering on the similarity values needs no intermediate
graph.

## Slide 10 — Stage 4, meaning enters

Up to here the pipeline only knows similarity. Now a local LLM reads each
community and writes behavioural triples: subject, relation, target.

Two constraints matter. The relation comes from a **fixed vocabulary**, seven
for network flows and ten for host events. And generation is
**grammar-constrained**, so the output is schema-valid by construction.

**The headline:** 100% schema-valid output, every community, every model. The
free-text parsing fallback never fired once.

## Slide 11 — Stage 5, the knowledge graph

Two layers. The behavioural layer is the subjects and targets from the triples.
The ATT&CK layer is 691 technique nodes from the MITRE STIX bundle. Bridge
edges connect them through a fixed relation-to-technique mapping: a port-scan
relation reaches T1046, a brute-force relation reaches T1110 and its
sub-techniques.

**Say plainly:** the bridge is what makes the next stage possible.

## Slide 12 — Stages 6–7, scoped retrieval and report

Four steps: the LLM writes a hypothetical attack description (HyDE), ChromaDB
returns candidates, **the graph restricts that candidate set**, and the report
is generated under a JSON schema with five fields.

**Land it:** 691 technique descriptions become a handful of behaviourally
justified candidates. That reduction is the whole idea.

---

# Part 3 — Setup (slides 13–15, ~3 min)

Move briskly. This section earns no marks but losing time here costs you the
results section.

## Slide 13 — Datasets

Two abstraction levels on purpose. CIC-IDS-2017 is network flows from a
controlled testbed and carries the full pipeline through report generation.
DARPA CADETS E3 is host audit logs from a real red-team engagement and tests
whether the approach survives a different data modality.

## Slide 14 — Models and hardware

Three open-weight models, 3.1B to 12.2B, quantised. One consumer laptop with
4 GB of VRAM. Fixed seed 42, temperature 0.

**Say:** the hardware is the point, not an apology. If it runs here it runs in
an air-gapped environment.

## Slide 15 — How it is evaluated

Every grounded condition is compared against a baseline that keeps the same
model and the same evidence and removes **only** the graph constraint.
CIC-IDS baseline is direct LLM classification with no retrieval; DARPA baseline
is unscoped similarity retrieval over all 691 techniques.

**Flag it yourself:** the two baselines differ, so the two deltas are not the
same measurement. Saying this before anyone asks buys you credibility.

---

# Part 4 — Results (slides 16–22, ~7 min)

## Slide 16 — RQ1, clustering works

0.837 purity at 0.938 intra-cluster similarity, only 5 of 14,182 alerts
unclustered, 0.987 purity per window on DARPA.

**The honest caveat, say it out loud:** separating attack from benign is easy.
Separating one technique from another is the hard part, and that is what the
rest of the pipeline exists to do.

## Slide 17 — RQ2, the graph inherits the model's biases

Same communities, three different graphs. Mistral-Nemo calls 41 of 45 triples
port scans. The coder model calls 34 of 46 denial-of-service. The 3B model sits
between them.

**The interpretation:** the graph is a faithful record of what the LLM believed
the alerts showed. That is not always what the alerts showed.

## Slide 18 — RQ3, classification results

**Lead with macro-F1, not exact match.** One technique, T1046, covers 14 of the
18 communities, so exact match mostly measures one class. On macro-F1 the
grounded condition doubles Mistral's baseline, 0.400 against 0.200, and both
Qwen baselines are exactly zero: without grounding they never named a correct
technique for any class.

Then the exact-match numbers, with the caveat that the intervals overlap.

## Slide 19 — The main finding (slow down here)

This is the strongest slide in the deck. Give it 90 seconds.

Every model's exact-match rate **equals** its reachability rate. Across all
three models the scoped retrieval was handed 22 communities where the correct
technique was in the candidate set, and it selected correctly **22 times**.

**Say it explicitly:** no model ever misclassified a community whose behaviour
it had extracted correctly. The bottleneck is extraction, not retrieval. That is
why the 72-point spread between models is produced at Stage 4, before retrieval
even begins.

## Slide 20 — Is the graph doing the work?

Same scoring function, same inputs, constraint removed: 0.0%, 5.6%, 0.0%.

**Why it fails is interesting:** the unconstrained predictions land on plausible
neighbours like T1205 Traffic Signaling and T1049 Network Connections
Discovery. The embedding puts you in the right region and cannot land on the
right point. That is exactly what a constraint is for.

**Pre-empt the fairness objection:** this is not a strawman. It is your own
notebook's fallback branch, the code path that already runs when a community
produces no KG candidates.

## Slide 21 — DARPA transfer

+0.425, +0.438, +0.431 F1. Three models, nearly identical gains, and the
bootstrap intervals are disjoint from the baselines.

Two things to point out: the improvement does not depend on model scale, and
**the model ranking flips** — the coder model is worst on CIC-IDS and best
here. Precision is near 1.0 while recall is about 0.5: the pipeline is
conservative, and when it names a technique it is almost always right.

## Slide 22 — Correctness and grounding diverge

The coder model writes the best-grounded reports and the worst classifications.
Internally consistent, well-evidenced reports about the wrong attack.

**The lesson:** a system reporting only grounding would rank the worst model
first. Both metrics are needed, and that is the evaluative contribution.

---

# Part 5 — Limitations and Conclusions (slides 23–27, ~3 min)

## Slide 23 — Limitations

Two headings, one sentence each, then move. Do not read this slide aloud.

- **The alert text is the ceiling.** A single SYN packet to port 21 looks the
  same whether it is reconnaissance, brute force or a beacon.
- **The evidence is narrow.** 18 scoreable communities, one dominant technique,
  overlapping intervals. DARPA is the firmer result.

## Slide 24 — Circularity (own this)

Your second supervisor raised this directly. **Concede first, then defend.**

> "The bridge and the ground-truth mapping were curated by the same person. On
> CIC-IDS they share much of their structure, and once extraction assigns the
> right relation the bridge largely determines the technique. The inferential
> work happens at extraction."

Then the three reasons it is not a lookup of the answer key:

1. The mapping is one-to-many: 7 relations reach 12 technique identifiers.
2. Removing the preference rule changes 0, 0 and 1 predictions, so the expert
   prior contributes essentially nothing.
3. DARPA's ground truth was transcribed independently from the engagement
   report, and there the same bridge reaches recall of only about 0.5. A
   mapping that restated the answer key would recover everything.

## Slides 25–27 — Contributions, Conclusions, Future work

Contributions: architectural, empirical, evaluative. Conclusions: the three RQ
answers, then the take-home line. Future work: lead with richer alert
representation, since your own error attribution says that is where the gain is.

---

# Part 6 — The Three Questions

## Q1 — Why does the KG constraint improve retrieval over conventional RAG, and when could that advantage disappear?

**Why it works.** Conventional RAG searches the whole corpus with a short
query. Here that is 691 technique descriptions against a few sentences of HyDE
text. The graph replaces that open-domain search with a closed-set choice among
the 2–5 techniques the observed behaviour actually reaches. It is not a
re-ranking tweak; it eliminates most wrong answers before the model sees them.

**The evidence.** Same scorer, constraint removed: 0.833 drops to 0.000. And
within scoped candidate sets the rerank was correct 22 out of 22 times.
Unconstrained similarity lands in the right neighbourhood and never on the
right point.

**When it disappears — three cases, be specific:**

1. **When extraction fails.** The constraint can only help if the correct
   technique is reachable from the extracted relations. The coder model is the
   proof: 2 of 18 reachable, 11.1% accuracy. A perfect retriever could not have
   done better.
2. **When the mapping does not cover the technique.** 12 identifiers for
   network flows, 21 for host events, out of 200-plus. Anything outside is
   unreachable by construction.
3. **When the candidate set stops being selective.** If a relation mapped to
   fifty techniques instead of three, the constraint would approach unscoped
   retrieval and the advantage would shrink toward zero.

**Close on:** the advantage is real but conditional. It converts extraction
quality into classification accuracy, and it cannot manufacture quality that
extraction did not produce.

---

## Q2 — How could this process real-time SIEM streams while keeping scalability, explainability and privacy?

**Start with the cost structure**, because it is the honest core of the answer:

- Stages 1–3 touch every alert: 14,182 on CIC-IDS.
- Stages 4–7 touch every **community**: 54 extractions, 18 reports.
- So LLM inference, the expensive part, scales with community count, not alert
  volume — roughly a 260-fold reduction on this dataset. That is why it runs on
  one laptop.

**State the ceiling before they find it.** Clustering computes an n×n
similarity matrix, so it is quadratic in alerts while LLM cost is linear in
communities. At 14,182 alerts that term is negligible; at ten times the volume
it dominates and the bottleneck moves from inference to clustering.

**So the architecture for streaming:** sliding-window community detection with
incremental embedding, and a trigger that decides when enough alerts have
accumulated to be worth reporting. The anchoring mechanism itself is
indifferent to how communities are formed, so it carries over unchanged.

**Explainability survives** because it is structural, not added on: every
report traces back through a named technique, to the bridge edge, to the
extracted triple, to the alert sentences. An analyst can walk that chain.

**Privacy survives** because nothing changes: the models run locally through
llama-cpp, and the only external artefact is the ATT&CK bundle, which is public
and static.

**If pressed on numbers, say so plainly:** wall-clock time was not
instrumented, so I make no throughput claim. What I can defend is the cost
structure and where the bottleneck moves.

---

## Q3 — What would it take to generalise to a much larger portion of ATT&CK and to other data sources?

**Three things, in increasing difficulty.**

**1. The mapping (mechanical).** Currently hand-curated: 12 identifiers for
network flows, 21 for host events. Extending it is annotation work, not
research. The route: prompt an LLM with each ATT&CK technique description to
propose the observable behaviours that would indicate it, then curate manually.
Feasible but tedious, and it does not diminish over time — every ATT&CK release
adds maintenance.

**2. The relation vocabulary (design).** Harder, because relations must stay
mutually distinguishable *from the evidence*. Seven relations worked for
network flows partly because they map onto visibly different flow signatures.
Push to fifty relations and the extractor starts confusing them, which the
coder model already demonstrates at seven when the distinguishing signal is
subtle.

**3. The alert representation (the real blocker).** My own error attribution
says this is where the ceiling is. Extending coverage without richer alert text
would add reachable techniques the extractor still cannot distinguish. Payload
summaries, temporal context, cross-host correlation come first.

**For new data sources**, DARPA is the evidence it transfers: a second ontology
of ten host relations, a different alert template, ground truth transcribed
independently, and the same +0.43 gain. What changes per source is the template
and the vocabulary. What does not change is the architecture.

**Close honestly:** the open question is whether it holds under a bridge
curated by someone blind to the evaluation data. That is the experiment I would
run next, and it is in Future Work.

---

# Handling pressure

**If you do not know:** "I did not measure that, so I would be guessing.
What I can tell you is…" then pivot to what you did measure. Never invent a
number. Every figure you quote must exist in the thesis.

**If challenged on the small sample:** agree immediately. 18 communities, one
dominant technique, overlapping intervals. Then point at DARPA, where the
intervals are disjoint and all three models agree.

**If asked why not a bigger model / GPU:** the constraint was the research
question, not a limitation. The point was whether this works where cloud APIs
are prohibited.

**If asked what you would do differently:** instrument runtime, and curate the
bridge blind to the evaluation data. Both are honest, both are in Future Work.

**Pace.** You know this work better than anyone in the room. Slow down on
slides 19 and 20 — they are your strongest evidence, and rushing them is the
single easiest way to undersell the thesis.
