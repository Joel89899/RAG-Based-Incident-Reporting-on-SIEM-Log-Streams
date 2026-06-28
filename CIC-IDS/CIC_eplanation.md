# Deep Dive Explanation of the CIC-IDS-2017 Threat Mapping Notebook

This notebook implements a complete pipeline for analyzing network traffic flows, clustering them into semantic groups, and mapping each group to MITRE ATT&CK techniques. It uses a local large language model (Mistral-Nemo) to extract structured relationships, builds a knowledge graph, and employs retrieval-augmented generation (RAG) with ChromaDB for final technique prediction. The code also compares performance with and without a rule‑based engine (ablation study).

Below we walk through every cell, explaining **what** it does, **why** it matters, and **how** it fits into the bigger picture. We use plain language and avoid unnecessary jargon – think of this as a guided tour for a motivated beginner.

---

## Cell 1: Setting the Random Seed
```python
import os, random
import numpy as np

SEED = 42
os.environ['PYTHONHASHSEED'] = str(SEED)
random.seed(SEED)
np.random.seed(SEED)

try:
    import torch
    torch.manual_seed(SEED)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(SEED)
    try:
        torch.use_deterministic_algorithms(True, warn_only=True)
    except Exception:
        pass
except ImportError:
    pass

print('Seeded with', SEED)
```
**What it does:** Sets a fixed random seed (42) for Python’s built‑in random, NumPy, and PyTorch.  
**Why:** Ensures reproducibility – every time you run the notebook, the random numbers (e.g., sampling, model initialisation) are the same. This is crucial for scientific experiments.  
**How:** The seed is stored in environment variables and called for each library. PyTorch also enables deterministic algorithms where possible.  
**Fact:** Seed 42 is a popular choice (from “Hitchhiker’s Guide to the Galaxy”).

---

## Cell 2: Configuration and Setup
```python
import os, json, re, pandas as pd, numpy as np
import networkx as nx, chromadb
from pathlib import Path
from collections import Counter, defaultdict
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer, util
from llama_cpp import Llama, LlamaGrammar

# Model: Mistral-Nemo-12B (Q5_K_M GGUF)
MODELS_DIR = Path('../models')
MODEL_REGISTRY = {
    'mistral-nemo-12b':{'file': 'Mistral-Nemo-Instruct-2407-Q5_K_M.gguf',
                        'repo': 'bartowski/Mistral-Nemo-Instruct-2407-GGUF','fmt': 'mistral'},
}
ACTIVE_MODEL = 'mistral-nemo-12b'

# Ablation switch: True = rule engine on, False = rule engine off.
USE_RULE_ENGINE = False

_cfg = MODEL_REGISTRY[ACTIVE_MODEL]
MODEL_PATH  = str(MODELS_DIR / _cfg['file'])
MODEL_FMT   = _cfg['fmt']
RULE_TAG    = 'rules_on' if USE_RULE_ENGINE else 'rules_off'
RESULTS_DIR = Path(f'../results/{ACTIVE_MODEL}/{RULE_TAG}')
print(f'Active model: {ACTIVE_MODEL}  ->  {MODEL_PATH}')
print(f'Rule engine:  {"ON" if USE_RULE_ENGINE else "OFF (ablation)"}')
print(f'Results dir:  {RESULTS_DIR}')
ATTCK_DIR   = Path('../data/attck')
CHROMA_DIR  = Path('../data/chroma')
RANDOM_SEED = 42

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)
```
**What it does:**  
- Imports all necessary libraries (pandas, networkx, chromadb, sentence‑transformers, llama‑cpp).  
- Defines the model to use (Mistral‑Nemo 12B GGUF) and its path.  
- Toggles the rule engine on/off via `USE_RULE_ENGINE`. This is the **ablation** switch.  
- Creates directories for results and ChromaDB persistence.  
**Why:** This is the central configuration cell – change `USE_RULE_ENGINE` to run the experiment with or without the rule‑based logic.  
**How:** `MODEL_REGISTRY` stores model info; `RESULTS_DIR` uses the toggle to separate output folders, so you can compare both runs.  
**Fact:** “Ablation” means removing a component to see its effect – here we turn off the rule engine to measure its contribution.

---

