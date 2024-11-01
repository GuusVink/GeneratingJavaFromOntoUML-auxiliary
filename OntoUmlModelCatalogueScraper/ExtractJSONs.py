"""
Get a single folder of OntoUML JSON files for different projects
"""
import os
import logging
import shutil

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# The 82 projects supposedly supported by the transformation
to_be_copied_projects = ['aguiar2018rdbs-o', 'aguiar2019ooco', 'bank-account2013', 'bank-model', 'barcelos2013normative-acts', 'barcelos2015transport-networks', 'barros2020programming', 'bernasconi2023fair-principles', 'brazilian-governmental-organizational-structures', 'buchtela2020connection', 'buridan-ontology2021', 'carolla2014campus-management', 'castro2012cloudvulnerability', 'cgts2021sebim', 'chartered-service', 'clergy-ontology', 'construction-model', 'demori2023miscon', 'digitaldoctor2022', 'elikan2018brand-identity', 'eu-rent-refactored2022', 'experiment2013', 'formula-one2023', 'fraller2019abc', 'fumagalli2022criminal-investigation', 'g809-2015', 'genealogy2013', 'gomes2022digital-technology', 'guarino2016value', 'haridy2021egyptian-e-government', 'health-organizations', 'idaf2013', 'internal-affairs2013', 'internship', 'it-infrastructure', 'jacobs2022sdpontology', 'junior2018o4c', 'khantong2020ontology', 'kritz2020ontobg', 'laurier2018rea', 'library', 'machacova2023gym', 'martinez2013human-genome', 'music-ontology', 'neves2021grain-production', 'online-mentoring', 'pereira2015doacao-orgaos', 'pereira2020ontotrans', 'photography', 'plato-ontology2019', 'project-assets2013', 'project-management-ontology', 'public-expense-ontology2020', 'public-organization2013', 'public-tender', 'qam', 'ramirez2015userfeedback', 'real-estate-ontology', 'recommendation-ontology', 'road-accident2013', 'rocha2023ciencia-aberta', 'santos2020valuenetworks', 'scientific-experiment2013', 'scientific-publication2013', 'short-examples2013', 'silva2012itarchitecture', 'silva2021sebim', 'silveira2021oap', 'social-contract', 'social-contracts2013', 'sousa2022triponto', 'sportbooking2021', 'srro-ontology', 'stock-broker2021', 'telecom-equipment2013', 'tender2013', 'tourbo2021', 'university-ontology', 'valaski2020medical-appointment', 'zanetti2019orm-o', 'zhou2017hazard-ontology-robotic-strolling', 'zhou2017hazard-ontology-train-control']

logger.info("Logger initiated")

# Path to a local version of the OntoUML model catalogue
repo_path = None

if repo_path is None:
    print("Forgot to set the path to the local location of the OntoUML model catalogue!")
    exit(-1)

output_path = 'modelJsons'

os.listdir(repo_path)

# Structure:    Project -> Type -> StereoType -> Count
type_stats = {}  # Dict containing the stats of each ontology project

for project in to_be_copied_projects:
    p_path = os.path.join(repo_path, project)
    json_path = os.path.join(p_path, "ontology.json")

    output_json_path = os.path.join(output_path, (project + '.json'))

    if not os.path.isfile(json_path):
        logger.error(f"JSON file does not exist for project {project}")
        continue

    shutil.copyfile(json_path, output_json_path)
    # with open(json_path, 'r') as in_f, open(output_json_path, 'w') as out_f:
    #     print(in_f)

