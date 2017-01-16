import random
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

file_name = input("Enter absolute file name: ")
k = int(input("Enter value for k: "))
f = open(file_name, "r")
dataset = []
for line in f:
    x, y = line.replace("\n", "").replace("\t", " ").split(" ")
    dataset.append((float(x), float(y)))

clusters = []
means = []

# initialize with random means
def initialize_means():
    dataset_copy = dataset[:]
    random.shuffle(dataset_copy)
    means = dataset_copy[0:k]
    return means


def distance(point_a, point_b):
    if len(point_b) == 0:
        return float('inf')
    return math.sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2)


def find_closest_mean(point, means):
    # the index of the closest mean
    mean = min(means, key=lambda m: distance(point, m))
    return means.index(mean)


def assign_points_to_clusters(dataset, means):
    clusters = [[] for _ in range(k)]
    for point in dataset:
        idx = find_closest_mean(point, means)
        clusters[idx].append(point)
    return clusters


def update(clusters):
    means = []
    for cluster in clusters:
        points_in_cluster = len(cluster)
        mean = [sum(x) / points_in_cluster for x in zip(*cluster)]
        means.append(mean)
    return means


def k_means(dataset):
    means = initialize_means()
    clusters = assign_points_to_clusters(dataset, means)
    while True:
        means_new = update(clusters)
        if means == means_new:
            return clusters
        means = means_new
        clusters.clear()
        clusters = assign_points_to_clusters(dataset, means)

clusters = k_means(dataset)
for i in range(len(clusters)):
    print("Points in cluster {0}: ".format(i))
    print(clusters[i])
colors = iter(cm.rainbow(np.linspace(0, 1, len(clusters))))

for cluster in clusters:
    plt.scatter(*zip(*cluster), color=next(colors))
title = "k = {0}".format(k)
plt.title(title)
plt.show()

