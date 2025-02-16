from tkinter import *
from tkinter import messagebox
from tkcalendar import *
from tkinter import ttk
from customtkinter import *
import PIL
from PIL import ImageTk
from Bilio import *
import json
import json as js
from Adherent import Adherent
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from chart import *
from livre import *
from tkinter import TOP, X
import shutil
import os



#Gestion
gestion = Biblio()
gestion.load_data()
totalBooks = len(gestion.get_livres())
Emprnts = gestion.get_all_emprunts()
TotalCopies = gestion.getTotalCopies()
availableBooks = len(gestion.get_available_books())
TotalAvailableCopies = gestion.getTotalAvailableCopies()
borrowedBooks = TotalCopies - TotalAvailableCopies
totalClients = len(gestion.get_all_clients())
top5Books = gestion.TopLivres()


def defaultSettings():
    try:
        with open("Database/settings.json", "r") as file:
            data_dict = js.load(file)
        theme = data_dict["theme"]
        set_appearance_mode(theme)
        changeTheme(chart, theme,  7, "Database/Emprunts.txt")
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        set_appearance_mode("light")
        changeTheme(chart, "light", 7, "Database/Emprunts.txt")




def change_theme():
    if get_appearance_mode() == "Dark":
        set_appearance_mode("light")
        Modevr.set("Light mode")
        changeTheme(chart, "light", 7, "Database/Emprunts.txt")
    else:
        set_appearance_mode("dark")


        Modevr.set("Dark mode")
        changeTheme(chart, "dark", 7, "Database/Emprunts.txt")


    update_menu_colors()
def hideShowSideBar():
    if sideMenu.winfo_ismapped():
        sideMenu.pack_forget()
        border.configure(cursor="sb_right_arrow")
    else:
        main.pack_forget()
        border.pack_forget()
        sideMenu.pack(side=LEFT, fill=Y)
        border.pack(side=LEFT, fill=Y)
        main.pack(side=LEFT, fill=BOTH, expand=YES)
        border.configure(cursor="sb_left_arrow")
def BtnColor(button):
    btnList = [dashboard, books, clients, AddBook, AddLoan, settings, Loans, AddClient]
    for btn in btnList:
        if btn.cget("text").strip() == button:
            btn.configure(fg_color=btnActiveColor, hover=False)
        else:
            btn.configure(hover=True,fg_color=bgColor)
    global currentFrame
    if button == "Accueil":
        TitleMain.configure(text="Accueil")
        currentFrame = "Accueil"
    elif button == "Livres":
        TitleMain.configure(text="Livres")
        currentFrame = "Livres"
    elif button == "Adherents":
        TitleMain.configure(text="Adherents")
        currentFrame = "Adherents"
    elif button == "Emprunts":
        TitleMain.configure(text="Emprunts")
        currentFrame = "Emprunts"
    elif button == "Ajouter un livre":
        TitleMain.configure(text="Ajouter un livre")
        currentFrame = "Ajouter un livre"
    elif button == "Ajouter un emprunt":
        TitleMain.configure(text="Ajouter un emprunt")
        currentFrame = "Ajouter un emprunt"
    elif button == "Ajouter un adherent":
        TitleMain.configure(text="Ajouter un adherent")
        currentFrame = "Ajouter un adherent"
    elif button == "Paramètres":
        TitleMain.configure(text="Paramètres")
        currentFrame = "Paramètres"




def update_menu_colors():
    current_mode = get_appearance_mode()
    if current_mode == "Dark":
        bg_color = bgColor[1]
        fg_color = "#ffffff"
        active_bg = btnActiveColor[1]
        active_fg = "#ffffff"
    else:
        bg_color = bgColor[0]
        fg_color = "#000000"
        active_bg = btnActiveColor[0]
        active_fg = "#000000"

    menu_font = ("Arial", 12)
    menubar.configure(background=bg_color, foreground=fg_color,
                      activebackground=active_bg, activeforeground=active_fg,
                      font=menu_font, borderwidth=0)
    for menu in [file, edit, view, help_, mode, zoom]:
        menu.configure(background=bg_color, foreground=fg_color,
                       activebackground=active_bg, activeforeground=active_fg,
                       font=menu_font, borderwidth=0, border=0)
def updateMain(frame):
    dashboardContent.pack_forget()
    livresContent.pack_forget()
    adherentsContent.pack_forget()
    empruntsContent.pack_forget()
    ajouterLivreContent.pack_forget()
    ajouterEmpruntContent.pack_forget()
    ajouterAdherentContent.pack_forget()
    parametresContent.pack_forget()
    if frame == "Accueil":
        dashboardContent.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)
    elif frame == "Livres":
        livresContent.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)
    elif frame == "Adherents":
        adherentsContent.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)
    elif frame == "Emprunts":
        empruntsContent.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)
    elif frame == "Ajouter un livre":
        ajouterLivreContent.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)
    elif frame == "Ajouter un emprunt":
        ajouterEmpruntContent.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)
    elif frame == "Ajouter un adherent":
        ajouterAdherentContent.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)
    elif frame == "Paramètres":
        parametresContent.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)
    else:
        dashboardContent.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)
def updateStats():
    global totalBooks, availableBooks, borrowedBooks, totalClients, TotalCopies, TotalAvailableCopies, top5Books


    totalBooks = len(gestion.get_livres())
    TotalCopies = gestion.getTotalCopies()
    availableBooks = len(gestion.get_available_books())
    TotalAvailableCopies = gestion.getTotalAvailableCopies()
    borrowedBooks = TotalCopies - TotalAvailableCopies
    totalClients = len(gestion.get_all_clients())
    top5Books = gestion.TopLivres()

set_appearance_mode("dark")
currentFrame="Accueil"
app = CTk()
app.title("Bibliotheque")
app.geometry("1000x600")
app.iconbitmap("images/logo.ico")



#Colors
bgColor = ("#fff", "#18181b")
mainColor = ("#fff", "#09090b")
btnActiveColor = ("#3fdfff", "#00b4d8")

