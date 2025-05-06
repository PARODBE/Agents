import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import random

# ----------------------------
# CONFIGURACIÓN STREAMLIT
# ----------------------------
st.set_page_config(page_title="Rosetta Agent System", layout="wide")

# Redirección controlada desde otro punto
if "navigation_target" in st.session_state:
    page = st.session_state["navigation_target"]
    del st.session_state["navigation_target"]
else:
    page = st.sidebar.radio("📂 Navigation", ["🧠 Agent Graph", "✅ Validation Summary", "🧪 Committee Review"])

# ----------------------------
# PÁGINA 1: GRAFO DE AGENTES
# ----------------------------
if page == "🧠 Agent Graph":

    st.title("Rosetta Agent System")

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
            "Discover novel imaging-genomic signatures predicting resistance to immunotherapy"
        ]
    )

    st.session_state["selected_question"] = question
    active_nodes = get_active_nodes(question)
    fig = draw_graph(active_nodes)
    st.pyplot(fig)

# ----------------------------
# PÁGINA 2: VALIDACIÓN
# ----------------------------
elif page == "✅ Validation Summary":

    st.title("🔍 Researcher Agent Validation")

    question = st.session_state.get("selected_question", "")
    st.markdown(f"### 📌 Question: *{question}*")

    agent_outputs = {
        "Treatment agent": "Adding pertuzumab improves pathological complete response in HER2+ breast cancer.",
        "Prognostic agent": "Patients with HER2+ tumors show improved survival when treated early.",
        "Diagnosis agent": "HER2+ subtype is confirmed by overexpression of HER2 protein in immunohistochemistry.",
        "Guidelines agent": "NCCN recommends trastuzumab and pertuzumab for HER2+ breast cancer treatment.",
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
        active_agents = ["Treatment agent", "Prognostic agent"]

    results = {}
    is_discovery_question = "discover novel imaging-genomic signatures" in question.lower()

    for agent in active_agents:
        if is_discovery_question:
            scores = {
                "Performance": round(random.uniform(0.75, 0.85), 2),
                "Source Match": 0.0,
                "Scientific Support": 0.0,
                "Plausibility": round(random.uniform(0.7, 0.85), 2),
                "Contradiction Risk": round(random.uniform(0.0, 0.2), 2)
            }
        else:
            scores = {
                "Performance": round(random.uniform(0.75, 0.95), 2),
                "Source Match": round(random.uniform(0.3, 0.95), 2),
                "Scientific Support": round(random.uniform(0.3, 0.9), 2),
                "Plausibility": round(random.uniform(0.5, 1.0), 2),
                "Contradiction Risk": round(random.uniform(0.0, 0.4), 2)
            }
        results[agent] = scores

    global_score = {
        key: round(sum(agent_scores[key] for agent_scores in results.values()) / len(results), 2)
        for key in ["Performance", "Source Match", "Scientific Support", "Plausibility", "Contradiction Risk"]
    }

    final_score = round(
        0.4 * global_score["Performance"] +
        0.2 * global_score["Source Match"] +
        0.15 * global_score["Scientific Support"] +
        0.15 * global_score["Plausibility"] +
        0.1 * (1 - global_score["Contradiction Risk"]),
        2
    )

    for agent in active_agents:
        st.markdown(f"#### 🤖 {agent}")
        st.markdown(f"**Output:** *{agent_outputs.get(agent, 'No output available.')}*")
        st.write(results[agent])

    st.markdown("---")
    st.subheader("📊 Aggregated Validation")

    if global_score["Source Match"] == 0 and global_score["Scientific Support"] == 0:
        st.warning("⚠️ No supporting scientific literature was found for any agent.")
        st.info("This may indicate a novel hypothesis. Recommend expert committee review.")
        if st.button("🔎 Evaluate as Scientific Committee"):
            st.session_state["hypothesis_under_review"] = question
            st.session_state["navigation_target"] = "🧪 Committee Review"
            st.rerun()
    else:
        st.write(global_score)
        st.success(f"🧠 Final Certainty Score: **{final_score * 100:.1f}%**")
        st.progress(final_score)

# ----------------------------
# PÁGINA 3: COMITÉ CIENTÍFICO
# ----------------------------
elif page == "🧪 Committee Review":

    st.title("🧪 Scientific Committee Review")

    hypothesis = st.session_state.get("hypothesis_under_review", "No hypothesis submitted.")
    st.markdown("### 🧬 Candidate Hypothesis for Evaluation:")
    st.info(f"**{hypothesis}**")

    st.markdown("---")
    st.subheader("🧭 Committee Evaluation Criteria")

    plausible = st.checkbox("✅ Biologically plausible")
    internally_coherent = st.checkbox("✅ Internally consistent across data modalities")
    testable = st.checkbox("✅ Feasible to validate experimentally")
    original = st.checkbox("✅ Clearly novel compared to existing literature")

    total_score = sum([plausible, internally_coherent, testable, original])
    score_percent = int((total_score / 4) * 100)

    st.markdown(f"### 🔢 Committee Review Score: **{score_percent}%**")

    if score_percent >= 75:
        st.success("✅ Approved for inclusion in the Research Ideas Pool.")
        if st.button("📦 Add to Research Idea Pool"):
            st.session_state.setdefault("research_ideas", []).append(hypothesis)
            st.success("✅ Hypothesis added to pool.")
    else:
        st.warning("🕵️ More review or evidence needed before approval.")

    st.markdown("---")
    st.subheader("📦 Validated Research Ideas Pool")

    ideas = st.session_state.get("research_ideas", [])
    if ideas:
        for idea in ideas:
            st.markdown(f"🧠 **{idea}**")
    else:
        st.info("No research ideas approved yet.")
