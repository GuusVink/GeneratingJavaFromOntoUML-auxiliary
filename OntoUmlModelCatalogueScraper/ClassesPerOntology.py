"""
Get the total number of classes present per OntoUML model.

"""
import json


with open('repo_stats.json') as f:
    stats: dict = json.load(f)

    total_number_of_classes = {model_name: sum(stat['Class'].values()) for model_name, stat in stats.items()}

    print(total_number_of_classes)
