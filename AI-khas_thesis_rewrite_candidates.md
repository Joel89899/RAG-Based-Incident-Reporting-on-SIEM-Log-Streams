# Review Candidates for Turnitin-Marked Thesis Text

This file is for review only. None of these candidates has been applied to the
thesis. The English abstract and its keywords are excluded as requested.

The candidates preserve the reported measurements, model names, citations,
technical meaning, and limitations. Passages that reproduce pipeline inputs,
prompts, or model outputs are identified as experimental records and should
remain verbatim unless the corresponding experiment is rerun.

## Introduction

### I-01 — Turnitin page 14; `chapters/introduction.tex`, opening paragraph

Security Operations Centres (SOCs) monitor organisational systems for signs of
compromise, but the volume of alerts exceeds what their staff can inspect.
Firewalls, network sensors, and endpoint tools may generate more than 10,000
alerts per day, of which up to 70\% are false positives
\cite{Baha2025AIncidents}. Alert fatigue follows from this mismatch between the
rate at which systems produce security data and the rate at which analysts can
interpret it, rather than from a lack of effort by individual analysts
\cite{Bussari2026RAGSec:Networks}.

### I-02 — Turnitin page 15; `chapters/introduction.tex`, RAG sentence

RAG offers a more targeted use of language models within a SIEM: relevant
MITRE ATT\&CK material is retrieved first, and that material supplies the
context for real-time response guidance \cite{Ismail2025EnhancingCopilot}.

### I-03 — Turnitin page 15; `chapters/introduction.tex`, grouping problem

An intrusion rarely appears as one definitive alert. Its traces are distributed
across log sources and may be separated by hours or days. Yet many AI-based
tools still classify alerts independently, without establishing which records
belong to the same attack \cite{Pan2025Qwen3-PoweredDecision-Making}. This
removes the relationships needed to represent attack progression and makes the
output harder to interpret. Without those relationships, an incident report
cannot preserve the sequence of events that a senior analyst needs
\cite{Baha2025AIncidents}.

### I-04 — Turnitin page 15; `chapters/introduction.tex`, verifiability

Fluency does not make an incident report trustworthy. Current evaluations
often rely on text-similarity scores or expert ratings, neither of which tests
directly whether the report's technical claims match the attack behaviour
described by authoritative threat knowledge
\cite{Bussari2026RAGSec:Networks,Blefari2026CyberRAG:Tool}. A ground-truth-based
evaluation is therefore needed to distinguish a reliable report from one that
merely sounds convincing.

### I-05 — Turnitin pages 15–16; `chapters/introduction.tex`, privacy

Cloud deployment creates a separate problem. Many LLM-based SOC tools transmit
logs to commercial APIs or managed services. Such transmission may be
unacceptable in defence, critical infrastructure, finance, and healthcare,
where logs expose internal addresses, user names, process trees, and
vulnerability information. A pipeline that requires a cloud round trip is not
suitable for environments in which those records must remain on site.

### I-06 — Turnitin page 16; `chapters/introduction.tex`, thesis response

The proposed pipeline addresses these constraints through seven stages that
run on local hardware. Each stage passes its output directly to the next, and
no stage sends log data to a cloud service.

### I-07 — Turnitin page 17; `chapters/introduction.tex`, research-question roadmap

The evaluation follows three research questions: one concerns alert grouping,
one examines knowledge-graph construction, and the third tests retrieval and
report generation. Chapter~\ref{chap:related-work} derives these questions from
the literature review; Chapter~\ref{chap:implementation} specifies how each is
tested.

### I-08 — Turnitin page 17; `chapters/introduction.tex`, contribution lead-in

The thesis contributes a locally deployable architecture and evaluates it
across models and datasets. It also introduces a paired measure of
classification correctness and evidential grounding.

### I-09 — Turnitin page 17; `chapters/introduction.tex`, architectural contribution

\textbf{Architectural.} The pipeline converts SIEM alerts into incident reports
grounded in ATT\&CK without transmitting the source data. Its knowledge graph
does more than annotate an LLM response after generation: extracted behavioural
relations determine which ATT\&CK techniques retrieval may return. The graph
therefore records an auditable constraint that replaces a search across the
entire ATT\&CK matrix with a choice among candidates supported by the observed
behaviour.

### I-10 — Turnitin pages 17–18; `chapters/introduction.tex`, empirical contribution

\textbf{Empirical.} Three models were compared on two datasets at each measured
stage of the pipeline. Their ranking changes with the data: the strongest model
on network flows is not the strongest on host audit logs, while a 3B model at
4-bit quantisation remains usable when the larger models do not fit the
available hardware. Error attribution places the difference at triple
extraction. Whenever a model extracted the correct behaviour, graph-scoped
retrieval selected the correct technique.