#Icons
logoImage = CTkImage(PIL.Image.open("images/logo.png"), size=(30, 30))
ThemeIcon = CTkImage(dark_image=PIL.Image.open("images/moon.png"),light_image=PIL.Image.open("images/sun.png") ,size=(20, 20))
dashboardIcon = CTkImage(dark_image=PIL.Image.open("images/homeLight.png"),light_image=PIL.Image.open("images/home.png"), size=(15, 15))
plusIcon = CTkImage(dark_image=PIL.Image.open("images/plusLight.png"),light_image=PIL.Image.open("images/plus.png"), size=(15, 15))
plusIconLight = CTkImage(PIL.Image.open("images/plusLight.png"), size=(15, 15))
bookIcon = CTkImage(dark_image=PIL.Image.open("images/bookLight.png"),light_image=PIL.Image.open("images/book.png"), size=(15, 15))
clientsIcon = CTkImage(dark_image=PIL.Image.open("images/clientsLight.png"),light_image=PIL.Image.open("images/clients.png"), size=(15, 15))
loanIcon = CTkImage(dark_image=PIL.Image.open("images/loanLight.png"),light_image=PIL.Image.open("images/loan.png"), size=(15, 15))
settingsIcon = CTkImage(dark_image=PIL.Image.open("images/settingsLight.png"),light_image=PIL.Image.open("images/settings.png"), size=(15, 15))
AddClientIcon = CTkImage(dark_image=PIL.Image.open("images/user-addLight.png"),light_image=PIL.Image.open("images/user-add.png"), size=(15, 15))
expandIcon = CTkImage(dark_image=PIL.Image.open("images/sidebarLight.png"),light_image=PIL.Image.open("images/sidebar.png"), size=(20, 20))
stockIcon = CTkImage(PIL.Image.open("images/stock.png"), size=(15, 15))
exitIcon = CTkImage(PIL.Image.open("images/exit.png"), size=(15, 15))
penIcon = CTkImage(PIL.Image.open("images/pen.png"), size=(20, 20))







#Side Menu----------------------------------------------------------------------
sideMenu = CTkFrame(app, fg_color=bgColor, bg_color=bgColor, border_width=0)
TitleFrame = CTkFrame(sideMenu, border_width=0, fg_color=bgColor)
sideTitle = CTkLabel(TitleFrame, text=" MaBibliotheque        ", font=("Arial", 20), fg_color=bgColor, justify="left", compound="left", anchor="w", bg_color=bgColor, image=logoImage)
ThemeBtn = CTkButton(TitleFrame, text="", image=ThemeIcon, width=40, height=40, fg_color=mainColor, bg_color=bgColor, hover_color=("#e2e8f0", "#27272a"), command=change_theme, border_width=1, border_color=("#e2e8f0","#27272a"))

BtnFrame = CTkFrame(sideMenu, fg_color=bgColor, border_width=0)
CTkLabel(BtnFrame, text="Menu", font=("Arial", 13, "bold"), bg_color=bgColor, justify="left", compound="left", anchor="w").pack(side=TOP, fill=X, padx=5, pady=0)
dashboard = CTkButton(BtnFrame, text="  Accueil", fg_color=bgColor, bg_color=bgColor, hover_color=("#e2e8f0", "#27272a"), border_width=0, text_color=("#000", "#fff"), font=("Arial", 15), cursor="hand2", image=dashboardIcon, compound="left", anchor="w", height=33, command=lambda: BtnColor("Accueil") & updateMain("Accueil"))
books = CTkButton(BtnFrame, text="  Livres", fg_color=bgColor, bg_color=bgColor, hover_color=("#e2e8f0", "#27272a"), border_width=0, text_color=("#000", "#fff"), font=("Arial", 15), cursor="hand2", image=bookIcon, compound="left", anchor="w", height=33, command=lambda: BtnColor("Livres") & updateMain("Livres"))
clients = CTkButton(BtnFrame, text="  Adherents", fg_color=bgColor, bg_color=bgColor, hover_color=("#e2e8f0", "#27272a"), border_width=0, text_color=("#000", "#fff"), font=("Arial", 15), cursor="hand2", image=clientsIcon, compound="left", anchor="w", height=33, command=lambda: BtnColor("Adherents") & updateMain("Adherents"))
Loans = CTkButton(BtnFrame, text="  Emprunts", fg_color=bgColor, bg_color=bgColor, hover_color=("#e2e8f0", "#27272a"), border_width=0, text_color=("#000", "#fff"), font=("Arial", 15), cursor="hand2", image=loanIcon, compound="left", anchor="w", height=33, command=lambda: BtnColor("Emprunts") & updateMain("Emprunts"))
AddBook = CTkButton(BtnFrame, text="  Ajouter un livre", fg_color=bgColor, bg_color=bgColor, hover_color=("#e2e8f0", "#27272a"), border_width=0, text_color=("#000", "#fff"), font=("Arial", 15), cursor="hand2", image=plusIcon, compound="left", anchor="w", height=33, command=lambda: BtnColor("Ajouter un livre") & updateMain("Ajouter un livre"))
AddLoan = CTkButton(BtnFrame, text="  Ajouter un emprunt", fg_color=bgColor, bg_color=bgColor, hover_color=("#e2e8f0", "#27272a"), border_width=0, text_color=("#000", "#fff"), font=("Arial", 15), cursor="hand2", image=loanIcon, compound="left", anchor="w", height=33, command=lambda: BtnColor("Ajouter un emprunt") & updateMain("Ajouter un emprunt"))
AddClient = CTkButton(BtnFrame, text="  Ajouter un adherent", fg_color=bgColor, bg_color=bgColor, hover_color=("#e2e8f0", "#27272a"), border_width=0, text_color=("#000", "#fff"), font=("Arial", 15), cursor="hand2", image=AddClientIcon, compound="left", anchor="w", height=33, command=lambda: BtnColor("Ajouter un adherent") & updateMain("Ajouter un adherent"))
settings = CTkButton(BtnFrame, text="  Paramètres", fg_color=bgColor, bg_color=bgColor, hover_color=("#e2e8f0", "#27272a"), border_width=0, text_color=("#000", "#fff"), font=("Arial", 15), cursor="hand2", image=settingsIcon, compound="left", anchor="w", height=33, command=lambda: BtnColor("Paramètres") & updateMain("Paramètres"))

Exit = CTkButton(BtnFrame, text="  Quitter", fg_color=bgColor, bg_color=bgColor, border_width=1, border_color="red", text_color=("red", "red"), font=("Arial", 15), cursor="hand2", image=exitIcon, compound="left", anchor="w", height=33, hover=False, command=lambda: app.destroy())


