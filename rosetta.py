import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.image as mpimg
import networkx as nx
import os

# --- SETUP DEL GRAFO ---

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

# --- POSICIONES EN CAPAS ---

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

# --- ICONOS ---
icon_paths = {
    "Diagnosis agent": "xray.png",
    "Treatment agent": "treatment.png",
    "Prognostic agent": "survival.png",
    "Guidelines agent": "guidelines.png",
    "Protocol agent": "protocol.png",
    "Graph-researcher agent": "graph.png"
}

# --- FUNCIONES ---

def draw_graph(active_nodes=None):
    fig, ax = plt.subplots(figsize=(15, 12))
    ax.set_title("Rosetta Agent System (Layered Layout with Icons)", fontsize=16)

    for node in G.nodes():
        x, y = pos[node]
        width = 2.2
        height = 0.9
        color = "lightgreen" if active_nodes and node in active_nodes else "lightblue"
        rect = mpatches.FancyBboxPatch((x - width/2, y - height/2), width, height,
                                       boxstyle="round,pad=0.05", ec="black", fc=color)
        ax.add_patch(rect)
        ax.text(x, y + 0.3, node, ha='center', va='center', fontsize=8)

        if node in icon_paths and os.path.exists(icon_paths[node]):
            img = mpimg.imread(icon_paths[node])
            ax.imshow(img, extent=(x - 0.3, x + 0.3, y - 0.3, y + 0.3), zorder=10)

    for u, v in G.edges():
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        ax.annotate("",
                    xy=(x2, y2), xycoords='data',
                    xytext=(x1, y1), textcoords='data',
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

# --- INTERFAZ STREAMLIT ---

st.title("Rosetta Agent System")
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