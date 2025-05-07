import streamlit as st

# Mostrar tooltips con imágenes para cada Researcher Agent
st.markdown("### 🧬 Researcher Agent Insights (Hover to Preview)")

# Diccionario de imágenes para cada Researcher Agent
agent_images = {
    "Diagnosis Researcher agent": "https://your.image.url/diagnosis.png",
    "Treatment Researcher agent": "https://your.image.url/treatment.png",
    "Prognostic Researcher agent": "https://your.image.url/prognostic.png",
    "Guidelines Researcher agent": "https://your.image.url/guidelines.png",
    "Genomic Researcher agent": "https://raw.githubusercontent.com/PARODBE/Agents/main/validation.png"
}

# Función para mostrar hover tooltips
def display_image_on_hover(name, image_url, i):
    hover_class = f'hoverable_{i}'
    tooltip_class = f'tooltip_{i}'
    popup_class = f'image-popup_{i}'
    css = f'''
        .{hover_class} {{
            position: relative;
            display: inline-block;
            cursor: pointer;
            margin: 6px;
        }}
        .{hover_class} .{tooltip_class} {{
            opacity: 0;
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            transition: opacity 0.5s;
            background-color: rgba(0, 0, 0, 0.85);
            color: #fff;
            padding: 4px;
            border-radius: 4px;
            white-space: nowrap;
            z-index: 1000;
        }}
        .{hover_class}:hover .{tooltip_class} {{
            opacity: 1;
        }}
        .{popup_class} {{
            display: none;
            position: absolute;
            top: -220px;
            left: -30px;
            width: 200px;
            height: 140px;
            background-image: url('{image_url}');
            background-size: cover;
            border: 1px solid #ccc;
            z-index: 999;
        }}
        .{hover_class}:hover .{popup_class} {{
            display: block;
        }}
    '''
    html = f'''
        <style>{css}</style>
        <div class="{hover_class}">
            <b>{name}</b>
            <div class="{tooltip_class}">{name}</div>
            <div class="{popup_class}"></div>
        </div>
    '''
    st.markdown(f"{tooltip_css}{image_hover}", unsafe_allow_html=True)

# Mostrar cada agente con su imagen
for i, (agent, url) in enumerate(agent_images.items()):
    display_image_on_hover(agent, url, i)


# import streamlit as st
# import matplotlib.pyplot as plt
# import matplotlib.patches as mpatches
# import networkx as nx
# import random

# # ----------------------------
# # CONFIGURACIÓN STREAMLIT
# # ----------------------------
# st.set_page_config(page_title="Rosetta Agent System", layout="wide")

# # Navigation pages
# pages = ["🧠 Agent Graph", "✅ Validation Summary", "🧪 Committee Review"]

# # Initialize session state
# if "active_page" not in st.session_state:
#     st.session_state.active_page = pages[0]

# # If a navigation_target exists, update active page and clear it
# if "navigation_target" in st.session_state:
#     st.session_state.active_page = st.session_state["navigation_target"]
#     del st.session_state["navigation_target"]

# # Sidebar control
# selected_page = st.sidebar.radio("📂 Navigation", pages, index=pages.index(st.session_state.active_page))

# # Update only if changed by user interaction
# if selected_page != st.session_state.active_page:
#     st.session_state.active_page = selected_page

# # Use current active page
# page = st.session_state.active_page

# # ----------------------------
# # PÁGINA 1: GRAFO DE AGENTES
# # ----------------------------
# if page == "🧠 Agent Graph":

#     st.title("Rosetta Agent System")

#     G = nx.DiGraph()
#     G.add_node("Rosetta Agent", layer=0)
#     G.add_node("Question-classifier agent", layer=1)
#     G.add_edge("Rosetta Agent", "Question-classifier agent")

#     functional_agents = ["Diagnosis agent", "Treatment agent", "Prognostic agent", "Guidelines agent", "Genomic agent"]
#     researcher_agents = [f"{a.split()[0]} Researcher agent" for a in functional_agents]