#border
border = CTkFrame(app, width=2, height=600, bg_color=("#e2e8f0", "#27272a"), border_width=0, fg_color=("#e2e8f0", "#27272a"), cursor="sb_left_arrow")
border.bind("<Button-1>", lambda e: hideShowSideBar())

#main----------------------------------------------------------------------
main = CTkFrame(app, fg_color=mainColor, border_width=0)
#-----Title
MainFrame = CTkFrame(main, border_width=0, fg_color=mainColor)
FrameTitle = CTkFrame(MainFrame, border_width=0, fg_color=mainColor)
TitleMain = CTkLabel(FrameTitle, text="Dashboard", font=("Arial", 30), compound="left", anchor="w")
expandBtn = CTkButton(FrameTitle, text="", image=expandIcon, width=40, height=40, fg_color=mainColor, bg_color=bgColor, hover_color=("#e2e8f0", "#27272a"), command=hideShowSideBar, border_width=1, border_color=("#e2e8f0","#27272a"))
vBorder = CTkFrame(MainFrame, width=800, height=2, bg_color=("#e2e8f0", "#27272a"), border_width=0, fg_color=("#e2e8f0", "#27272a"))
#-----Content
mainContent = CTkFrame(main, border_width=0, fg_color=mainColor)

#--------Dashboard------------------------------------------------------------------
dashboardContent = CTkScrollableFrame(mainContent, border_width=0, fg_color=mainColor)
dashboardContent.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)


statsFrame = CTkFrame(dashboardContent, fg_color=mainColor)


