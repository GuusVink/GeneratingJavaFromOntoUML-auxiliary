#  Copyright (c) 2024.
from TransformationExecutor import TransformationExecutor


# Create a transformation executor
#   - provide a path of the OntoUML json to be transformed
#   - provide the project folder where the code should be generated ('None' indicates the code will be generated in
#       the Eclipse workspace)
#   - Indicate whether the generated code should be tested by means of compiling it. Requires the
#       java_generation_location to contain an ANT build file.
transformation_executor = TransformationExecutor('project-management-ontology.json', java_generation_location=None,
                                                 test_generated_code=True)

# run the transformation
transformation_executor.execute_entire_transformation_chain()

# If desired, retrieve the results of the transformation
results = transformation_executor.finalize_and_get_results()
print(results)
