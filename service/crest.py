import eos.db
from eos.types import Crest as CrestUser
import config

class Crest():

    _instance = None
    @classmethod
    def getInstance(cls):
        if cls._instance == None:
            cls._instance = Crest()

        return cls._instance

    def __init__(self):
        pass

    def getCrestCharacters(self):
        return eos.db.getCrestCharacters()

    def getCrestCharacter(self, charID):
        return eos.db.getCrestCharacter(charID)

    def getFittings(self, charID):
        char = self.getCrestCharacter(charID)
        char.auth()
        return char.eve.get('https://api-sisi.testeveonline.com/characters/%d/fittings/'%char.ID)

    def postFitting(self, charID, json):
        char = self.getCrestCharacter(charID)
        char.auth()
        res = char.eve._session.post('https://api-sisi.testeveonline.com/characters/%d/fittings/'%char.ID, data=json)
        return res

    def newChar(self, connection):
        connection()
        info = connection.whoami()
        char = CrestUser(info['CharacterName'], info['CharacterID'], connection.refresh_token)
        eos.db.save(char)

