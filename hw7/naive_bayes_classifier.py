import random, copy

file_name = "house-votes-84.txt"
congressmen = []
total_number_of_congressmen = 0
with open(file_name, "r") as file:
    for line in file:
        congressman = line.split(",")
        congressman[16] = congressman[16].replace("\n", "")
        congressmen.append(congressman)
        total_number_of_congressmen += 1

test_population_size = 40
number_of_runs = 20
accuracy_mean = 0

for run in range(number_of_runs):
    congressmen_copy = copy.copy(congressmen)
    test = []
    study = []
    random.shuffle(congressmen_copy)
    for i in range(test_population_size):
        test.append(congressmen_copy.pop(0))

    study = congressmen_copy

    votes_for_question_democrat = {"y": [0] * 16, "n": [0] * 16, "?": [0] * 16}
    votes_for_question_republican = {"y": [0] * 16, "n": [0] * 16, "?": [0] * 16}
    number_of_democrats = 0
    number_of_republicans = 0

    for congressman in study:
        current = {}
        if congressman[0] == "democrat":
            number_of_democrats += 1
            current = votes_for_question_democrat
        else:
            number_of_republicans += 1
            current = votes_for_question_republican
        for i in range(1, len(congressman) - 1):
            current[congressman[i]][i] += 1

    #classify

    classification = []
    for congressman in test:
        probability_democrat = 1
        for i in range(1, len(congressman) - 1):
            probability_democrat *= votes_for_question_democrat[congressman[i]][i] / number_of_democrats
        probability_democrat *= number_of_democrats / total_number_of_congressmen

        probability_republican = 1
        for i in range(1, len(congressman) - 1):
            probability_republican *= votes_for_question_republican[congressman[i]][i] / number_of_republicans
        probability_republican *= number_of_republicans / total_number_of_congressmen

        category = max(("democrat", probability_democrat), ("republican", probability_republican), key=lambda prob: prob[1])

        classification.append((congressman, category))

    accuracy = 0
    for classifee in classification:
        if classifee[0][0] == classifee[1][0]:
            accuracy += 1
    accuracy /= test_population_size
    accuracy_mean += accuracy
    print("Accuracy for run number {0} is {1}%".format(run, accuracy * 100))
accuracy_mean /= number_of_runs
print("Mean accuracy is {0}%".format(accuracy_mean*100))