totalBooksFrame = CTkFrame(statsFrame, fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#1e1e1e"))
CTkLabel(totalBooksFrame, text="Total de livres", font=("Arial", 15, "bold"), justify="left", anchor="w", compound="left").pack(pady=(15,5), padx=15, anchor="w")
CTkLabel(totalBooksFrame, text=TotalCopies, font=("Arial", 25)).pack(pady=(0,0), padx=15, anchor="w")
CTkLabel(totalBooksFrame, text="+20% par rapport au mois précédent", font=("Arial", 10), justify="left", anchor="w", compound="left", text_color=("#27272a", "#e3e8f0")).pack(pady=(0,3), padx=15, anchor="w")


availableBooksFrame = CTkFrame(statsFrame, fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#1e1e1e"))
CTkLabel(availableBooksFrame, text="Livres disponibles", font=("Arial", 15, "bold"), justify="left", anchor="w", compound="left").pack(pady=(15,5), padx=15, anchor="w")
CTkLabel(availableBooksFrame, text=TotalAvailableCopies, font=("Arial", 25)).pack(pady=(0,0), padx=15, anchor="w")
CTkLabel(availableBooksFrame, text="+10% par rapport au mois précédent", font=("Arial", 10), justify="left", anchor="w", compound="left", text_color=("#27272a","#e3e8f0")).pack(pady=(0,3), padx=15, anchor="w")


borrowedBooksFrame = CTkFrame(statsFrame, fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#1e1e1e"))
CTkLabel(borrowedBooksFrame, text="Livres empruntés", font=("Arial", 15, "bold"), justify="left", anchor="w", compound="left").pack(pady=(15,5), padx=15, anchor="w")
CTkLabel(borrowedBooksFrame, text=borrowedBooks, font=("Arial", 25)).pack(pady=(0,0), padx=15, anchor="w")
CTkLabel(borrowedBooksFrame, text="+10% par rapport au mois précédent", font=("Arial", 10), justify="left", anchor="w", compound="left", text_color=("#27272a","#e3e8f0")).pack(pady=(0,3), padx=15, anchor="w")


totalClientsFrame = CTkFrame(statsFrame, fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#1e1e1e"))
CTkLabel(totalClientsFrame, text="Total de clients", font=("Arial", 15, "bold"), justify="left", anchor="w", compound="left").pack(pady=(15,5), padx=15, anchor="w")
CTkLabel(totalClientsFrame, text=totalClients, font=("Arial", 25)).pack(pady=(0,0), padx=15, anchor="w")
CTkLabel(totalClientsFrame, text="+10% par rapport au mois précédent", font=("Arial", 10), justify="left", anchor="w", compound="left", text_color=("#27272a","#e3e8f0")).pack(pady=(0,3), padx=15, anchor="w")

#Recent Activity
recentFrame = CTkScrollableFrame(dashboardContent, fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#1e1e1e"), label_text="Activité récente", label_font=("Arial", 20, "bold"), label_text_color=("#000", "#fff"), label_fg_color=("#fff", "#1e1e1e"), label_anchor="w")
recentActivitiesFile = open("Database/recentActivities.txt", "r")
recentActivities = recentActivitiesFile.readlines()
recentActivities.reverse()
class RecentActivity(CTkFrame):
    def __init__(self, parent, text, font, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(side=TOP, fill=BOTH, expand=True, padx=5)
        self.activity = CTkLabel(self, text=text, font=font)
        self.activity.pack(side=LEFT, pady=5, padx=10, anchor="w", expand=False)
        self.configure(fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=0, border_color=("#e2e8f0", "#1e1e1e"))
for activity in recentActivities:
    if activity != "\n":
        RecentActivity(recentFrame, text=f"{activity.strip("\n")}", font=("Arial", 15))
recentActivitiesFile.close()



#Top 5 Books
class BookListItem(CTkFrame):
    def __init__(self, parent, name, nbrEmprunt, auteur, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(side=TOP, fill=X, expand=False, padx=5, pady=1)
        self.configure(fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=0, border_color=("#e2e8f0", "#1e1e1e"))
        self.rankCircle = CTkLabel(self, text=f"{i+1}", font=("Arial", 15, "bold"), fg_color=("#1e1e1e", "#fff"), corner_radius=100, width=40, height=40, text_color=("#fff", "#1e1e1e"))
        self.rankCircle.pack(side=LEFT, padx=10, pady=10)
        self.bookInfoFrame = CTkFrame(self, fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=0, border_color=("#e2e8f0", "#1e1e1e"))
        self.bookInfoFrame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=0)
        self.bookTitle = CTkLabel(self.bookInfoFrame, text=f"{name}", font=("Arial Bold", 15), justify="left", anchor="w")
        self.bookTitle.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=0, anchor="w")
        self.bookAuthor = CTkLabel(self.bookInfoFrame, text=f"de {auteur}", font=("Arial", 15), justify="left", anchor="w", text_color=("#666666", "#b5b5b5"))
        self.bookAuthor.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=0, anchor="w")
        self.NbrEmprunt = CTkLabel(self, text=f"   {nbrEmprunt}   ", font=("Arial", 15), justify="right", anchor="e", compound="left", image=loanIcon, text_color=("#666666", "#b5b5b5"))
        self.NbrEmprunt.pack(side=RIGHT, fill=X, expand=True, padx=5, pady=0, anchor="e")
class BookListItem2(CTkFrame):
    def __init__(self, parent, name, nbrDisponible, auteur, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(side=TOP, fill=X, expand=False, padx=5, pady=2)
        self.configure(fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=0, border_color=("#e2e8f0", "#1e1e1e"))
        self.bookInfoFrame = CTkFrame(self, fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=0, border_color=("#e2e8f0", "#1e1e1e"))
        self.bookInfoFrame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=0)
        self.bookTitle = CTkLabel(self.bookInfoFrame, text=f"{name}", font=("Arial Bold", 15), justify="left", anchor="w")
        self.bookTitle.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=0, anchor="w")
        self.bookAuthor = CTkLabel(self.bookInfoFrame, text=f"de {auteur}", font=("Arial", 15), justify="left", anchor="w", text_color=("#666666", "#b5b5b5"))
        self.bookAuthor.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=0, anchor="w")
        self.NbrDisponible = CTkLabel(self, text=f"   {nbrDisponible}   ", font=("Arial", 15), justify="right", anchor="e", compound="left", image=stockIcon, text_color="red")
        self.NbrDisponible.pack(side=RIGHT, fill=X, expand=True, padx=5, pady=0, anchor="e")







top5BooksFrame = CTkFrame(dashboardContent, fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#1e1e1e"))
CTkLabel(top5BooksFrame, text="Top 5 Livres", font=("Arial", 20, "bold")).pack(pady=(20,10), padx=20, anchor="w")
for i in range(5) if len(top5Books) >= 5 else range(len(top5Books)):
    book = top5Books[i]
    BookListItem(top5BooksFrame, book.get_titre(), book.getNbrEmprunt(), str(f"{book.get_auteur().get_nom()} {book.get_auteur().get_prenomm()}"))


bottomFrame = CTkFrame(dashboardContent, fg_color=mainColor, border_width=0, corner_radius=0, bg_color=mainColor)
bottomFrame.pack(side=BOTTOM, fill=BOTH, expand=False, padx=(0,5))

outOfStockFrame = CTkFrame(bottomFrame, fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#1e1e1e"))

CTkLabel(outOfStockFrame, text="Livres non disponibles ou presque", font=("Arial", 20, "bold")).pack(pady=(20,10), padx=20, anchor="w")
outOfStockBooks = gestion.get_livres_non_disponibles()
for book in outOfStockBooks:
    BookListItem2(outOfStockFrame, book.get_titre(), book.get_nbr_exemplaire_disponible(), str(f"{book.get_auteur().get_nom()} {book.get_auteur().get_prenomm()}"))

#Chart
chartFrame = CTkFrame(bottomFrame   , fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#1e1e1e"))
CTitleFrame = CTkFrame(chartFrame, fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=0, border_color=("#e2e8f0", "#1e1e1e"))
CTkLabel(CTitleFrame, text="Les emprunts", font=("Arial", 20, "bold")).pack(side=LEFT, pady=0, padx=0, anchor="w")

chart = CTkFrame(chartFrame, fg_color=("#fff", "#1e1e1e"), bg_color=("#fff", "#1e1e1e"), border_width=0)
chart.pack(side=BOTTOM, fill=BOTH, expand=True, padx=10, pady=10)

controlFrame = CTkFrame(CTitleFrame, fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=0)
controlFrame.pack(side=RIGHT, fill=Y, padx=0, pady=0)

CTkLabel(controlFrame, text="Periode : ", font=("Arial", 15, "bold")).pack(side=LEFT, padx=5, pady=5)
rangeSelector = CTkComboBox(controlFrame, values=["7", "14", "30"], width=80, command=lambda x: change_range(x))
rangeSelector.set("7")
rangeSelector.pack(side=RIGHT, padx=5, pady=5)

def change_range(days):
    try:
        changeDayrange(chart, days, get_appearance_mode().lower(), "Database/Emprunts.txt")
    except ValueError:
        pass




histogram = LoanChart(7, get_appearance_mode().lower(), "Database/Emprunts.txt")
histogram.embed_in_tkinter(chart)




def refreshDashboard():
    updateStats()
    totalBooksFrame.winfo_children()[1].configure(text=TotalCopies)
    availableBooksFrame.winfo_children()[1].configure(text=TotalAvailableCopies)
    borrowedBooksFrame.winfo_children()[1].configure(text=borrowedBooks)
    totalClientsFrame.winfo_children()[1].configure(text=totalClients)
    for widget in recentFrame.winfo_children():
        widget.destroy()
    recentActivitiesFile = open("Database/recentActivities.txt", "r")
    recentActivities = recentActivitiesFile.readlines()
    recentActivities.reverse()
    for activity in recentActivities:
        if activity != "\n":
            RecentActivity(recentFrame, text=f"{activity.strip()}", font=("Arial", 15))
    recentActivitiesFile.close()
    for widget in top5BooksFrame.winfo_children()[1:]:
        widget.destroy()
    for i in range(5) if len(top5Books) >= 5 else range(len(top5Books)):
        book = top5Books[i]
        BookListItem(top5BooksFrame, book.get_titre(), book.getNbrEmprunt(), str(f"{book.get_auteur().get_nom()} {book.get_auteur().get_prenomm()}"))
    for widget in outOfStockFrame.winfo_children()[1:]:
        widget.destroy()
    outOfStockBooks = gestion.get_livres_non_disponibles()
    for book in outOfStockBooks:
        BookListItem2(outOfStockFrame, book.get_titre(), book.get_nbr_exemplaire_disponible(), str(f"{book.get_auteur().get_nom()} {book.get_auteur().get_prenomm()}"))
    changeDayrange(chart, rangeSelector.get(), get_appearance_mode().lower(), "Database/Emprunts.txt")







#Position
statsFrame.pack(side=TOP, fill=X, pady=(0,10))
totalBooksFrame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0,5))
bottomFrame.pack(side=BOTTOM, fill=BOTH, expand=TRUE, pady=10)
availableBooksFrame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0,5))
borrowedBooksFrame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0,5))
totalClientsFrame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0,5))
recentFrame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0,5))
top5BooksFrame.pack(side=LEFT, fill=BOTH, expand=False, padx=(0,5))
outOfStockFrame.pack(side=LEFT, fill=BOTH, expand=False, padx=(0,5))
chartFrame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0,5))
CTitleFrame.pack(side=TOP, fill=X, pady=(20,10), padx=20)




