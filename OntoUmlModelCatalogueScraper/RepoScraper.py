"""\
Script to calculate stereotype occurrences within the OntoUML model repository.
Stores these statistics in a JSON file.

"""

import os
import json
import logging
from util import get_contents_stereotype_frequencies

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

logger.info("Logger initiated")

# Path to a local version of the OntoUML model catalogue
repo_path = None

if repo_path is None:
    print("Forgot to set the path to the local location of the OntoUML model catalogue!")
    exit(-1)

os.listdir(repo_path)

# Structure:    Project -> Type -> StereoType -> Count
type_stats = {}  # Dict containing the stats of each ontology project

for project in os.listdir(repo_path):
    p_path = os.path.join(repo_path, project)
    json_path = os.path.join(p_path, "ontology.json")

    if not os.path.isfile(json_path):
        logger.error(f"JSON file does not exist for project {project}")
        continue

    with open(json_path, 'r') as f:
        ontology = json.load(f)
        contents = ontology['model']['contents']

        type_stats[project] = get_contents_stereotype_frequencies(contents)


with open("repo_stats.json", "w") as f:
    json.dump(type_stats, f, indent=4)
