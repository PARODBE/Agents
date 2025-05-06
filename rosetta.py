import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import random

# ----------------------------
# CONFIGURACIÓN STREAMLIT
# ----------------------------
st.set_page_config(page_title="Rosetta Agent System", layout="wide")
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["🧠 Agent Graph", "✅ Validation Summary"])

# ----------------------------
# PÁGINA 1: GRAFO DE AGENTES
# ----------------------------
if page == "🧠 Agent Graph":

    st.title("Rosetta Agent System")

    # --- GRAFO SETUP ---
    G = nx.DiGraph()
    G.add_node("Rosetta Agent", layer=0)
    G.add_node("Question-classifier agent", layer=1)
    G.add_edge("Rosetta Agent", "Question-classifier agent")

    functional_agents = ["Diagnosis agent", "Treatment agent", "Prognostic agent", "Guidelines agent", "Genomic agent"]
    researcher_agents = [f"{a.split()[0]} Researcher agent" for a in functional_agents]

    for agent, researcher in zip(functional_agents, researcher_agents):
        G.add_node(agent, layer=2)
        G.add_node(researcher, layer=3)
        G.add_edge("Question-classifier agent", agent)
        G.add_edge(agent, researcher)

    G.add_node("Multi-researcher agent", layer=5)
    for researcher in researcher_agents:
        G.add_edge(researcher, "Multi-researcher agent")

    G.add_node("Protocol agent", layer=5)
    G.add_node("Graph-researcher agent", layer=6)
    G.add_edge("Multi-researcher agent", "Protocol agent")
    G.add_edge("Multi-researcher agent", "Graph-researcher agent")

    # --- POSICIONES ---
    layer_positions = {
        0: ["Rosetta Agent"],
        1: ["Question-classifier agent"],
        2: functional_agents,
        3: researcher_agents,
        4: ["Multi-researcher agent"],
        5: ["Protocol agent", "Graph-researcher agent"]
    }

    pos = {}
    y_gap = -2.2
    x_gap = 3.5
    for layer, nodes in layer_positions.items():
        y = layer * y_gap
        n = len(nodes)
        for i, node in enumerate(nodes):
            x = (i - (n - 1) / 2) * x_gap
            pos[node] = (x, y)

    def draw_graph(active_nodes=None):
        fig, ax = plt.subplots(figsize=(15, 12))
        ax.set_title("Rosetta Agent System", fontsize=16)

        node_width = 2.2
        node_height = 0.9

        for node in G.nodes():
            x, y = pos[node]
            color = "lightgreen" if active_nodes and node in active_nodes else "lightblue"
            rect = mpatches.FancyBboxPatch((x - node_width / 2, y - node_height / 2), node_width, node_height,
                                           boxstyle="round,pad=0.05", ec="black", fc=color)
            ax.add_patch(rect)
            ax.text(x, y, node, ha='center', va='center', fontsize=8, wrap=True)

        for u, v in G.edges():
            x1, y1 = pos[u]
            x2, y2 = pos[v]
            start = (x1, y1 - node_height / 2)
            end = (x2, y2 + node_height / 2)
            ax.annotate("",
                        xy=end, xycoords='data',
                        xytext=start, textcoords='data',
                        arrowprops=dict(arrowstyle="->", lw=1.2))

        ax.set_xlim(-12, 12)
        ax.set_ylim(-14, 2)
        ax.axis('off')
        return fig

    def get_active_nodes(question):
        active = {"Rosetta Agent", "Question-classifier agent"}
        if "diagnosis" in question.lower():
            active.update(["Diagnosis agent", "Diagnosis Researcher agent"])
        if "treatment" in question.lower():
            active.update(["Treatment agent", "Treatment Researcher agent"])
        if "prognosis" in question.lower():
            active.update(["Prognostic agent", "Prognostic Researcher agent"])
        if "guideline" in question.lower():
            active.update(["Guidelines agent", "Guidelines Researcher agent"])
        if "genomic" in question.lower():
            active.update(["Genomic agent", "Genomic Researcher agent"])
        if "protocol" in question.lower():
            active.update(["Multi-researcher agent", "Protocol agent"])
        if "hypothesis" in question.lower() or "graph" in question.lower():
            active.update(["Multi-researcher agent", "Graph-researcher agent"])
        return active

    question = st.selectbox(
        "Select a question:",
        [
            "What is the best treatment for HER2+ breast cancer?",
            "What is the prognosis for stage III colon cancer?",
            "Is there a new hypothesis linking treatment and prognosis?",
            "Can you design a clinical protocol for triple-negative breast cancer?",
            "Show all agents"
        ]
    )

    active_nodes = get_active_nodes(question)
    fig = draw_graph(active_nodes)
    st.pyplot(fig)

