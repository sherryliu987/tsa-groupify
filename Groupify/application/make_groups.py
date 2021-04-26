import pandas as pd
from io import StringIO
from itertools import permutations
import numpy as np
import matplotlib.pyplot as plt
from mpld3 import fig_to_html, plugins

global csv


def make_groups(df, num_groups):
    chunk_size = int(df[df.columns[0]].count() / num_groups)
    perms = permutations(df['Name'].tolist())
    groups = []
    for c in list(perms):
        # print(c)
        group = chunkArray(c, chunk_size)
        if group in groups:
            continue
        groups.append(group)

    return groups


def chunkArray(myArray, chunk_size):
    index = 0
    array_length = len(myArray)
    tempArray = []

    while index < array_length:
        chunk = myArray[index: index + chunk_size]
        tempArray.append(chunk)
        index += chunk_size
    return frozenset(frozenset(i) for i in tempArray)


def getGroupRows(group):
    df = pd.read_csv(StringIO(csv))
    return df[df["Name"].isin(group)]


def getAvgAge(group):
    dfgroup = getGroupRows(group)
    return np.sum(dfgroup['Age'].tolist()) / len(dfgroup['Age'].tolist())


def getMaleFemaleRatio(group):
    dfgroup = getGroupRows(group)
    return (dfgroup['Gender'].tolist().count('M')) / len(dfgroup['Gender'].tolist())


def getAvgSkill(group):
    dfgroup = getGroupRows(group)
    people_list = dfgroup['Experience'].tolist()
    avg_skill = np.sum(people_list) / len(people_list)
    return avg_skill


def getRaceIndex(group):
    dfgroup = getGroupRows(group)
    percent_black = dfgroup['Race'].tolist().count('AA') / len(dfgroup['Race'].tolist())
    percent_asian = dfgroup['Race'].tolist().count('AS') / len(dfgroup['Race'].tolist())
    percent_americanind = dfgroup['Race'].tolist().count('AIAN') / len(
        dfgroup['Race'].tolist())
    percent_white = dfgroup['Race'].tolist().count('WH') / len(dfgroup['Race'].tolist())
    percent_nathaw = dfgroup['Race'].tolist().count('NHPI') / len(
        dfgroup['Race'].tolist())

    return [percent_black, percent_asian, percent_americanind, percent_white, percent_nathaw]


def get_population_values(dfpop):
    return [getRaceIndex(dfpop['Name']), getAvgAge(dfpop['Name']),
            getMaleFemaleRatio(dfpop['Name']), getAvgSkill(dfpop['Name'])]


def compute_groups(csv_string, num_groups):
    global csv
    csv = csv_string

    df = pd.read_csv(StringIO(csv))
    print(df)

    population_values = get_population_values(df)
    for v in population_values[0]:
        population_values = np.append(population_values, v)
    population_values = np.delete(population_values, 0)

    groups_list = list(make_groups(df, int(num_groups)))

    new_groups_list = []
    for group in groups_list:
        new_groups_list.append(list(group))
    groups_list = new_groups_list

    # list(list(groups_list[0])[0])  # does this do anything?

    print(groups_list)

    group_value_list = []
    for i in groups_list:
        group_values = [0, 0, 0, 0, 0, 0, 0, 0]
        for x in i:
            group_values = get_population_values(getGroupRows(list(x)))
            for v in group_values[0]:
                group_values = np.append(group_values, v)
            group_values = np.delete(group_values, 0)
        group_value_list.append(group_values)

    print(group_value_list)
    print("POPULATION", population_values)
    best = float('inf')
    best_group = []

    print("num possible: ", len(groups_list))
    print("GROUP VALUE LIST")
    print(group_value_list)

    for i in range(len(group_value_list)):
        the_sum = 0
        for x in range(8):
            the_sum += (abs(population_values[x] - group_value_list[i][x]))
        print("sum: ", the_sum)
        if the_sum < best:
            print("found new best!")
            best = the_sum
            best_group = groups_list[i]

    final_groups = []
    idx = 1
    for g in best_group:
        team = {"id": idx, "people": list(g)}
        final_groups.append(team)
        idx += 1
    return final_groups


def generate_graphs():
    df = pd.read_csv(StringIO(csv))

    fig, ((race, gender), (age, exp)) = plt.subplots(2, 2)

    race_labels = "Asian", "Black or African American", "White", " American Indian or Alaska Native", "Native Hawaiian or Other Pacific Islander"
    race.pie(x=pie_plot(df, "Race", ["AS", "AA", "WH", "AIAN", "NHPI"]), labels=race_labels)
    race.set_title("Race")
    gender.pie(x=pie_plot(df, "Gender", ["M", "F", "O"]), labels=["Male", "Female", "Nonbinary/Other"])
    gender.set_title("Gender")
    age.boxplot(df["Age"])
    age.set_title("Age")
    exp.hist(df["Experience"])
    exp.set_title("Experience")

    return fig_to_html(fig)


def pie_plot(df, var, possible):
    areas = []
    for p in possible:
        areas = np.append(areas, sum(df[var] == p))
    print(areas)
    return areas