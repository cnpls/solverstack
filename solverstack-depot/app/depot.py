from copy import deepcopy

import numpy as np


class KMeans:
    def __init__(self, k):
        self.k = k

    @staticmethod
    def get_dist(a, b, axis=1):
        return np.linalg.norm(a - b, axis=axis)

    def fit(self, x, y):
        self.x = x
        self.y = y
        self.X = list(zip(x, y))
        self.centroids = self.get_centroids()

        self.old_centroids = np.zeros(self.centroids.shape)
        self.clusters = np.zeros(len(self.X), dtype=np.int32)
        self.delta = self.get_dist(self.centroids, self.old_centroids, None)

    def get_centroids(self):
        """get centroids using instance data"""
        c_x = np.random.randint(np.min(self.x), np.max(self.x), size=self.k)
        c_y = np.random.randint(np.min(self.y), np.max(self.y), size=self.k)

        return np.array(list(zip(c_x, c_y)), dtype=np.float32)

    def predict(self, x=None, y=None):
        if x is None or y is None:
            X = list(self.X)
        else:
            X = list(zip(x, y))

        run = 0
        while self.delta != 0:
            for i in range(len(X)):
                distances = self.get_dist(X[i], self.centroids)
                cluster = np.argmin(distances)
                self.clusters[i] = cluster
            self.old_centroids = deepcopy(self.centroids)

            for i in range(self.k):
                points = [X[j] for j in range(len(X)) if self.clusters[j] == i]
                self.centroids[i] = np.mean(points, axis=0)

            self.delta = self.get_dist(self.centroids, self.old_centroids, None)

            if np.isnan(self.delta):
                break

            run += 1


def create_origin(lats: list, lons: list):
    """
    Use k-means clustering to find a single origin for
    geocoded destinations.

    :lats:      list-like of clean zipcodes
    :lons:      list-like of expected country abbreviations

    :return:    dict {"latitude": float, "longitude": float}
    """

    # simplify euclidean distance calculation by projecting to positive vals
    x = np.array(lats, dtype=float) + 90
    y = np.array(lons, dtype=float) + 180

    k = 1  # desired n locations solution
    kmeans = KMeans(k)
    kmeans.fit(x, y)
    kmeans.predict()

    origin = {
        "latitude": kmeans.centroids[0][0] - 90,
        "longitude": kmeans.centroids[0][1] - 180,
    }

    return origin