### I-11 — Turnitin page 18; `chapters/introduction.tex`, evaluative contribution

\textbf{Evaluative.} The evaluation separates correctness from grounding.
Exact match tests the assigned ATT\&CK identifier against ground truth, whereas
cosine similarity measures how closely a generated report follows the retrieved
ATT\&CK procedure text. The experiments show that these scores can move in
opposite directions, so either score alone gives an incomplete account of
report quality. Because the framework requires only technique labels and the
retrieved context, it can be reused with other models and datasets.

### I-12 — Turnitin page 19; `chapters/introduction.tex`, Chapter 3 roadmap

\textbf{Chapter~\ref{chap:related-work}} reviews the five bodies of work on
which the pipeline depends. It uses that review to formulate the three research
questions and to distinguish this thesis from the closest existing systems.

### I-13 — Turnitin page 19; `chapters/introduction.tex`, Chapter 5 roadmap

\textbf{Chapter~\ref{chap:approach}} explains the seven pipeline stages,
including alert templating, embedding, community detection, triple extraction,
knowledge-graph construction, scoped retrieval, and grammar-constrained report
generation.

## Background and related work

### B-01 — Turnitin page 23; `chapters/background.tex`, embedding model

Alert sentences are embedded with all-MiniLM-L6-v2, a Sentence-BERT model that
returns a 384-dimensional vector for each input
\cite{Reimers2019Sentence-BERT:BERT-networks}. The smaller representation keeps
pairwise comparisons practical for approximately 14,000 alerts while retaining
the sentence-level signal needed for semantic similarity. Its contrastive
training places paraphrases near one another and unrelated sentences farther
apart, so similarity depends on meaning rather than exact word overlap.

### B-02 — Turnitin page 23; `chapters/background.tex`, community detection

In this thesis, communities are formed directly from sentence embeddings. A
greedy procedure groups alerts when their pairwise cosine similarity exceeds a
selected threshold. This avoids constructing an intermediate graph and leaves
the grouping stage unsupervised, while the embedding space supplies the
semantic proximity on which the grouping depends.

### B-03 — Turnitin page 30; `chapters/background.tex`, exact match

\textbf{Exact match rate} is the proportion of evaluated communities for which
the assigned ATT\&CK identifier equals the ground-truth identifier. An
assignment of T1046 is correct only when the reference label is also T1046;
assigning it to a T1110 community is an error. No partial credit is awarded.

### B-04 — Turnitin page 30; `chapters/background.tex`, parent match

\textbf{Parent match rate} allows for the hierarchy within ATT\&CK. A
sub-technique such as T1110.001 counts as a match when the reference label is
its parent, T1110, and the reverse comparison is treated in the same way. The
metric therefore recognises assignments that identify the correct behaviour at
an adjacent level of specificity.

### RW-01 — Turnitin page 33; `chapters/related-work.tex`, RQ3

\textbf{RQ3.} To what extent does knowledge-graph-grounded retrieval improve
the coherence, factual consistency, and evidential alignment of security
incident reports relative to ungrounded LLM generation?

### RW-02 — Turnitin page 33; `chapters/related-work.tex`, search sources

The review searched IEEE Xplore, Scopus, and the ACM Digital Library. IEEE
Xplore covers the main cybersecurity and networking conferences and journals;
Scopus extends the search across disciplines; and the ACM Digital Library adds
systems and human--computer interaction research relevant to SOC tools.

## Methodology

### M-01 — Turnitin page 44; `chapters/method.tex`, CIC-IDS selection

CIC-IDS-2017 is distributed as weekday capture files. Monday was excluded
because it contains only benign traffic, and Wednesday was excluded because it
contains only denial-of-service traffic. The remaining files combine benign
flows with reconnaissance, brute-force, web, infiltration, and botnet traffic.
To limit class imbalance, each label was sampled to at most 2{,}000 flows using
the fixed seed 42. This produced the reproducible working set used in the
experiments.

### M-02 — Turnitin pages 44–45; `chapters/method.tex`, CIC-IDS ground truth

Each CIC-IDS attack family was assigned one ATT\&CK technique as ground truth.
The mapping was created from the MITRE STIX~2.1 bundle by matching the dataset
label to the corresponding technique; for example, PortScan maps to Network
Service Discovery (T1046). These labels are withheld from the pipeline and used
only when its output is scored.

### M-03 — Turnitin page 45; `chapters/method.tex`, DARPA dataset

