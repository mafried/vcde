import json
import numpy as np
import networkx as nx
from fa2 import ForceAtlas2
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
INPUT = Path(__file__).parent.parent / "graph.json"
OUTPUT = Path(__file__).resolve().parent / "graph_sampled.json"

# --- 1. Originaldaten laden ---
with open(INPUT) as f:
    data = json.load(f)

# Node-Metadaten als Lookup-Tabelle
node_meta = {n["id"]: n for n in data["nodes"]}

# --- 2. Graph aufbauen ---
G = nx.Graph()
for node in data["nodes"]:
    G.add_node(node["id"])
for edge in data["edges"]:
    G.add_edge(edge["source"], edge["target"])

G.remove_edges_from(nx.selfloop_edges(G))
print(f"Original: {G.number_of_nodes()} Knoten, {G.number_of_edges()} Kanten")

# --- 3. k-Core anwenden ---
K = 10
core = nx.k_core(G, k=K)
print(f"k={K}-Core: {core.number_of_nodes()} Knoten, {core.number_of_edges()} Kanten")

# --- 4. FA2 Layout auf dem reduzierten Graphen ---
np.random.seed(42)

fa2 = ForceAtlas2(
    outboundAttractionDistribution=True,
    edgeWeightInfluence=1.0,
    jitterTolerance=1.0,
    barnesHutOptimize=True,
    barnesHutTheta=1.2,
    scalingRatio=10.0,
    strongGravityMode=False,
    gravity=0.5,
    verbose=True
)

positions = fa2.forceatlas2_networkx_layout(core, pos=None, iterations=1000)

# --- 5. Export ---
nodes_out = []
for node_id in core.nodes():
    meta = node_meta[node_id]
    x, y = positions[node_id]
    nodes_out.append({
        "id":        node_id,
        "x":         x,
        "y":         y,
        "community": meta.get("community", 0),
        "category":  meta.get("category", ""),
        "name":      meta.get("name", str(node_id))
    })

edges_out = [
    {"source": u, "target": v}
    for u, v in core.edges()
]

with open(OUTPUT, "w") as f:
    json.dump({"nodes": nodes_out, "edges": edges_out}, f)

print(f"Gespeichert: {OUTPUT}")
print(f"Nodes: {len(nodes_out)}, Edges: {len(edges_out)}")