# ----------------------------
# PÁGINA 2: VALIDACIÓN Y SCORES
# ----------------------------
elif page == "✅ Validation Summary":

    st.title("🔍 Researcher Agent Validation")

    # Define outputs by agent
    question = "What is the best treatment and long-term prognosis for HER2+ breast cancer?"
    st.markdown(f"### 📌 Question: *{question}*")

    agent_outputs = {
        "Treatment agent": "Adding pertuzumab improves pathological complete response in HER2+ breast cancer.",
        "Prognostic agent": "Patients with HER2+ tumors show improved survival when treated early.",
        "Diagnosis agent": "HER2+ subtype is confirmed by overexpression of HER2 protein in immunohistochemistry.",
        "Guidelines agent": "NCCN recommends trastuzumab and pertuzumab for HER2+ breast cancer treatment."
        "Genomic agent": "HER2+ breast cancer is characterized by ERBB2 gene amplification, leading to HER2 protein overexpression."
    }

    active_agents = []
    if "treatment" in question.lower():
        active_agents.append("Treatment agent")
    if "prognosis" in question.lower():
        active_agents.append("Prognostic agent")
    if "diagnosis" in question.lower():
        active_agents.append("Diagnosis agent")
    if "guideline" in question.lower():
        active_agents.append("Guidelines agent")
    if "genomic" in question.lower():
        active_agents.append("Genomic agent")
    if not active_agents:
        active_agents = ["Treatment agent", "Prognostic agent"]  # default

    # Simulate scores per agent
    results = {}
    for agent in active_agents:
        scores = {
            "Performance": round(random.uniform(0.75, 0.95), 2),
            "Source Match": round(random.uniform(0.0, 0.95), 2),
            "Scientific Support": round(random.uniform(0.0, 0.9), 2),
            "Plausibility": round(random.uniform(0.5, 1.0), 2),
            "Contradiction Risk": round(random.uniform(0.0, 0.4), 2)
        }
        results[agent] = scores

    # Aggregate global scores
    global_score = {
        key: round(sum(agent_scores[key] for agent_scores in results.values()) / len(results), 2)
        for key in ["Performance", "Source Match", "Scientific Support", "Plausibility", "Contradiction Risk"]
    }

    # Final certainty score
    final_score = round(
        0.4 * global_score["Performance"] +
        0.2 * global_score["Source Match"] +
        0.15 * global_score["Scientific Support"] +
        0.15 * global_score["Plausibility"] +
        0.1 * (1 - global_score["Contradiction Risk"]),
        2
    )

    # Show agent outputs and individual scores
    for agent in active_agents:
        st.markdown(f"#### 🤖 {agent}")
        st.markdown(f"**Output:** *{agent_outputs.get(agent, 'No output available.')}*")
        st.write(results[agent])

    st.markdown("---")
    st.subheader("📊 Aggregated Validation")

    if global_score["Source Match"] == 0 and global_score["Scientific Support"] == 0:
        st.warning("⚠️ No supporting scientific literature was found for any agent.")
        st.info("This may indicate a novel hypothesis. Recommend expert committee review.")
    else:
        st.write(global_score)
        st.success(f"🧠 Final Certainty Score: **{final_score * 100:.1f}%**")
        st.progress(final_score)

    with st.expander("ℹ️ How are the scores evaluated?"):
        st.markdown("""
### 🔹 Source Match Score  
**Does the literature say something similar?**  
- A RAG (Retrieval-Augmented Generation) system retrieves top-k relevant abstracts from biomedical databases like PubMed.  
- The agent's output is compared semantically to each abstract.  
- **Metric:** Cosine similarity of embeddings (e.g., BioSentVec, SciBERT, SBERT).  
- **Score:** Average similarity score over top-k documents, normalized to 0–1.

---

### 🔹 Scientific Support Score  
**Are the sources high quality and reliable?**  
- For each retrieved source, a biomedical LLM is prompted to assess:  
  • Study type (e.g., RCT, cohort, review)  
  • Journal quality and impact  
  • Sample size (parsed or inferred)  
  • Citation count (via Semantic Scholar API or CrossRef)  
  • Recency (based on publication year)  
- The LLM produces a support confidence score per abstract.  
- **Score:** Weighted average of evidence-level, impact, sample size, citation count, and recency.

---

### 🔹 Plausibility Score  
**Does the claim make biomedical sense?**  
- Evaluated using a domain-tuned LLM (e.g., BioMedLM, PubMedGPT).  
- Prompt example:  
  *"Is the following medical hypothesis plausible based on current knowledge? Rate from 0 (implausible) to 1 (very plausible): '{claim}'."*  
- **Score:** LLM confidence score directly (or derived from likelihood/logits).

---

### 🔹 Contradiction Risk Score  
**Is there evidence against the agent’s output?**  
- The same RAG-retrieved documents are passed to the LLM or a contradiction classifier.  
- Prompt example:  
  *"Does this abstract contradict the following statement? Answer: supports / contradicts / unrelated."*  
- **Score:** Probability of contradiction. Final score is `1 - contradiction_prob`.

---

### 🟢 Performance Score  
**How well did the model perform during development?**  
- Based on traditional validation data:
  - Classification → AUC, F1-score, Accuracy  
  - Regression → RMSE, MAE, R²  
- **Score:** Rescaled metric from 0–1 (e.g., AUC of 0.88 → score 0.88)
        """)
