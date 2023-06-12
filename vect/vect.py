import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import CountVectorizer


## 덴드로그램
method = 'ward'
z = linkage(docu_tfidt_matrix, method)
plt.rcParams['font.family'] = 'Malgun Gothic'
fig, ax = plt.subplots(figsize = (20, 20))
dendrogram(z, ax=ax, labels = docu_tfidf_matrix.index, orientation = 'right')


## 클러스터링
analyser = AgglomerativeClustering(linkage = method, n_clusters = 4)
cluster_id = pd.DataFrame(analyser.fit_predict(docu_tfidf_matrix), columns = ['그룹 id'])
cluster_data = pd.concat((cluster_id, data), axis = 1).sort_values('그룹 id')
cluster_data
