# noinspection PyPackageRequirements
import pyclip
from logbook import Logger

logger = Logger(__name__)


def toClipboard(text):
    pyclip.copy(text)


def fromClipboard():
    """
    Read text from clipboard. Uses pyclip to grab in a cross-platform, reliable manner.
    """
    data = pyclip.paste(text=True)
    if not isinstance(data, str):
        data = data.decode('utf-8')
    logger.debug("Pasted data: {}", data)
    return data
