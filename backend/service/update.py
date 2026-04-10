"""
Mobile update-check service — replaces service/update.py.

wx.CallAfter removed; the callback is a plain Python callable.
The version-check logic is otherwise identical to the desktop version.
"""

import calendar
import threading
from typing import Callable, Optional

import dateutil.parser
from logbook import Logger
from packaging.version import Version

import config
from service.network import Network
from service.settings import UpdateSettings

pyfalog = Logger(__name__)


class CheckUpdateThread(threading.Thread):
    def __init__(self, callback: Optional[Callable] = None):
        super().__init__(name="CheckUpdate", daemon=True)
        self.callback = callback
        self.settings = UpdateSettings.getInstance()
        self.running = True

    def run(self):
        network = Network.getInstance()
        try:
            try:
                response = network.get(
                    url=f"https://www.pyfa.io/update_check?pyfa_version={config.version}"
                        f"&client_hash={config.getClientSecret()}",
                    type=network.UPDATE,
                    timeout=5,
                )
            except Exception:
                response = network.get(
                    url="https://api.github.com/repos/pyfa-org/Pyfa/releases",
                    type=network.UPDATE,
                    timeout=5,
                )

            json_response = response.json()
            json_response.sort(
                key=lambda x: calendar.timegm(
                    dateutil.parser.parse(x["published_at"]).utctimetuple()
                ),
                reverse=True,
            )

            for release in json_response[:5]:
                r_version = Version(release["tag_name"])
                c_version = Version(config.version or "0.0.0")

                if (
                    not c_version.is_prerelease
                    and r_version.is_prerelease
                    and self.settings.get("prerelease")
                ):
                    continue

                if self.settings.get("version") == "v" + config.version:
                    self.settings.set("version", None)

                if release["tag_name"] == self.settings.get("version"):
                    break

                if r_version > c_version:
                    # Plain callback — no wx.CallAfter
                    if self.callback:
                        self.callback(release, r_version)
                    break

        except Exception as e:
            pyfalog.error("Update check failed: {0}", e)

    def stop(self):
        self.running = False


class Update:
    _instance: Optional["Update"] = None

    @classmethod
    def getInstance(cls) -> "Update":
        if cls._instance is None:
            cls._instance = Update()
        return cls._instance

    @staticmethod
    def checkUpdate(callback: Optional[Callable] = None):
        """Start the update-check thread.  callback(release, version) on update found."""
        thread = CheckUpdateThread(callback=callback)
        pyfalog.debug("Starting update-check thread")
        thread.start()
        return thread