#     for agent, researcher in zip(functional_agents, researcher_agents):
#         G.add_node(agent, layer=2)
#         G.add_node(researcher, layer=3)
#         G.add_edge("Question-classifier agent", agent)
#         G.add_edge(agent, researcher)

#     G.add_node("Multi-researcher agent", layer=5)
#     for researcher in researcher_agents:
#         G.add_edge(researcher, "Multi-researcher agent")

#     G.add_node("Protocol agent", layer=5)
#     G.add_node("Graph-researcher agent", layer=6)
#     G.add_edge("Multi-researcher agent", "Protocol agent")
#     G.add_edge("Multi-researcher agent", "Graph-researcher agent")

#     layer_positions = {
#         0: ["Rosetta Agent"],
#         1: ["Question-classifier agent"],
#         2: functional_agents,
#         3: researcher_agents,
#         4: ["Multi-researcher agent"],
#         5: ["Protocol agent", "Graph-researcher agent"]
#     }

#     pos = {}
#     y_gap = -2.2
#     x_gap = 3.5
#     for layer, nodes in layer_positions.items():
#         y = layer * y_gap
#         n = len(nodes)
#         for i, node in enumerate(nodes):
#             x = (i - (n - 1) / 2) * x_gap
#             pos[node] = (x, y)

#     def draw_graph(active_nodes=None):
#         fig, ax = plt.subplots(figsize=(15, 12))
#         ax.set_title("Rosetta Agent System", fontsize=16)

#         node_width = 2.2
#         node_height = 0.9

#         for node in G.nodes():
#             x, y = pos[node]
#             color = "lightgreen" if active_nodes and node in active_nodes else "lightblue"
#             rect = mpatches.FancyBboxPatch((x - node_width / 2, y - node_height / 2), node_width, node_height,
#                                            boxstyle="round,pad=0.05", ec="black", fc=color)
#             ax.add_patch(rect)
#             ax.text(x, y, node, ha='center', va='center', fontsize=8, wrap=True)

#         for u, v in G.edges():
#             x1, y1 = pos[u]
#             x2, y2 = pos[v]
#             start = (x1, y1 - node_height / 2)
#             end = (x2, y2 + node_height / 2)
#             ax.annotate("",
#                         xy=end, xycoords='data',
#                         xytext=start, textcoords='data',
#                         arrowprops=dict(arrowstyle="->", lw=1.2))

#         ax.set_xlim(-12, 12)
#         ax.set_ylim(-14, 2)
#         ax.axis('off')
#         return fig

#     def get_active_nodes(question):
#         active = {"Rosetta Agent", "Question-classifier agent"}
    
#         if question == "What biomarkers support diagnosis of triple-negative breast cancer?":
#             active.update(["Diagnosis agent", "Diagnosis Researcher agent"])
    
#         elif question == "How effective is trastuzumab in early-stage HER2+ patients?":
#             active.update(["Treatment agent", "Treatment Researcher agent",
#                            "Prognostic agent", "Prognostic Researcher agent"])
    
#         elif question == "Discover novel imaging-genomic signatures predicting resistance to immunotherapy":
#             active.update([
#                 "Genomic agent", "Genomic Researcher agent",
#                 "Multi-researcher agent", "Protocol agent", "Graph-researcher agent"
#             ])
    
#         return active

#     question = st.selectbox(
#     "Select a question:",
#     [
#         "What biomarkers support diagnosis of triple-negative breast cancer?",
#         "How effective is trastuzumab in early-stage HER2+ patients?",
#         "Discover novel imaging-genomic signatures predicting resistance to immunotherapy"
#     ]
# )

#     st.session_state["selected_question"] = question
#     active_nodes = get_active_nodes(question)
#     fig = draw_graph(active_nodes)
#     st.pyplot(fig)

# # ----------------------------
# # PÁGINA 2: VALIDACIÓN
# # ----------------------------
# elif page == "✅ Validation Summary":

#     st.title("🔍 Researcher Agent Validation")

#     question = st.session_state.get("selected_question", "")
#     st.markdown(f"### 📌 Question: *{question}*")
    