DARPA CADETS~E3 contains host audit records collected during a red-team
engagement. Its Common Data Model records describe processes, file objects, and
network flows. The engagement report divides the activity into four attack
windows, W1--W4, and documents the adversary techniques associated with each
window.

### M-04 — Turnitin page 45; `chapters/method.tex`, DARPA ground truth

The DARPA engagement report supplied two reference sets for each window. The
\emph{observable} set contains techniques expected to leave evidence in the
audit stream; the broader \emph{campaign} set also includes reported activity
that may not appear in those logs. Scoring uses the observable set because the
pipeline cannot recover behaviour absent from its input. For example, the W1
set is $\{$T1190, T1071, T1105, T1059, T1055, T1222$\}$.

### M-05 — Turnitin page 45; `chapters/method.tex`, model selection

The language model is a replaceable part of the pipeline, provided that it can
follow instructions under grammar-constrained decoding. The comparison covers
a 12B general-purpose model, a 7B code-oriented model, and a 3B model intended
for tighter hardware limits. Each model drives triple extraction, HyDE query
generation, and report generation through \code{llama-cpp-python}; all
inference remains on the host. Chapter~\ref{chap:implementation} records the
exact model releases, quantisations, and hardware.

### M-06 — Turnitin pages 45–46; `chapters/method.tex`, evaluation overview

Evaluation follows the pipeline at three points. Clustering metrics measure the
coherence of alert communities; classification metrics compare each assigned
ATT\&CK technique with ground truth; and report metrics test completeness and
grounding in the retrieved context. Every graph-scoped condition is paired with
a baseline that removes the graph constraint while retaining the same model and
evidence. Chapter~\ref{chap:implementation} defines the metrics, baselines, and
scoring protocol.

## Proposed approach

### PA-01 — Turnitin page 48; `chapters/proposed-approach.tex`, template lead-in

The descriptor phrases are joined in a fixed order to form one alert sentence.
The following example is produced for an SSH flow:

### PA-02 — Turnitin page 48; template output

Keep the alert sentence beginning `Network flow targeting SSH on port 22`
verbatim. It is an output of the deterministic template, not ordinary thesis
prose. Editing it in the thesis would make the documented example differ from
the implemented representation.

### PA-03 — Turnitin page 50; `chapters/proposed-approach.tex`, lookup limits

The lookup cannot tell whether a non-standard port hosts a legitimate service
or carries command-and-control traffic. It also assigns the same unknown-port
label regardless of how frequently that port occurs. The Stage~4 context
summary partly addresses the second limitation by reporting port diversity for
the community rather than for an individual flow.

### PA-04 — Turnitin page 50; `chapters/proposed-approach.tex`, DARPA templates

CADETS E3 required a host-event template because its records are audit events,
not network-flow summaries. Process execution, file operations, and privilege
changes are rendered as ``Process [name] [verb] [target][role tag]''. The verb
comes from the CDM event type: \texttt{EVENT\_EXECUTE} becomes ``executed'',
\texttt{EVENT\_WRITE} becomes ``wrote to'',
\code{EVENT_MODIFY_FILE_ATTRIBUTES} becomes ``changed permissions on'',
\texttt{EVENT\_FORK} becomes ``forked'',
\code{EVENT_CHANGE_PRINCIPAL} becomes ``changed privilege via'', and
\texttt{EVENT\_UNLINK} becomes ``deleted''.

### PA-05 — Turnitin page 51; `chapters/proposed-approach.tex`, template sparsity

A CIC-IDS sentence contains eight descriptors derived from fifteen flow
features, whereas a DARPA sentence usually contains one clause. The shorter
DARPA representation yields lower cosine similarities, so its operating
threshold is 0.75 rather than 0.80. This loss of embedding density was accepted
to keep each host event readable to an analyst and interpretable without
requiring the model to infer the meaning of flow statistics.

### PA-06 — Turnitin page 51; `chapters/proposed-approach.tex`, embedding

The all-MiniLM-L6-v2 sentence transformer encodes every alert as a
384-dimensional vector \cite{Reimers2019Sentence-BERT:BERT-networks}. Its size
keeps inference practical on the target hardware, and prior security-alert
studies provide evidence for its suitability
\cite{Baha2025AIncidents,FernandezSaura2026EnhancingSharing}. Embeddings are
computed once and reused during clustering and retrieval.

### PA-07 — Turnitin page 53; relation-definition excerpts

Keep the highlighted relation definitions beginning `Evidence: repeated
similar-sized connections`, `: outbound control channel`, and `regular IAT
timing` verbatim. They reproduce the prompt used during the experiment.
Rewording them without rerunning extraction would change the documented
experimental condition.

