#  Copyright (c) 2024.
import re
import subprocess
import os
from pathlib import Path
from dotenv import load_dotenv

from OntoUML2JavaTransformationExecution.TransformationResult import TransformationExecResult
from OntoUML2JavaTransformationExecution.TransformationStage import TransformationStage


class TransformationExecutor:
    """
    Class that executes an OntoUML2Java transformation.
    Requires the OntoUML-Java-Generation eclipse project to be available.
    """

    # Path to the Eclipse workspace that contains the OntoUML2Java transformation projects
    #   If set to None, path will be retrieved from the environment variable ECLIPSE_ONTOUML_2_JAVA_WORKSPACE
    ECLIPSE_WORKSPACE_PATH = None

    ECORE_MODEL_PROJECT = "nl.guusgrievink.emf.ontouml.model"
    ATL_PROJECT = r"nl.guusgrievink.atl.OntoUML2ImplementationModel"
    ACCELEO_PROJECT = r"nl.guusgrievink.ontouml.implementationmodel.gen.java"

    GENERATED_CODE_PROJECT = r"TestCodeGeneration"

    def __init__(self, ontouml_json_path, java_generation_location=None, test_generated_code=False):
        """
        Initializes an OntoUML2Java transformation executor.

        :param ontouml_json_path: OntoUML JSON file location of model to be used.
        :param java_generation_location: Where the code should be generated. If None, will generate code in the used Eclipse
            workspace 'TestCodeGeneration' project. Default is None.
        :param test_generated_code: Whether to compile the generated code. Requires an ANT Build file to be present
            in the generated code location (which is present in the Eclipse workspace
        """
        self.__set_eclipse_workspace_path()

        self.ecore_model_project_path = os.path.join(self.ECLIPSE_WORKSPACE_PATH, self.ECORE_MODEL_PROJECT)
        self.atl_project_path = os.path.join(self.ECLIPSE_WORKSPACE_PATH, self.ATL_PROJECT)

        if java_generation_location is None:
            self.code_generation_project_path = os.path.join(self.ECLIPSE_WORKSPACE_PATH, self.GENERATED_CODE_PROJECT)
        else:
            self.code_generation_project_path = java_generation_location

        self.test_generated_code = test_generated_code

        self.ontoUML_json_path = os.path.abspath(ontouml_json_path)
        self.model_name = Path(ontouml_json_path).stem

        self.model_xmi_path = None

        self.relative_output_uml_path = None
        self.absolute_output_uml_path = None

        self.transformation_result = TransformationExecResult(self.model_name)
        self.transformation_failed = False

    def __set_eclipse_workspace_path(self):
        """
        Sets the path to the Eclipse project containing the EMF OntoUML2Java project.
        Expected to be either included in the source code of this class, or as an environment variable.
        """
        if self.ECLIPSE_WORKSPACE_PATH is None:
            load_dotenv()
            self.ECLIPSE_WORKSPACE_PATH = os.getenv("ECLIPSE_ONTOUML_2_JAVA_WORKSPACE")

        if self.ECLIPSE_WORKSPACE_PATH is None:
            raise ValueError("The path of the Eclipse OntoUML2Java workspace has not been set in either the code or "
                             "as an environment variable.")

    def __handle_result(self, result):
        if result.returncode != 0:
            self.transformation_failed = True
        return result.returncode

    def __ontouml_json_2_ontouml_ecore(self):
        """
        First step in the transformation: Read an OntoUML JSON into an EMF compatible XMI adhering to the OntoUML
        Ecore metamodel.
        :return: return code of the executed step.
        """
        # Path where the XMI model will be stored
        self.model_xmi_path = os.path.join(self.ecore_model_project_path, 'generated-models', 'model-repo', self.model_name + ".xmi")

        print(f"** Starting OntoUML JSON reading for {self.model_name}...")
        ant_prop_jsonPath = f"-DjsonPath={self.ontoUML_json_path}"
        ant_prop_outputXmiPath = f"-DoutputXmiPath={self.model_xmi_path}"

        self.transformation_result.mark_start_time()
        resultReadJson = subprocess.run(["ant", ant_prop_jsonPath, ant_prop_outputXmiPath, "convertFromModelRepo"],
                                        cwd=self.ecore_model_project_path, shell=True, stdout=subprocess.PIPE,
                                        encoding='utf-8')
        self.transformation_result.mark_end_time(TransformationStage.READ_ONTOUML)
        self.transformation_result.interpret_ontouml_read_result(resultReadJson)
        return self.__handle_result(resultReadJson)

    def __onto_uml_ecore_2_implementation_model(self):
        """
        Second step in the transformation. Call the ATL OntoUML to Implementation model transformation.
        :return: return code of the executed step.
        """
        self.relative_output_uml_path = os.path.join("generated-models", "model-repo", self.model_name + ".uml")
        self.absolute_output_uml_path = os.path.join(self.atl_project_path, self.relative_output_uml_path)

        print(f"** Starting ATL transformation for {self.model_name}...")
        if self.transformation_failed:
            print("Not performing ATL transformation as previous step failed")
            return -1


        ant_prop_targetPath = f"-DtargetPath={self.relative_output_uml_path}"

        # The path of the OntoUML XMI model. The ATL plugin interprets something before a ':' to be the protocol to be
        # used for reading a model. However, our path starts with 'C://...' (or any other letter) which indicates the
        # disk. Therefore, remove everything up till the colon before handing over to ATL.
        model_xmi_path_without_disk = re.sub(r'^.+:', '', self.model_xmi_path)
        ant_prop_sourcePath = f"-DsourcePath={model_xmi_path_without_disk}"

        self.transformation_result.mark_start_time()
        resultATLTransformation = subprocess.run(
            ["ant", ant_prop_sourcePath, ant_prop_targetPath, "OntoUML2ImplementationModel"], shell=True,
            cwd=self.atl_project_path, stdout=subprocess.PIPE, encoding='utf-8')
        self.transformation_result.mark_end_time(TransformationStage.ATL)
        self.transformation_result.interpret_atl_result(resultATLTransformation)
        return self.__handle_result(resultATLTransformation)

    def __implementation_model_2_java(self):
        """
        Third step in the transformation. Use the Acceleo project to generate Java code from the implementation model.
        :return: return code of the executed step.
        """
        print(f"** Starting Acceleo generation for {self.model_name}...")
        if self.transformation_failed:
            print("Not performing Acceleo transformation as previous step failed")
            return -1

        self._clear_generated_code_source()

        uml2java_project_path = os.path.join(self.ECLIPSE_WORKSPACE_PATH, TransformationExecutor.ACCELEO_PROJECT)

        ant_prop_sourceModel = f"-DsourceModel={self.absolute_output_uml_path}"
        # Generate code in source folder
        ant_prop_targetFolder = f"-DtargetFolder={os.path.join(self.code_generation_project_path, 'src')}"

        self.transformation_result.mark_start_time()
        resultAcceleo = subprocess.run(['ant', ant_prop_sourceModel, ant_prop_targetFolder, "Uml2java"], shell=True,
                                       cwd=uml2java_project_path, stdout=subprocess.PIPE, encoding='utf-8')
        self.transformation_result.mark_end_time(TransformationStage.ACCELEO)
        self.transformation_result.interpret_acceleo_result(resultAcceleo)
        return self.__handle_result(resultAcceleo)

    def _clear_generated_code_source(self):
        """
        Call the ANT task to clear the folder in which the code will be generated.
        Useful in case multiple models are tested in sequence.
        :return:
        """
        print("Remove source files from other projects")
        subprocess.run(['ant', 'clear-source-files'], shell=True, encoding='utf-8',
                       cwd=self.code_generation_project_path)

    def __compile_check_generated_code(self):
        """
        Validation step. Try to compile the generated Java code.
        :return: return code of the compilation.
        """
        print("** Compiling generated code")
        if self.transformation_failed:
            print("Not performing Compilation check as previous step failed")
            return -1

        # Clean project
        subprocess.run(['ant', 'clean'], shell=True, cwd=self.code_generation_project_path)

        # Compile and get result
        compile_result = subprocess.run(['ant', 'build-project'], shell=True, cwd=self.code_generation_project_path,
                                        stdout=subprocess.PIPE, encoding='utf-8')
        self.transformation_result.interpret_compile_result(compile_result)
        return self.__handle_result(compile_result)

    def execute_entire_transformation_chain(self):
        self.__ontouml_json_2_ontouml_ecore()
        self.__onto_uml_ecore_2_implementation_model()
        self.__implementation_model_2_java()

        if self.test_generated_code:
            self.__compile_check_generated_code()

    def finalize_and_get_results(self) -> dict:
        """
        Finalizes the transformation and gets the results.
        :return: Dict containing information about the executed transformation.
        """
        self.transformation_result.finalize_results()
        return self.transformation_result.get_results_dicts()
