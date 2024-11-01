import yaml, json

from jsonschema import validate

with open('ontouml-schema.yaml') as onto_schema, open('ontouml-flower.json') as flower_json, open('ontouml-flower language-string-fixed.json') as flower_language_string_fixed:
    ontouml_schema = yaml.safe_load(onto_schema)

    # Raises exception in case json does not validate
    try:
        ontouml_flower = json.load(flower_json)
        validate(instance=ontouml_flower, schema=ontouml_schema)
        print("Passed for json exported from VP!")
    except Exception as e:
        print("Failed for json exported from VP:")
        # raise e  # uncomment to see the cause of the validation failure

    try:
        # JSON file in which strings were transformed into the expected language strings
        ontouml_flower_language_string_fixed = json.load(flower_language_string_fixed)
        validate(instance=ontouml_flower_language_string_fixed, schema=ontouml_schema)
        print("Passed for json adjusted to fix language strings!")
    except Exception as e:
        print("Failed for json adjusted to fix language strings:")
        # raise e  # uncomment to see the cause of the validation failure
