import re
from Auteur import *
class livre:
    def __init__(self,code,titre,auteur,nbr_ttl_exemplaire,nbr_exemplaire_disponible):
        self.template=r"^L\d{4}$"
        if not re.match(self.template,code):
            raise Exception("Le code inserer doit commencer par la lettre 'L' majiscule suivie par quatre chiffre ")
        elif not isinstance(auteur,Auteur):
            raise Exception("INVALIDE !!")
        elif (not isinstance(nbr_ttl_exemplaire,int)) or (not isinstance(nbr_exemplaire_disponible,int)):
            raise Exception("le nombre saisie doit etre un entier")
        elif nbr_ttl_exemplaire < 0 or nbr_exemplaire_disponible > nbr_ttl_exemplaire:
            raise Exception(" ERROR réviser les iformations donner !!")
        else:
            self.__code=code
            self.__auteur=auteur
            self.__titre=titre
            self.__nbr_ttl_exemplaire=nbr_ttl_exemplaire
            self.__nbr_exemplaire_disponible=nbr_exemplaire_disponible
            self.__nbrEmprunt = 0

            

    #getters 

    def get_code(self):
        return self.__code
    def get_titre(self):
        return self.__titre
    def get_auteur(self):
        return self.__auteur
    def get_nbr_ttl_exemplaire(self):
        return  self.__nbr_ttl_exemplaire
    def get_nbr_exemplaire_disponible(self):
        return self.__nbr_exemplaire_disponible
    def getNbrEmprunt(self):
        return self.__nbrEmprunt
    
    #setters

    def set_code(self,new_code):
        if re.match(self.template,new_code):
            self.__code=new_code
        else:
            raise Exception("Le code inserer doit commencer par la lettre 'L' majiscule suivie par quatre chiffre ")
    
    def set_titre(self,new_titre):
        self.__titre=new_titre

    def set_auteur(self,new_auteur):
        if isinstance(new_auteur,Auteur):
            self.__auteur=new_auteur
        else:
            raise Exception("INVALIDE !!")
    
    def set_nbr_ttl_exemplaire(self,new_value):
        if isinstance(new_value,int) and new_value > 0 :
            self.__nbr_ttl_exemplaire=new_value
        else:
            raise Exception("le nombre saisie doit etre un entier positif")
    
    def set_nbr_exemplaire_disponible(self,new_value2):
        if isinstance(new_value2,int) and new_value2 <= self.get_nbr_ttl_exemplaire():
            self.__nbr_exemplaire_disponible=new_value2
        else:
             raise Exception(" le nombre des exemplaires disponibles doit etre un entier positif inferieur au nombre des exemplaires")
    def addNbrEmprunt(self):
        self.__nbrEmprunt += 1
    #methoode
    def LivreDisponible(self):
        return self.get_nbr_exemplaire_disponible() > 0
    def __str__(self):
        return f"---------Livre {self.__code}--------- \n├── Titre : {self.__titre}.\n├── Auteur : {self.__auteur}.\n├── Le nombre total des exemplaires : {self.__nbr_ttl_exemplaire}.\n├── Le nombre des exemplaires disponibles : {self.__nbr_exemplaire_disponible}\n├── Nombre des emprunts : {self.getNbrEmprunt()}"
    def to_dict(self):
        """Convert the book object to a dictionary for JSON serialization"""
        return {
            "code": self.__code,
            "titre": self.__titre,
            "auteur": self.__auteur.to_dict(),
            "nbr_ttl_exemplaire": self.__nbr_ttl_exemplaire,
            "nbr_exemplaire_disponible": self.__nbr_exemplaire_disponible,
            "nbrEmprunt": self.__nbrEmprunt
        }
    @classmethod
    def from_dict(cls, data):
        """Create a livre instance from a dictionary"""
        # Create Auteur instance from the nested author data
        auteur_data = data["auteur"]
        auteur = Auteur(
            nom=auteur_data["nom"],
            prenom=auteur_data["prenom"],
            code=auteur_data["code"]
        )
        
        # Create the livre instance
        livre_instance = cls(
            code=data["code"],
            titre=data["titre"],
            auteur=auteur,
            nbr_ttl_exemplaire=int(data["nbr_ttl_exemplaire"]),
            nbr_exemplaire_disponible=int(data["nbr_exemplaire_disponible"])
        )
        
        # Set the nbrEmprunt value after creation using direct attribute access
        livre_instance._livre__nbrEmprunt = int(data.get("nbrEmprunt", 0))
        return livre_instance
