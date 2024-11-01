"""
A script for calculating values from the OntoUML model repository statistics file. This statistics file is
generated from the RepoScraper.py script.
"""

import json
import os.path

import pandas as pd

from OntoUmlModelCatalogueScraper.SupportedOntologiesPerTransformationSet import project_c_stereotype_presence
from util import recursive_dict_sum

CSV_STORAGE_LOCATION = r"analysis_stats"


def store_csv(df, name, **kwargs):
    if not name.endswith('.csv'):
        name += '.csv'
    path = os.path.join(CSV_STORAGE_LOCATION, name)
    df.to_csv(path, **kwargs)


class color:
    """
    Colors that can be used in the sys out stream (command line interface). From https://stackoverflow.com/a/60246996.
    """
    PURPLE = '\033[1;35;48m'
    CYAN = '\033[1;36;48m'
    BOLD = '\033[1;37;48m'
    BLUE = '\033[1;34;48m'
    GREEN = '\033[1;32;48m'
    YELLOW = '\033[1;33;48m'
    RED = '\033[1;31;48m'
    BLACK = '\033[1;30;48m'
    UNDERLINE = '\033[4;37;48m'
    END = '\033[1;37;0m'


def p_header(text):
    """
    Print a header line to indicate specific values in the command line output.
    :param text: Text to be printed in a specific color.
    :return: None
    """
    print(color.BLUE + text + color.END)


####### Groups of stereotypes

with open("class-stereotypes-readthedocs.txt") as f:
    stereotypes_considered_valid_readthedocs = [line.strip() for line in f]

with open("class-stereotypes-metamodel.txt") as f:
    stereotypes_considered_valid_pi_metamodel = [line.strip() for line in f]

with open("class-stereotypes-ufo-a.txt") as f:\
    stereotypes_ufo_a = [line.strip() for line in f]

################

with open("repo_stats.json") as f:
    stats: dict = json.load(f)

    total_counts = recursive_dict_sum(*stats.values())
    most_frequent_classes = dict(
        sorted(total_counts['Class'].items(), key=lambda item: (-item[1], item[0].lower()), reverse=False))

    p_header("Number of projects analysed:")
    n_projects = len(stats)
    print(n_projects)

    p_header("Average number of classes per project:")
    # INFO: In the current JSON structure, a class is limited to 1 stereotype, but this might not be the case in the
    #   future.
    print(color.YELLOW + "Warning, n_classes is based on the number of stereotypes. See in code documentation for "
                         "more info." + color.END)
    n_total_classes = sum(total_counts["Class"].values())
    print(f"{n_total_classes / n_projects:.2f}  ( calculated by {n_total_classes} / {n_projects})")

    p_header("Class stereotypes that do not appear in the repo:")
    stereotypes_not_in_repo = list(set(stereotypes_considered_valid_pi_metamodel) - set(most_frequent_classes.keys()))
    stereotypes_not_in_repo.sort(key=lambda item: item.lower())
    print(stereotypes_not_in_repo)

    p_header("Class stereotypes that do appear in the repo, but not the metamodel:")
    stereotypes_not_in_metamodel = list(set(most_frequent_classes.keys()) - set(stereotypes_considered_valid_pi_metamodel))
    stereotypes_not_in_metamodel.sort(key=lambda item: item.lower())
    print(stereotypes_not_in_metamodel)

    p_header("Most frequent Class stereotypes:")
    print(most_frequent_classes)

    p_header("Most frequent Class stereotype appearance in projects:")
    c_stereotype_occurrence_count = {}
    for ontology_stats in stats.values():
        c_stereotypes_in_ontology = ontology_stats['Class'].keys()
        for stereotype in c_stereotypes_in_ontology:
            if stereotype in c_stereotype_occurrence_count:
                c_stereotype_occurrence_count[stereotype] += 1
            else:
                c_stereotype_occurrence_count[stereotype] = 1

    c_stereotype_occurrence_count = dict(
        sorted(c_stereotype_occurrence_count.items(), key=lambda item: (-item[1], item[0].lower()), reverse=False))
    print(c_stereotype_occurrence_count)

