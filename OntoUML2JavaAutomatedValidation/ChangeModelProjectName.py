#  Copyright (c) 2024.
import os
import json
from pathlib import Path

""""
Script to change the name of the OntoUML Project to the name of the JSON file.
Done for convenience to distinguish the generated Java projects.
"""
for json_file in os.listdir('modelJsons-original'):
    with open(os.path.join('modelJsons-original', json_file)) as f_in, open(os.path.join('modelJsons', json_file), 'w') as f_out:
        loaded = json.load(f_in)
        loaded['name'] = Path(json_file).stem
        json.dump(loaded, f_out, indent=2)