#-----------------------------------------------------------------------------



# -------Livres-------------------------------------------------------------------

livresContent = CTkFrame(mainContent, border_width=0, fg_color=mainColor)
livresContent.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)

# -------Adherents-------------------------------------------------------------------
adherentsContent = CTkFrame(mainContent, border_width=0, fg_color=mainColor)
adherentsContent.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)

# -------Emprunts-------------------------------------------------------------------
empruntsContent = CTkFrame(mainContent, border_width=0, fg_color=mainColor)
empruntsContent.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)
searchFrame = CTkFrame(empruntsContent, fg_color='transparent', corner_radius=10, border_width=1, border_color=("#e2e8f0", "#1e1e1e"))
searchInput = CTkEntry(searchFrame, placeholder_text='Rechercher par livre, code Emprunt, Adherent', fg_color=("#fff", "#1e1e1e"), corner_radius=7, border_width=1, border_color=("#e2e8f0", "#1e1e1e"), height=35)
filterCombo = CTkComboBox(searchFrame, values=['tous', 'rendu','en cours', 'non rendu'], corner_radius=7, height=35, fg_color=("#e2e8f0", "#27272a"), button_color=("#e2e8f0", "#27272a"), button_hover_color="#515153", border_color=("#e2e8f0", "#27272a"), command=lambda e: Emp.filter(e))
AddEmp = CTkButton(searchFrame, text='Ajouter', fg_color=('#000', '#1e1e1e'), corner_radius=7, border_width=0, border_color=("#e2e8f0", "#1e1e1e"), height=35, text_color="#fff",hover_color=('#515153','#515153'), compound='left', anchor='center', image=plusIconLight, cursor='hand2', command=lambda: BtnColor("Ajouter un emprunt") & updateMain("Ajouter un emprunt"))
EmpruntsFrame = CTkScrollableFrame(empruntsContent, fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#1e1e1e"))

class EmpruntItem(CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)
        self.configure(fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=0, border_color=("#e2e8f0", "#1e1e1e"))
        
        # Header
        CTkLabel(self, text='ID', font=('Arial bold', 12), compound='center', justify='center', pady=6).grid(row=0, column=0)
        CTkLabel(self, text='Livre', font=('Arial bold', 12), compound='center', justify='center', pady=6).grid(row=0, column=1)
        CTkLabel(self, text='Empruteur', font=('Arial bold', 12), compound='center', justify='center', pady=6).grid(row=0, column=2)
        CTkLabel(self, text='Etat', font=('Arial bold', 12), compound='center', justify='center', pady=6).grid(row=0, column=3)
        CTkLabel(self, text='Date de retour prevue', font=('Arial bold', 12), compound='center', justify='center', pady=6).grid(row=0, column=4)
        CTkLabel(self, text='Date de retour effective', font=('Arial bold', 12), compound='center', justify='center', pady=6).grid(row=0, column=5)
        CTkLabel(self, text='Action', font=('Arial bold', 12), compound='center', justify='center', pady=6).grid(row=0, column=6)
        CTkFrame(self, height=2, width=1700, bg_color=("#e2e8f0", "#27272a"), border_width=0, fg_color=("#e2e8f0", "#27272a")).grid(row=1, column=0, columnspan=7)
        
        self.row = 2
        self.display_emprunts(Emprnts)
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

    def display_emprunts(self, emprunts):
        for widget in self.grid_slaves():
            if int(widget.grid_info()["row"]) > 1:
                widget.grid_forget()
        
        for elt in emprunts:
            col = 0
            dREff = elt.getDateRetourEffective() if elt.getDateRetourEffective() else '-'
            for SudoElt in [elt.getCode(), elt.getLivreEmprunte().get_titre(), str(elt.getEmprunteurLivre().get_nom() +" "+ elt.getEmprunteurLivre().get_prenomm()), elt.etatEmprunt(), elt.getDateRetourPrevue(), dREff]:
                if len(str(SudoElt)) >= 20:
                    text = str(SudoElt)[:21]+'...'
                else:
                    text = str(SudoElt)
                if str(SudoElt) == 'rendu':
                    bg = '#77c67c'
                    pdy = 0
                elif str(SudoElt) == 'en cours':
                    bg = ('#63f3fd', '#00ccff')
                    pdy = 0
                elif str(SudoElt) == 'non rendu':
                    bg = '#ff1900'
                    pdy = 0
                else:
                    bg = 'transparent'
                    pdy = 15
                label = CTkLabel(self, text=text, justify="center", corner_radius=50, fg_color=bg, pady=pdy)
                label.grid(row=self.row, column=col)
                col += 1
            Action = CTkLabel(self, text='', justify="center", compound='center', anchor='center', image=penIcon, cursor='hand2')
            Action.grid(row=self.row, column=6)
            Action.bind("<Button-1>", lambda e, code=elt.getCode(): self.retour(code))
            self.row += 1

    def search_emprunts(self, search_term):
        filtered_emprunts = [elt for elt in Emprnts if search_term.lower() in elt.getLivreEmprunte().get_titre().lower() or search_term.lower() in str(elt.getCode()).lower() or search_term.lower() in str(elt.getEmprunteurLivre().code).lower() or search_term.lower() in str(f'{elt.getEmprunteurLivre().get_nom()} {elt.getEmprunteurLivre().get_prenomm()}').lower()]
        self.row = 2
        self.display_emprunts(filtered_emprunts)

    def filter(self, filter):
        if filter == 'tous':
            self.display_emprunts(Emprnts)
            return
        filtered_emprunts = [elt for elt in Emprnts if elt.etatEmprunt() == filter]
        self.row = 2
        self.display_emprunts(filtered_emprunts)

    def retour(self, code):
        if messagebox.askyesno('Retour d\'un emprunt', f'Etes-vous sur de vouloir retourner l\'emprunt N° {code}?'):
            try:
                gestion.retourEmprunt(code)
                self.display_emprunts(Emprnts)
                messagebox.showinfo('Succes', 'Emprunt retourne avec succes')
            except Exception as e:
                messagebox.showerror('Erreur', str(e))
                print(e)

Emp = EmpruntItem(EmpruntsFrame)

def on_search(event):
    keyword = searchInput.get()
    Emp.search_emprunts(keyword)

searchInput.bind("<KeyRelease>", on_search)

# Position
searchFrame.pack(side=TOP, fill=X, pady=0, padx=0)
EmpruntsFrame.pack(side=TOP, fill=BOTH, expand=True, pady=(5, 5), padx=0)
searchInput.pack(side=LEFT, fill=X, expand=True, padx=0, pady=0)
filterCombo.pack(side=LEFT, fill=X, expand=False, padx=(5, 0), pady=0)
AddEmp.pack(side=LEFT, expand=False, padx=(5, 0), pady=0)

#-------Ajouter un livre-------------------------------------------------------------------
ajouterLivreContent = CTkFrame(mainContent, border_width=0, fg_color=mainColor)

#Frame----------------
frame2 = CTkFrame(ajouterLivreContent,corner_radius=10, fg_color=("#fff", "#1e1e1e"), border_width=1, border_color=("#e2e8f0", "#1e1e1e"))
frame2.pack(pady=10, padx=20,expand=True)

# Ajout de l'image
image_label = CTkLabel(frame2, text="Aucune image sélectionnée", width=200, height=250)
image_label.grid(row=0, column=0, rowspan=7, padx=20, pady=5)

selected_image_path = None

images_folder = "images/Books"
json_file = "Database/images.json"
os.makedirs(images_folder, exist_ok=True)
def choisir_image():
    global selected_image_path
    filepath = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
    if filepath:
        selected_image_path = filepath
        img = PIL.Image.open(filepath)
        img = img.resize((150, 200),PIL.Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        image_label.configure(image=img, text="")
        image_label.image = img

    #-----------
    filename = os.path.basename(filepath)
    destination_path = os.path.join(images_folder, filename)
    #copie
    shutil.copy(filepath, destination_path)

    #-----------
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            try:
                images_data = json.load(f)
            except json.JSONDecodeError:
                images_data = []
    else:
        images_data = []

    #new data
    new_entry = {
        "livreId": entry_codee.get(),
        "image": destination_path.replace("\\", "/")  # Normalize path
    }
    images_data.append(new_entry)

    # Save data
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(images_data, f, indent=4, ensure_ascii=False)

#fonction ajouter un livre
def ajouterLivre():
    code = entry_codee.get()
    if not code:
        messagebox.showerror("Erreur", "Veuillez entrer un code de livre !")
        return

    if not os.path.exists("Database"):
        os.makedirs("Database")

    titre=entry_titre.get()
    nomA=entry_nom.get()
    prenomA=entry_prenom.get()
    codeA=entry_code.get()
    nbrTtl=entry_total.get()
    nbrDispo=entry_disponible.get()


    try:
        lvr = livre(code, titre,Auteur(nomA,prenomA,codeA),int(nbrTtl),int(nbrDispo),nbrEmprunt=0)
    except Exception as e:
        messagebox.showerror("Erreur", e)
    else:
        gestion.ajouterLivre(lvr)
        messagebox.showinfo("Succès", f"Le livre {titre} a été ajouté.")
        refreshDashboard()
        entry_code.delete(0, "end")
        entry_nom.delete(0, "end")
        entry_codee.delete(0, "end")
        entry_prenom.delete(0, "end")
        entry_total.delete(0, "end")
        entry_disponible.delete(0, "end")
        entry_titre.delete(0, "end")
        image_label.configure(image="")
        selected_image = None


# Création des entrées
CTkLabel(frame2, text="Code du livre:").grid(row=0, column=1, sticky="w", pady=(20,5))
entry_codee = CTkEntry(frame2, placeholder_text="Code du livre", width=250)
entry_codee.grid(row=0, column=2, padx=10, pady=(20,5))

CTkLabel(frame2, text="Titre:").grid(row=1, column=1, sticky="w")
entry_titre = CTkEntry(frame2, placeholder_text="Titre", width=250)
entry_titre.grid(row=1, column=2, padx=10, pady=5)

CTkLabel(frame2, text="Nom de l'auteur:").grid(row=2, column=1, sticky="w")
entry_nom = CTkEntry(frame2, placeholder_text="Nom de l'auteur", width=250)
entry_nom.grid(row=2, column=2, padx=10, pady=5)

CTkLabel(frame2, text="Prénom de l'auteur:").grid(row=3, column=1, sticky="w")
entry_prenom = CTkEntry(frame2, placeholder_text="Prénom de l'auteur", width=250)
entry_prenom.grid(row=3, column=2, padx=10, pady=5)

CTkLabel(frame2, text="Code de l'auteur:").grid(row=4, column=1, sticky="w")
entry_code = CTkEntry(frame2, placeholder_text="Code de l'auteur", width=250)
entry_code.grid(row=4, column=2, padx=10, pady=5)

CTkLabel(frame2, text="Nombre total:").grid(row=5, column=1, sticky="w")
entry_total = CTkEntry(frame2, placeholder_text="Nombre total d'exemplaires", width=250)
entry_total.grid(row=5, column=2, padx=10, pady=5)

CTkLabel(frame2, text="Nombre disponible:").grid(row=6, column=1, sticky="w")
entry_disponible = CTkEntry(frame2, placeholder_text="Nombre disponible d'exemplaires", width=250)
entry_disponible.grid(row=6, column=2, padx=10, pady=5)

#Création des buttons
ajouter_button = CTkButton(frame2, text="Ajouter un livre",fg_color=("#0078D7", "#005A9E"),corner_radius=8,  border_width=1,  border_color=("#A4C8E1", "#004680"),  height=36,  text_color="#fff",  hover_color=("#005A9E", "#004680"),compound="left",  anchor="center", command=ajouterLivre)
ajouter_button.grid(row=8, column=0, columnspan=2, pady=30)

image_button = CTkButton(frame2, text="Choisir une image",fg_color=("#0078D7", "#005A9E"),corner_radius=8,  border_width=1,  border_color=("#A4C8E1", "#004680"),  height=36,  text_color="#fff",  hover_color=("#005A9E", "#004680"),compound="left",  anchor="center", command=choisir_image)
image_button.grid(row=8, column=1, columnspan=2, pady=30,padx=10)

afficher_button = CTkButton(frame2, text="Afficher les livres",fg_color=("#0078D7", "#005A9E"),corner_radius=8,  border_width=1,  border_color=("#A4C8E1", "#004680"),  height=36,  text_color="#fff",  hover_color=("#005A9E", "#004680"),compound="left",  anchor="center", command=lambda: BtnColor("Livres") & updateMain("Livres"))
afficher_button.grid(row=8, column=3, columnspan=2, pady=30,padx=(0,20))
ajouterLivreContent.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)
#-------Ajouter un emprunt-------------------------------------------------------------------
ajouterEmpruntContent = CTkFrame(mainContent, border_width=0, fg_color=mainColor)

frame1 = CTkFrame(ajouterEmpruntContent,corner_radius=10, fg_color=("#fff", "#1e1e1e"), border_width=1, border_color=("#e2e8f0", "#1e1e1e"))
frame1.pack(pady=10, padx=20,expand=True)

label_title = CTkLabel(frame1, text="Ajouter un Emprunt", font=("Arial", 20, "bold"))
label_title.pack(pady=10)

# Entrée du code adhérent
label_codeA = CTkLabel(frame1, text="Code Adhérent :", font=("Arial", 14))
label_codeA.pack()
entry_codeA = CTkEntry(frame1, width=250)
entry_codeA.pack(pady=5,padx=50)

# Entrée du code livre
label_codeL = CTkLabel(frame1, text="Code Livre :", font=("Arial", 14))
label_codeL.pack()
entry_codeL = CTkEntry(frame1, width=250)
entry_codeL.pack(pady=5,padx=50)

# Fonction pour appeler ajouterEmprunt
def ajouter_emprunt():
    codeA = entry_codeA.get().strip()
    codeL = entry_codeL.get().strip()

    if not codeA or not codeL:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
        return

    try:
        gestion.ajouterEmprunt(codeA, codeL)
        Emp.display_emprunts(Emprnts)
        refreshDashboard()
        messagebox.showinfo("Succès", f"Emprunt ajouté pour l'adhérent {codeA} et le livre {codeL}")
        entry_codeL.delete(0, "end")
        entry_codeA.delete(0, "end")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")

# Bouton pour ajouter un emprunt
btn_ajouter = CTkButton(frame1, text="Ajouter Emprunt", command=ajouter_emprunt,
                            fg_color=("#0078D7", "#005A9E"), text_color="#fff",
                            hover_color=("#005A9E", "#004680"), corner_radius=8)
btn_ajouter.pack(pady=15)

ajouterEmpruntContent.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)
#-------Ajouter un adherent-------------------------------------------------------------------
ajouterAdherentContent = CTkFrame(mainContent, border_width=0, fg_color=mainColor)
ajouterAdherentContent.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)

