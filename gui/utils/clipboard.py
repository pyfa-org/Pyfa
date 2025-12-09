# noinspection PyPackageRequirements
import wx
from logbook import Logger

logger = Logger(__name__)


def toClipboard(text):
    """
    Copy text to clipboard. Explicitly uses CLIPBOARD selection, not PRIMARY.

    On X11 systems, wxPython can confuse between PRIMARY and CLIPBOARD selections,
    causing "already open" errors. This function ensures we always use CLIPBOARD.

    See: https://discuss.wxpython.org/t/wx-theclipboard-pasting-different-content-on-every-second-paste/35361
    """
    clipboard = wx.Clipboard()
    try:
        # Explicitly use CLIPBOARD selection, not PRIMARY selection
        # This prevents X11 confusion between the two clipboard types
        clipboard.UsePrimarySelection(False)

        if clipboard.Open():
            try:
                data = wx.TextDataObject(text)
                clipboard.SetData(data)
                clipboard.Flush()  # Ensure clipboard manager gets the data
                return True
            finally:
                clipboard.Close()
        else:
            logger.debug("Failed to open clipboard for writing")
            return False
    except Exception as e:
        logger.warning("Error writing to clipboard: {}", e)
        return False


def fromClipboard():
    """
    Read text from clipboard. Explicitly uses CLIPBOARD selection, not PRIMARY.

    On X11 systems, wxPython can confuse between PRIMARY and CLIPBOARD selections,
    causing "already open" errors. This function ensures we always use CLIPBOARD.

    See: https://discuss.wxpython.org/t/wx-theclipboard-pasting-different-content-on-every-second-paste/35361
    """
    clipboard = wx.Clipboard()
    try:
        # Explicitly use CLIPBOARD selection, not PRIMARY selection
        # This prevents X11 confusion between the two clipboard types
        clipboard.UsePrimarySelection(False)

        if clipboard.Open():
            try:
                data = wx.TextDataObject()
                if clipboard.GetData(data):
                    return data.GetText()
                else:
                    logger.debug("Clipboard open but no CLIPBOARD data available")
                    return None
            finally:
                clipboard.Close()
        else:
            logger.debug("Failed to open clipboard for reading")
            return None
    except Exception as e:
        logger.warning("Error reading from clipboard: {}", e)
        return None
