import math
import random

file_name = "breast-cancer.arff"

class Node:
    def __init__(self, attribute_name):
        self.attribute_name = attribute_name
        self.edge_values = []
        self.neighbours = []
        self.prediction = ""

    def add_neighbour(self, neighbour, edge_value):
        self.neighbours.append(neighbour)
        self.edge_values.append(edge_value)

    def set_prediction(self, prediction):
        self.prediction = prediction

    def is_leaf(self):
        return self.attribute_name == "leaf"


file = open(file_name, "r")

individuals = []

for line in file:
    if line[0] != "%" and line[0] != "@":
        line = line.replace("'", "").replace("\n", "")
        line_split = line.split(",")
        individuals.append(line_split)


attribute_names = ['age', 'menopause', 'tumor-size', 'inv-nodes', 'node-caps', 'deg-malig', 'breast', 'breast-quad', 'irradiat', 'Class']

def count_individuals(examples):
    classes = {'age': {}, 'menopause': {}, 'tumor-size': {}, 'inv-nodes': {}, 'node-caps': {}, 'deg-malig': {},
               'breast': {}, 'breast-quad': {}, 'irradiat': {}, 'Class': {}}

    for individual in examples:
        for index, attribute in enumerate(individual):
            class_name = attribute_names[index]
            if attribute in classes[class_name]:
                classes[class_name][attribute] += 1
            else:
                classes[class_name][attribute] = 1
    return classes




def entropy(examples, target_attribute):
    number_of_examples = len(examples)
    counts = count_individuals(examples)[target_attribute]
    result = 0
    for key, value in counts.items():
        probabilty = value / number_of_examples
        result += probabilty * math.log2(probabilty)
    result *= -1
    return result


def split_by_attribute(examples, attribute):
    splitted = {}
    attribute_index = attribute_names.index(attribute)

    for eg in examples:
        cls = eg[attribute_index]
        if cls in splitted:
            splitted[cls].append(eg)
        else:
            splitted[cls] = [eg]
    return splitted


def info_gain(examples, attribute, target_attribute):
    number_of_examples = len(examples)
    splitted = split_by_attribute(examples, attribute)
    result = 0
    for key, value in splitted.items():
        result += len(value) * entropy(value, target_attribute)
    result /= number_of_examples

    return entropy(examples, target_attribute) - result


def id3(examples, target_attribute, attributes):
    counted = count_individuals(examples)
    target_attribute_counts = counted[target_attribute]
    for key, value in target_attribute_counts.items():
        if value == len(examples):
            # All Di have equal classes
            leaf_node = Node("leaf")
            leaf_node.set_prediction(key)
            return leaf_node
    if len(attributes) == 0:
        # there are no more attributes
        most_popular = max(target_attribute_counts.keys(), key=lambda k: target_attribute_counts[k])
        leaf_node = Node("leaf")
        leaf_node.set_prediction(most_popular)
        return leaf_node

    best_attribute = max(attributes, key=lambda attr: info_gain(examples, attr, target_attribute))
    node = Node(best_attribute)
    attributes_copy = attributes[:]
    attributes_copy.remove(best_attribute)
    for key, value in counted[best_attribute].items():
        examples_new = []
        idx = attribute_names.index(best_attribute)
        for eg in examples:
            if eg[idx] == key:
                examples_new.append(eg)

        node.add_neighbour(id3(examples_new, target_attribute, attributes_copy), key)
    return node


def predict(root_node, individual):
    if root_node.is_leaf():
        return root_node.prediction

    root_attr = root_node.attribute_name
    idx = attribute_names.index(root_attr)
    attr_value = individual[idx]
    prediction = ""
    for index, edge_value in enumerate(root_node.edge_values):
        if edge_value == attr_value:
            prediction = predict(root_node.neighbours[index], individual)
            break

    return prediction

def test(number_of_runs):
    for target in attribute_names:
        mean_accuracy = 0
        for _ in range(number_of_runs):
            size_train_set = int(0.8*len(individuals))
            individuals_copy = individuals[:]
            train = []
            random.shuffle(individuals_copy)
            for i in range(size_train_set):
                train.append(individuals_copy.pop(0))

            test = individuals_copy
            attribute_names_copy = attribute_names[:]
            attribute_names_copy.remove(target)
            attribute_index = attribute_names.index(target)

            node = id3(train, target, attribute_names_copy)

            accuracy = 0
            counted = count_individuals(train)[target]
            most_popular = max(counted.keys(), key=lambda k: counted[k])

            for individual in test:
                prediction = predict(node, individual)
                if prediction == "":
                    prediction = most_popular
                if prediction == individual[attribute_index]:
                    accuracy += 1
            accuracy /= len(test)
            mean_accuracy += accuracy
        mean_accuracy /= number_of_runs
        print("Mean accuracy for {0} number of runs, predicting attribute: '{1}'  is {2}".format(number_of_runs, target, mean_accuracy))

test(10)









