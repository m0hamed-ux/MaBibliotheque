from customtkinter import *
from PIL import Image
import re
import json as js


def validate_login():
    username = username_entry.get()
    password = password_entry.get()
    with open("Database/settings.json", "r") as file:
        data_dict = js.load(file)
    loginP = data_dict["login"]
    passwordP = data_dict["password"]
    

    if not re.match(loginP, username):
        error_label.configure(text="Nom d'utilisateur est invalid !", text_color="red")
        return
    elif not re.match(passwordP, password):
        error_label.configure(text="Mot de passe est invalid !", text_color="red")
        return
    else:
        login.destroy()
        from App import mainloop as start
        start()


login = CTk(fg_color="#CAF0F8")
login.geometry("800x600")
login.title("Login Page")


side_img = CTkImage(Image.open("images/logo.png"), size=(400, 350))
username_icon = CTkImage(Image.open("images/user-icon.png"), size=(30, 30))
password_icon = CTkImage(Image.open("images/pass-icon.png"), size=(17, 17))
google_icon = CTkImage(Image.open("images/google-icon.png"), size=(17, 17))


CTkLabel(master=login,text="", image=side_img).pack(expand=True, side="left")


frame = CTkFrame(master=login, width=400, height=600, fg_color="#CAF0F8")
frame.pack(expand=True, side="right")

CTkLabel(master=frame, text="Content de vous revoir !", text_color="#004D88", anchor="w", justify="left",
         font=("Arial Bold", 28)).pack(anchor="w", pady=(50, 5), padx=(0, 25))
CTkLabel(master=frame, text="Connectez-vous à votre compte", text_color="#004D88", anchor="w", justify="left",
         font=("Arial Bold", 14)).pack(anchor="w", padx=(0, 25))


CTkLabel(master=frame, text="Nom d'utilisateur:", text_color="#004D88", anchor="w", justify="left", font=("Arial Bold", 16),
         image=username_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(0, 25))
username_entry = CTkEntry(master=frame, width=300, fg_color="#FFFFFF", border_color="#90E0EF", border_width=1,
                          text_color="#000000")
username_entry.pack(anchor="w", padx=(0, 25))

CTkLabel(master=frame, text="  Mot de passe:", text_color="#004D88", anchor="w", justify="left", font=("Arial Bold", 16),
         image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(0, 25))
password_entry = CTkEntry(master=frame, width=300, fg_color="#FFFFFF", border_color="#90E0EF", border_width=1,
                          text_color="#000000", show="*")
password_entry.pack(anchor="w", padx=(0, 25))

error_label = CTkLabel(master=frame, text="", text_color="red", anchor="w", justify="left", font=("Arial Bold", 12))
error_label.pack(anchor="w", pady=(10, 0), padx=(0, 25))


CTkButton(master=frame, text="Se Connecter", fg_color="#004D88", hover_color="#90E0EF", font=("Arial Bold", 14),
          text_color="#FFFFFF", width=300, command=validate_login).pack(anchor="w", pady=(40, 0), padx=(0, 25))


CTkButton(master=frame, text="Continuer avec Google", fg_color="#FFFFFF", hover_color="#EEEEEE", font=("Arial Bold", 12),
          text_color="#004D88", width=300, image=google_icon).pack(anchor="w", pady=(20, 0), padx=(0, 25))

login.mainloop()