## Cell 3: Listing CIC‑IDS‑2017 CSV Files
```python
data_path = '../data/cicids'
csv_files = [f for f in os.listdir(data_path) if f.endswith('.csv')]
# drop Monday (benign-only) and Wednesday (DoS-only) for balance
csv_files_filtered = [f for f in csv_files if 'Monday' not in f and 'Wednesday' not in f]
for f in csv_files_filtered:
    print(f)
```
**What it does:** Lists all CSV files in the data folder and filters out Monday (only benign traffic) and Wednesday (only DoS attacks) to create a more balanced dataset.  
**Why:** The original CIC‑IDS‑2017 has seven days; Monday has only normal traffic, Wednesday is heavy on DoS. Keeping them would skew the training/evaluation.  
**How:** Simple string matching on filenames.

---

## Cell 4: Load and Combine CSV Files
```python
dfs = []
for f in csv_files_filtered:
    df_temp = pd.read_csv(os.path.join(data_path, f))
    df_temp['Source_File'] = f
    dfs.append(df_temp)
df_combined = pd.concat(dfs, ignore_index=True)
print(len(df_combined), 'rows')
```
**What it does:** Reads each filtered CSV, adds a column indicating the source file, and concatenates all into one DataFrame.  
**Why:** We need a unified dataset for processing.  
**How:** Pandas `read_csv` and `concat`.

---

## Cell 5: Clean and Inspect Labels
```python
df_combined[' Label'] = df_combined[' Label'].str.replace('�', '-', regex=False)
df_combined[' Label'] = df_combined[' Label'].str.replace(r'\s*-\s*', ' - ', regex=True).str.strip()
print(df_combined[' Label'].value_counts())
```
**What it does:** Cleans the label column (fixes encoding issues) and prints the count of each attack type.  
**Why:** Labels are the ground truth; we need to understand the class distribution.  
**Output:** Shows many BENIGN flows, then PortScan, DDoS, etc. This informs later sampling to avoid class imbalance.

---

## Cell 6: Downsample to at Most 2000 per Label
```python
sampled_dfs = []
for label in df_combined[' Label'].unique():
    label_df = df_combined[df_combined[' Label'] == label]
    sampled_dfs.append(label_df.sample(n=min(2000, len(label_df)), random_state=42))
df_sampled = pd.concat(sampled_dfs, ignore_index=True)
print(len(df_sampled), 'sampled')
```
**What it does:** For each label, take up to 2000 random samples (or all if fewer). This creates a manageable, balanced dataset.  
**Why:** To avoid bias toward majority classes and keep the notebook fast.  
**How:** Uses `sample` with fixed random state for reproducibility.

---

## Cell 7: Select Relevant Features
```python
columns_to_keep = [
    ' Label', ' Destination Port', ' Flow Duration', ' Total Fwd Packets',
    ' Total Backward Packets', ' SYN Flag Count', ' RST Flag Count', 'FIN Flag Count',
    'Flow Bytes/s', ' Flow Packets/s', ' Flow IAT Mean', ' Down/Up Ratio',
    ' Average Packet Size', ' Packet Length Std', 'Active Mean', 'Idle Mean']
df_filtered = df_sampled[columns_to_keep]
print(df_filtered.shape)
```
**What it does:** Keeps only 16 flow features that are commonly used for intrusion detection.  
**Why:** Many features are redundant or not useful; selecting a core set reduces noise and speeds processing.  
**How:** Simple column selection.

---

## Cell 8: Load MITRE ATT&CK Techniques
```python
with open('../data/attck/enterprise-attack.json', 'r', encoding='utf-8') as f:
    bundle = json.load(f)

attck_techniques = {}
for obj in bundle.get('objects', []):
    if obj.get('type') != 'attack-pattern' or obj.get('revoked') or obj.get('x_mitre_deprecated'):
        continue
    tid = next((r.get('external_id') for r in obj.get('external_references', [])
                if r.get('source_name') == 'mitre-attack'), None)
    if not tid:
        continue
    tactics = [p.get('phase_name','').capitalize() for p in obj.get('kill_chain_phases', []) if p.get('phase_name')]
    attck_techniques[tid] = {'name': obj.get('name','Unknown'), 'tactics': tactics,
                             'description': obj.get('description','')}
print(len(attck_techniques), 'techniques loaded')
```
**What it does:** Parses the official MITRE ATT&CK STIX JSON file, extracts only non‑deprecated attack patterns, and stores them in a dictionary keyed by technique ID (e.g., T1046).  
**Why:** We need a reference of all techniques and their descriptions for mapping and retrieval.  
**How:** Reads JSON, iterates over objects, filters by type and status, extracts external ID and kill‑chain phases.