### PA-08 — Turnitin pages 53–54; `chapters/proposed-approach.tex`, constrained output

A JSON-schema grammar constrains generation so that the output is machine
readable. It permits a \texttt{triples} array containing one to four objects;
every object must contain a \texttt{subject}, one of seven allowed
\texttt{relation} values, and a \texttt{target}. This removes free-text parsing
and prevents relations outside the vocabulary. Temperature is set to zero for
deterministic decoding. Extracting typed relations with an LLM follows earlier
security knowledge-graph work
\cite{Li2025DesignModels,Hu2024LLM-TIKG:Model}.

### PA-09 — Turnitin page 54; `chapters/proposed-approach.tex`, prompt importance

Triple extraction connects unsupervised communities to their semantic
interpretation, making its prompt consequential for every later stage. If the
prompt elicits the wrong relation, the bridge points retrieval towards the
wrong ATT\&CK techniques and the error persists through report generation.

### PA-10 — Turnitin page 54; `chapters/proposed-approach.tex`, prompt structure

The prompt has five components. The system instruction states the task and
output constraint. Relation definitions specify the seven permitted
behaviours. A context summary reports the number of flows, destination-port
diversity, and traffic concentration on the busiest port. Up to six alert
sentences supply community-level evidence. Finally, worked examples show how
to justify a small number of well-supported triples for port scans,
brute-force attempts, and denial-of-service traffic.

## Implementation and worked example

### IM-01 — Turnitin page 65; `chapters/implementation.tex`, clustering parameter

The greedy community-detection routine uses one tunable value: the minimum
cosine similarity required between alert embeddings in the same community.

### IM-02 — Turnitin page 66; threshold-sweep reference

Chapter~\ref{chap:results} reports the complete sweeps and explains the choice
of operating threshold for each dataset.

### IM-03 — Turnitin page 72; `chapters/implementation.tex`, error attribution

For every scored community, the evaluation checks whether an extracted
relation reaches the ground-truth technique through
\code{RELATION_TO_TECHNIQUES}. If it does, the correct technique was available
to retrieval and a wrong assignment is attributed to that stage. If it does
not, the failure occurred during triple extraction; communities with no
triples fall into the same category. This procedure measures the upper bound
that Stage~4 places on classification accuracy.

### IM-04 — Turnitin page 72; `chapters/implementation.tex`, worked-example lead-in

The worked example follows one CIC-IDS SSH brute-force community through the
seven stages. Appendix~\ref{chap:appendix} contains the complete prompts.

### IM-05 — Turnitin pages 72–73; alert example

Use this lead-in: `Stage~1 renders each flow as an alert sentence; one of the
six sentences is reproduced below.`

Keep the following alert sentence verbatim. It is the actual Stage~1
representation and should not be rewritten independently of the template.

### IM-06 — Turnitin page 73; triple example

Use this lead-in: `Given the six alert sentences and the single-port community
context, Stage~4 returns one triple.`

Keep the JSON triple verbatim because it records the extractor's output.

### IM-07 — Turnitin page 73; bridge and HyDE lead-in

Stage~5 maps \code{BRUTE_FORCES_CREDENTIAL} to T1110 and T1110.001, adding a
bridge edge from the behavioural subject to each technique. Stage~6 then uses
the triple to generate the HyDE query reproduced below.

### IM-08 — Turnitin page 73; HyDE text

Keep the passage beginning `The adversary employs a brute force attack against
SSH services` verbatim. It is model-generated experimental output. A polished
rewrite would no longer be the query used for retrieval.

### IM-09 — Turnitin pages 73–74; generated report

Use this lead-in: `KG-scoped retrieval ranks T1110.001 (Password Guessing)
first. Stage~7 generates the following report from that result.`

Keep the JSON report, including its highlighted summary and evidence fields,
verbatim. Those fields are measured outputs, and changing them would invalidate
the reported faithfulness score.

## Results and discussion

### RD-01 — Turnitin page 82; `chapters/results.tex`, coder-model retrieval

\textbf{Qwen2.5-Coder-7B.} Only 2 of the 18 communities are exact matches,
giving a rate of 11.1\%, and the retrieval hit rate is likewise 0.111. Triple
extraction accounts for this result. Most communities are assigned a
denial-of-service relation, so their HyDE queries describe flooding and
retrieval returns T1498 or T1499 candidates regardless of the reference label.
Although every community receives a graph-scoped candidate set, that constraint
cannot recover a technique excluded by an incorrect behavioural relation.

### RD-02 — Turnitin page 82; `chapters/results.tex`, 3B result

