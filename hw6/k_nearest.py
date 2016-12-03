import random
import math

filename = "IRIS/iris.txt"

k = int(input("Enter K: "))
plants = []
with open(filename, "r") as f:
    for line in f:
        plant = line.split(",")
        plant[4] = plant[4].replace("\n", "")
        plant[0], plant[1], plant[2], plant[3] = float(plant[0]), float(plant[1]), float(plant[2]), float(plant[3])
        plants.append(plant)

testing_population_size = 20
# choose 20 random
testing = []
random.shuffle(plants)
for _ in range(testing_population_size):
    testing.append(plants.pop())


def get_distance(plantA, plantB):
    return math.sqrt(sum([(plantA[i] - plantB[i]) ** 2 for i in range(4)]))


def get_k_nearest(plant):
    return list(map(lambda x: x[1], sorted([(get_distance(plant, pl), pl) for pl in plants], key=lambda x: x[0])))[0:k]


def classify(plant):
    k_nearest = get_k_nearest(plant)
    counts = {"Iris-setosa": 0, "Iris-versicolor": 0, "Iris-virginica": 0}
    for plant in k_nearest:
        counts[plant[4]] += 1
    return max(list(counts.keys()), key=lambda key: counts[key])


def classify_all():
    accuracy = 0
    for plant in testing:
        cl = classify(plant)
        print("Real: {0}".format(plant[4]), "Predicted: {0}".format(cl))
        if cl == plant[4]:
            accuracy += 1
    print("Accuracy: {0}%".format(100 * (accuracy/testing_population_size)))

classify_all()