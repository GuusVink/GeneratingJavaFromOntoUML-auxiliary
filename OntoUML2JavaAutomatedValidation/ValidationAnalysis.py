#  Copyright (c) 2024.
import pandas as pd
import re

WARNING_GENERALISATION_SET = "Contains GeneralizationSet"
WARNING_PROPERTY_WITHOUT_TYPE = "Contains property without type"
WARNING_EMPTY_STRING = "Contains empty string"

COMPILE_ERROR_MULTIPLE_INHERITENCE = "Multiple class inheritance present"
COMPILE_ERROR_VARIABLE_ALREADY_DEFINED = "Duplicate variable definition"
COMPILE_ERROR_CANNOT_OVERRIDE_FROM_SUPER = "Cannot override from super"
COMPILE_ERROR_RESERVED_KEYWORD_NAME = "Reserved keyword name"
NON_RESOLVED_COMPILE_ERROR_CATEGORY = 'Could not extract'

java_name_regex = r"[a-zA-Z_$][a-zA-Z_$0-9]*"

pd.options.mode.copy_on_write = True


def extract_compile_error(error_str: str):
    """
    From the stdout of a Java build task, use regex to identify different categories of compilation errors.
    :param error_str: String of the console output of a failed Java build.
    :return: A 2-tuple of an error category and detail field with the corresponding class/variable name(s)
    """

    # Multiple inheritence
    if match := re.compile(f"public class ({java_name_regex}) extends {java_name_regex}, {java_name_regex}").search(error_str):
        return (COMPILE_ERROR_MULTIPLE_INHERITENCE, match.group(1))
    # Variable already defined
    if match := re.compile(f"error: (variable|method) ({java_name_regex})(\\(\\))? is already defined in {java_name_regex} ({java_name_regex})").search(error_str):
        return (COMPILE_ERROR_VARIABLE_ALREADY_DEFINED, f"variable {match.group(2)} in {match.group(4)}")
    # Usage of reserved name
    if match := re.compile("(" + java_name_regex + r")\.java.{0,10} error: <identifier> expected").search(error_str):
        return (COMPILE_ERROR_RESERVED_KEYWORD_NAME, match.group(1))
    # Cannot override
    if match := re.compile(f"error: ({java_name_regex})(\\(\\))? in ({java_name_regex}) cannot override {java_name_regex}(\\(\\))? in ({java_name_regex})").search(error_str):
        return COMPILE_ERROR_CANNOT_OVERRIDE_FROM_SUPER, f"attribute {match.group(1)} in classes {match.group(3)} and {match.group(5)}"
    return (NON_RESOLVED_COMPILE_ERROR_CATEGORY, None)