---

## Cells 9–11: Map CIC Labels to ATT&CK Techniques
**Cell 9:**
```python
label_to_technique = {
    'BENIGN': None,
    'FTP - Patator': 'T1110.001',
    'SSH - Patator': 'T1110.001',
    'DDoS': 'T1498.001',
    'PortScan': 'T1046',
    'Bot': 'T1071.001',
    'Web Attack - Brute Force': 'T1110.001',
    'Web Attack - XSS': 'T1059.007',
    'Infiltration': 'T1203',
    'Web Attack - Sql Injection': 'T1190'}
```
**Cell 10:**
```python
df_sampled['Technique'] = df_sampled[' Label'].map(label_to_technique)
```
**Cell 11:**
```python
def get_tactics(tech_id):
    if pd.isna(tech_id):
        return None
    return attck_techniques.get(tech_id, {}).get('tactics', None)

df_sampled['Tactics'] = df_sampled['Technique'].apply(get_tactics)
print('unmapped:', df_sampled['Technique'].isna().sum())
```
**What they do:**  
- Cell 9 defines a manual mapping from CIC‑IDS labels to MITRE technique IDs (based on known equivalence).  
- Cell 10 creates a new column 'Technique' with the technique ID.  
- Cell 11 looks up the tactics (e.g., Discovery, Credential Access) from the ATT&CK data and adds a 'Tactics' column. BENIGN rows get None.  
**Why:** This provides the ground truth for evaluation later.  
**How:** Simple dictionary mapping and apply.

---

## Cell 12: Helper Functions for Semantic Descriptors
```python
def get_port_service(port: int) -> str: ...
def describe_duration(dur: float) -> str: ...
def describe_volume(fwd: int, bwd: int) -> str: ...
# ... many more functions
```
**What it does:** Defines a set of functions that translate numeric flow features into human‑readable, neutral descriptions. For example, `describe_duration` converts microseconds to “sub‑second connection” or “long‑duration connection”.  
**Why:** We will build a natural‑language “alert” that describes the flow without revealing the true attack label. The LLM later uses this description to infer the attack type.  
**How:** Each function uses if‑else logic to bucket values into descriptive phrases.

---

## Cell 13: Build Semantic Alert Text
```python
def build_semantic_alert(row: pd.Series) -> str:
    # ... extracts features, calls descriptor functions, and returns a single paragraph
```
**What it does:** For each row, it composes a text like:  
> “Network flow targeting HTTPS on port 443. Connection profile: sub‑second connection. Traffic exchange: low packet count, with 10 outbound and 5 inbound packets. TCP behavior: connections closed with FIN. Timing pattern: sub‑10ms inter‑arrival timing. ...”

**Why:** This alert is a neutral description of the flow’s statistics. It contains **no** attack label – all labels are hidden. This prevents the LLM from cheating and forces it to reason from patterns.  
**How:** Calls all descriptor functions and concatenates.

---

## Cell 14: Generate Alert Texts for All Rows
```python
df_filtered['alert_text'] = df_filtered.apply(build_semantic_alert, axis=1)
alert_texts = df_filtered['alert_text'].tolist()
print(len(alert_texts), 'alerts')
```
**What it does:** Applies the `build_semantic_alert` function to every row, creating a new column `alert_text`, and stores the list of all alerts.  
**Why:** We now have a corpus of ~14k neutral descriptions ready for embedding.

---

