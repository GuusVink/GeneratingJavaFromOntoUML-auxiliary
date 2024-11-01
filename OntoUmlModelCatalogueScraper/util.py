import logging

logger = logging.getLogger(__name__)

types_without_stereotypes = []


def recursive_dict_add(dict1, dict2):
    """
    Adds the values within a dict that have the same key. Resulting in merging the dictionaries without overwriting one
    of the values but rather summing them. Does this recursively for inner dicts.

    Note that the inner dicts should have the same depth at which the numbers are added. I.e., adding {A: {X: 5}} and
    {X: 7} will not add 5 and 7.
    :param dict1: Dictionary with either numbers or other dicts as values.
    :param dict2: Dictionary with either numbers or other dicts as values.
    :return: A dictionary with all keys from both dict1 and
    dict2 where values that have the same key and are on the same level are added together.
    """
    if type(dict1) is not dict or type(dict2) is not dict:
        return dict1 + dict2

    new_dict = dict1.copy()
    for key in dict2.keys():
        if key in dict1.keys():
            new_dict[key] = recursive_dict_add(dict1[key], dict2[key])
        else:
            new_dict[key] = dict2[key]
    return new_dict


def recursive_dict_sum(*dicts):
    """
    Adds multiple dicts together using the recursive_dict_add function.
    :param dicts: multiple dicts to be added.
    :return: One dictionary with all keys present of dicts where the values are added for the same keys.
    """
    result = {}
    for d in dicts:
        result = recursive_dict_add(result, d)
    return result


def get_contents_stereotype_frequencies(contents_list: list[dict, ...]) -> dict:
    """
    Get the frequency of stereotypes for several types within the contents of an OntoUML Package.
    This is done recursively for sub-Packages.
    :param contents_list: A list of OntoUML elements according to the OntoUML metamodel.
    :return: A dictionary with structure Type -> Stereotype -> n_occurrences
    """
    if contents_list is None:
        return {}

    stereotype_count = {}

    for element in contents_list:
        type = element["type"]
        if type == "Package":
            counts_to_add = get_contents_stereotype_frequencies(element['contents'])
            stereotype_count = recursive_dict_add(stereotype_count, counts_to_add)
            continue

        if "stereotype" not in element.keys():
            if type not in types_without_stereotypes:
                logger.warning(f"Type {type} has no stereotype field")
                types_without_stereotypes.append(type)
            continue

        stereotype = element["stereotype"]

        if type in stereotype_count.keys():
            if stereotype in stereotype_count[type]:
                stereotype_count[type][stereotype] += 1
            else:
                stereotype_count[type][stereotype] = 1
        else:
            stereotype_count[type] = {stereotype: 1}

    return stereotype_count
