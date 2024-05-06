#!/usr/bin/env python3

import collections
import json

DATABASE_JSON = "results.json"
NONDET_GRAPH_FILENAME = "nondet_graph.dot"


def extract_edges(data):
    edges = set()
    for (args, result) in data.items():
        if args == "":
            continue
        #if "b" in args:
        #    continue
        if "U" in args:
            continue
        prev_result = data[args[:-1]]
        # This deduplicates edges:
        edges.add((prev_result, args[-1], result))
    return edges


def write_nondet_graph(edges):
    sources = collections.Counter((n1, e) for (n1, e, _) in edges)
    with open(NONDET_GRAPH_FILENAME, "w") as fp:
        fp.write("digraph G {\n")
        fp.write("A;S;T;E;\n")
        for (n1, e, n2) in edges:
            if sources[(n1, e)] > 1:
                color_tag = ",color=red"
            else:
                color_tag = ""
            fp.write(f"{n1} -> {n2} [label=\"{e}\"{color_tag}]\n")
        fp.write("}\n")


def run():
    with open(DATABASE_JSON, "r") as fp:
        data = json.load(fp)
    edges = extract_edges(data)
    write_nondet_graph(edges)


if __name__ == "__main__":
    run()
