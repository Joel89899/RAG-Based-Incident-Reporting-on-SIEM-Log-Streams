

## From:
## To:
## Cc:
## Date:
## From:
## To:
## Date:
Re: Thesis Supervision Inquiry and Proposal Draft
Mwende, Joel (Stud SRH-University) Joel.Mwende@stud.srh-university.de
schwarz@posteo.de
Schwarz, Klaus (Lehre SRH Hochschulen Berlin GmbH) Klaus.Schwarz@srh-
hochschulen.de
## Thu 19. Mar 2026, 20:11
Master Thesis Proposal SRH.pdf 221 KB
## Dear Professor,
I hope you are doing well. I am reaching out to ask whether you might be open to supervising my
MSc thesis as part of the requirements for SRH and CyberMACS. I have attached my proposal
outlining the planned study.
I would greatly appreciate any feedback and would be happy to meet regularly at a time that suits
you.
Thank you for your time.
Kind regards,
## Joel Mwende
Schwarz, Klaus (Lehre SRH Hochschulen Berlin GmbH) Klaus.Schwarz@srh-
hochschulen.de
Mwende, Joel (Stud SRH-University) Joel.Mwende@stud.srh-university.de,
schwarz@posteo.de
## Mon 23. Mar 2026, 18:09
## Dear Joel,
Thank you for submitting your thesis proposal. I have reviewed it carefully. The following
assessment reflects my position as potential first supervisor.
## STRENGTHS
The literature review is honest and accurate. The gap you identify, closed model dependency in
existing SOC automation work, is real and correctly motivated. Your three research questions are
specific and your hypotheses are falsifiable. The experimental design, stratified sampling, three
repetitions, Cohen's Kappa for manual dimensions, is methodologically sound on the surface. The
## 1 / 11

choice of BETH and UNSW-NB15 is defensible.
## CRITICAL ISSUES
- The contribution is a benchmark, not a thesis.
You did not train the models. You did not design the dataset. You did not build the evaluation
infrastructure. The ReAct agent wrapper is the only original artifact in this proposal and it is a
Python loop calling Ollama with tool definitions. Running five pre-trained models on an existing
dataset and reporting which one scores higher is a conference paper at best. It is not a master's
thesis. The result does not transfer to a different task, a different dataset, or next quarter's model
release. A benchmarking study that will be obsolete before the thesis is defended is not a
contribution to the field.
- The failure taxonomy does not rescue the contribution.
The taxonomy is the only element with potential novelty. However, manually annotating outputs
from systems you do not control or understand at the weights level produces observations, not
explanations. You cannot open the models. Any mechanistic claim about why one model fails
differently from another is speculation.
- BETH is not the right dataset for this evaluation.
BETH was designed for unsupervised anomaly detection. Its labels are binary anomaly flags, not
structured multi-category judgments. The mapping from BETH labels to attack classification correct
or incorrect requires methodological choices that the proposal does not address.
- Two errors that must be corrected regardless of direction.
First, every date in the timeframe table reads 2024. This is 2026. Second, Reference 9 contains the
placeholder text from the conference submission template. Both errors suggest the proposal was
not reviewed before submission. I also guess you are aware of SRH's AI policy by now.
## PATH FORWARD
I will not supervise the thesis as currently proposed. I am willing to supervise one of two directions.
Option A: Pipeline transfer to security telemetry.
You apply the methodology you are currently learning in the OSINT course directly to SIEM log
data. Embeddings and community detection discover incident threads across fragmented alert
streams. Zero-shot classification with grammar constraints maps communities to MITRE ATT&CK
techniques. A knowledge graph reconstructs attack chains. A RAG layer retrieves contextual threat
intelligence. The output is a Level 3 actionable incident report evaluated for factual consistency
against ATT&CK procedure descriptions as ground truth. This produces a working artifact, a
## 2 / 11

