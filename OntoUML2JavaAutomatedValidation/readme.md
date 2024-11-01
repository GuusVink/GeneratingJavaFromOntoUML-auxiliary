# OntoUML2Java Automated validation

Scripts to perform the automated validation of the OntoUML2Java transformation and to analyse the results.
Requires the OntoUML2Java transformation provided in [OntoUML2JavaTransformationExecution](../OntoUML2JavaTransformationExecution) to be working.



## Summary of the scripts

### modelJsons-relationStereotypesRenamed
Folder containing the 82 models used
for the automated validation.
Two changes have been made to the models in this folder:
1. The name of the Project (i.e., the top level element) is renamed to match the name of the ontology (i.e., the same name as the JSON file in this case)
2. The relation stereotype 'Formal' is renamed to 'formal'

### automated_validation_results.csv
Results from running the automated validation on the 


### AutomatedValidation.py
Script to perform the automated validation using the OntoUML2JavaTransformation execution.
Yields a CSV files (like [automated_validation_results.csv](automated_validation_results.csv)) with the results of the validation.


### ChangeModelProjectName.py
Script used to change the Project elements in the JSON file to match the name of the ontology.

### ExportForLatex.py
Script to select the relevant data to be included in the created report.

### TimePlot.py
Script used to plot the information on the execution times of the transformation.

### ValidationAnalysis.py
Script to analyse the results of the performed validation.