## Cell 15: Community Context and Rule Engine Functions
```python
def build_community_context(cid: int) -> str: ...
def community_flow_stats(cid: int) -> dict: ...
def infer_relation_from_context(cid: int, force: bool = False) -> str | None: ...
def reconcile_community_triples(triples: list, cid: int) -> list: ...
```
**What it does:** Defines functions that operate at the community (cluster) level:  
- `build_community_context` summarises port diversity and concentration across all flows in that community.  
- `community_flow_stats` computes aggregate statistics (e.g., average packet rate).  
- `infer_relation_from_context` uses these stats to infer a high‑level relation (e.g., `PERFORMS_PORT_SCAN`, `CAUSES_DENIAL_OF_SERVICE`) based on heuristic rules.  
- `reconcile_community_triples` optionally overrides LLM‑extracted triples with the rule‑engine inference.  
**Why:** The rule engine provides a purely statistical baseline. When `USE_RULE_ENGINE` is False, these functions are still defined but their output is ignored, allowing a clean ablation.  
**How:** The logic is based on thresholds (e.g., number of unique ports, SYN counts, packet rates). They are a form of simple signature‑based detection.

---

## Cell 16: Embed Alerts with Sentence‑BERT
```python
embedder = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = embedder.encode(alert_texts, convert_to_tensor=True)
print('encoded', embeddings.shape)
```
**What it does:** Loads a lightweight sentence‑transformer model (`all‑MiniLM‑L6‑v2`) and encodes all alert texts into 384‑dimensional vectors.  
**Why:** These dense embeddings capture semantic similarity between alerts. Similar flow patterns (e.g., port scans) will have similar vectors.  
**How:** The model is pre‑trained on a large corpus to produce meaningful sentence representations.

---

## Cell 17: Threshold Sweep for Community Detection
```python
# defines functions for purity and intra‑cluster similarity
# loops over thresholds [0.50, 0.55, ..., 0.95]
# uses sentence_transformers.util.community_detection
```
**What it does:** For each similarity threshold, it runs `community_detection` on the embeddings to find groups of highly similar alerts. It then calculates:  
- **Label purity:** % of majority label in each community (averaged).  
- **Intra‑cluster similarity:** average cosine similarity within each community.  
- **Combined score** = purity × similarity (only if at least 5 communities).  
The results are printed and saved.  
**Why:** We need to choose a threshold that yields clean, coherent communities. A high threshold gives purer but fewer communities; a low threshold mixes different attack types.  
**How:** `community_detection` is a greedy algorithm that merges nodes with similarity > threshold. The sweep helps us find a sweet spot.

---

## Cell 18: Best Threshold
```python
BEST_THRESHOLD=0.80
```
**What it does:** Picks 0.80 as the optimal threshold (based on the sweep results).  
**Why:** In the output, 0.80 had high purity (0.837) and high intra‑sim (0.9416) with a decent number of communities.  
**How:** Manual selection (you could automate it, but here it’s hard‑coded).

---

## Cell 19: Detect Communities with Best Threshold
```python
communities = util.community_detection(embeddings, min_community_size=2, threshold=BEST_THRESHOLD)
print(len(communities), 'communities at threshold', BEST_THRESHOLD)
```
**What it does:** Runs the community detection once with threshold 0.80.  
**Why:** We now have a list of community indices – each community is a list of alert indices that belong together.

---

## Cells 20–21: Assign Community IDs and Compute Metrics
**Cell 20:**
```python
comm_ids = np.full(len(df_filtered), -1, dtype=int)
for cid, members in enumerate(communities):
    comm_ids[np.asarray(members, dtype=int)] = cid
df_filtered['community_id'] = comm_ids
```
**Cell 21:**
```python
# Compute label purity and intra‑cluster similarity for the chosen communities
# Store metrics in a JSON file
```
**What they do:**  
- Cell 20 assigns a community ID to each row (‑1 for unclustered).  
- Cell 21 recalculates purity and similarity specifically for the 0.80 threshold, saves the metrics.  
**Why:** We need to know which flows belong to which cluster for later processing.

---

## Cell 22: Save Processed Data
```python
df_filtered['Technique'] = df_sampled.loc[df_filtered.index, 'Technique'].values
df_filtered['Tactics']   = df_sampled.loc[df_filtered.index, 'Tactics'].apply(str).values
PROCESSED_DATA_DIR = Path('../data/results')
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
df_filtered.to_csv(PROCESSED_DATA_DIR / 'cicids_processed.csv', index=False)
print('saved', len(df_filtered), 'rows ->', PROCESSED_DATA_DIR / 'cicids_processed.csv')
```
**What it does:** Adds the technique and tactics columns back (they were dropped earlier) and saves the final DataFrame to CSV for later use.  
**Why:** Persistent storage of the processed dataset.