durable evaluation framework, and a genuine contribution to the field.
Option B: Domain-adaptive contrastive learning for security log embeddings.
You design a loss function that encodes the structural relationships of the ATT&CK technique
hierarchy into the embedding space. Log sequences belonging to the same technique are pulled
together. Techniques that are distant in the kill chain are pushed apart. The distance weighting is
derived from domain knowledge, not arbitrary. The output is a security-specific embedder that other
researchers can use and that is not obsoleted by the next model release. This is the harder path
and the higher payoff.
Both options require you to demonstrate that you can execute the foundational methodology. Your
current OSINT course paper submission is the immediate test of that.
Please revise the proposal in line with one of the two directions above and resubmit for review.
Best regards,

## Prof. Dr. Klaus Dieter Schwarz
Head of Study Programme
M.Sc. Computer Science focus Cyber Security
## Campus Leipzig
SRH University of Applied Sciences Heidelberg
School of Technology and Architecture
## Prager Str. 40
## D-04317 Leipzig
klaus.schwarz@srh-hochschulen.de
www.srh-university.de

## Rektor: Prof. Dr. Victoria Büsch
## Vorsitzender University Board: Prof. Dr. Christof Hettich

## Trägergesellschaft
SRH Hochschulen GmbH
Ludwig-Guttmann-Str. 6
## 69123 Heidelberg
## Geschäftsführer: Dr. Thorsten Bagschik
Amtsgericht Mannheim, HRB 337518
## 3 / 11

## From:
## To:
## Date:
## From:
## To:
## Cc:
## Date:
## From:
## To:
Mwende, Joel (Stud SRH-University) Joel.Mwende@stud.srh-university.de
Schwarz, Klaus (Lehre SRH Hochschulen Berlin GmbH) Klaus.Schwarz@srh-
hochschulen.de
## Tue 24. Mar 2026, 11:59
## Dear Professor,
Thank you very much for your detailed feedback.
I will rework the OSINT assignment and rewrite my proposal accordingly.
Thank you again for your guidance.
Kind regards,
## Joel Isaria Mwende
Mwende, Joel (Stud SRH-University) Joel.Mwende@stud.srh-university.de
Schwarz, Klaus (Lehre SRH Hochschulen Berlin GmbH) Klaus.Schwarz@srh-
hochschulen.de
Klaus Schwarz schwarz@posteo.de
## Wed 8. Apr 2026, 09:12
Master Thesis Proposal_Revised.pdf 278 KB
## Dear Professor,
Thank you again for your detailed feedback on my previous submission.
As discussed, I have revised my thesis proposal accordingly. I am submitting the updated version
for your review.
I appreciate your guidance and would be grateful for any further comments you may have.
Kind regards,
## Joel Isaria Mwende
Mwende, Joel (Stud SRH-University) Joel.Mwende@stud.srh-university.de
Schwarz, Klaus (Lehre SRH Hochschulen Berlin GmbH) Klaus.Schwarz@srh-
hochschulen.de, Klaus Schwarz schwarz@posteo.de
## 4 / 11

## Date:
## From:
## To:
## Cc:
## Date:
## Mon 13. Apr 2026, 08:26
Master Thesis Proposal_Revised.pdf 283 KB
## Dear Professor,
I hope you are doing well.
Please find the updated version of my research proposal attached. I have made a few minor
adjustments, and I would be grateful for any comments or recommendations you may have.
Thank you for your guidance.
Kind regards,
## Joel Mwende
Klaus Schwarz schwarz@posteo.de
Mwende, Joel (Stud SRH-University) Joel.Mwende@stud.srh-university.de
Schwarz, Klaus (Lehre SRH Hochschulen Berlin GmbH) Klaus.Schwarz@srh-
hochschulen.de
## Mon 13. Apr 2026, 15:51
## Dear Joel,
Thank you for your revised proposal. I can see that substantial work went into the literature
review.
Before I can provide a full assessment, I need to understand one thing. You reference Louvain
community detection throughout the proposal as your clustering method in Stage 1. You also
discuss the limitation identified in SauronEyes [15] regarding Louvain's inability to handle
overlapping communities, and you state that this will be addressed in error analysis.
Can you walk me through exactly what you plan to implement? Specifically, which library and
which function call will perform the clustering? What does the input to that function look like and
what does the output look like? How does the algorithm you plan to use handle the case where
one alert belongs to two attack chains? Will you use fast_clustering from lang chain, the one we
used during the OSINT Course?
Also, please clarify the following for me:
## 5 / 11

