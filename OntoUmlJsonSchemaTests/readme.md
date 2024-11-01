# OntoUML JSON Schema tests

Code to test whether an OntoUML JSON file passes the [OntoUML JSON Schema](https://github.com/OntoUML/ontouml-schema/tree/master).

`ontouml-flower.json` contains OntoUML JSON exported from the [OntoUML Visual Paradigm plugin](https://github.com/OntoUML/ontouml-vp-plugin) (version 0.5.3).
A screenshot of this OntoUML model is included in `ontouml-flower.png`

`ontouml-schema.yaml` contains the OntoUML JSON Schema, retrieved from https://github.com/OntoUML/ontouml-schema/tree/master at 1 November 2024.

**ValidateJsonFile.py** contains code to validate a JSON file against this OntoUML JSON Schema.
At the moment, this validation fails. Indicating that the VP plugin and JSON Schema are not aligned.

At a first glance, the JSON exported from the VP plugin contains plain strings instead of language strings (for names and descriptions in the OntoUML model).
`ontouml-flower language-string-fixed.json` has adjustments made to change the plain strings into language strings. Still, the validation fails.
To see how the validation fails, the code in **ValidateJsonFile.py** can be changed to reraise the exception thrown by the validation, which nicely indicates where the validation went wrong.