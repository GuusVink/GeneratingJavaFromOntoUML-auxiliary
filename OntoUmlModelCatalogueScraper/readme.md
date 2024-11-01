# OntoUML Model Catalogue scraper

Scripts to gather information from OntoUML models in the [OntoUML model catalogue](https://github.com/OntoUML/ontouml-models?tab=readme-ov-file).
Requires the model catalogue to be locally present on the PC (and the path to this folder to be set in the code).


1. **ExtractJSONs.py** Gathers all OntoUML JSON files from the catalogue and stores them in **modelJsons**
2. **RepoScraper.py** Counts the class/relation stereotypes present in each project and stores this in **repo_stats.json**

The following four scripts contain code to analyse these repo stats:

- **ClassAnalysis.py** Calculates statistics on the class stereotypes. Prints this information and stores in **analysis_stats** as csv files
- **ClassesPerOntology.py** Prints the number of classes in each OntoUML model.
- **RelationAnalysis.py** Similar to ClassAnalysis.py, but less extensive and for relation instead of class stereotypes.
- **SupportedOntologiesPerTransformation.py** Derives the OntoUML models which contain a subset of class stereotypes given by a selection of stereotypes. Or in other words, for a selection of class stereotypes supported by a transformation, derive the OntoUML models that could be transformed.


### Other files

**class-stereotypes-\*.txt** contain several selections of stereotypes, such as those that are present in the [platform-independent metamodel](https://github.com/OntoUML/ontouml-metamodel).

**util.py** Utility functions used by some of the analysis scripts.
**tests** Some test cases for these utility functions