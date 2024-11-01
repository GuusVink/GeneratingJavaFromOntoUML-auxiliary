# OntoUML2JavaTransformationExecution

Python scripts to execute the [OntoUML2Java transformation](https://github.com/GuusVink/ontouml-java-generation) implemented in EMF.

## Requirements
- Eclipse workspace of the [OntoUML2Java transformation](https://github.com/GuusVink/ontouml-java-generation) to be present on the PC
  - Location/path of the Eclipse workspace to be defined as an environment variable called `ECLIPSE_ONTOUML_2_JAVA_WORKSPACE` OR defined in [TransformationExecutor.py](TransformationExecutor.py)
- A working Java 21 (or newer) SDK
  - Such as https://www.graalvm.org/
  - The Java executable should be added to the system path
- A working installation of the [ANT build tool](https://ant.apache.org/)
  - The ANT executable should be added to the system path


## Example
[Example.py](Example.py) contains an example on how to use the [TransformationExecutor](TransformationExecutor.py) class\
to execute the OntoUML to Java transformation.