\textbf{Qwen2.5-3B.} Despite its smaller parameter count, the 3B model reaches
27.8\% exact match, compared with 11.1\% for the coder model. Its extracted
relations are less concentrated in one behaviour, although all five correct
assignments still belong to PortScan communities.

### RD-03 — Turnitin page 83; `chapters/results.tex`, extraction ceiling

The coder model's 11.1\% exact-match rate originates before retrieval. It
assigned denial-of-service relations to 16 of 18 communities, after which the
pipeline classified the behaviour represented by those relations. Better
reranking cannot correct a technique that never enters the candidate set. For
this dataset, improvement must begin with the alert representation or the
triple extractor.

### RD-04 — Turnitin page 85; `chapters/results.tex`, Figure 7.6 caption

Correctness and faithfulness for the three CIC-IDS-2017 models. Qwen2.5-Coder
produces reports closely aligned with retrieved evidence but assigns the wrong
techniques (bottom right). Mistral-Nemo assigns techniques more accurately,
although its report language is less similar to ATT\&CK procedure text (top
left). No model occupies the high-correctness, high-faithfulness quadrant. The
dashed lines show majority-class accuracy and mean faithfulness across models.

### RD-05 — Turnitin page 85; `chapters/results.tex`, interpreting both metrics

Faithfulness and correctness answer different questions. Exact match tests the
assigned technique against ground truth; faithfulness tests whether the report
follows the evidence returned by retrieval. A high exact-match score paired
with low faithfulness indicates a correct assignment that is weakly supported
in the report. The reverse pairing indicates that the report follows its
evidence closely, but that the evidence points to the wrong technique. Both
scores are therefore needed.

### RD-06 — Turnitin page 85; `chapters/results.tex`, Mistral grounding

Mistral-Nemo-12B combines 0.833 correctness with 0.478 faithfulness. Its
evidence fields retain packet counts, TCP flag patterns, and timing categories,
whereas ATT\&CK procedure descriptions express behaviour in operational terms.
This difference in register helps explain why summary grounding reaches 0.727
but evidence grounding reaches only 0.567. The correctly classified example in
Chapter~\ref{chap:implementation}, whose faithfulness score is 0.396, exhibits
the same vocabulary mismatch.

### RD-07 — Turnitin page 87; `chapters/results.tex`, DARPA precision and recall

Under KG anchoring, precision ranges from 0.958 to 1.000, whereas recall ranges
from 0.475 to 0.558. The system therefore makes few incorrect assignments but
misses roughly half of the techniques used in the engagement. Some reference
techniques, including T1055 and T1222, may leave evidence too subtle for the
current host-event templates. The main constraint on recall is thus the alert
representation rather than retrieval.

### RD-08 — Turnitin page 87; Figure 7.8 caption

DARPA CADETS E3 F1 scores by attack window and model, comparing KG-anchored
retrieval with the unscoped baseline.

### RD-09 — Turnitin pages 87–88; `chapters/results.tex`, per-window results

Figure~\ref{fig:darpa-per-window} separates F1 by attack window. KG anchoring
outperforms the baseline in every window for every model, with gains of
approximately 0.33--0.61. All three models attain their highest anchored scores
in W3 (0.80--0.83), whose activity leaves the clearest traces in the audit
stream. Baseline scores remain between 0.15 and 0.32. Because the gain recurs
across all four windows, it cannot be attributed to one unusually easy segment
of the engagement.

### RD-10 — Turnitin page 88; clustering subsection heading

`How Coherently Does Semantic Clustering Group Related Alerts?`

### RD-11 — Turnitin page 90; `chapters/results.tex`, host ontology

The coder model assigns a wider variety of relations when the host ontology
provides finer behavioural categories.

### RD-12 — Turnitin page 90; `chapters/results.tex`, 3B consistency

Qwen2.5-3B does not lead either dataset, but its performance is stable. It
reaches 27.8\% exact match on CIC-IDS, above the coder model's 11.1\%, and an
F1 of 0.685 on DARPA, less than three points below the leading result. A 3B
model at 4-bit quantisation can therefore support this pipeline on hardware
that cannot accommodate the larger alternatives, including the air-gapped
systems considered in this thesis.

### RD-13 — Turnitin page 90; `chapters/results.tex`, weakness lead-in

The errors are not distributed randomly. Their pattern identifies the stages
and data conditions that limit classification.

### RD-14 — Turnitin page 90; `chapters/results.tex`, minority classes

