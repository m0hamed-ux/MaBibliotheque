from customtkinter import *
from tkinter import messagebox, ttk
from datetime import date
import json
from Bilio import *
from Adherent import *
import PIL
from tkcalendar import DateEntry



gestion = Biblio()
gestion.load_data()
gestion.getDefault()
Adherents = gestion.get_all_clients().values()



#images
editIcon = CTkImage(PIL.Image.open("images/edit.png"), size=(20, 20))
deletIcon = CTkImage(PIL.Image.open("images/delet.png"), size=(20, 20))
# class Adherent:
#     code = 1
#     try:
#         with open("Database/adherent.json", "r") as file:
#             adherents_data = json.load(file)
#             if adherents_data:
#                 code = adherents_data[-1]["code"] + 1
#     except (FileNotFoundError, json.JSONDecodeError):
#         pass

#     def __init__(self, nom, prenom, dateAdhesion, **kwargs):
#         if not isinstance(dateAdhesion, date) or dateAdhesion > date.today():
#             raise Exception("Date inscription invalide")
#         else:
#             if "code" in kwargs:
#                 self.__code = kwargs["code"]
#             else:
#                 self.__code = Adherent.code
#                 Adherent.code += 1
#             self.__nom = nom
#             self.__prenom = prenom
#             self.__DateAdhésion = dateAdhesion

#     def getCode(self):
#         return self.__code
    
#     def getDateAdhesion(self):
#         return self.__DateAdhésion

#     def getNom(self):
#         return self.__nom
    
#     def getPrenom(self):
#         return self.__prenom

#     def to_dict(self):
#         return {"nom": self.getNom(), "prenom": self.getPrenom(), "dateAdhesion": self.__DateAdhésion.strftime('%Y-%m-%d'), "code": self.__code}

#     @classmethod
#     def from_dict(cls, data):
#         return cls(data["nom"], data["prenom"], date.fromisoformat(data["dateAdhesion"]), code=data["code"])

#     def __str__(self):
#         return f"{self.getNom()} {self.getPrenom()}, Code: {self.getCode()}, Date d'adhésion: {self.getDateAdhesion().day}/{self.getDateAdhesion().month}/{self.getDateAdhesion().year}"

#     def fidelite(self):
#         """Retourne la fidélité de l'adhérent (ex. nombre d'années d'adhésion)."""
#         return (date.today() - self.getDateAdhesion()).days // 365