## From:
## To:
## Cc:
## Bcc:
## Date:
- Which two open-weight LLM configurations will you use? Please provide model names,
parameter counts, and quantization levels.
- Can you describe why the DARPA Transparent Computing dataset is the right Dataset for your
thesis?
- What will be working as ground truth in your thesis to measure against?
Best regards,
## Prof. Dr. Klaus Dieter Schwarz
Mwende, Joel (Stud SRH-University) Joel.Mwende@stud.srh-university.de
Klaus Schwarz schwarz@posteo.de
Schwarz, Klaus (Lehre SRH Hochschulen Berlin GmbH) Klaus.Schwarz@srh-
hochschulen.de
navaneethsrhteacher@gmail.com , tugce.balli@khas.edu.tr , joelmwende@gmail.com ,
Shivananjappa, Navaneeth (Lehre SRH Hochschulen Berlin GmbH)
Navaneeth.Shivananjappa@srh-hochschulen.de, Shivananjappa, Navaneeth (Lehre SRH
Hochschulen Berlin GmbH extern) Navaneeth.Shivananjappa.extern@srh-
hochschulen.de
## Mon 13. Apr 2026, 22:48
## Dear Professor,
Thank you for your questions. Here is some clarification as requested.
The Louvain community detection will use 'community_multilevel' from python-igraph. The input is
a weighted graph in which edges connect alert pairs with cosine similarity > 0.95. Communities with
intra-tactic homogeneity <0.70 will be flagged as potential overlapping cases (per the limitation
noted in SauronEyes) and excluded from classification. LangChain's fast_clustering was not
suitable, as it is designed for document retrieval rather than graph-based alert correlation.
As for the LLMs, the intention was to use the 8B/12B models (Mistral Nemo 12B at Q5_K_M
quantization and Qwen3-8B-Instruct at Q4_K_M quantization). Given hardware constraints on my
machine (4GB VRAM on an RTX 3070 Ti), the pipeline will likely use qwen2.5:3b (Q4_K_M) for
## 6 / 11

## From:
## To:
## Date:
initial evaluation. A trial run on CIC-IDS 2017 with this model completed successfully, and larger
models remain a target for future replication on higher-VRAM hardware.
As for the dataset, DARPA TC was chosen because it contains real red-team activity with ATT&CK
labels, aligns with the evaluation setups of key papers (AGLHunter, SauronEyes), and its raw audit
logs closely reflect enterprise SIEM telemetry. However, one consideration is its scale, which will be
addressed through stratified sampling and incremental pipeline validation.
Ground truth will come from ATT&CK tactic/technique labels mapped via the MITRE STIX bundle
(for CIC-IDS 2017) and DARPA's official ground-truth report (for TC). Report consistency will be
measured against retrieved ATT&CK procedure descriptions.
As mentioned earlier, I have tested the embedding and clustering stages on the CIC-IDS 2017
dataset. Here is a link to the code, notebooks, and sample outputs if you would like to review the
actual flow and intermediate results.
I am happy to make any adjustments based on your feedback.
## Best Regards,
## Joel Isaria Mwende.
Klaus Schwarz schwarz@posteo.de
Mwende, Joel (Stud SRH-University) Joel.Mwende@stud.srh-university.de
## Wed 15. Apr 2026, 10:10
## Dear Joel,
I received your message regarding my availability. Firstly, I am currently waiting for your response
and was unaware that you were waiting for my input. Secondly, your thesis proposal is of such
poor quality that I fear it will fail under the current circumstances. Finally, I am not currently
seeing that you are devoting the necessary effort to your thesis work to achieve a passing grade,
let alone a satisfactory one.
Please respond soon with more care and better quality.
Best regards,
## Klaus Schwarz
## 7 / 11

