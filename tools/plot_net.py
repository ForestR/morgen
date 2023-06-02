"""
Using the networkx and pyvis libraries to read a network file, create a directed graph, and visualize it interactively using an HTML file.

Make sure to replace the file paths and folder paths (filepath and save_path) with your specific paths before running the code.
"""

import json

import networkx as nx
from pyvis.network import Network

# Read the network file
filepath = "your/folder/path/morgen/networks"  # Replace with your networks folder path.
network = "pipeline"

# Read the network file
filename = f"{filepath}/{network}.net"

# Create an empty directed graph
G = nx.DiGraph()

# Read the network file and add nodes and edges to the graph
with open(filename, "r") as file:
    for line in file:
        if line.startswith("#"):
            continue  # Skip comment lines

        values = line.strip().split(",")
        edge_type = values[0]
        identifier_in = values[1]
        identifier_out = values[2]

        # Check if the line has enough elements
        if len(values) >= 4:
            pipe_length = values[3]
        else:
            pipe_length = "NaN"  # Handle missing pipe length

        # Add nodes and edges to the graph
        G.add_edge(identifier_in, identifier_out, length=float(pipe_length) if pipe_length != "NaN" else None,
                   type=edge_type)

# Find the input and output nodes
input_nodes = [node for node in G.nodes if G.in_degree(node) == 0]
output_nodes = [node for node in G.nodes if G.out_degree(node) == 0]

# Create an interactive network visualization using pyvis
nt = Network(notebook=True, height="900px", width="100%")

# Add nodes and edges to the visualization
for node in G.nodes:
    # Set specific attributes for input and output nodes
    node_color = "lime" if node in input_nodes else "tomato" if node in output_nodes else "lightskyblue"
    nt.add_node(node, color=node_color)

for (u, v, attrs) in G.edges(data=True):
    # Determine the color based on edge_type
    color = "limegreen" if attrs["type"] == "S" \
        else "crimson" if attrs["type"] == "C" \
        else "gray" if attrs["type"] == "V" \
        else "aqua"
    width = 1 if attrs["type"] == "P" else 5  # Set a higher width for specific edge types
    nt.add_edge(u, v, value=attrs["length"] if attrs["length"] is not None else "NaN", color=color, width=width)

# Set the physics simulation options for dragging and deformation
options = {"physics": {"enabled": True}}
nt.set_options(json.dumps(options))

# Display the interactive network visualization
save_path = "your/folder/path"  # Replace with the address where the document is stored
nt.show(f"{save_path}/{network}_network.html")
