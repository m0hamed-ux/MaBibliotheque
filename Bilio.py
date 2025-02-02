from livre import *
from Adherent import *
from Auteur import *
from Emprunt import *
from datetime import date
import json
import csv
class Biblio:
    def __init__(self):
        self.__livres={}
        self.__adherents={}
        self.__emprunts={}
    def load_data(self):
        """Load data from JSON files, creating them if they don't exist"""
        try:
            with open("Database/adherent.json", "r") as f:
                data = json.load(f)
                loaded_adherents = [Adherent.from_dict(item) for item in data]
                self.__adherents = {adh.getCode(): adh for adh in loaded_adherents}
        except (FileNotFoundError, json.JSONDecodeError):
            self.__adherents = {}
            with open("Database/adherent.json", "w") as f:
                json.dump([], f)

        try:
            with open("Database/livres.json", "r") as f:
                data = json.load(f)
                loaded_livres = [livre.from_dict(item) for item in data]
                self.__livres = {livre.get_code(): livre for livre in loaded_livres}
        except (FileNotFoundError, json.JSONDecodeError):
            self.__livres = {}
            with open("Database/livres.json", "w") as f:
                json.dump([], f)

        try:
            with open("Database/emprunts.json", "r") as f:
                data = json.load(f)
                loaded_emprunts = [Emprunt.from_dict(item) for item in data]
                self.__emprunts = {emprunt.getCode(): emprunt for emprunt in loaded_emprunts}
        except (FileNotFoundError, json.JSONDecodeError):
            self.__emprunts = {}
            with open("Database/emprunts.json", "w") as f:
                json.dump([], f)
    def save_data(self):
        with open("Database/adherent.json", "w") as f:
            json.dump([adh.to_dict() for adh in self.__adherents.values()], f, indent=4)
        with open("Database/livres.json", "w") as f:
            json.dump([livre.to_dict() for livre in self.__livres.values()], f, indent=4)
        with open("Database/emprunts.json", "w") as f:
            json.dump([emprunt.to_dict() for emprunt in self.__emprunts.values()], f, indent=4)


    def ajouterLivre(self):
        print("---Saisir les information de livre :---")
        code = input("Code (Ex : L1234) : ")
        if code in self.__livres:
            raise Exception("Il existe déjà un livre avec ce code !")
        titre = input("Titre : ")
        print("Les Informations d'auteur : ")
        auteur = Auteur(input("├── Nom : "), input("├── Prenom : "), input("├── Code (Ex : A1234) : "))
        nbr_ttl_exemplaire = int(input("Le nombre total des exemplaires : "))
        lvr = livre(code, titre, auteur, nbr_ttl_exemplaire, nbr_ttl_exemplaire)
        self.__livres[code] = lvr
        try:
            with open("Database/livres.json", "r") as f:
                livres = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            livres = []

        livres.append(lvr.to_dict())

        with open("Database/livres.json", "w") as f:
            json.dump(livres, f, indent=4)
        # update recent activities
        f = open("Database/recentActivities.txt", "a")
        f.write(f"Le livre {lvr.get_titre()} a ete ajoute le {date.today().strftime('%d/%m/%Y')}\n")
        f.close()
    def ajouterAdherent(self):
        print("---Saisir les information de l'adherent :---")
        nom = input("Nom : ")
        prenom = input("Prenom : ")
        print("La date d'adhésion : ")
        day = int(input("├── Jour : "))
        month = int(input("├── Mois : "))
        year = int(input("├── Annee : "))
        try:
            dateAdhesion = date(year, month, day)
        except Exception as e:
            print(e)
        else:
            Adh = Adherent(nom, prenom, dateAdhesion)
            self.__adherents[Adh.getCode()] = Adh
            # update recent activities
            f = open("Database/recentActivities.txt", "a")
            f.write(f"L'adherent {Adh.get_nom()} {Adh.get_prenomm()} a ete ajoute le {dateAdhesion.strftime('%d/%m/%Y')}\n")
            f.close()
            try:
                with open("Database/adherent.json", "r") as f:
                    adherents = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                adherents = []

            adherents.append(Adh.to_dict())

            with open("Database/adherent.json", "w") as f:
                json.dump(adherents, f, indent=4)
            
    def rechercherAdherent(self,code):
        return self.__adherents.get(int(code))
        
    def rechercherLivre(self,code):
        return self.__livres.get(code)
    def ajouterEmprunt(self, codeA, codeL):
        adherent = self.rechercherAdherent(int(codeA))
        livre = self.rechercherLivre(codeL)
        if livre and adherent and livre.LivreDisponible():
            dateEmprunt = date.today()
            dateRetourPrevue = dateEmprunt + timedelta(days=3)
            emprunt = Emprunt(livre, adherent, dateEmprunt, dateRetourPrevue, dateREffective=None)
            self.__emprunts[emprunt.getCode()] = emprunt
            livre.set_nbr_exemplaire_disponible(livre.get_nbr_exemplaire_disponible()-1)
            livre.addNbrEmprunt()
            try:
                with open("Database/emprunts.json", "r") as f:
                    emprunts = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                emprunts = []

            emprunts.append(emprunt.to_dict())

            with open("Database/emprunts.json", "w") as f:
                json.dump(emprunts, f, indent=4)
            # update recent activities
            f = open("Database/recentActivities.txt", "a")
            f.write(f"L'adherent {adherent.getCode()} a emprunte le livre {livre.get_code()} le {dateEmprunt.strftime('%d/%m/%Y')}\n")
            f.close()
            # Update emprunts.txt 
            try:
                with open("Database/emprunts.txt", "r") as f:
                    lines = f.readlines()
            except FileNotFoundError:
                lines = []
                
            today = date.today().strftime('%d-%m-%Y')
            found = False
            

            for i, line in enumerate(lines):
                if line.strip():
                    emprunt_date, count = line.strip().split(":")
                    if emprunt_date == today:
                        lines[i] = f"{today}:{int(count) + 1}\n"
                        found = True
                        break

            if not found:
                lines.append(f"{today}:1\n")
                
            with open("Database/emprunts.txt", "w") as f:
                f.writelines(lines)
        self.save_data()



    def retourEmprunt(self,codeEmprunt):
        emprunt = self.__emprunts.get(int(codeEmprunt))
        if emprunt:
            if emprunt.etatEmprunt() != "rendu" or emprunt.getDateRetourEffective():
                emprunt.setDateRetourEffective(date.today())
                emprunt.getLivreEmprunte().set_nbr_exemplaire_disponible(emprunt.getLivreEmprunte().get_nbr_exemplaire_disponible()+1) 
                self.save_data()
                return True
            else:
                raise Exception("Ce livre est deja rendu")
        raise Exception("il n'y a pas de emprunt avec ce code!")
    def topEmprunts(self):
        if not self.__livres:
            return []
        max_emprunts = max(livre.getNbrEmprunt() for livre in self.__livres.values())
        return [livre for livre in self.__livres.values() if livre.getNbrEmprunt() == max_emprunts]
    def emprunteurs(self):
        emprunteurs = {emprunt for emprunt in self.__emprunts.values() 
                      if emprunt.etatEmprunt() in ["en cours","non rendu"]}
        if not emprunteurs:
            raise Exception("la liste est vide")
        return list(emprunteurs)
    def datePossibilitéEmprunt(self,codeL):
        livre = self.rechercherLivre(codeL)
        if not livre:
            raise Exception("Livre introuvable.")
        if livre.LivreDisponible():
            print("Le livre est disponible.")
            return
        for emprunt in self.__emprunts.values():
            if emprunt.getLivreEmprunte() == livre and emprunt.etatEmprunt() == "en cours":
                print("ce livre sera disponible le : ",emprunt.getDateRetourPrevue().strftime('%d/%m/%Y'))
                return
        print("Il n'est pas prevu qu'il soit disponible.")
    def AfficherLivres(self):
        if not self.__livres:
            raise Exception("la liste est vide")
        print("La list des livres : ")
        for livre in self.__livres.values():
            print(f"{livre}")
    def AfficherAdherents(self):
        if not self.__adherents:
            raise Exception("la liste est vide")
        print("La list des adherents : ")
        for adherent in self.__adherents.values():
            print(f"├── {adherent}")
    def Rapport(self):
        print(f"Nombres des livres : {len(self.__livres)}\nNombres des adherents : {len(self.__adherents)}")
    def get_livres(self):
        return self.__livres
    def getTotalCopies(self):
        return sum(int(livre.get_nbr_ttl_exemplaire()) for livre in self.__livres.values())
    def getTotalAvailableCopies(self):
        return sum(int(livre.get_nbr_exemplaire_disponible()) for livre in self.__livres.values())
    def get_available_books(self):
        return [livre for livre in self.__livres.values() if livre.LivreDisponible()]
    def get_borrowed_books(self):
        return [livre for livre in self.__livres.values() if not livre.LivreDisponible()]
    def get_all_clients(self):
        return self.__adherents
    def get_all_emprunts(self):
        return list(self.__emprunts.values())
    def TopLivres(self):
        return sorted(self.__livres.values(), key=lambda x: x.getNbrEmprunt(), reverse=True)
    def save_livres_csv(self):
        try:
            with open("Database/CSV/livres.csv", "w", newline='', encoding='utf-8') as f:
                fieldnames = ["Code", "Titre", "Auteur", "Nombre total d'exemplaires", "Nombre d'exemplaires disponibles", "Nombre d'emprunts"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for livre in self.__livres.values():
                    writer.writerow({
                        "Code": livre.get_code(),
                        "Titre": livre.get_titre(),
                        "Auteur": livre.get_auteur().get_nom(),
                        "Nombre total d'exemplaires": livre.get_nbr_ttl_exemplaire(),
                        "Nombre d'exemplaires disponibles": livre.get_nbr_exemplaire_disponible(),
                        "Nombre d'emprunts": livre.getNbrEmprunt()
                    })
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des livres: {e}")
    def save_emprunts_csv(self):
        try:
            with open("Database/CSV/emprunts.csv", "w", newline='', encoding='utf-8') as f:
                fieldnames = ["Code", "Livre", "Adherent", "Date d'emprunt", "Date de retour prevue", "Date de retour effective"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for emprunt in self.__emprunts.values():
                    writer.writerow({
                        "Code": emprunt.getCode(),
                        "Livre": emprunt.getLivreEmprunte().get_code(),
                        "Adherent": emprunt.getEmprunteurLivre().getCode(),
                        "Date d'emprunt": emprunt.getDateEmprunt().strftime('%d/%m/%Y'),
                        "Date de retour prevue": emprunt.getDateRetourPrevue().strftime('%d/%m/%Y'),
                        "Date de retour effective": emprunt.getDateRetourEffective().strftime('%d/%m/%Y') if emprunt.getDateRetourEffective() else ""
                    })
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des emprunts: {e}")
    def save_adherents_csv(self):
        try:
            with open("Database/CSV/adherents.csv", "w", newline='', encoding='utf-8') as f:
                fieldnames = ["Code", "Nom", "Prenom", "Date d'adhésion"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for adherent in self.__adherents.values():
                    writer.writerow({
                        "Code": adherent.getCode(),
                        "Nom": adherent.get_nom(),
                        "Prenom": adherent.get_prenomm(),
                        "Date d'adhésion": adherent.getDateDateAdhésion().strftime('%d/%m/%Y')
                    })
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des adherents: {e}")
    def get_livres_non_disponibles(self):
        return [livre for livre in self.__livres.values() if not livre.LivreDisponible() or livre.get_nbr_exemplaire_disponible() <= 3]
