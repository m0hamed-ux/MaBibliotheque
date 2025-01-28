from livre import *
from Adherent import *
from Auteur import *
from Emprunt import *
from datetime import *
class Emprunt:
    code=0
#---------constructeur---------    
    def __init__(self,livreEmprunte,EmprunteurLivre,dateEmprunt,dateRPrevue,dateREffective):
        Emprunt.code+=1
        if not isinstance(livreEmprunte,livre):
            raise Exception("Le nom de livre est invalide!")
        elif not isinstance(EmprunteurLivre,Adherent):
            raise Exception("L'emprunteur du livre est invalide!")
        elif not isinstance(dateEmprunt,date) and dateEmprunt<date.today:
            raise Exception("La date d'emprunt est invalide!")
        elif not isinstance(dateRPrevue,date) and dateRPrevue>date.today:
            raise Exception("La date de retour prévue est invalide!")
        else:
            self.__code=Emprunt.code
            self.__livreEmprunte=livreEmprunte
            self.__EmprunteurLivre=EmprunteurLivre
            self.__dateEmprunt=dateEmprunt
            self.__dateRetourPrevue=dateRPrevue
            self.__dateRetourEffective=dateREffective
#---------getter-----------        
    def getCode(self):
        return self.__code
    def getLivreEmprunte(self):
        return self.__livreEmprunte
    def getEmprunteurLivre(self):
        return self.__EmprunteurLivre
    def getDateEmprunt(self):
        return self.__dateEmprunt
    def getDateRetourPrevue(self):
        return self.__dateRetourPrevue
    def getDateRetourEffective(self):
        return self.__dateRetourEffective
#--------setter--------------    
    def setLivreEmprunte(self,value):
        if not isinstance(value,livre):
            raise Exception("Le nom de livre est invalide!")
        else:
            self.__livreEmprunte=value
    def setEmprunteurLivre(self,value):
        if not isinstance(value,Adherent):
            raise Exception("L'emprunteur du livre est invalide!")
        else:
            self.__EmprunteurLivre=value
    def setDateEmprunt(self,value):
        if not isinstance(value,date) and value==date.today:
            raise Exception("La date d'emprunt est invalide!")
        else:
            self.__dateEmprunt=value
    def setDateRetourPrevue(self,value):
        if not isinstance(value,date) and value<date.today:
            raise Exception("La date de retour prévue est invalide!")
        else:
            self.__dateRetourPrevue=value
    def getDateRetourPrevue(self):
        return self.__dateRetourPrevue
    def setDateRetourEffective(self,value):
        if not isinstance(value,date):
            raise Exception("La date de retour effective est invalide!")
        else:
            self.__dateRetourEffective=value
    def getDateRetourEffective(self):
        return self.__dateRetourEffective
#---------methodes-------------
    def etatEmprunt(self):
        etat=""
        if self.__dateRetourEffective:
            etat = "rendu"
        elif self.__dateRetourPrevue >= date.today():
           etat = "en cours"
        else:
            etat = "non rendu"
        return etat
    def __str__(self):
        return f"------Emprunt N° : {self.__code}------\n├── Livre : {self.__livreEmprunte.get_code()}\n├── Emprunteur : {self.__EmprunteurLivre.getCode()}\n├── la date d’emprunt : {self.__dateEmprunt}\n├── la date de retour prévue : {self.__dateRetourPrevue}\n├── la date de retour effective : {self.__dateRetourEffective}\n├── Etat : {self.etatEmprunt()}"