---

## Cell 23: Load the Large Language Model (LLM)
```python
llm = Llama(model_path=MODEL_PATH, n_ctx=4096, n_gpu_layers=-1, n_threads=8,
            n_batch=256, verbose=False, seed=RANDOM_SEED)
print('LLM loaded')

def chat(system, user, max_tokens=512, temperature=0.0, grammar=None, repeat_penalty=1.1):
    msgs = []
    if system:
        msgs.append({'role': 'system', 'content': system})
    msgs.append({'role': 'user', 'content': user})
    kw = dict(messages=msgs, max_tokens=max_tokens, temperature=temperature,
              seed=RANDOM_SEED, repeat_penalty=repeat_penalty)
    if grammar is not None:
        kw['grammar'] = grammar
    out = llm.create_chat_completion(**kw)
    return out['choices'][0]['message']['content'].strip()
```
**What it does:** Loads the Mistral‑Nemo model using `llama‑cpp` (a lightweight C++ inference library). The `chat` function sends a system and user prompt to the model and returns the generated text.  
**Why:** We will use the LLM to extract semantic triples from the alert clusters.  
**How:** `n_gpu_layers=-1` offloads all layers to GPU (if available). `temperature=0` makes output deterministic.

---

## Cell 24: Define JSON Schema and Grammar for Triple Extraction
```python
SECURITY_RELATIONS = [
    'PERFORMS_RECONNAISSANCE', 'PERFORMS_PORT_SCAN', 'BRUTE_FORCES_CREDENTIAL',
    'EXPLOITS_VULNERABILITY', 'ESTABLISHES_C2', 'PERFORMS_BEACONING',
    'CAUSES_DENIAL_OF_SERVICE']

TRIPLE_SCHEMA = { ... }
grammar = LlamaGrammar.from_json_schema(json.dumps(TRIPLE_SCHEMA))
```
**What it does:** Defines a JSON schema for the LLM to output a list of triples (subject‑relation‑object). The relations are limited to the `SECURITY_RELATIONS` list. `grammar` enforces that the LLM output is valid JSON conforming to the schema.  
**Why:** We want structured output from the LLM, not free text, so we can parse it reliably.  
**How:** `llama‑cpp` supports GBNF grammars derived from JSON schema.

---

## Cell 25: Relation Guide and Entity Normalisation
```python
RELATION_GUIDE = """ ... """  # long string with evidence cues for each relation
def normalise_entity(text: str) -> str:
    # converts to lowercase, replaces non‑alnum with underscores
```
**What it does:** Provides detailed instructions to the LLM on how to choose a relation based on flow evidence. Also defines a function to normalise entity names (e.g., “SSH port 22” → “ssh_port_22”).  
**Why:** The LLM needs clear guidelines to produce consistent and meaningful triples.

---

## Cell 26: Function to Extract Triples from a Community
```python
def extract_triples(alert_texts: list, community_id: int, community_context: str = '') -> list:
    # Builds a prompt with RELATION_GUIDE, up to 6 alert samples, and community context.
    # Calls chat() with the grammar, parses JSON, validates triples.
```
**What it does:** For a given community, it picks a few alert texts, adds the community‑level summary, and asks the LLM to output between 1‑4 triples describing the attack behaviour.  
**Why:** Instead of processing each alert individually (expensive), we summarise the whole cluster and let the LLM generalise.  
**How:** The prompt includes examples and a mandatory block if the rule engine inferred a relation (when `USE_RULE_ENGINE` is True). This enforces consistency with the rule engine.

---

## Cell 27: Extract Triples for All Communities
```python
community_triples = {}
for cid, group in community_df.groupby('community_id'):
    if len(group) < MIN_COMMUNITY_SIZE:
        continue
    texts = group['alert_text'].dropna().tolist()
    ctx = build_community_context(int(cid))
    triples = extract_triples(texts, int(cid), community_context=ctx)
    triples = reconcile_community_triples(triples, int(cid))
    community_triples[str(int(cid))] = triples
```
**What it does:** Iterates over each community, extracts triples using the LLM, and optionally reconciles with the rule‑engine inference. It prints the dominant label and triples for visual inspection.  
**Why:** This is the core step – translating raw clusters into high‑level threat intelligence.  
**How:** The `reconcile_community_triples` function overrides the LLM output with the rule‑engine relation if the rule engine is on.

