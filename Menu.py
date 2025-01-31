from termcolor import *
from Bilio import *

Bib = Biblio()
Bib.load_data()
while True:
    print(colored("\n-------------Menu-------------", "light_green"))
    print(colored('''1) Ajouter un livre
2) Ajouter un adhérent
3) Rechercher un adhérent par code
4) Rechercher un livre par code
5) Ajouter un emprunt
6) Ajouter le retour d’un emprunt
7) Afficher tous les livres
8) Afficher tous les adherents
9) Afficher le livre le plus demandé
10) Lister les emprunteurs
11) Vérifier la date de disponibilité d’un livre
12) Rapport
13) Quiter
''', "light_blue"))
    choix = int(input(colored("Saiser votre choix : ", "light_green")))
    if choix == 1:
        try:
            Bib.ajouterLivre()
        except Exception as e:
            print(colored(e, "red"))
        else:
            print(colored("Bien ajouter", "green"))
    elif choix == 2:
        try:
            Bib.ajouterAdherent()
        except Exception as e:
            print(colored(e, "red"))
        else:
            print(colored("Bien ajouter", "green"))
    elif choix == 3:
        try:
            adherent = Bib.rechercherAdherent(int(input("Saiser le code : ")))
        except Exception as e:
            print(colored(e, "red"))
        else:
            if adherent:
                print(adherent)
            else:
                print(colored("il n'y a pas d'adherent avec ce code!", "red"))
    elif choix == 4:
        try:
            Livre = Bib.rechercherLivre(input("Saiser le code : "))
        except Exception as e:
            print(colored(e, "red"))
        else:
            if Livre:
                print(Livre)
            else:
                print(colored("il n'y a pas de livre avec ce code!", "red"))
    elif choix == 5:
        try:
            codeA = int(input("saisir le code de l'Adherent : "))
            codeL = input("saisir le code de livre : ")
            Bib.ajouterEmprunt(codeA, codeL)
        except Exception as e:
            print(colored(e, "red"))
        else:
            print(colored("Bien ajouter", "green"))
    elif choix == 6:
        try:
            Bib.retourEmprunt(input("saisir le code de l'Emprunt : "))
        except Exception as e:
            print(colored(e, "red"))
    elif choix == 7:
        try:
            Bib.AfficherLivres()
        except Exception as e:
            print(colored(e, "red"))
    elif choix == 8:
        try:
            Bib.AfficherAdherents()
        except Exception as e:
            print(colored(e, "red"))
    elif choix == 9:
        try:
            Bib.topEmprunts()
        except Exception as e:
            print(colored(e, "red"))
        else:
            print(colored("les livres les plus demandé sont : "))
            for elt in Bib.topEmprunts():
                print(elt)
    elif choix == 10:
        try: 
            Bib.emprunteurs()
        except Exception as e:
            print(colored(e, "red"))
        else:
            print(colored("---La liste des emprunteurs---", "light_green"))
            for elt in Bib.emprunteurs():
                print(elt)
    elif choix == 11:
        try:
            Bib.datePossibilitéEmprunt(input("Saisir le code de livre : "))
        except Exception as e:
            print(colored(e, "red"))
    elif choix == 12:
        Bib.Rapport()
    elif choix == 13:
        break
    else:
        print(colored("Invalid","red"))