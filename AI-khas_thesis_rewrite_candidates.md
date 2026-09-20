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

