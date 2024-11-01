#  Copyright (c) 2024.
import datetime
import json
import os
import pandas as pd

from OntoUML2JavaTransformationExecution.TransformationExecutor import TransformationExecutor


if __name__ == '__main__':

    # Get the number of classes per model
    with open('../OntoUmlModelCatalogueScraper/repo_stats.json') as f:
        stats: dict = json.load(f)
        num_classes_per_ontology = {model_name: sum(stat['Class'].values()) for model_name, stat in stats.items()}


    folder_with_ontologies = 'modelJsons-relationStereotypesRenamed'
    models_to_transform = os.listdir(folder_with_ontologies)

    # To test the automated validation for a smaller subset of models.
    # models_to_transform = ['buridan-ontology2021.json']

    count_transformed = 0

    transformation_results = []
    exceptions = []

    for json_file in models_to_transform:
        try:
            full_path = os.path.abspath(os.path.join(folder_with_ontologies, json_file))

            # Initialize Tranformation chain object
            transformation_executor = TransformationExecutor(full_path, test_generated_code=True)
            transformation_executor.execute_entire_transformation_chain()

            # Get the results of the transformation
            transformation_result_dict = transformation_executor.finalize_and_get_results()

            # Add the number of classes to the results
            model_name = transformation_result_dict['model']
            transformation_result_dict['n_classes'] = num_classes_per_ontology[model_name]

            transformation_results.append(transformation_result_dict)

            count_transformed += 1

        except Exception as e:
            print(e)
            exceptions.append(json_file)

    print(f"Done with {count_transformed} models")
    print(f"Exceptions for models {exceptions}")

    df: pd.DataFrame = pd.DataFrame(transformation_results)
    current_date_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    df.to_csv(f'results/transformation_results {current_date_time} test run.csv')