def analyse_fault_modes(file_path, print_ontologies_with_warning_or_error=None):
    """
    For a csv file with the results of the executed automated validation, extracts the fault modes.
    Including the type of ATL warnings and the category of compilation error.

    For projects that do not yield valid Java code, a separate CSV is created that contains these compilation
    error categories.

    :param file_path: location of CSV file with the results of the automated performed validation.
    :param print_ontologies_with_warning_or_error: For a specific ATL warning or Compile error category, list the models
    that contain such a warning/error. (I.e., one of the constants defined at the top of this file.
    :return:
    """
    df: pd.DataFrame = pd.read_csv(file_path, index_col=0)
    df['atl_warnings_present'] = None

    not_compiled = df[df['transformation_successful'] & ~df['generated_code_compiles']]

    print(f"Fault mode analysis for {file_path}")
    print(f"{len(not_compiled)} models yield code that is not compilable")

    not_compiled['compile_error_category'] = None
    not_compiled['compile_error_category_detail'] = None

    ATL_warnings_occurrence = {
        WARNING_GENERALISATION_SET: [],
        WARNING_PROPERTY_WITHOUT_TYPE: [],
        WARNING_EMPTY_STRING: []
    }

    compile_error_categories_occurences = {
        COMPILE_ERROR_CANNOT_OVERRIDE_FROM_SUPER: [],
        COMPILE_ERROR_RESERVED_KEYWORD_NAME: [],
        COMPILE_ERROR_VARIABLE_ALREADY_DEFINED: [],
        COMPILE_ERROR_MULTIPLE_INHERITENCE: [],
        NON_RESOLVED_COMPILE_ERROR_CATEGORY: []
    }

    for index, row in df.iterrows():
        # ATL Warnings
        warnings_str = row['atl_warnings']
        model_name = row['model']
        if isinstance(warnings_str, str):
            new_warning_str = '' # With unique warnings
            if "Warning: OntoUML model contains GeneralizationSets" in warnings_str:
                ATL_warnings_occurrence[WARNING_GENERALISATION_SET].append(model_name)
                new_warning_str += WARNING_GENERALISATION_SET + ', '
            if "Warning: Property without type found in OntoUML model" in warnings_str:
                ATL_warnings_occurrence[WARNING_PROPERTY_WITHOUT_TYPE].append(model_name)
                new_warning_str += WARNING_PROPERTY_WITHOUT_TYPE + ', '
            if "Warning: Empty string found" in warnings_str:
                ATL_warnings_occurrence[WARNING_EMPTY_STRING].append(model_name)
                new_warning_str += WARNING_EMPTY_STRING + ', '

            if new_warning_str.endswith(', '):
                # I.e., contains warning
                df.loc[index, 'atl_warnings_present'] = new_warning_str[:-2] # and remove last comma
                if index in not_compiled.index:
                    not_compiled.loc[index, 'atl_warnings_present'] = new_warning_str[:-2]  # and remove last comma

        # Compilation errors
        compile_error_string = row['compilation_errors']

        if isinstance(compile_error_string, str): # so not empty or none
            compile_error_category, compile_error_details = extract_compile_error(compile_error_string)
            compile_error_categories_occurences[compile_error_category].append(model_name)
            not_compiled.loc[index, 'compile_error_category'] = compile_error_category
            not_compiled.loc[index, 'compile_error_category_detail'] = compile_error_details

    print("ATL Warnings present in all projects:")
    print({k: len(v) for k, v in ATL_warnings_occurrence.items()})

    print("Compile error categories for failed projects")
    print(dict(map(lambda kv: (kv[0], len(kv[1])), compile_error_categories_occurences.items())))

    if print_ontologies_with_warning_or_error:
        print(f"\nOntologies with warning/error {print_ontologies_with_warning_or_error}")
        if print_ontologies_with_warning_or_error in ATL_warnings_occurrence:
            print(ATL_warnings_occurrence[print_ontologies_with_warning_or_error])
        elif print_ontologies_with_warning_or_error in compile_error_categories_occurences:
            print(compile_error_categories_occurences[print_ontologies_with_warning_or_error])

    not_compiled.to_csv(file_path[:-4] + ' fault modes analysed.csv')
    df.to_csv(file_path)
    print("\n\n\n")


def analyse_csv(file_path):
    """
    Prints some stats for a CSV file containing the results of the automated performed validation.
    :param file_path: location of CSV file with the results of the automated performed validation.
    :return:
    """
    df: pd.DataFrame = pd.read_csv(file_path, index_col=0)
    print(f"Analysis for {file_path}")
    n_successful_transformation = df['transformation_successful'].sum()
    print(f"Successful transformation = {n_successful_transformation}")

    n_compiled_successful = (df['generated_code_compiles'] & df['transformation_successful']).sum()
    print(f"Successful compilation = {n_compiled_successful}")

    completed_transformations = df[df['transformation_successful']]
    avg_time = completed_transformations['transformation_time_s'].mean()
    print(f"Average time of completed transformations = {avg_time:.2f} s")
    print(f"  Per step:   read OntoUML = {completed_transformations['read_ontouml_time_s'].mean()}s, ATL Time = {pd.to_numeric(completed_transformations['atl_time_s']).mean()}s, acceleo time = {pd.to_numeric(completed_transformations['acceleo_time_s']).mean()}")

    failed_at_atl_or_before = df[df['transformation_failed_at_stage'].isin(['read_ontouml', 'im_2_java'])]
    print(f"Nr of transformations failed at ATL or before = {len(failed_at_atl_or_before)}")
    print("\n\n\n")


if __name__ == '__main__':
    analyse_csv(r'automated_validation_results.csv')
    analyse_fault_modes(r'automated_validation_results.csv')