---

## Cells 28–29: Baseline Generation and Triple Metrics
**Cell 28:**
```python
def generate_baseline_report(raw_triples: str, alert_context: str=None, cid: int=None) -> dict:
    # Uses LLM without retrieval to predict a technique ID from the triples alone.
```
**Cell 29:**
```python
# Compute statistics: total triples, valid triples, relation counts, etc.
```
**What they do:**  
- Cell 28 defines a function that takes the raw triples and asks the LLM to directly map them to a technique ID (no RAG). This serves as a **baseline** to compare against the full RAG pipeline.  
- Cell 29 computes metrics about the extracted triples (e.g., how many unique subjects, relation distribution).  
**Why:** We need to know the quality of the triple extraction itself.

---

## Cell 30: Build the Knowledge Graph
```python
G = nx.DiGraph()
# Add behavioural nodes and edges from triples (with weights).
# Add ATT&CK technique nodes.
# Add bridge edges from each relation to a set of candidate technique IDs.
```
**What it does:** Constructs a directed graph with two layers:  
- **Behavioural layer:** nodes are entities (subjects/targets) and edges are triples (with relation labels).  
- **ATT&CK layer:** nodes are techniques.  
- **Bridge edges:** connect behavioural nodes to technique nodes based on a mapping from relations to possible technique IDs (e.g., `PERFORMS_PORT_SCAN` → T1046).  
**Why:** The graph integrates extracted knowledge with external threat intelligence, enabling reasoning and retrieval.  
**How:** Uses `networkx`. The bridge edges are added with a fixed mapping (hard‑coded in `RELATION_TO_TECHNIQUES`).

---

## Cell 31: Save Graph and Metrics
```python
nx.write_graphml(G, RESULTS_DIR / 'knowledge_graph.graphml')
# Save node and edge CSVs, compute metrics (reachable ATT&CK nodes, etc.)
```
**What it does:** Writes the graph to a file and saves summary statistics.  
**Why:** Graph can be visualised in tools like Gephi. Metrics help assess the connectivity and coverage.

---

## Cell 32: Set Up ChromaDB with ATT&CK Techniques
```python
EMBED_MODEL = 'all-MiniLM-L6-v2'
TOP_K = 10
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)
client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = client.get_or_create_collection(name='attack_techniques', embedding_function=ef)
# Add all ATT&CK techniques to the collection (documents = technique description + name + ID)
```
**What it does:** Creates a vector database (ChromaDB) containing all ATT&CK techniques, each stored with its name, description, tactic, and an embedding.  
**Why:** We will perform retrieval (RAG) – given a query, we find the most similar techniques.  
**How:** `sentence‑transformers` are used to embed technique descriptions.

---

## Cell 33: Report Grammar
```python
REPORT_SCHEMA = { ... }  # defines fields: technique_id, tactic, summary, evidence, next_step
report_grammar = LlamaGrammar.from_json_schema(json.dumps(REPORT_SCHEMA))
```
**What it does:** Creates a JSON schema for the final incident report that the LLM must generate.  
**Why:** The final output must be structured (technique ID, tactic, summary, evidence, next step) for easy parsing.

---

## Cell 34: Build HyDE Query and Tactic Scope
```python
def build_hyde_query(cid: int):
    # Uses LLM to generate a hypothetical document (HyDE) describing the attack based on triples and graph context.
    # Also determines tactic scope (e.g., 'discovery') from the relation(s).
```
**What it does:** For each community, it constructs a **HyDE** (Hypothetical Document Embeddings) query – a synthetic description of the attack technique, written by the LLM. This description is later used for retrieval. It also determines a tactic scope (e.g., “discovery” or “credential‑access”) to filter retrieval results.  
**Why:** HyDE often improves retrieval performance by creating a more complete query. The tactic scope narrows the search to relevant techniques.  
**How:** The LLM is prompted to write a technical description mimicking MITRE style.

---