p_header("Projects containing relator but not role: ")
print([project for project, stereotypes in project_c_stereotype_presence.items() if
       'relator' in stereotypes and 'role' not in stereotypes])

p_header("Projects containing role but not relator: ")
print([project for project, stereotypes in project_c_stereotype_presence.items() if
       'relator' not in stereotypes and 'role' in stereotypes])

p_header("Projects containing event but not situation: ")
print([project for project, stereotypes in project_c_stereotype_presence.items() if
       'situation' not in stereotypes and 'event' in stereotypes])


def get_projects_with_stereotype(stereotype, print_result=False, not_in=False):
    """
    Returns a list of projects that contain a specific class stereotype (at least once).
    :param stereotype: Class stereotype to search for.
    :param print_result: Whether to print the found project to system out
    :param not_in: If set to true, all projects in which a Class stereotype does NOT appear will be provided.
    :return: A list of projects containing a specific class stereotype
    """
    containing_projects = []
    for project, stereotypes_present in project_c_stereotype_presence.items():
        if stereotype in stereotypes_present and not not_in:
            containing_projects.append(project)
        elif stereotype not in stereotypes_present and not_in:
            containing_projects.append(project)

    if print_result:
        if not not_in:
            p_header(f"Projects that contain class stereotype '{stereotype}':")
        else:
            p_header(f"Projects that DO NOT contain class stereotype '{stereotype}':")
        print(containing_projects)
    return containing_projects


get_projects_with_stereotype("Goal", True, False)
get_projects_with_stereotype("collective", True)
get_projects_with_stereotype("quality", True)

get_projects_with_stereotype("mode", True)

# Combine data per stereotype into dataframe and write to csv
df = pd.DataFrame(index=list(most_frequent_classes.keys()))
df.insert(0, "class_stereotype_occurs_in_x_projects", pd.Series(c_stereotype_occurrence_count))
df.insert(1, "class_stereotype_total_freq", pd.Series(most_frequent_classes))

is_valid_stereotype_series_pi_metamodel = pd.Series(
    {stereotype: stereotype in stereotypes_considered_valid_readthedocs for stereotype in df.index.to_list()})
df.insert(2, "is_valid_stereotype_pi_metamodel", is_valid_stereotype_series_pi_metamodel)

is_valid_stereotype_series_readthedocs = pd.Series(
    {stereotype: stereotype in stereotypes_considered_valid_readthedocs for stereotype in df.index.to_list()})
df.insert(3, "is_valid_stereotype_readthedocs", is_valid_stereotype_series_readthedocs)

is_ufo_a_stereotype = pd.Series(
    {stereotype: stereotype in stereotypes_ufo_a for stereotype in df.index.to_list()})
df.insert(4, "is_ufo_a_stereotype", is_ufo_a_stereotype)


# CSV with all info
store_csv(df, "stereotype_statistics.csv", index_label="class_stereotype")


# Store top 10 based on project occurrence
#   Both all stereotypes and filtered on valid according to the pi metamodel and ufo-a types
df.sort_values(by="class_stereotype_occurs_in_x_projects", axis=0, ascending=False, inplace=True)
store_csv(df.head(10)['class_stereotype_occurs_in_x_projects'], 'top_10_stereotype_project_occurrence.csv',
          index_label="class_stereotype")
store_csv(df.loc[df["is_valid_stereotype_pi_metamodel"] & df['is_ufo_a_stereotype'], 'class_stereotype_occurs_in_x_projects'].head(10),
          'top_10_stereotype_project_occurrence_valid_pi_and_ufo_a.csv', index_label='class_stereotype')

# Store top 10 based on total occurrence
#   Both all stereotypes and filtered on valid according to the pi metamodel and ufo-a types
df.sort_values(by="class_stereotype_total_freq", axis=0, ascending=False, inplace=True)
store_csv(df.head(10)['class_stereotype_total_freq'], 'top_10_stereotype_total_occurrence.csv',
          index_label="class_stereotype")
store_csv(df.loc[df["is_valid_stereotype_pi_metamodel"] & df['is_ufo_a_stereotype'], 'class_stereotype_total_freq'].head(10),
          'top_10_stereotype_total_occurrence_valid_pi_and_ufo_a.csv', index_label='class_stereotype')
