from multiprocessing import Pool
from sklearn.metrics.pairwise import pairwise_distances
from scipy.sparse.csgraph import connected_components
from collections import OrderedDict
from copy import deepcopy
import numpy as np

THRESHOLD = 0.35

def distance(vecs):
    vec1 = vecs[0]
    vecAll = vecs[1]
    Dis_matrix = pairwise_distances(vec1, vecAll, metric='cosine', n_jobs=1)
    Dis_matrix = Dis_matrix.astype(np.float16)
    return Dis_matrix

def chunks_vec(l, n):
    for i in range(0, l.shape[0], n):
        yield l[i:i + n]

def compute_distance_matrix(vectors, chunk_size=1000, num_workers=2):
    vector_chunks = list(chunks_vec(vectors, chunk_size))
    vector_chunks = [(i, vectors) for i in vector_chunks]

    pool = Pool(num_workers)
    Dis_matrix = pool.map(distance, vector_chunks)
    Dis_matrix = np.vstack(Dis_matrix)
    pool.terminate()
    
    return Dis_matrix

def cluster_documents(distance_matrix):
    graph = deepcopy(distance_matrix)
    graph[graph <= THRESHOLD] = 2
    graph[graph != 2] = 0
    graph[graph == 2] = 1
    graph = graph.astype(np.int8)
    res = connected_components(graph, directed=False)

    cluster_labels = res[1]
    num_cluster = res[0]
    res_cluster = OrderedDict()

    for i in range(len(cluster_labels)):
        if cluster_labels[i] in res_cluster: 
            res_cluster[cluster_labels[i]].append(i)
        else: 
            res_cluster[cluster_labels[i]] = [i]

    res_cluster = [res_cluster[i] for i in range(num_cluster)]
    res_cluster = [sorted(r) for r in res_cluster if len(r) > 1]
    res_cluster.sort(key=len, reverse=True)
    
    return res_cluster