## Cell 35: Generate RAG Report
```python
def generate_rag_report(hyde_query, raw_triples, alert_context, docs, metas, candidate_id=None, kg_candidate_ids=None):
    # Builds a prompt that includes retrieved ATT&CK docs, HyDE query, and triples.
    # Forces the LLM to output a JSON report with technique_id, etc.
```
**What it does:** Takes the HyDE query, the raw triples, the retrieved technique documents, and a list of candidate IDs (from the knowledge graph). It asks the LLM to write a structured incident report, selecting one technique from the allowed set.  
**Why:** This is the final step of the RAG pipeline – it combines retrieved knowledge with extracted evidence to produce a reasoned mapping.  
**How:** The prompt constrains the LLM to pick from the candidate list, preventing hallucination.

---

## Cell 36: Filter Evaluable Communities
```python
PURITY_MIN = 0.70
# For each community, compute the majority label and its share.
# Keep only those with >70% purity and not BENIGN.
```
**What it does:** Among all communities, it selects those that are “clean” – majority attack label with at least 70% purity – and discards noisy or benign‑dominated communities.  
**Why:** We want to evaluate technique mapping on reliable clusters; mixing multiple attack types would make evaluation unfair.  
**How:** Simple statistics.

---

## Cell 37: Evaluate RAG vs Baselines
```python
for cid in eval_cids:
    # Build HyDE, retrieve techniques, run RAG, run baseline (no retrieval), run rules‑only baseline.
    # Compute exact match, parent match, faithfulness, etc.
```
**What it does:** For each clean community, it runs three systems:  
1. **Full RAG** (HyDE + retrieval + LLM report)  
2. **Baseline** (LLM directly from triples, no retrieval)  
3. **Rules‑only** (the rule engine’s inferred relation mapped to a technique)  
It records whether the predicted technique exactly matches the ground truth, or if it’s a parent (e.g., T1110 vs T1110.001). It also computes faithfulness (similarity between generated summary and retrieved context).  
**Why:** To compare the benefit of retrieval and rule engine.

---

## Cell 38: Error Attribution
```python
# Determine if the ground truth technique is reachable from the extracted relations.
# If yes, the error is due to retrieval; if not, due to extraction failure.
```
**What it does:** Analyses why a community was misclassified. If the correct technique was not even in the candidate list from the KG, then the triple extraction failed. If it was in the list but retrieval picked something else, then retrieval is at fault.  
**Why:** Helps pinpoint the bottleneck.

---

## Cell 39: Generate Metrics
```python
# Compute micro, macro accuracy, bootstrap confidence intervals, macro F1, confusion matrix.
```
**What it does:** Computes overall performance metrics:  
- **Micro accuracy:** raw percentage of correct predictions.  
- **Macro accuracy:** average accuracy per technique (equal weight, removes majority bias).  
- **Macro F1:** harmonic mean of precision/recall per class.  
- **Confidence intervals** via bootstrap.  
- **Confusion matrix** for RAG.  
**Why:** Gives a comprehensive view of performance, especially important because classes are imbalanced.

---

## Cell 40: Report Quality
```python
# Assesses completeness, grounding (cosine similarity between generated summary/evidence and triples), faithfulness, name consistency.
```
**What it does:** Evaluates the quality of the generated reports independently of technique‑ID correctness.  
**Why:** A report could have the right ID but poor explanation, or vice versa.

---

## Cell 41: Ablation Comparison
```python
# Loads the rag_metrics.json from both rules_on and rules_off runs and compares them.
```
**What it does:** If you have run the notebook twice (once with `USE_RULE_ENGINE=True` and once with `False`), this cell loads both results and prints a comparison table.  
**Why:** The final step of the ablation study to see the impact of the rule engine on performance.

---

## Summary
This notebook demonstrates a full pipeline from raw network flows to threat technique mapping using a combination of semantic clustering, rule‑based heuristics, LLM extraction, knowledge graphs, and RAG. The ablation study shows whether the rule engine adds value. For a beginner, the key takeaway is how different components (feature engineering, clustering, LLM prompting, retrieval) can be assembled into a coherent system, and how each part is evaluated.

---

**Note:** This document is intended for educational purposes. To reproduce the results, you need the CIC‑IDS‑2017 dataset, the MITRE ATT&CK JSON file, and the Mistral‑Nemo GGUF model.