class Application:
    def __init__(self, root):
        self.root = root
        
        self.nav_frame = CTkFrame(self.root)
        self.nav_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.bouton_adherents = CTkButton(self.nav_frame, text="Adhérents", command=self.afficher_page_adherents)
        self.bouton_adherents.grid(row=0, column=0, padx=10, pady=5)

        self.bouton_ajouter = CTkButton(self.nav_frame, text="Ajouter un Adhérent", command=self.afficher_page_ajouter)
        self.bouton_ajouter.grid(row=0, column=1, padx=10, pady=5)

        self.page_adherents = CTkFrame(self.root)
        self.page_ajouter = CTkFrame(self.root)

        self.liste_adherents_label = CTkLabel(self.page_adherents, text="Liste des adhérents", font=("Arial", 16))
        self.liste_adherents_label.grid(row=0, column=0, padx=20, pady=20)

        self.chercher_label = CTkLabel(self.page_adherents, text="Chercher par code ou nom:")
        self.chercher_label.grid(row=1, column=0, padx=10, pady=5)
        
        self.chercher_entry = CTkEntry(self.page_adherents)
        self.chercher_entry.grid(row=1, column=1, padx=10, pady=5)

        self.chercher_button = CTkButton(self.page_adherents, text="Chercher", command=self.chercher_adhérent)
        self.chercher_button.grid(row=1, column=2, padx=10, pady=5)

        self.revenir_button = CTkButton(self.page_adherents, text="Revenir à la liste", command=self.revenir_a_la_liste)
        self.revenir_button.grid(row=5, column=3, padx=10, pady=5)

        self.treeview = ttk.Treeview(self.page_adherents, columns=("Code", "Nom", "Prénom", "Date d'adhésion"), show="headings")
        self.treeview.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.treeview.heading("Code", text="Code")
        self.treeview.heading("Nom", text="Nom")
        self.treeview.heading("Prénom", text="Prénom")
        self.treeview.heading("Date d'adhésion", text="Date d'adhésion")

        self.treeview.column("Code", width=100)
        self.treeview.column("Nom", width=150)
        self.treeview.column("Prénom", width=150)
        self.treeview.column("Date d'adhésion", width=150)

        self.vider_button = CTkButton(self.page_adherents, text="Vider la liste", command=self.vider_liste_adhérent)
        self.vider_button.grid(row=4, column=0,  pady=10)

        self.supprimer_button = CTkButton(self.page_adherents, text="Supprimer un adhérent", command=self.supprimer_adhérent)
        self.supprimer_button.grid(row=4, column=1, pady=10)

        self.modifier_button = CTkButton(self.page_adherents, text="Modifier un Adhérent", command=self.modifier_adherent)
        self.modifier_button.grid(row=4, column=2, pady=10)

        self.nom_label = CTkLabel(self.page_ajouter, text="Nom:")
        self.nom_label.grid(row=0, column=0, padx=10, pady=5)

        self.nom_entry = CTkEntry(self.page_ajouter)
        self.nom_entry.grid(row=0, column=1, padx=10, pady=5)

        self.prenom_label = CTkLabel(self.page_ajouter, text="Prénom:")
        self.prenom_label.grid(row=1, column=0, padx=10, pady=5)

        self.prenom_entry = CTkEntry(self.page_ajouter)
        self.prenom_entry.grid(row=1, column=1, padx=10, pady=5)

        self.date_adhesion_label = CTkLabel(self.page_ajouter, text="Date d'adhésion (YYYY-MM-DD):")
        self.date_adhesion_label.grid(row=2, column=0, padx=10, pady=5)

        self.date_adhesion_entry = CTkEntry(self.page_ajouter)
        self.date_adhesion_entry.grid(row=2, column=1, padx=10, pady=5)

        self.ajouter_button = CTkButton(self.page_ajouter, text="Ajouter", command=self.ajouter_adherent)
        self.ajouter_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.retour_button = CTkButton(self.page_ajouter, text="Retour à Adhérents", command=self.afficher_page_adherents)
        self.retour_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.treeview_ajouter = ttk.Treeview(self.page_ajouter, columns=("Code", "Nom", "Prénom", "Date d'adhésion"), show="headings")
        self.treeview_ajouter.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        self.treeview_ajouter.heading("Code", text="Code")
        self.treeview_ajouter.heading("Nom", text="Nom")
        self.treeview_ajouter.heading("Prénom", text="Prénom")
        self.treeview_ajouter.heading("Date d'adhésion", text="Date d'adhésion")

        self.treeview_ajouter.column("Code", width=100)
        self.treeview_ajouter.column("Nom", width=150)
        self.treeview_ajouter.column("Prénom", width=150)
        self.treeview_ajouter.column("Date d'adhésion", width=150)

        self.afficher_adherents()

    def afficher_page_adherents(self):
        self.page_ajouter.grid_forget()  
        self.page_adherents.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")  
        self.vider_liste_adhérent()  
        self.afficher_adherents()  

    def afficher_page_ajouter(self):
        self.page_adherents.grid_forget()  
        self.page_ajouter.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")  

    def afficher_adherents(self):
        self.vider_liste_adhérent()  
        self.vider_liste_ajouter()   
        try:
            with open("Database/adherent.json", "r") as file:
                adherents_data = json.load(file)
                for adherent_data in adherents_data:
                    adherent = Adherent.from_dict(adherent_data)
                    self.treeview.insert("", "end", values=(adherent.getCode(), adherent.getNom(), adherent.getPrenom(), adherent.getDateAdhesion()))
                    self.treeview_ajouter.insert("", "end", values=(adherent.getCode(), adherent.getNom(), adherent.getPrenom(), adherent.getDateAdhesion()))
        except (FileNotFoundError, json.JSONDecodeError):
            pass


    def chercher_adhérent(self):
        code_ou_nom = self.chercher_entry.get().strip()  
        self.vider_liste_adhérent()  

        if not code_ou_nom: 
            return
        
        try:
            with open("Database/adherent.json", "r") as file:
                adherents_data = json.load(file)
                found = False  
                for adherent_data in adherents_data:
                    
                    if (str(adherent_data["code"]) == code_ou_nom) or (code_ou_nom.lower() in adherent_data["nom"].lower()) or (code_ou_nom.lower() in adherent_data["prenom"].lower()):
                        adherent = Adherent.from_dict(adherent_data)
                        self.treeview.insert("", "end", values=(adherent.getCode(), adherent.getNom(), adherent.getPrenom(), adherent.getDateAdhesion()))
                        found = True

                if not found:
                    messagebox.showinfo("Aucun résultat", "Aucun adhérent trouvé correspondant à votre recherche.")
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Erreur", "Le fichier des adhérents est introuvable ou endommagé.")
        
        self.chercher_entry.delete(0, END)


    def vider_liste_adhérent(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)

    def vider_liste_ajouter(self):
        for item in self.treeview_ajouter.get_children():
            self.treeview_ajouter.delete(item)


    def revenir_a_la_liste(self):
        self.afficher_page_adherents()
        
    def supprimer_adhérent(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un adhérent à supprimer.")
            return

        result = messagebox.askyesno("Confirmer la suppression", "Êtes-vous sûr de vouloir supprimer cet adhérent ?")
        if result:
            item = self.treeview.item(selected_item)
            code_to_delete = item['values'][0]

            try:
                with open("Database/adherent.json", "r") as file:
                    adherents_data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                adherents_data = []

            adherents_data = [adherent for adherent in adherents_data if adherent["code"] != code_to_delete]

            with open("Database/adherent.json", "w") as file:
                json.dump(adherents_data, file, indent=4)

            self.afficher_adherents() 

    def ajouter_adherent(self):
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        date_adhesion_str = self.date_adhesion_entry.get()

        try:
            date_adhesion = date.fromisoformat(date_adhesion_str)
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide. Utilisez le format YYYY-MM-DD.")
            return

        adherent = Adherent(nom, prenom, date_adhesion)

        try:
            with open("Database/adherent.json", "r") as file:
                adherents_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            adherents_data = []  

        adherents_data.append(adherent.to_dict())

        try:
            with open("Database/adherent.json", "w") as file:
                json.dump(adherents_data, file, indent=4)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde : {e}")
            return

        self.afficher_adherents()

        self.afficher_page_adherents()
        messagebox.showinfo("Succès", "Adhérent ajouté avec succès.")


    def modifier_adherent(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un adhérent à modifier.")
            return

        item = self.treeview.item(selected_item)
        code = item['values'][0]
        nom = item['values'][1]
        prenom = item['values'][2]
        date_adhesion = item['values'][3]

        self.modifier_window = CTkToplevel(self.root)
        self.modifier_window.title("Modifier un Adhérent")

        self.nom_label = CTkLabel(self.modifier_window, text="Nom:")
        self.nom_label.grid(row=0, column=0, padx=10, pady=5)
        self.nom_entry = CTkEntry(self.modifier_window)
        self.nom_entry.insert(0, nom)
        self.nom_entry.grid(row=0, column=1, padx=10, pady=5)

        self.prenom_label = CTkLabel(self.modifier_window, text="Prénom:")
        self.prenom_label.grid(row=1, column=0, padx=10, pady=5)
        self.prenom_entry = CTkEntry(self.modifier_window)
        self.prenom_entry.insert(0, prenom)
        self.prenom_entry.grid(row=1, column=1, padx=10, pady=5)

        self.date_adhesion_label = CTkLabel(self.modifier_window, text="Date d'adhésion:")
        self.date_adhesion_label.grid(row=2, column=0, padx=10, pady=5)
        self.date_adhesion_entry = CTkEntry(self.modifier_window)
        self.date_adhesion_entry.insert(0, date_adhesion)
        self.date_adhesion_entry.grid(row=2, column=1, padx=10, pady=5)

        self.sauvegarder_button = CTkButton(self.modifier_window, text="Sauvegarder", command=lambda: self.sauvegarder_modifications(code))
        self.sauvegarder_button.grid(row=3, column=0, columnspan=2, pady=10)

    def sauvegarder_modifications(self, code):
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        date_adhesion_str = self.date_adhesion_entry.get()

        try:
            date_adhesion = date.fromisoformat(date_adhesion_str)
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide. Utilisez le format YYYY-MM-DD.")
            return

        try:
            with open("Database/adherent.json", "r") as file:
                adherents_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            adherents_data = []

        for adherent in adherents_data:
            if adherent["code"] == code:
                adherent["nom"] = nom
                adherent["prenom"] = prenom
                adherent["dateAdhesion"] = date_adhesion.strftime('%Y-%m-%d')
                break

        with open("Database/adherent.json", "w") as file:
            json.dump(adherents_data, file, indent=4)

        self.afficher_adherents()
        self.modifier_window.destroy()
        messagebox.showinfo("Succès", "Les informations de l'adhérent ont été mises à jour.")


class AdhrentsList(CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)
        self.configure(fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=0, border_color=("#e2e8f0", "#1e1e1e"))
        Adherents = gestion.get_all_clients().values()
        # Header
        CTkLabel(self, text='Code', font=('Arial bold', 12), compound='center', justify='center', pady=6).grid(row=0, column=0)
        CTkLabel(self, text='Nom', font=('Arial bold', 12), compound='center', justify='center', pady=6).grid(row=0, column=1)
        CTkLabel(self, text='Prenom', font=('Arial bold', 12), compound='center', justify='center', pady=6).grid(row=0, column=2)
        CTkLabel(self, text='Date d\'adhésion', font=('Arial bold', 12), compound='center', justify='center', pady=6).grid(row=0, column=3)
        CTkLabel(self, text='Action', font=('Arial bold', 12), compound='center', justify='center', pady=6).grid(row=0, column=4)
        CTkFrame(self, height=2, width=1700, bg_color=("#e2e8f0", "#27272a"), border_width=0, fg_color=("#e2e8f0", "#27272a")).grid(row=1, column=0, columnspan=5)
        
        self.row = 2
        self.afficher_adherents(Adherents)
        self.columnconfigure((0, 1, 2, 3, 4), weight=1)

    def afficher_adherents(self, adhrs):
        Adherents = gestion.get_all_clients().values()
        for widget in self.grid_slaves():
            if int(widget.grid_info()["row"]) > 1:
                widget.grid_forget()
        
        for elt in adhrs:
            col = 0
            for SudoElt in [elt.getCode(), elt.get_nom(), elt.get_prenomm(), str(elt.getDateDateAdhésion())]:
                label = CTkLabel(self, text=str(SudoElt), justify="center", corner_radius=50, fg_color='transparent', pady=10)
                label.grid(row=self.row, column=col)
                col += 1
            ButtonsFrame = CTkFrame(self, fg_color='transparent')
            ButtonsFrame.grid(row=self.row, column=4)
            Modifier = CTkLabel(ButtonsFrame, text='', justify="center", compound='center', anchor='center', cursor='hand2', image=editIcon)
            Modifier.pack(side=LEFT, padx=5)
            Supp = CTkLabel(ButtonsFrame, text='', justify="center", compound='center', anchor='center', cursor='hand2', image=deletIcon)
            Supp.pack(side=RIGHT, padx=5)
            Modifier.bind("<Button-1>", lambda e, code=elt.getCode(): self.modifier_adherent(code))
            Supp.bind("<Button-1>", lambda e, code=elt.getCode(): self.supprimer_adhérent(code))
            self.row += 1

    def search_adherent(self, search_term):
        Adherents = gestion.get_all_clients().values()
        filtered_emprunts = [elt for elt in Adherents if search_term.lower() in str(elt.getCode()).lower() or search_term.lower() in str(elt.get_nom()).lower() or search_term.lower() in str(elt.get_prenomm()).lower()]
        self.row = 2
        self.afficher_adherents(filtered_emprunts)
    def modifier_adherent(self, code):
        Adherents = gestion.get_all_clients().values()
        adherents_list = gestion.get_all_clients()
        Adrnt = adherents_list[code]
        nom = Adrnt.get_nom()
        prenom = Adrnt.get_prenomm()
        date_adhesion = Adrnt.getDateDateAdhésion()

        self.modifier_window = CTkToplevel(self)
        self.modifier_window.title("Modifier un Adhérent")

        self.nom_label = CTkLabel(self.modifier_window, text="Nom:")
        self.nom_label.grid(row=0, column=0, padx=10, pady=5)
        self.nom_entry = CTkEntry(self.modifier_window)
        self.nom_entry.insert(0, nom)
        self.nom_entry.grid(row=0, column=1, padx=10, pady=5)

        self.prenom_label = CTkLabel(self.modifier_window, text="Prénom:")
        self.prenom_label.grid(row=1, column=0, padx=10, pady=5)
        self.prenom_entry = CTkEntry(self.modifier_window)
        self.prenom_entry.insert(0, prenom)
        self.prenom_entry.grid(row=1, column=1, padx=10, pady=5)

        self.date_adhesion_label = CTkLabel(self.modifier_window, text="Date d'adhésion:")
        self.date_adhesion_label.grid(row=2, column=0, padx=10, pady=5)
        self.date_adhesion_entry = CTkEntry(self.modifier_window)
        self.date_adhesion_entry.insert(0, date_adhesion)
        self.date_adhesion_entry.grid(row=2, column=1, padx=10, pady=5)

        self.sauvegarder_button = CTkButton(self.modifier_window, text="Sauvegarder", command=lambda : self.Enrg(code))
        self.sauvegarder_button.grid(row=3, column=0, columnspan=2, pady=10)

        
    def Enrg(self, code):
        Adherents = gestion.get_all_clients().values()
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        date_adhesion_str = self.date_adhesion_entry.get()

        try:
            date_adhesion = date.fromisoformat(date_adhesion_str)
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide. Utilisez le format YYYY-MM-DD.")
            return
        if messagebox.askyesno('Modifier d\'un Adherent', f'Êtes-vous sûr de vouloir modifier cet adhérent N° {code} ?'):
            try:
                gestion.modifierAdherent(code, nom, prenom, date_adhesion)
                self.afficher_adherents(Adherents)
                self.modifier_window.destroy()
                messagebox.showinfo('Succes', 'Les informations de l\'adhérent ont été mises à jour.')
            except Exception as e:
                messagebox.showerror('Erreur', str(e))
                print(e)


    def supprimer_adhérent(self, code):
        Adherents = gestion.get_all_clients().values()
        if messagebox.askyesno('Supprimer d\'un Adherent', f'Êtes-vous sûr de vouloir supprimer cet adhérent N° {code} ?'):
            try:
                gestion.supprimerAdherent(code)
                self.afficher_adherents(Adherents)
                messagebox.showinfo('Succes', 'Adherent supprime avec succes')
            except Exception as e:
                messagebox.showerror('Erreur', str(e))
                print(e)
class AjouterAdhr(CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(expand=True, pady=10, padx=20)
        self.configure(fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#1e1e1e"))
        
        label_title = CTkLabel(self , text="Ajouter un Adherent", font=("Arial", 20, "bold"))
        label_title.grid(row=0, column=0, columnspan=2, pady=10)
        self.nom_label = CTkLabel(self, text="Nom:")
        self.nom_label.grid(row=1, column=0, padx=10, pady=5)

        self.nom_entry = CTkEntry(self)
        self.nom_entry.grid(row=1, column=1, padx=10, pady=5)

        self.prenom_label = CTkLabel(self, text="Prénom:")
        self.prenom_label.grid(row=2, column=0, padx=10, pady=5)

        self.prenom_entry = CTkEntry(self)
        self.prenom_entry.grid(row=2, column=1, padx=10, pady=5)

        self.date_adhesion_label = CTkLabel(self, text="Date d'adhésion (YYYY-MM-DD):")
        self.date_adhesion_label.grid(row=3, column=0, padx=10, pady=5)

        self.date_adhesion_entry = DateEntry(self, date_pattern='yyyy-mm-dd', height=10)
        self.date_adhesion_entry.grid(row=3, column=1, padx=10, pady=5)

        self.ajouter_button = CTkButton(self, text="Ajouter", fg_color=("#0078D7", "#005A9E"), text_color="#fff",
                            hover_color=("#005A9E", "#004680"), corner_radius=8, command=self.Ajouter)
        self.ajouter_button.grid(row=4, column=0, columnspan=2, pady=10)

    def Ajouter(self):
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        date_adhesion_str = self.date_adhesion_entry.get_date()
        if len(nom) == 0 or len(prenom) == 0:
            messagebox.showerror("Erreur", 'Veuillez remplir tous les champs!')
            return

        try:
            gestion.ajouterAdherent(nom, prenom, date_adhesion_str)
            messagebox.showinfo('Succes', 'Adherent a ete ajoute avec succes')
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            return
        



# app = CTk()
# Adh = AjouterAdhr(app)
# app.mainloop()