\textbf{Minority classes are rarely recovered.} T1203 and T1071.001 each occur
in one community, and none of the three models identifies either correctly.
Each model also recovers at most one of the two brute-force communities. Because
the pipeline remains unsupervised through Stage~4, it cannot up-weight rare
classes as a supervised classifier could. In CIC-IDS, infiltration and botnet
flows resemble reconnaissance at the feature level; their embeddings therefore
fall near port-scan communities and elicit the corresponding relation during
extraction.

### RD-15 — Turnitin pages 90–91; `chapters/results.tex`, flow ambiguity

\textbf{Some flow records are behaviourally ambiguous.} A single SYN packet to
port 21 may belong to a scan, a credential attack, or a botnet callback. Flow
statistics alone do not expose payload content, state across connections, or
attacker intent, so later stages cannot recover distinctions absent from the
alert text. The DARPA result supports this interpretation: classification
improves when process names, file paths, and connection direction provide
richer evidence.

### RD-16 — Turnitin page 91; `chapters/results.tex`, HyDE error propagation

\textbf{HyDE preserves errors as readily as evidence.} An incorrect relation
produces a query about the wrong attack, which in turn retrieves the wrong
techniques. Report generation can then produce a coherent account of a
misclassified event. This sequence is visible in the coder model's CIC-IDS
results, where repeated denial-of-service relations lead to internally
consistent flood reports for non-flood communities. Faithfulness captures that
internal consistency; exact match reveals the incorrect technique.

### RD-17 — Turnitin page 91; `chapters/results.tex`, timing scope

The experiments did not record wall-clock duration, so no throughput estimate
is reported. Scalability can still be analysed from how often each stage runs,
although this describes computational growth rather than measured execution
time.

### RD-18 — Turnitin page 91; `chapters/results.tex`, two scaling regimes

Stages~1--3 operate per alert: the template processes each record, the encoder
embeds 14{,}182 sentences, and clustering compares their vectors. Stages~4--7
operate per community. On CIC-IDS, this required 54 triple extractions and 18
scored reports rather than one language-model call per alert. LLM inference
therefore scales with community count, and clustering reduced the number of
items sent to a language model by roughly a factor of 260. That reduction makes
single-laptop inference feasible, including use of the 3B quantised model.

### RD-19 — Turnitin pages 91–92; `chapters/results.tex`, clustering ceiling

Community detection has a different limit: its $n \times n$ similarity matrix
grows quadratically with the number of alerts, whereas LLM inference grows with
the number of communities. The quadratic term is manageable at 14{,}182 alerts
but would dominate at roughly ten times that volume. A live deployment would
therefore need the sliding-window design proposed in
Chapter~\ref{chap:conclusions}. This scaling limit belongs to the current
clustering implementation; graph anchoring does not depend on how the
communities are produced.

### RD-20 — Turnitin page 92; `chapters/results.tex`, maintenance

Maintenance is concentrated in the ATT\&CK corpus, the bridge mapping, and
model validation. The STIX snapshot contains 691 retrievable technique records,
whereas the current ATT\&CK release distinguishes 222 techniques and 475
sub-techniques. Framework revisions therefore require the corpus and mapping to
be refreshed. Bridge coverage is also manual: the present mapping reaches 12
network-flow technique identifiers and 21 host-event identifiers, and each
extension requires new curation. Replacing the language model is mechanically
simpler, but not evidentially free. With identical prompts and graph logic, the
tested models range from 11.1\% to 83.3\% exact match; any replacement must
therefore be validated on labelled data.

### RD-21 — Turnitin page 92; `chapters/results.tex`, dataset and corpus limits

CIC-IDS-2017 was collected in a controlled laboratory and contains limited
attack diversity. CADETS E3 is closer to an operational setting, but it covers
one engagement on FreeBSD. The retrieval corpus introduces another mismatch:
ATT\&CK procedure descriptions are often more abstract than the alert text.
This difference in granularity lowers the measured grounding scores and limits
how broadly the results can be interpreted.

### RD-22 — Turnitin pages 92–93; `chapters/results.tex`, threshold selection

The operating threshold was chosen from a sweep by locating the region where
purity and intra-cluster similarity levelled off without reducing communities
below a scoreable size. That criterion is a heuristic. Optimising instead for
minority-class recall could select another threshold and change later results.
One threshold was used for all models within a dataset to preserve the
comparison, so clustering was not individually tuned to any model.

### RD-23 — Turnitin page 93; `chapters/results.tex`, baseline comparability

The baseline differs by dataset. CIC-IDS uses direct LLM classification,
whereas DARPA uses unscoped similarity retrieval. Both remove graph-based
candidate restriction while holding their model and evidence constant, but
they remove different components of the full pipeline. Their improvements
should therefore be interpreted within each dataset, not as identical measures
that can be compared directly across datasets.