#     agent_outputs = {
#     "Diagnosis agent": "Triple-negative breast cancer is typically diagnosed by lack of ER, PR, and HER2 expression in IHC.",
#     "Treatment agent": "Trastuzumab shows high efficacy in improving response rates in early-stage HER2+ patients.",
#     "Prognostic agent": "Early-stage HER2+ breast cancer patients treated with trastuzumab demonstrate improved 5-year survival.",
#     "Genomic agent": (
#         "A novel resistance signature was identified, characterized by:\n"
#         "- 🧠 Imaging: Increased peritumoral edema and low radiomic entropy in T2-weighted MRI\n"
#         "- 🧬 Genomics: Co-occurrence of PTEN deletion, low IFNG expression, and MLH1 promoter hypermethylation\n"
#         "\nThese features suggest an immunologically 'cold' tumor phenotype resistant to checkpoint inhibition."
#     ),
#     "Protocol agent": "Designed protocol integrates imaging-genomic stratification for a prospective immunotherapy trial.",
#     "Graph-researcher agent": "Latent graph embeddings reveal clusters of resistance across imaging and genomic domains."
# }

#     active_agents = []
#     if "treatment" in question.lower():
#         active_agents.append("Treatment agent")
#     if "prognosis" in question.lower():
#         active_agents.append("Prognostic agent")
#     if "diagnosis" in question.lower():
#         active_agents.append("Diagnosis agent")
#     if "guideline" in question.lower():
#         active_agents.append("Guidelines agent")
#     if "genomic" in question.lower():
#         active_agents.append("Genomic agent")
#     if not active_agents:
#         active_agents = ["Treatment agent", "Prognostic agent"]

#     results = {}
#     is_discovery_question = "discover novel imaging-genomic signatures" in question.lower()

#     for agent in active_agents:
#         if is_discovery_question:
#             scores = {
#                 "Performance": round(random.uniform(0.75, 0.85), 2),
#                 "Source Match": 0.0,
#                 "Scientific Support": 0.0,
#                 "Plausibility": round(random.uniform(0.7, 0.85), 2),
#                 "Contradiction Risk": round(random.uniform(0.0, 0.2), 2)
#             }
#         else:
#             scores = {
#                 "Performance": round(random.uniform(0.75, 0.95), 2),
#                 "Source Match": round(random.uniform(0.3, 0.95), 2),
#                 "Scientific Support": round(random.uniform(0.3, 0.9), 2),
#                 "Plausibility": round(random.uniform(0.5, 1.0), 2),
#                 "Contradiction Risk": round(random.uniform(0.0, 0.4), 2)
#             }
#         results[agent] = scores

#     global_score = {
#         key: round(sum(agent_scores[key] for agent_scores in results.values()) / len(results), 2)
#         for key in ["Performance", "Source Match", "Scientific Support", "Plausibility", "Contradiction Risk"]
#     }

#     final_score = round(
#         0.4 * global_score["Performance"] +
#         0.2 * global_score["Source Match"] +
#         0.15 * global_score["Scientific Support"] +
#         0.15 * global_score["Plausibility"] +
#         0.1 * (1 - global_score["Contradiction Risk"]),
#         2
#     )

#     for agent in active_agents:
#         st.markdown(f"#### 🤖 {agent}")
#         st.markdown(f"**Output:** *{agent_outputs.get(agent, 'No output available.')}*")
#         st.write(results[agent])

#     st.markdown("---")
#     st.subheader("📊 Aggregated Validation")

#     if global_score["Source Match"] == 0 and global_score["Scientific Support"] == 0:
#         st.warning("⚠️ No supporting scientific literature was found for any agent.")
#         st.info("This may indicate a novel hypothesis. Recommend expert committee review.")
#         if st.button("🔎 Evaluate as Scientific Committee"):
#             st.session_state["hypothesis_under_review"] = question
#             st.session_state["navigation_target"] = "🧪 Committee Review"
#             st.rerun()
#     else:
#         st.write(global_score)
#         st.success(f"🧠 Final Certainty Score: **{final_score * 100:.1f}%**")
#         st.progress(final_score)

