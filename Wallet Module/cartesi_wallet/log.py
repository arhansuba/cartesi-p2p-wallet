
import logging
import os
from datetime import datetime, timezone

LOG_FMT = 'level={levelname} ts={asctime} module={module} msg="{message}"'
LOG_LEVEL = "INFO"

LOG_LEVEL_ENV_VAR = "LOG_LEVEL"
if LOG_LEVEL_ENV_VAR in os.environ:
    LOG_LEVEL = os.environ.get(LOG_LEVEL_ENV_VAR)

logging.basicConfig(level=LOG_LEVEL, format=LOG_FMT, style="{")

# ISO-8061 date format
logging.Formatter.formatTime = (lambda self, record, datefmt=None:
                                datetime.fromtimestamp(
                                    record.created, timezone.utc)
                                .astimezone()
                                .isoformat(sep="T", timespec="milliseconds"))

logger = logging.getLogger(__name__)
