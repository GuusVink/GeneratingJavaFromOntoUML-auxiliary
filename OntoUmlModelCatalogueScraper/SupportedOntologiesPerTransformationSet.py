#  Copyright (c) 2024.
import json


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

# For each project, which class stereotypes occurs in them
project_c_stereotype_presence = {project: set(stats[project]['Class'].keys()) for project in stats.keys()}


def project_stereotypes_is_subset(stereotype_set: set | list, print_result=False):
    """
    Returns a list of projects of which the stereotypes are a subset of the set provided.
    I.e., all projects containing the same or fewer stereotypes as stereotype_set.
    :param stereotype_set:
    :param print_result:
    :return:
    """
    matching_projects = []
    for project, stereotypes_present in project_c_stereotype_presence.items():
        if stereotypes_present <= set(stereotype_set):
            matching_projects.append(project)
    if print_result:
        p_header(f"Projects that contain no more than the stereotypes [{stereotype_set}]:")
        print(f"Projects found = {len(matching_projects)}, namely: ")
        print(matching_projects)
    return matching_projects

def get_sequence_of_num_supported(types_ordered: list, print_result=False):
    cumulative_supported_models = dict()
    for i in range(len(types_ordered)):
        num_supported_models = len(project_stereotypes_is_subset(types_ordered[:i + 1]))
        cumulative_supported_models[types_ordered[i]] = num_supported_models

    print(cumulative_supported_models)


top_10_occurrence_project = ['kind', 'relator', 'role', 'subkind', 'category', 'roleMixin', 'mode', 'collective',
                             'phase', 'quality']
top_10_total_occurrence = ['subkind', 'role', 'kind', 'relator', 'category', 'roleMixin', 'mode', 'phase', 'quality',
                           'collective']

get_sequence_of_num_supported(top_10_occurrence_project)
get_sequence_of_num_supported(top_10_total_occurrence)
