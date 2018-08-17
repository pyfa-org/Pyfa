import sys
from logbook import Logger
import threading
from service.esi import Esi

pyfalog = Logger(__name__)


class Insurance():
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Insurance()

        return cls.instance

    def __init__(self):
        self.__testvariable = 5

    def apiFetch(self, callback):
        thread = InsuranceImportThread((self.apiFetchCallback, callback))
        thread.start()

    def apiFetchCallback(self, response, othercallback, e=None):
        pyfalog.info(response)
        wx.CallAfter(othercallback, e)


class InsuranceImportThread(threading.Thread):
    def __init__(self, callback):
        threading.Thread.__init__(self)
        self.name = "InsuranceImport"
        self.callback = callback

    def run(self):
        try:
            sEsi = Esi.getInstance()
            resp = sEsi.getInsurance()
            self.callback[0](resp, self.callback[1])
        except Exception as ex:
            pyfalog.warn(ex)
            self.callback[0](None, self.callback[1](sys.exc_info()))
