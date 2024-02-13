import sys
from pathlib import Path
root_path=Path(__file__).parent.parent.parent
sys.path.append(str(root_path))

import src.services.func1 as func1
from src.LogSettings import logger,logging

test=func1.Ideator()

test._doBruteThink("")