#-------Paramètres-------------------------------------------------------------------
parametresContent = CTkFrame(mainContent, border_width=0, fg_color=mainColor)
parametresContent.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)

parametresTitle = CTkLabel(parametresContent, text="Paramètres", font=("Hubot Sans", 24, "bold"), text_color=("#03045E", "#FFFFFF"))
parametresTitle.pack(side=TOP, pady=(10, 20), padx=20, anchor="w")

themeFrame = CTkFrame(parametresContent, fg_color=mainColor, border_width=0)
themeFrame.pack(side=TOP, fill=X, padx=20, pady=10)

themeLabel = CTkLabel(themeFrame, text="Thème", font=("Hubot Sans", 18, "bold"), text_color=("#03045E", "#FFFFFF"))
themeLabel.pack(side=TOP, anchor="w", pady=(0, 10))

themeVar = IntVar()

def update_theme():
    theme = themeVar.get()
    set_appearance_mode('dark' if theme == 1 else 'light')
    update_menu_colors()
    with open("Database/settings.json", "r") as file:
        data_dict = js.load(file)
    data_dict["theme"] = 'dark' if themeVar.get() == 1 else 'light'
    with open("Database/settings.json", "w") as file:
        js.dump(data_dict, file, indent=4)
def getTheme():
    with open("Database/settings.json", "r") as file:
        data_dict = js.load(file)
    Ctheme = data_dict["theme"]
    themeVar.set(1 if Ctheme.lower() == 'dark' else 2)
