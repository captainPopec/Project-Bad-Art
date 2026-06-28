
import numpy as np
import maad
from maad import util
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/fancy graf.csv', encoding='latin1')
#df = df.dropna() # ako mi je prvi stupac prazan, sgunro će uklnoiti cijelu tablicu jer jer klasificriao red koa NaN

#dfa=pd.read_csv('C:/Users/Korisnik/OneDrive - Prirodoslovno-matematički fakultet/Self Investing/Projekti/Bad Art/Podatci za analizu/Antropofonija_revised.csv', encoding='latin1')
#dfa = dfa.dropna(subset=['tActivity', 'H', 'AGI'])

#df['tActivity'] = pd.to_numeric(df['tActivity'], errors='coerce')
#df['H'] = pd.to_numeric(df['H'], errors='coerce')
#df['AGI'] = pd.to_numeric(df['AGI'], errors='coerce')


#dfa['tActivity'] = pd.to_numeric(dfa['tActivity'], errors='coerce')
#dfa['H'] = pd.to_numeric(dfa['H'], errors='coerce')
#dfa['AGI'] = pd.to_numeric(dfa['AGI'], errors='coerce')


d1='log(med*ACI*H)'
d2 = 'S2N *med'
d3 = 'log(AGI*H*med)'

fig = plt.figure(figsize=(14, 11))
ax=fig.add_subplot(111, projection= '3d')
ax.scatter(df[d1+'o'], df[d2+'o'], df[d3+'o'],color='r', marker='v',label='Izdvojeni')
ax.plot(df[d1+'o'], df[d2+'o'], df[d3+'o'], color='r')
ax.scatter(df[d1+'kl'], df[d2+'kl'], df[d3+'kl'],color='orange', marker='o', label='orkestralna glazba')
ax.plot(df[d1+'kl'], df[d2+'kl'], df[d3+'kl'], color='orange')
ax.scatter(df[d1+'g'], df[d2+'g'], df[d3+'g'],color='b', marker='s', label='govor')
ax.plot(df[d1+'g'], df[d2+'g'], df[d3+'g'], color='b')



ax.set_xlabel(d1)
ax.set_ylabel(d2)
ax.set_zlabel(d3)
ax.legend()



from sklearn.cluster import KMeans

X = df[[d1, d2, d3]].dropna()

# Apply K-means clustering (choose the number of clusters, say 3)
kmeans = KMeans(n_clusters=3)
kmeans.fit(X)
labels = kmeans.labels_

# Scatter plot with clusters
fig = plt.figure(figsize=(14, 11))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X.iloc[:, 0], X.iloc[:, 1], X.iloc[:, 2], c=labels, cmap='flag', marker='o')

ax.set_xlabel(d1)
ax.set_ylabel(d2)
ax.set_zlabel(d3)


plt.show()

'''

x=np.array([0.032619581,
0.005556184,
0.027531583,
0.014203289,
0.038787727,
0.048463502,
0.096770988,
0.047700912,0.232391357])

logarithmic_mean = np.exp(np.mean(np.log(x)))

print("Logarithmic Mean:", logarithmic_mean)
print(np.average(x))
'''