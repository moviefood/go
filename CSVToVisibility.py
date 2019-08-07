import pandas as pd
from TimeSeriesVisibility import generate_visibility_graph

import matplotlib.pyplot as plt
import networkx as nx


data_frame = pd.read_csv("DatabaseHits.csv")

month_humidity = []
average_humidity = []
month_temp = []
average_temp = []

temp_sum = 0.0
temp_count = 1
hum_sum = 0.0
hum_count = 1
current_month = 25
for index, row in data_frame.iterrows():
    month_index = str(row[1]).replace(':', '')
    if current_month != month_index[2:4]:
        if temp_count != 0:
            temp_average = round(temp_sum / temp_count, 2)
            average_temp.append(temp_average)
            month_temp.append(int(current_month))
            print(current_month, temp_average)
        if hum_count != 0:
            hum_average = round(hum_sum / hum_count, 2)
            average_humidity.append(hum_average)
            month_humidity.append(int(current_month))
            print(current_month, hum_average)
        temp_sum = temp_count = hum_sum = hum_count = 0
        current_month = month_index[2:4]
    for i in xrange(4, 5):
        if row[i] != 999 and row[i] != 99950:
            hum_sum += row[i]
            hum_count += 1
    for i in xrange(6, 11):
        if row[i] != 999:
            temp_sum += row[i]
            temp_count += 1

g1 = generate_visibility_graph({
    "t": range(len(month_temp)),
    "x": average_temp
})

g2 = generate_visibility_graph({
    "t": range(len(month_humidity)),
    "x": average_humidity
})

print(g1.edges())
print(g2.edges())
graph_pos = nx.circular_layout(g1)
nx.draw_networkx_nodes(g1, graph_pos, node_size=1000, node_color='skyblue')
nx.draw_networkx_edges(g1, graph_pos)
nx.draw_networkx_labels(g1, graph_pos, font_size=12, font_family='sans-serif')

plt.figure()
plt.stem(range(len(month_temp)), average_temp)

plt.figure()
graph_pos = nx.circular_layout(g2)
nx.draw_networkx_nodes(g2, graph_pos, node_size=1000, node_color='skyblue')
nx.draw_networkx_edges(g2, graph_pos)
nx.draw_networkx_labels(g2, graph_pos, font_size=12, font_family='sans-serif')

plt.figure()
plt.stem(range(len(month_humidity)), average_humidity)

plt.show()