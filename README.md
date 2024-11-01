# GeneratingJavaFromOntoUML - Auxiliary scripts

This repository contains Python scripts used in the Master's thesis 'Generating Java from OntoUML'.
The scripts are separated in four folders, each with a readme file containing further information.

### Setup
- Requires Python 3.12 (or newer)
- Package requirements are included in `requirements.txt` (i.e. `pip install -r requirements.txt`)

## Summary of the different folders

- [**OntoUmlModelCatalogueScraper**](OntoUmlModelCatalogueScraper/readme.md) contains scripts to analyse the occurrence of stereotypes for models in the OntoUML model catalogue.
- [**OntoUML2JavaTransformationExecution**](OntoUML2JavaTransformationExecution/readme.md) contains scripts to execute the OntoUML2Java transformation (developed with EMF) using ANT tasks.
- [**OntoUML2JavaAutomatedValidation**](OntoUML2JavaAutomatedValidation/readme.md) contains scripts to execute the OntoUML2Java transformation for models from the OntoUML model catalogue and to gather and analyse the results.
- [**OntoUmlJsonSchemaTests**](OntoUmlJsonSchemaTests/readme.md) contains an OntoUML JSON file generated with the Visual Paradigm and the OntoUML JSON Schema, as well as a script to test whether the JSON file adheres to the Schema.