### RD-24 — Turnitin page 93; `chapters/results.tex`, circularity

The CIC-IDS mapping introduces a risk of circularity because the same author
curated both the relation-to-technique bridge and the reference labels with
knowledge of the attack families. Once extraction assigns the correct relation,
the bridge sharply narrows the answer, as the error attribution confirms. The
result should therefore be read narrowly: extracted-behaviour routing
outperforms unscoped retrieval and parametric classification on this dataset;
it does not show that reranking adds independent reasoning. The mapping still
allows one relation to reach several techniques, and the DARPA labels were
transcribed separately from its engagement report. A stronger future test
would use a bridge curated without access to the evaluation families.

### RD-25 — Turnitin page 93; `chapters/results.tex`, multi-label exception

CIC-IDS supplies one reference technique per community, so its score cannot
give partial credit when several techniques are present. This makes the
reported values conservative with respect to practical utility. DARPA partly
addresses the limitation by scoring a set of techniques for each attack
window.

### RD-26 — Turnitin page 94; `chapters/results.tex`, report-metric limitation

The report metrics measure semantic alignment, not the truth of individual
claims. Text can be close to an ATT\&CK procedure description while still
inventing a process name, port, or other technical detail. Faithfulness should
therefore be interpreted as retrieval alignment rather than factual
verification. Expert review would test a dimension that the current automated
metrics do not capture.

### RD-27 — Turnitin page 94; `chapters/results.tex`, summary of gains

Graph-scoped retrieval improves technique classification in every tested
condition. Mistral-Nemo on CIC-IDS and Qwen2.5-Coder on DARPA provide the
strongest model--dataset pairings; their outputs are structurally complete and
usually assign the correct technique while remaining aligned with retrieved
ATT\&CK text. The 3B results also show that the approach remains usable on
hardware available to a small SOC team.

### RD-28 — Turnitin page 94; `chapters/results.tex`, summary of failures

Error attribution places the remaining failures upstream of retrieval. Rare
classes provide little signal, flow records can hide distinctions in attacker
intent, and some observed signatures differ from the behaviour assumed by an
ATT\&CK description. When the correct technique entered the scoped candidate
set, reranking selected it. The most direct route to improvement is therefore a
richer alert representation and a more reliable extractor, rather than another
change to retrieval.

## Conclusion

### C-01 — Turnitin page 95; `chapters/conclusions.tex`, opening

This thesis tests whether open-weight models on consumer hardware can turn raw
SIEM logs into incident reports by grouping related alerts and grounding their
interpretation in threat knowledge. The experiments in
Chapter~\ref{chap:results} support that approach, but also identify constraints
that must be addressed before operational deployment.

### C-02 — Turnitin pages 96–97; `chapters/conclusions.tex`, empirical contribution

\textbf{Empirical.} Model size does not determine performance across data
types. Mistral-Nemo-12B exceeds the coder model by 72 percentage points on
network flows, while the coder model exceeds Mistral-Nemo by 7.5 F1 points on
host audit records. Error attribution places this reversal at extraction: no
model misclassified a community after extracting a relation that reached the
correct technique. Qwen2.5-3B provides the steadier compromise, with 27.8\%
exact match on CIC-IDS and 0.685 F1 on DARPA. Grammar-constrained decoding also
prevents malformed reports; every generated report contains all required
fields.

### C-03 — Turnitin page 97; `chapters/conclusions.tex`, evaluative contribution

\textbf{Evaluative.} Exact match and semantic grounding expose different
failures. On CIC-IDS, the coder model has the highest faithfulness score (0.621)
and the lowest exact-match rate (11.1\%): it writes evidence-aligned reports for
the wrong techniques. Reporting both metrics makes this case visible. The same
framework can be reused when models or datasets change because it depends only
on reference technique labels and the context returned by retrieval.

### C-04 — Turnitin page 97; `chapters/conclusions.tex`, alert-text limitation

The principal limitation lies in the alert representation. At the flow level,
a SYN packet sent to an FTP port can indicate reconnaissance, credential
guessing, or beaconing. Packet statistics do not reveal payload content,
cross-flow state, or longer temporal relationships, and no downstream model
can infer a distinction absent from its input. CADETS E3 supports this
interpretation: process names, paths, and connection direction produce better
classification across all three models.

### C-05 — Turnitin page 97; `chapters/conclusions.tex`, generalisation limits

