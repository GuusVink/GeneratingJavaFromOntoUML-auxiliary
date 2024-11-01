#  Copyright (c) 2024.
from OntoUML2JavaTransformationExecution.TransformationStage import TransformationStage

import subprocess
import time
import re

class TransformationExecResult:
    """
    Object containing the results of an executed transformation.
    Includes transformation execution time, warnings provided, and occurred errors.
    """

    def __init__(self, model_name):
        self.ontouml_model = model_name
        self.total_time_ns = 0
        self.read_ontouml_json_success = False
        self.ontouml_2_im_success = False
        self.atl_warnings = None
        self.im_2_java_success = False
        self.acceleo_warnings = None
        self.finished_transformation = False
        self.generated_code_compiles = False
        self.generated_code_compilation_errors = None
        self.ontouml_read_errors = None

        self.time_per_stage = dict()

    def mark_start_time(self):
        """
        Record start time.
        :return:
        """
        self.start_time_ns = time.time_ns()

    def mark_end_time(self, transformation_stage: TransformationStage):
        """
        Mark end time. The time passed since 'mark_start_time' is collected as the exection time of the transformation
        step provided by 'transformation_stage'
        :param transformation_stage: What transformation step/stage to record the time for.
        :return:
        """
        if self.start_time_ns is None:
            raise RuntimeError('Start time not marked before calculating endtime.')
        else:
            end_time_ns = time.time_ns()
            passed_time = end_time_ns - self.start_time_ns
            self.total_time_ns += passed_time
            self.time_per_stage[transformation_stage] = passed_time / 1000000000
            self.start_time_ns = None

    def interpret_ontouml_read_result(self, result: subprocess.CompletedProcess[str]):
        if result.returncode == 0:
            self.read_ontouml_json_success = True
        else:
            self.read_ontouml_json_success = False
            self.ontouml_read_errors = result.stdout[:5000] + f"\n [and {result.stdout[5000:].count('\n')} more lines]"

    def interpret_atl_result(self, result: subprocess.CompletedProcess[str]):
        if result.returncode == 0:
            self.ontouml_2_im_success = True
        else:
            self.ontouml_2_im_success = False

        self.atl_warnings = self._extract_atl_warnings(result.stdout)

    def interpret_acceleo_result(self, result: subprocess.CompletedProcess[str]):
        if result.returncode == 0:
            self.im_2_java_success = True
        else:
            self.im_2_java_success = False

        if (warn := self._extract_acceleo_warnings(result.stdout)) != "":
            self.acceleo_warnings = warn

    def interpret_compile_result(self, result: subprocess.CompletedProcess[str]):
        if result.returncode == 0:
            self.generated_code_compiles = True
        else:
            self.generated_code_compilation_errors = result.stdout[:5000] + f"\n [and {result.stdout[5000:].count('\n')} more lines]"

    def finalize_results(self):
        """
        Step to be called once the transformation is finished. Prints results.
        :return:
        """
        self.finished_transformation = self.read_ontouml_json_success and self.ontouml_2_im_success and self.im_2_java_success
        print(f"\n\n {'*' * 80} \n")
        if self.finished_transformation:
            passed_time_s = self.total_time_ns / 1000000000
            print(f"Finished transformation {self.ontouml_model} with time: {passed_time_s} (s)")
            print(f"ATL warnings: {self.atl_warnings}")
            print(f"Acceleo warnings: {self.acceleo_warnings}")
            print(f"Code compiles:\n {self.generated_code_compiles} "
                  f"{self.generated_code_compilation_errors}")
        else:
            print(
                f"Transformation failed at {self.__transformation_failed_at_stage()}")
            print(f"\nOntoUML read errors:\n {self.ontouml_read_errors}")
        print(f"\n\n {'*' * 80} \n")

    def _extract_atl_warnings(self, cons_log: str):
        if cons_log is None:
            print(f"{'!'*80}\n !!! Did not get STDOUT for ATL process !!!\n{'!'*80}")
            return set()
        regex = r"Warning:.*\n"
        unique_warns = set()
        for match in re.finditer(regex, cons_log):
            unique_warns.add(match.group(0).strip())

        return unique_warns

    def _extract_acceleo_warnings(self, cons_log: str):
        if cons_log is None:
            print(f"{'!'*80}\n !!! Did not get STDOUT for ACCELEO process !!!\n{'!'*80}")
            return None
        regex = r"\[java\] (.*)\n"
        result = ""
        for match in re.finditer(regex, cons_log):
            result += match.group(1) + "\n"
        return result

    def __get_stage_time(self, stage: TransformationStage):
        if stage in self.time_per_stage:
            return self.time_per_stage[stage]
        else:
            return -1,

    def get_results_dicts(self) -> dict:
        """
        Returns a dictionary with the transformation results.
        Expects "finalize_transformation" to have been called before.
        :return: Dict containing information about the executed transformation.
        """
        result = {
            'model': self.ontouml_model,
            'transformation_successful': self.finished_transformation,
            'generated_code_compiles': self.generated_code_compiles,
            'transformation_failed_at_stage': self.__transformation_failed_at_stage(),
            'transformation_time_s': self.total_time_ns / 1000000000,
            'ontouml_read_errors': self.ontouml_read_errors,
            'atl_warnings': self.atl_warnings,
            'acceleo_warnings': self.acceleo_warnings,
            'compilation_errors': self.generated_code_compilation_errors,
            'read_ontouml_time_s': self.__get_stage_time(TransformationStage.READ_ONTOUML),
            'atl_time_s': self.__get_stage_time(TransformationStage.ATL),
            'acceleo_time_s': self.__get_stage_time(TransformationStage.ACCELEO)
        }
        return result

    def __transformation_failed_at_stage(self):
        if not self.read_ontouml_json_success:
            return 'read_ontouml'
        elif not self.ontouml_2_im_success:
            return 'ontouml_2_im'
        elif not self.im_2_java_success:
            return 'im_2_java'
        else:
            return None