#     with st.expander("ℹ️ How are the scores evaluated?"):
#         st.markdown("""
#         ### 🔹 Source Match Score  
#         **Does the literature say something similar?**  
#         - A RAG (Retrieval-Augmented Generation) system retrieves top-k relevant abstracts from biomedical databases like PubMed.  
#         - The agent's output is compared semantically to each abstract.  
#         - **Metric:** Cosine similarity of embeddings (e.g., BioSentVec, SciBERT, SBERT).  
#         - **Score:** Average similarity score over top-k documents, normalized to 0–1.
    
#         ---
    
#         ### 🔹 Scientific Support Score  
#         **Are the sources high quality and reliable?**  
#         - For each retrieved source, a biomedical LLM is prompted to assess:  
#           • Study type (e.g., RCT, cohort, review)  
#           • Journal quality and impact  
#           • Sample size (parsed or inferred)  
#           • Citation count (via Semantic Scholar API or CrossRef)  
#           • Recency (based on publication year)  
#         - The LLM produces a support confidence score per abstract.  
#         - **Score:** Weighted average of evidence-level, impact, sample size, citation count, and recency.
    
#         ---
    
#         ### 🔹 Plausibility Score  
#         **Does the claim make biomedical sense?**  
#         - Evaluated using a domain-tuned LLM (e.g., BioMedLM, PubMedGPT).  
#         - Prompt example:  
#           *"Is the following medical hypothesis plausible based on current knowledge? Rate from 0 (implausible) to 1 (very plausible): '{claim}'."*  
#         - **Score:** LLM confidence score directly (or derived from likelihood/logits).
    
#         ---
    
#         ### 🔹 Contradiction Risk Score  
#         **Is there evidence against the agent’s output?**  
#         - The same RAG-retrieved documents are passed to the LLM or a contradiction classifier.  
#         - Prompt example:  
#           *"Does this abstract contradict the following statement? Answer: supports / contradicts / unrelated."*  
#         - **Score:** Probability of contradiction. Final score is `1 - contradiction_prob`.
    
#         ---
    
#         ### 🟢 Performance Score  
#         **How well did the model perform during development?**  
#         - Based on traditional validation data:
#           - Classification → AUC, F1-score, Accuracy  
#           - Regression → RMSE, MAE, R²  
#         - **Score:** Rescaled metric from 0–1 (e.g., AUC of 0.88 → score 0.88)
#         """)

# # ----------------------------
# # PÁGINA 3: COMITÉ CIENTÍFICO
# # ----------------------------
# elif page == "🧪 Committee Review":

#     st.title("🧪 Scientific Committee Review")

#     hypothesis = st.session_state.get("hypothesis_under_review", "No hypothesis submitted.")
#     st.markdown("### 🧬 Candidate Hypothesis for Evaluation:")
#     st.info(f"**{hypothesis}**")

#     st.markdown("---")
#     st.subheader("🧭 Committee Evaluation Criteria")

#     plausible = st.checkbox("✅ Biologically plausible")
#     internally_coherent = st.checkbox("✅ Internally consistent across data modalities")
#     testable = st.checkbox("✅ Feasible to validate experimentally")
#     original = st.checkbox("✅ Clearly novel compared to existing literature")

#     total_score = sum([plausible, internally_coherent, testable, original])
#     score_percent = int((total_score / 4) * 100)

#     st.markdown(f"### 🔢 Committee Review Score: **{score_percent}%**")

#     if score_percent >= 75:
#         st.success("✅ Approved for inclusion in the Research Ideas Pool.")
#         if st.button("📦 Add to Research Idea Pool"):
#             st.session_state.setdefault("research_ideas", []).append(hypothesis)
#             st.success("✅ Hypothesis added to pool.")
#     else:
#         st.warning("🕵️ More review or evidence needed before approval.")

#     st.markdown("---")
#     st.subheader("📦 Validated Research Ideas Pool")

#     ideas = st.session_state.get("research_ideas", [])
#     if ideas:
#         for idea in ideas:
#             st.markdown(f"🧠 **{idea}**")
#     else:
#         st.info("No research ideas approved yet.")