Generalisation is also limited by the evaluation data. The experiments cover a
controlled network testbed, one FreeBSD red-team engagement, and only a small
part of ATT\&CK. Threshold selection favours purity and tightness; another
objective could alter both the communities and their downstream scores.
CIC-IDS further supplies one reference technique per community even though an
operational incident may contain several, so the reported score cannot reflect
partial multi-technique recovery and should be treated as a lower bound on
practical utility.

### C-06 — Turnitin pages 97–98; `chapters/conclusions.tex`, human evaluation

Semantic similarity cannot verify factual detail. A report may resemble an
ATT\&CK procedure in embedding space while inventing ports, timestamps, or
process names. The present evaluation does not include expert review, which
would provide an independent assessment of those claims.

### C-07 — Turnitin page 98; `chapters/conclusions.tex`, implication lead-in

The findings have three consequences for the design and evaluation of
LLM-assisted SOC tools.

### C-08 — Turnitin page 98; `chapters/conclusions.tex`, role of the graph

The knowledge graph contributes a constraint, not additional evidence. On
CIC-IDS, the coder model creates the largest reachable graph, with 12 technique
nodes, yet produces the weakest classifications. The strongest model reaches
only seven. Coverage is therefore less useful than accurate exclusion: a small
graph built from reliable relations removes more wrong candidates than a large
graph built from noisy extraction.

### C-09 — Turnitin page 98; `chapters/conclusions.tex`, model scale

Model scale is secondary to fit between a model and its input. Qwen2.5-3B
reaches 0.685 F1 on DARPA, whereas the larger coder model falls to 11.1\% exact
match on CIC-IDS. The model that leads one dataset performs worst on the other.
An organisation choosing a SOC model should consequently validate candidates
on its own telemetry instead of treating parameter count as a proxy for
suitability.

### C-10 — Turnitin page 98; `chapters/conclusions.tex`, evaluation

Incident-report generation still lacks a standard security benchmark. The
paired evaluation used here is reproducible: reference labels measure
correctness, and retrieved procedure text supplies a grounding target. It does
not replace analyst review, but it can reject systems whose technique
assignments or use of evidence fail before human evaluation begins.

### C-11 — Turnitin page 99; `chapters/conclusions.tex`, analyst interface

An operational interface should display the assigned technique, report fields,
source alerts, and retrieved ATT\&CK text together. Analysts could then accept,
correct, or reject an assignment rather than receiving an unexplained result.
Their corrections would also provide labelled feedback for later work on the
extractor and report generator. A live evaluation should measure whether this
interaction reduces triage time, which cannot be inferred from the static
datasets used here.

### C-12 — Turnitin page 100; `chapters/conclusions.tex`, technique coverage

\textbf{Expanded technique coverage.} The current bridge reaches 12 network
flow identifiers and 21 host-event identifiers, compared with more than 200
techniques in ATT\&CK. Candidate mappings could be proposed automatically from
procedure descriptions, but each would still require manual validation before
use. Extending the bridge to Lateral Movement, Persistence, Privilege
Escalation, and Defense Evasion is therefore mainly a curation task; the
pipeline architecture need not change.

### C-13 — Turnitin page 100; `chapters/conclusions.tex`, live ingestion

\textbf{Live stream ingestion.} The present implementation reads static CSV
and JSON files. Processing Kafka, Syslog, Wazuh, or Splunk input would require
incremental embeddings, sliding-window community detection, and a rule for
deciding when a community contains enough evidence to report. Embedding,
extraction, graph construction, and retrieval could remain unchanged, but
scheduling and window management would become part of the system.

### C-14 — Turnitin page 100; `chapters/conclusions.tex`, final problem statement

SIEM alert production continues to outpace manual triage, particularly for
multi-stage intrusions whose evidence is dispersed over time. Language models
can process that volume, but fluent reading alone is insufficient. A useful
incident report must expose the observations on which it rests and connect
them to recognised threat behaviour.

### C-15 — Turnitin page 100; `chapters/conclusions.tex`, final graph statement

The experiments show that a graph constructed from alert-derived relations can
provide this connection by restricting retrieval to behaviourally supported
ATT\&CK techniques. This restriction improved both classification and grounding
in the tested conditions. The graph does not replace the language model or
supply new facts. Its purpose is narrower: to prevent the report generator from
discussing techniques unsupported by the extracted evidence, leaving an
assignment that an analyst can inspect in a recognised taxonomy.

### C-16 — Turnitin page 101; `chapters/conclusions.tex`, final hardware statement

All seven stages ran on a laptop with 4~GB of VRAM and kept the logs on the
host. For an air-gapped SOC or an organisation subject to data-sovereignty
rules, local execution is not incidental to the design; it is a deployment
requirement.
