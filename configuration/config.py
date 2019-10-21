import logging
from pathlib import Path

local_config = []

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger_level = "DEBUG"

# project root
root = Path(__file__).resolve().parent.parent

# data folder
data_dir = root / "data"

# overwrite local config
try:
    import configuration.local_config as lc
    from configuration.local_config import *
    local_config = dir(lc)
    logger.warning("Local config used.")
except:
    pass

logger.info("Logger level %s", logger_level)