getTheme()

darkCmb = CTkRadioButton(themeFrame, text="Dark mode",variable=themeVar, value=1, font=("Roboto", 14), command=update_theme)
darkCmb.pack(side=TOP, anchor="w", pady=5)
lightCmb = CTkRadioButton(themeFrame, text="Light mode", variable=themeVar, value=2, font=("Roboto", 14), command=update_theme)
lightCmb.pack(side=TOP, anchor="w", pady=5)


languageFrame = CTkFrame(parametresContent, fg_color=mainColor, border_width=0)
languageFrame.pack(side=TOP, fill=X, padx=20, pady=10)

languageLabel = CTkLabel(languageFrame, text="Langue", font=("Hubot Sans", 18, "bold"), text_color=("#03045E", "#FFFFFF"))
languageLabel.pack(side=TOP, anchor="w", pady=(0, 10))

languageVar = StringVar(value="Français")

def update_language():
    language = languageVar.get()
    messagebox.showinfo("Langue", f"Langue sélectionnée : {language}")

CTkRadioButton(languageFrame, text="Français", variable=languageVar, value="Français", font=("Roboto", 14), command=update_language).pack(side=TOP, anchor="w", pady=5)
CTkRadioButton(languageFrame, text="English", variable=languageVar, value="English", font=("Roboto", 14), command=update_language).pack(side=TOP, anchor="w", pady=5)

