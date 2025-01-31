from tkinter import *
from tkinter import messagebox
from tkcalendar import *
from tkinter import ttk
from customtkinter import *
from PIL import Image, ImageTk
from Bilio import Biblio
import json
from Adherent import Adherent


#Variables


#Gestion
gestion = Biblio()
gestion.load_data()
totalBooks = len(gestion.get_livres())
availableBooks = len(gestion.get_available_books())
borrowedBooks = len(gestion.get_borrowed_books())
totalClients = len(gestion.get_all_clients())
        


def defaultSettings():
    with open("Database/settings.json", "r") as file:
        data_dict = json.load(file)
    if data_dict["theme"] == "light":
        set_appearance_mode("light")
    else:
        set_appearance_mode("dark")
    set_widget_scaling(data_dict["zoom"])
def change_theme():
    if get_appearance_mode() == "Dark":
        set_appearance_mode("light")
        Modevr.set("Light mode")
    else:
        set_appearance_mode("dark")
        Modevr.set("Dark mode")
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
    btnList = [dashboard, books, clients, AddBook, AddLoan, settings, Loans]
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
    if frame == "Accueil":
        dashboardContent.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)
    else:
        dashboardContent.pack_forget()
def updateStats():
    global totalBooks, availableBooks, borrowedBooks, totalClients
    totalBooks = len(gestion.get_livres())
    availableBooks = len(gestion.get_available_books())
    borrowedBooks = len(gestion.get_borrowed_books())
    totalClients = len(gestion.get_all_clients())


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
logoImage = CTkImage(Image.open("images/logo.png"), size=(30, 30))
ThemeIcon = CTkImage(dark_image=Image.open("images/moon.png"),light_image=Image.open("images/sun.png") ,size=(20, 20))
dashboardIcon = CTkImage(dark_image=Image.open("images/homeLight.png"),light_image=Image.open("images/home.png"), size=(15, 15))
plusIcon = CTkImage(dark_image=Image.open("images/plusLight.png"),light_image=Image.open("images/plus.png"), size=(15, 15))
bookIcon = CTkImage(dark_image=Image.open("images/bookLight.png"),light_image=Image.open("images/book.png"), size=(15, 15))
clientsIcon = CTkImage(dark_image=Image.open("images/clientsLight.png"),light_image=Image.open("images/clients.png"), size=(15, 15))
loanIcon = CTkImage(dark_image=Image.open("images/loanLight.png"),light_image=Image.open("images/loan.png"), size=(15, 15))
settingsIcon = CTkImage(dark_image=Image.open("images/settingsLight.png"),light_image=Image.open("images/settings.png"), size=(15, 15))
expandIcon = CTkImage(dark_image=Image.open("images/sidebarLight.png"),light_image=Image.open("images/sidebar.png"), size=(20, 20))
exitIcon = CTkImage(Image.open("images/exit.png"), size=(15, 15))







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
dashboardContent = CTkFrame(mainContent, border_width=0, fg_color=mainColor)
dashboardContent.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)


statsFrame = CTkFrame(dashboardContent, fg_color=mainColor)


totalBooksFrame = CTkFrame(statsFrame, fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#1e1e1e"))
CTkLabel(totalBooksFrame, text="Total de livres", font=("Arial", 15, "bold"), justify="left", anchor="w", compound="left").pack(pady=(15,5), padx=15, anchor="w")
CTkLabel(totalBooksFrame, text=totalBooks, font=("Arial", 25)).pack(pady=(0,0), padx=15, anchor="w")
CTkLabel(totalBooksFrame, text="+20% par rapport au mois précédent", font=("Arial", 10), justify="left", anchor="w", compound="left", text_color=("#27272a", "#e3e8f0")).pack(pady=(0,3), padx=15, anchor="w")


availableBooksFrame = CTkFrame(statsFrame, fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#1e1e1e"))
CTkLabel(availableBooksFrame, text="Livres disponibles", font=("Arial", 15, "bold"), justify="left", anchor="w", compound="left").pack(pady=(15,5), padx=15, anchor="w")
CTkLabel(availableBooksFrame, text=availableBooks, font=("Arial", 25)).pack(pady=(0,0), padx=15, anchor="w")
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
class RecentActivity(CTkFrame):
    def __init__(self, parent, text, font, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(side=TOP, fill=BOTH, expand=True, padx=5)
        self.activity = CTkLabel(self, text=text, font=font)
        self.activity.pack(side=LEFT, pady=2, padx=20, anchor="w", expand=False)
        self.configure(fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=0, border_color=("#e2e8f0", "#1e1e1e"))
for activity in recentActivities:
    if activity != "\n":
        RecentActivity(recentFrame, text=f"{activity}", font=("Arial", 15))
recentActivitiesFile.close()



#Top 5 Books
top5BooksFrame = CTkFrame(dashboardContent, fg_color=("#fff", "#1e1e1e"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#1e1e1e"))
CTkLabel(top5BooksFrame, text="Top 5 Books", font=("Arial", 20, "bold")).pack(pady=20, padx=20, anchor="w")

#Position
statsFrame.pack(side=TOP, fill=X, pady=(0,10))
totalBooksFrame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0,5))
availableBooksFrame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0,5))
borrowedBooksFrame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0,5))
totalClientsFrame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0,5))
recentFrame.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
top5BooksFrame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0,5))
#-----------------------------------------------------------------------------

# Your Content here ----------------------------------------------------------------------

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
file.add_command(label='Enregistrer les livres csv', command=None)
file.add_command(label='Enregistrer les emprunts csv', command=None)
file.add_command(label='Enregistrer les adherents csv', command=None)
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

def mainloop():
    app.mainloop()
if __name__ == "__main__":
    mainloop()
