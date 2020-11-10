import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
import copy

dataFrame = pd.DataFrame(
    {
        'x': [12, 20, 28, 18, 29, 33, 24, 45, 45, 52, 51, 52, 55, 53, 55, 61, 64, 69, 72],
        'y': [39, 36, 30, 52, 54, 46, 55, 59, 63, 70, 66, 63, 58, 23, 14, 8, 19, 7, 24]
    }
)

colorMap = {1: 'r', 2: 'g', 3: 'b'}


def Initialize(k):
    # Initialization
    np.random.seed(250)
    centroids = {
        i+1: [np.random.randint(0, 80), np.random.randint(0, 80)] for i in range(k)}
    return centroids


def sampleClosestPoints(centroids):
    for i in centroids.keys():
        dataFrame['distance_from_{}'.format(i)] = (

            np.sqrt(

                (dataFrame['x']-centroids[i][0])**2 +

                (dataFrame['y']-centroids[i][1])**2

            )

        )

    centroid_distance_cols = [

        'distance_from_{}'.format(i) for i in centroids.keys()]

    dataFrame['closest'] = dataFrame.loc[:,
                                         centroid_distance_cols].idxmin(axis=1)

    dataFrame['closest'] = dataFrame['closest'].map(

        lambda x: int(x.lstrip('distance_from_')))

    dataFrame['color'] = dataFrame['closest'].map(lambda x: colorMap[x])

    print(dataFrame.head(2))

    # plotDataFrame(dataFrame, centroids, colorMap, 2)

    return dataFrame

def plotDataFrame(df, centroid, centroid_color_mp, fidID):
    fig = plot.figure(figsize=(5, 5))
    plot.scatter(df['x'], df['y'], color=df['color'], alpha=0.5)
    for i in centroid.keys():
        plot.scatter(*centroid[i], color=centroid_color_mp[i])
    plot.xlim(0, 80)
    plot.ylim(0, 80)
    plot.savefig("test{}.png".format(fidID))


centroids = Initialize(3)
df = sampleClosestPoints(centroids)


def updateCentroids(old_centroids):
    for i in old_centroids.keys():
        old_centroids[i][0] = np.mean(df[df['closest'] == i]['x'])
        old_centroids[i][1] = np.mean(df[df['closest'] == i]['y'])
    return old_centroids

while True:
    closest_points = df['closest'].copy(deep=True)
    newCentroids = updateCentroids(centroids)
    df = sampleClosestPoints(newCentroids)
    if closest_points.equals(df['closest']):
        break

plotDataFrame(df,centroids,colorMap,3)