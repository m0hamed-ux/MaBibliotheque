from Personne import *
from datetime import *
from re import *
class Adherent(Personne) :
    code=0
    def __init__(self,nom,prenom,dateAdhesion):
        if not isinstance(dateAdhesion, date) or dateAdhesion > date.today():
            raise Exception ("date inscription invalide")
        else:
            Adherent.code +=1
            Personne.__init__(self,nom,prenom)
            self.__DateAdhésion = dateAdhesion
            self.__code = Adherent.code
        
    def getCode(self):
        return self.__code
    def getDateDateAdhésion(self):
        return self.__DateAdhésion
    def __str__(self):
        return super().__str__()+f", Le code est : {self.getCode()}, la date d'Adhésion : {self.getDateDateAdhésion().day}/{self.getDateDateAdhésion().month}/{self.getDateDateAdhésion().year}"