accountFrame = CTkFrame(parametresContent, fg_color=mainColor, border_width=0)
accountFrame.pack(side=TOP, fill=X, padx=20, pady=10)

accountLabel = CTkLabel(accountFrame, text="Paramètres du Compte", font=("Hubot Sans", 18, "bold"), text_color=("#03045E", "#FFFFFF"))
accountLabel.pack(side=TOP, anchor="w", pady=(0, 10))

usernameLabel = CTkLabel(accountFrame, text="Nom d'utilisateur", font=("Roboto", 14), text_color=("#03045E", "#FFFFFF"))
usernameLabel.pack(side=TOP, anchor="w", pady=(0, 5))

usernameEntry = CTkEntry(accountFrame, font=("Roboto", 14), placeholder_text="Entrez votre nom d'utilisateur", width=300)
usernameEntry.pack(side=TOP, anchor="w", pady=(0, 10))

passwordLabel = CTkLabel(accountFrame, text="Mot de passe", font=("Roboto", 14), text_color=("#03045E", "#FFFFFF"))
passwordLabel.pack(side=TOP, anchor="w", pady=(0, 5))

passwordEntry = CTkEntry(accountFrame, font=("Roboto", 14), placeholder_text="Entrez votre mot de passe", show="*", width=300)
passwordEntry.pack(side=TOP, anchor="w", pady=(0, 10))

def save_account_settings():
    username = usernameEntry.get()
    password = passwordEntry.get()
    if username and password:
        messagebox.showinfo("Succès", "Paramètres du compte mis à jour avec succès!")
    else:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

saveButton = CTkButton(accountFrame, text="Enregistrer", font=("Roboto", 14), fg_color="#00B4D8", hover_color="#90E0FF", command=save_account_settings)
saveButton.pack(side=TOP, anchor="w", pady=(10, 0))

parametresContent.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)















#Position----------------------------------------------------------------------
sideMenu.pack(side=LEFT, fill=Y)
TitleFrame.pack(side=TOP, fill=X, padx=5)
sideTitle.pack(side=LEFT, pady=30, padx=5)
ThemeBtn.pack(side=RIGHT)
BtnFrame.pack(side=TOP, fill=BOTH,expand=YES, padx=5, pady=0)
dashboard.pack(side=TOP, fill=X, padx=5, pady=5)
books.pack(side=TOP, fill=X, padx=5, pady=5)
clients.pack(side=TOP, fill=X, padx=5, pady=5)
Loans.pack(side=TOP, fill=X, padx=5, pady=5)
AddBook.pack(side=TOP, fill=X, padx=5, pady=5)
AddLoan.pack(side=TOP, fill=X, padx=5, pady=5)
AddClient.pack(side=TOP, fill=X, padx=5, pady=5)
settings.pack(side=TOP, fill=X, padx=5, pady=5)
Exit.pack(side=BOTTOM, fill=X, padx=5, pady=5)
border.pack(side=LEFT, fill=Y)



main.pack(side=LEFT, fill=BOTH, expand=YES)
MainFrame.pack(side=TOP, fill=X)
FrameTitle.pack(side=TOP, fill=X, padx=0, pady=0)
expandBtn.pack(side=LEFT, fill=X, padx=(15,5), pady=15)
TitleMain.pack(side=LEFT, fill=X, padx=5, pady=15)
vBorder.pack(side=TOP, fill=X)
mainContent.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)






#Menu------------------------------------------------------
menubar = Menu(app)
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Fichier', menu=file)
file.add_command(label='Enregistrer les livres csv', command=lambda: gestion.save_livres_csv() & messagebox.showinfo("Enregistrement", "Les livres ont ete enregistres avec succes"))
file.add_command(label='Enregistrer les emprunts csv', command=lambda: gestion.save_emprunts_csv() & messagebox.showinfo("Enregistrement", "Les emprunts ont ete enregistres avec succes"))
file.add_command(label='Enregistrer les adherents csv', command=lambda: gestion.save_adherents_csv() & messagebox.showinfo("Enregistrement", "Les adherents ont ete enregistres avec succes"))
file.add_separator()
file.add_command(label='Quitter', command=app.destroy)

edit = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Editer', menu=edit)
edit.add_command(label='Couper', command=None)
edit.add_command(label='Copier', command=None)
edit.add_command(label='Coller', command=None)
edit.add_command(label='Selectionner tout', command=None)
edit.add_separator()
edit.add_command(label='Find...', command=None)

view = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Voir', menu=view)
sideBarView = IntVar()
view.add_checkbutton(label="Barre latérale", command=hideShowSideBar, variable=sideBarView)
mode = Menu(view, tearoff=0)
Modevr = StringVar()
mode.add_radiobutton(label="Dark mode", variable=Modevr, value="Dark mode", command=lambda: set_appearance_mode("dark") & update_menu_colors())
mode.add_radiobutton(label="Light mode", variable=Modevr, value="Light mode", command=lambda: set_appearance_mode("light") & update_menu_colors())
Modevr.set("Light mode")
zoom = Menu(view, tearoff=0)
ZoomInt = IntVar()
zoom.add_radiobutton(label="60%", variable=ZoomInt, value=0.6, command=lambda: set_widget_scaling(0.6))
zoom.add_radiobutton(label="80%", variable=ZoomInt, value=0.8, command=lambda: set_widget_scaling(0.8))
zoom.add_radiobutton(label="100%", variable=ZoomInt, value=1, command=lambda: set_widget_scaling(1))
zoom.add_radiobutton(label="120%", variable=ZoomInt, value=1.2, command=lambda: set_widget_scaling(1.2))
zoom.add_radiobutton(label="150%", variable=ZoomInt, value=1.5, command=lambda: set_widget_scaling(1.5))
ZoomInt.set(1)
view.add_cascade(label="Thème", menu=mode)
view.add_cascade(label="Zoom", menu=zoom)
sideBarView.set(1)

help_ = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Aide', menu=help_)
help_.add_command(label='Aide', command=None)

app.config(menu=menubar)

update_menu_colors()







app.config(menu = menubar)

BtnColor("Accueil")
updateMain("Accueil")
defaultSettings()

def mainloop():
    app.mainloop()
if __name__ == "__main__":
    mainloop()