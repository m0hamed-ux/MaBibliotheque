from Personne import *
from datetime import *
from re import *
import json
class Adherent(Personne) :
    code = 1
    try:
        with open("Database/adherent.json", "r") as file:
            adherents = json.load(file)
            if adherents:
                code = max(adherent["code"] for adherent in adherents) + 1
            else:
                code = 1
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    def __init__(self,nom,prenom,dateAdhesion, **kwargs):
        
        if not isinstance(dateAdhesion, date) or dateAdhesion > date.today():
            raise Exception ("date inscription invalide")
        else:
            if "code" in kwargs:
                self.__code = kwargs["code"]
            else:
                self.__code = Adherent.code
                Adherent.code +=1
            Personne.__init__(self,nom,prenom)
            self.__DateAdhésion = dateAdhesion
            

    def getCode(self):
        return self.__code
    def getDateDateAdhésion(self):
        return self.__DateAdhésion
    def setDateAdhesion(self, dateAdhesion):
        if not isinstance(dateAdhesion, date) or dateAdhesion > date.today():
            raise Exception ("date inscription invalide")
        else:
            self.__DateAdhésion = dateAdhesion

    def to_dict(self):
        return {"nom": self.get_nom(), "prenom": self.get_prenomm(), "dateAdhesion": self.__DateAdhésion.strftime('%Y-%m-%d'), "code": self.__code}
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["nom"], data["prenom"], date.fromisoformat(data["dateAdhesion"]), code=data["code"])
    def __str__(self):
        return super().__str__()+f", Le code est : {self.getCode()}, la date d'Adhésion : {self.getDateDateAdhésion().day}/{self.getDateDateAdhésion().month}/{self.getDateDateAdhésion().year}"
