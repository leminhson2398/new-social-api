from starlette.config import Config
import logging
import sys
from os import path


CURDIR: str = path.dirname(
    path.abspath(__file__)
)

# append for import
sys.path.append("..")

# configure logging:
logging.basicConfig(
    format="%(asctime)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO
)

# main config:
config: Config = Config(
    path.join(CURDIR, ".env")
)
