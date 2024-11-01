"""
A script for calculating values from the OntoUML model repository statistics file. This statistics file is
generated from the RepoScraper.py script.
"""

import json
import os.path

import pandas as pd
from util import recursive_dict_sum

CSV_STORAGE_LOCATION = r"csv_files"


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


with open("repo_stats.json") as f:
    stats: dict = json.load(f)

    for key, val in stats.items():
        if 'Relation' not in val:
            val['Relation'] = {}

    total_counts = recursive_dict_sum(*stats.values())
    most_frequent_relations = dict(
        sorted(total_counts['Relation'].items(), key=lambda item: (-item[1], item[0].lower()), reverse=False))

    p_header("Number of projects analysed:")
    n_projects = len(stats)
    print(n_projects)

    p_header("Most frequent Relation stereotypes:")
    print(most_frequent_relations)

    p_header("Most frequent Relation stereotype appearance in projects:")
    r_stereotype_occurrence_count = {}
    for ontology_stats in stats.values():
        r_stereotypes_in_ontology = ontology_stats['Relation'].keys()
        for stereotype in r_stereotypes_in_ontology:
            if stereotype in r_stereotype_occurrence_count:
                r_stereotype_occurrence_count[stereotype] += 1
            else:
                r_stereotype_occurrence_count[stereotype] = 1

    c_stereotype_occurrence_count = dict(
        sorted(r_stereotype_occurrence_count.items(), key=lambda item: (-item[1], item[0].lower()), reverse=False))
    print(c_stereotype_occurrence_count)


# For each project, which relation stereotypes occurs in them
project_r_stereotype_presence = {project: set(stats[project]['Relation'].keys()) for project in stats.keys()}


def get_projects_with_stereotype(stereotype, print_result=False, not_in=False):
    """
    Returns a list of projects that contain a specific class stereotype (at least once).
    :param stereotype: Class stereotype to search for.
    :param print_result: Whether to print the found project to system out
    :param not_in: If set to true, all projects in which a Class stereotype does NOT appear will be provided.
    :return: A list of projects containing a specific class stereotype
    """
    containing_projects = []
    for project, stereotypes_present in project_r_stereotype_presence.items():
        if stereotype in stereotypes_present and not not_in:
            containing_projects.append(project)
        elif stereotype not in stereotypes_present and not_in:
            containing_projects.append(project)

    if print_result:
        if not not_in:
            p_header(f"Projects that contain relation stereotype '{stereotype}':")
        else:
            p_header(f"Projects that DO NOT contain relation stereotype '{stereotype}':")
        print(containing_projects)
    return containing_projects


get_projects_with_stereotype("derivation", True, False)