## From:
## To:
## Date:
## From:
## To:
Mwende, Joel (Stud SRH-University) Joel.Mwende@stud.srh-university.de
Klaus Schwarz schwarz@posteo.de, Schwarz, Klaus (Lehre SRH Hochschulen Berlin
GmbH) Klaus.Schwarz@srh-hochschulen.de
## Wed 15. Apr 2026, 10:43
## Dear Professor,
Thank you for your feedback.  I apologize for the confusion regarding communication.
I take your concerns seriously and want to improve my work. I previously conducted a systematic
literature review to identify what has been done in analyzing SOC data. And I went ahead and
proposed a pipeline inspired by the OSINT class, the only change being that I intended it to run
locally due to privacy concerns that may arise in real-world scenarios.
After that I proposed a technical pipeline that converts raw SIEM alert records into plain-text
representations and encodes them as 384-dimensional sentence embeddings using the all-MiniLM-
L6-v2 model, it then computes pairwise cosine similarity and applies Louvain community detection
to group semantically related alerts into incident communities, then each community is classified
against the MITRE ATT&CK framework using a locally deployed language model, lastly a RAG-
augmented generation step retrieves the most relevant ATT&CK procedure descriptions from a
ChromaDB vector knowledge base and uses them to produce a structured incident report. I them
implemented it with the smaller CIC-IDS dataset using qwen 2.5 with 3B parameters, a caveat due
to limited local processing capacity, and shared the Link to the pipeline in the previous response.
I am aware that the proposal document itself needs to better reflect this level of technical detail,
and I am ready to revise it based on your specific guidance. I would be very grateful if you could
point out the sections or criteria that need improvement, so I can address them precisely.
I would welcome the opportunity to discuss it with you directly at a time that suits you.
Kind regards,
## Joel Isaria Mwende
Klaus Schwarz schwarz@posteo.de
Mwende, Joel (Stud SRH-University) Joel.Mwende@stud.srh-university.de
## 8 / 11

Date:Wed 15. Apr 2026, 11:35
## ATT0006 9 KB
## Dear Joel,
Thank you for your reply. I have attached the SauronEyes paper to this email. Please read it in full
before responding. I suspect you may have been working from the abstract, as the full text was
behind the IEEE paywall.
I must be direct with you. I have now sent you three rounds of specific technical questions. In
each round, you restated your plan instead of answering the questions. You justify your choices
but you do not correct anything. That pattern needs to stop. This email contains my full technical
assessment. Please read it carefully.
- You misread the SauronEyes paper.
SauronEyes does not build its graph from embedding similarity. The paper constructs two graphs
directly from raw audit log structure. The Interaction Graph captures real causal system
relationships: process forked process, process wrote to file, process connected to socket. The
Knowledge Graph captures entity attributes: IP addresses, file paths, parent-child process
relationships. These edges carry meaning. They represent actual system calls with timestamps
and causal direction. The disentanglement module, the path-aware GNN, the LightGCN, all of it
operates on graph structure that exists in the data before any embedding is computed.
Your pipeline does something fundamentally different. You embed aler t text into 384-
dimensional vectors, compute pairwise cosine similarity, threshold it, and call the result a graph.
That graph has no causal structure. It has no directional edges. It has no entity-relationship
semantics. The edges mean only "these two alerts scored above 0.95 similarity." That is not a
graph problem. That is a proximity lookup on a vector space.
The paper also explicitly argues against the algorithm you chose. Section V-D.2 and Figure 4
explain why Louvain fails for attack reconstruction. The authors replace Louvain with BIGCLAM
because Louvain cannot handle overlapping communities. You identified this limitation in your
proposal and then chose Louvain anyway, with a filter for the cases where it fails. You adopted
the algorithm that your own reference paper rejects.
Further, community detection in SauronEyes is a post-detection visualization step. The system
SauronEyes_Disentangling_Voluminous_Logs_to_Unveil_Camouflaged_Attack_Intentions.pdf
## 6,2 MB
## 9 / 11

