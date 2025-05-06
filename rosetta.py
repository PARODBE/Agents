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

    functional_agents = ["Diagnosis agent", "Treatment agent", "Prognostic agent", "Guidelines agent"]
    researcher_agents = [f"{a.split()[0]} Researcher agent" for a in functional_agents]

    for agent, researcher in zip(functional_agents, researcher_agents):
        G.add_node(agent, layer=2)
        G.add_node(researcher, layer=3)
        G.add_edge("Question-classifier agent", agent)
        G.add_edge(agent, researcher)

    G.add_node("Multi-researcher agent", layer=4)
    for researcher in researcher_agents:
        G.add_edge(researcher, "Multi-researcher agent")

    G.add_node("Protocol agent", layer=5)
    G.add_node("Graph-researcher agent", layer=5)
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

    example_output = "Predicted survival improvement in HER2+ breast cancer when adding pertuzumab."
    st.markdown(f"### 💬 Agent's Output:\n> *{example_output}*")

    st.markdown("---")
    st.subheader("🧪 Validation Scores (simulated)")

    # Simulated scores
    performance_score = round(random.uniform(0.7, 0.95), 2)
    source_match = round(random.uniform(0.6, 0.95), 2)
    scientific_support = round(random.uniform(0.5, 0.9), 2)
    plausibility = round(random.uniform(0.6, 0.95), 2)
    contradiction_risk = round(random.uniform(0.0, 0.4), 2)

    final_score = round(
        0.4 * performance_score +
        0.2 * source_match +
        0.15 * scientific_support +
        0.15 * plausibility +
        0.1 * (1 - contradiction_risk),
        2
    )

    # Show table
    st.write({
        "Performance Score": performance_score,
        "Source Match Score": source_match,
        "Scientific Support Score": scientific_support,
        "Plausibility Score": plausibility,
        "Contradiction Risk Score": contradiction_risk,
        "➡️ Final Certainty Score": final_score
    })

    with st.expander("ℹ️ Explanation of Scores"):
        st.markdown("""
- **🔹 Source Match Score**  
  *Does the literature say something similar?*  
  ➤ Based on semantic similarity between agent output and abstracts.

- **🔹 Scientific Support Score**  
  *Are sources high-quality?*  
  ➤ Weighted by source type (e.g., RCT > review > preprint).

- **🔹 Plausibility Score**  
  *Does the claim make biomedical sense?*  
  ➤ Evaluated by a scientific LLM.

- **🔹 Contradiction Risk Score**  
  *Is there scientific evidence against this?*  
  ➤ Checked via semantic contradiction in retrieved papers.

- **🟢 Performance Score**  
  *How well did the model do on known validation data (e.g., AUC)?*
        """)

    st.progress(final_score)
    st.success(f"🧠 Final Certainty Score: **{final_score * 100:.1f}%**")
