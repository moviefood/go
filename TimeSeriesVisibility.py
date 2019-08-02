import numpy as np
from copy import deepcopy

import matplotlib.pyplot as plt
import networkx as nx


def generate_visibility_graph(time_series_dataset):
    g = nx.Graph()

    if type(time_series_dataset) is not dict or len(time_series_dataset) != 2:
        raise Exception("The argument parameter is not of correct type.")
    if "t" not in time_series_dataset or "x" not in time_series_dataset:
        raise Exception("The dataset is missing a \"t\" or an \"x\" key.")
    if type(time_series_dataset["t"]) is not list or type(time_series_dataset["x"]) is not list:
        raise Exception("The dataset items are not lists.")
    if len(time_series_dataset["t"]) != len(time_series_dataset["x"]):
        raise Exception("The lengths of the arrays must be equal.")
    if len(time_series_dataset["t"]) == 0:
        return g
    for j in xrange(len(time_series_dataset["t"])):
        g.add_node(j, label=time_series_dataset["t"][j])
    tsd = deepcopy(time_series_dataset)
    global s_index
    s_index = get_s_index(range(len(tsd["t"])), tsd["x"])
    print(s_index)
    for i in xrange(1, len(s_index)):
        cur_node = s_index[i]
        print("neightbors of " + str(cur_node))
        left = -1
        right = len(s_index)
        for j in list(g.neighbors(cur_node)):
            print("Node " + str(j))
            if j < cur_node:
                left = np.amax([left, j])
                print(str(left) + " " + str(j))
            else:
                right = np.amin([right, j])
                print(str(right) + " " + str(j))
        left += 1
        right -= 1
        updateVisibility(time_series_dataset, left, right, cur_node, g)
    return g


def updateVisibility(d, left, right, i, g):
    print(d)
    print(str(left) + " " + str(i) + " " + str(right))
    max_slope = np.NINF
    min_slope = np.Inf
    j = int(i + 1)
    while j <= right:
        print(str(j))
        if d["t"][j] == d["t"][i]:
            raise Exception("The dataset is not a function. Ensure all \"t\" values are unique.")
        slope = (float(d["x"][j]) - float(d["x"][i])) / (float(d["t"][j]) - float(d["t"][i]))
        print("Max Slopes: " + str(slope) + " " + str(max_slope))
        if slope > max_slope:
            max_slope = slope
            g.add_edge(i, j)
            print("Added (" + str(i) + ", " + str(j) + ")")
        j += 1

    j = int(i - 1)
    while j >= left:
        print("Itere" + str(j));
        if d["t"][j] == d["t"][i]:
            raise Exception("The dataset is not a function. Ensure all \"t\" values are unique.")
        slope = (float(d["x"][i]) - float(d["x"][j])) / (float(d["t"][i]) - float(d["t"][j]))
        print("Min Slopes: " + str(slope) + " " + str(min_slope))
        if slope < min_slope:
            min_slope = slope
            g.add_edge(i, j)
            print("Added (" + str(i) + ", " + str(j) + ")")
        j -= 1


def get_s_index(time_index, x_index):
    s_index = time_index
    x = x_index
    if len(x) > 1:
        mid = len(x) / 2
        lx = x[:mid]
        rx = x[mid:]
        lt = s_index[:mid]
        rt = s_index[mid:]
        get_s_index(lt, lx)
        get_s_index(rt, rx)
        i = j = k = 0
        while i < len(lx) and j < len(rx):
            if lx[i] > rx[j]:
                x[k] = lx[i]
                s_index[k] = lt[i]
                i += 1
            else:
                x[k] = rx[j]
                s_index[k] = rt[j]
                j += 1
            k += 1
        while i < len(lx):
            x[k] = lx[i]
            s_index[k] = lt[i]
            i += 1
            k += 1
        while j < len(rx):
            x[k] = rx[j]
            s_index[k] = rt[j]
            j += 1
            k += 1
    return s_index


def print_list(arr):
    s = ""
    for i in range(len(arr)):
        s += str(arr[i]) + " "
    print(s)


if __name__ == '__main__':
    timeSeriesData = {
        "t": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "x": [3, 4, 4, 7, 5, 0, 2, 8, 1, 9]
    }
    print("Given array is\n")
    print_list(timeSeriesData["t"])
    print_list(timeSeriesData["x"])
    print("s_index is:\n")
    g = generate_visibility_graph(timeSeriesData)
    print(g.edges())
    graph_pos = pos=nx.spring_layout(g)
    nx.draw_networkx_nodes(g, graph_pos, node_size=1000, node_color='skyblue')
    nx.draw_networkx_edges(g, graph_pos)
    nx.draw_networkx_labels(g, graph_pos, font_size=12, font_family='sans-serif')
    plt.show()