has already classified every edge as benign or malicious. Community detection groups confirmed
malicious edges into coherent attack campaigns for analyst presentation. You are using
community detection as a primary analytical step. That is a different task entirely.
- You do not understand how knowledge graphs are constructed.
This is my central concern. In my OSINT pipeline, graph construction works as follows. Text is
embedded. Communities are detected directly on the embedding space using a greedy cosine-
threshold approach. No graph is needed for this step because it operates on the similarity matrix
directly. Then, an LLM reads the actual text within each community and extracts semantic triples:
subject, relation, target. "Entity X performed action Y on Entity Z." Those triples become the
edges of a knowledge graph built with NetworkX. The edges carry real meaning because a
language model understood the content and identified the relationships.
Your pipeline skips this entirely. You go from embeddings to a similarity threshold to a graph
where the edges carry no semantic content at all. You then run Louvain on that graph, which just
re-clusters what the embeddings already encode. There is no step in your pipeline where
meaning enters the graph. Without an LLM extracting actual relationships from the alert content,
there is nothing for the knowledge graph to represent and nothing meaningful for your RAG layer
to retrieve against.
This is the same structural error as your SauronEyes misreading. SauronEyes builds graphs from
real system call relationships. My pipeline builds graphs from real entity relationships extracted
by an LLM. Both produce graphs where edges carry meaning. Your pipeline produces a graph
where the edges carry only "similar enough." That is not a knowledge graph. That is a similarity
matrix with extra steps.
- You did not use the course materials.
In my previous email, I asked whether you would use fast_clustering from LangChain. That
function does not exist. The tool used in my course is
sentence_transformers.util.community_detection. A student who had opened the course
notebook would have corrected me. You instead wrote that "LangChain's fast_clustering was not
suitable, as it is designed for document retrieval rather than graph-based alert correlation." That
sentence describes a non-existent function, from a library that does not contain it, dismissed
with a fabricated technical reason. This tells me you have not opened the course materials.
The course notebook contains the complete pipeline: embedding with all-MiniLM-L6-v2,
## 10 / 11

community detection with util.community_detection, LLM-based classification of communities,
LLM-based knowledge graph triple extraction, ChromaDB for RAG, and report generation. Every
component you are trying to build is already demonstrated in the materials I provided. You are
reconstructing a broken version of a working pipeline from surface-level readings of papers that
solve different problems.
- Your original questions remain unanswered.
Please name three specific DARPA TC fields and map each one to a production SIEM equivalent.
Please take one CIC-IDS 2017 label and walk through the exact STIX lookup that produces the
ATT&CK technique assignment. Please explain why a graph-based approach is the right choice
for data that has no inherent graph structure.
The RTX 3070 Ti has 8 GB of VRAM, not 4 GB.
- Where this leaves us.
I am not asking you to abandon your topic. Automated triage and classification of SIEM alerts
using local language models is a legitimate research question. But the pipeline must follow from
the properties of your data and the requirements of your research question. Right now you are
assembling techniques from paper abstracts without understanding why those techniques exist
or what data structures they require.
If you want to build something that works, go back to the course materials. The pipeline is there.
Adapt it to SIEM alert data. Use the embedding and community detection steps as they are
taught. Use the LLM to extract meaningful relationships from alert content and build a real
knowledge graph. Use ChromaDB and RAG to generate reports grounded in ATT&CK procedure
descriptions. That is a thesis. What you have now is not.
Please also send me the notebook link.
Best regards,
## Prof. Dr. Klaus Dieter Schwarz
## 10 Emails
## 11 / 11