import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as hic
import scipy.spatial.distance as dis


def dendrogram(h, labels, title='Hierarchical Classification', threshold=None):
    plt.figure(figsize=(15, 8))
    plt.title(title, fontsize=16, color='k')
    hic.dendrogram(h, labels=labels, leaf_rotation=90, leaf_font_size=10)
    if threshold:
        plt.axhline(threshold, c='r', linestyle='--')
    plt.xlabel('Country', fontsize=14, color='k')
    plt.ylabel('Distance', fontsize=14, color='k')
    plt.tight_layout()


def threshold(h):
    m = np.shape(h)[0]
    dist_1 = h[1:m, 2]
    dist_2 = h[0:m - 1, 2]
    diff = dist_1 - dist_2
    j = np.argmax(diff)
    threshold_value = (h[j, 2] + h[j + 1, 2]) / 2
    return threshold_value, j, m


def clusters(h, k):
    n = np.shape(h)[0] + 1
    g = np.arange(0, n)
    for i in range(n - k):
        k1 = h[i, 0]
        k2 = h[i, 1]
        g[g == k1] = n + i
        g[g == k2] = n + i
    cat = pd.Categorical(g)
    return ['C' + str(i) for i in cat.codes], cat.codes


# Load the dataset
dataset = 'dataIN/EuropeHappiness.csv'
table = pd.read_csv(dataset, index_col=0)

X = table.iloc[:, 1:].values
obsName = table.index.tolist()

methods = list(hic._LINKAGE_METHODS)
distances = dis._METRICS_NAMES

# HCA model
method = 5
distance = 7
HC = hic.linkage(X, method=methods[method], metric=distances[distance])
t, j, m = threshold(HC)
output_dir = './dataOUT/HCA'
os.makedirs(output_dir, exist_ok=True)
with open(os.path.join(output_dir, 'result.txt'), 'w') as file:
    file.write(f'threshold = {t}\njunction with max. diff = {j}\nno. of junctions = {m}')

k = m - j

# plot and save the dendrogram
dendrogram(
    HC,
    labels=obsName,
    title=f'Hierarchical Classification {methods[method]} - {distances[distance]}',
    threshold=t
)
plt.savefig(os.path.join(output_dir, 'hierarchical_classification.png'))

# determine cluster assignments and save results
labels, codes = clusters(HC, k)
ClusterTab = pd.DataFrame(data=labels, index=obsName, columns=['Cluster'])
ClusterTab.to_csv(os.path.join(output_dir, 'indClusters.csv'))

plt.show()
