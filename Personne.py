class Personne:
    def __init__(self,nom,prenom):
        if not isinstance(nom,str):
            raise Exception("le nom est invalid!")
        elif not isinstance(prenom,str):
            raise Exception("le prenom est invalid!")
        else:
            self.__nom=nom
            self.__prenom=prenom
        
    def get_nom(self):
        return self.__nom
        
    def set_nom(self,nom):
        if not isinstance(nom,str):
            raise Exception("le nom est invalid!")
        else:
            self.__nom=nom
        
    def get_prenomm(self):
        return self.__prenom
        
    def set_prenom(self,prenom):
        if not isinstance(prenom,str):
            raise Exception("le prenom est invalid!")
        else:
            self.__prenom=prenom
    
    def __str__(self):
        return f"Nom : {self.__nom}, Prenom : {self.__prenom}"