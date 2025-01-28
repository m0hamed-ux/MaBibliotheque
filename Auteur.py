from Personne import *
from re import *
class Auteur(Personne):
    def __init__(self, nom, prenom, code):
        if match("^A[0-9]{4}$", code):
            super().__init__(nom, prenom)
            self.__code = code
        else:
            raise Exception("Code invalide")
    def getCode(self):
        return self.__code
    def setCode(self, code):
        if match("^A[0-9]{4}$", code):
            self.__code = code
        else:
            raise Exception("Code invalide")
    def __str__(self):
        return f"L'auteur {self.getCode()} : " + super().__str__()