#  Copyright (c) 2024.
from enum import Enum

class TransformationStage(Enum):
    READ_ONTOUML = 1,
    ATL = 2,
    ACCELEO = 3,
    COMPILE_CHECK = 4
