# %%
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from random import randint

# %%
df = pd.read_csv("dataset_circles.csv")
df = df[['x','y']]
df['lable'] = np.zeros(len(df.index))
#print(df.loc[1]['x'])
#print(df.columns)
#print(df[df.lable==0].mean()['x'])
# 总点数
N = len(df.index)


# %%
# 聚类数
K = 2
dots = []
nxt_centroids = []
for i in range(0,K):
    dot = randint(0,N-1)
    nxt_centroids.append([df.loc[dot]['x'], df.loc[dot]['y']])
centroids = []

# %%
itreation = 0
while centroids != nxt_centroids:
    #print('itreation: {}'.format(itreation))
    #print('centroids = {}'.format(nxt_centroids))
    itreation = itreation+1
    centroids = list(nxt_centroids)
    nxt_centroids.clear()
    for i in range(0,N):
        x,y = df.loc[i][:K]
        distances = []
        for centroid in centroids:
            distances.append(np.sqrt((x-centroid[0])**2 + (y-centroid[1])**2))
        lable = np.argmin(distances)
        #print(distances)
        #print(lable)
        df.loc[i, 'lable'] = lable
    for i in range(0,K):
        nxt_centroids.append([df[df.lable==i].mean()['x'], df[df.lable==i].mean()['y']])

# %%
#print(df[['x','y']])
plt.scatter(df[df.lable==0]['x'],df[df.lable==0]['y'], color='r', marker='o')
plt.scatter(df[df.lable==1]['x'],df[df.lable==1]['y'], color='b')
plt.show()



