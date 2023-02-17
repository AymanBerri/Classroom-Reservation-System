import admin
import hashlib
import re
import student
import db_handler
import sign_up
from tkinter.messagebox import showerror
import tkinter as tk

class LoginGUI:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry("500x300")
        self.root.resizable(False,False)

        self.font = ("Arial", 11)

        # label frame
        self.labelFrame = tk.LabelFrame(self.root, text="Login Window", borderwidth=2, labelanchor="n", font=("Arial", 12))
        

        # Widgets
        self.id = tk.Label(self.labelFrame, text="User ID", font=self.font)
        self.entry_id = tk.Entry(self.labelFrame, width=30)

        self.password = tk.Label(self.labelFrame, text="User Password", font=self.font)
        self.entry_password = tk.Entry(self.labelFrame, width=30, show="*")

        self.login_button = tk.Button(self.root, text="Login", width=20, font=("Arial", 9, "bold"), command=self.login)
        self.sign_up_button = tk.Button(self.root, text="Sign Up", width=20, font=("Arial", 9, "bold"), command=self.sign_up)



        # grid
        self.labelFrame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Labels
        self.labels_padx = (60,10)
        self.labels_pady = (10, 10)
        self.id.grid(column=0, row=0, padx=self.labels_padx, pady=(self.labels_pady[0]+40 ,self.labels_pady[1]))
        self.password.grid(column=0, row=1, padx=self.labels_padx, pady=self.labels_pady)


        # entries
        self.entry_padx = (10, 0)
        self.entry_pady = (10, 10)
        self.entry_ipady = (2,2)
        self.entry_id.grid(column=2, row=0, padx=self.entry_padx, pady=(self.entry_pady[0]+40 ,self.entry_pady[1]), ipady=2)
        self.entry_password.grid(column=2, row=1, padx=self.entry_padx, pady=self.entry_pady, ipady=2)

        
        # button
        self.login_button.place(relx=.5, rely=.7, anchor= tk.CENTER)
        self.sign_up_button.place(relx=.5, rely=.8, anchor= tk.CENTER)


        self.root.mainloop()


    def login(self):
        user_id_check = self.validate_id(self.entry_id.get())
        user_password_check = self.validate_password(self.entry_password.get())

        # basically the program checks valid input before searching the DB for the user.
        if(not (user_id_check and user_password_check)): return


        # using the walrus assignment
        if(active_user := db_handler.check_user_exists(user_id_check, str(user_password_check))):
            print(f"[INFO] Howdy {active_user[1]}")
            self.root.update()
            self.root.destroy()

            # after we have the user, we point him to his window. We also pass his info that we got from "db_handler.check_user_exists"
            if(active_user[2] == "admin"):
                # ADMINSTRATOR
                admin.AdminGUI(active_user)
            else:
                # STUDENT
                student.StudentGUI(active_user)
        else:
            # the error is kept ambiguous for extra security
            showerror("Invalid info", "Either this user does not exist, or the password does not match.")

    def validate_id(self, id):
        if id == "" or not (re.search(r"^(\d){9}$", id)):
            self.entry_id.config(highlightbackground="red", highlightthickness=0.5)
            showerror("Invalid Student ID", "Please enter a valid Student Id of 9 digits.")
            return False
        self.entry_id.config(highlightthickness=0)
        return id 

    def validate_password(self, password):
        lower, upper, special, digit = 0, 0, 0, 0
        # password = "R@m@_f0rtu9e$"
        # accepted characters:
        capitalalphabets="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        smallalphabets="abcdefghijklmnopqrstuvwxyz"
        specialchar="$@_"
        digits="0123456789"
        if (len(password) >= 6):
            for i in password:
                # counting lowercase chars
                if (i in smallalphabets):
                    lower+=1           
                # counting uppercase chars
                if (i in capitalalphabets):
                    upper+=1           
                # counting digits
                if (i in digits):
                    digit+=1           
                # counting the mentioned special characters
                if(i in specialchar):
                    special+=1       

        # checks 

        if len(password) < 6:
            showerror("No password", "Please enter a 6 char password.")
            self.entry_password.config(highlightbackground="red", highlightthickness=0.5)
            return False
        if (lower<1 and upper<1):
            showerror("Invalid Password", "Password must have at least one upper and lower case letters")
            self.entry_password.config(highlightbackground="red", highlightthickness=0.5)
            return False
        if (digit<1):
            showerror("Invalid Password", f"Password must have at least one digit")
            self.entry_password.config(highlightbackground="red", highlightthickness=0.5)
            return False
        if (lower+special+upper+digit!=len(password)):
            showerror("Invalid Password", f"Password can only include letters, digits, and '{specialchar}'")
            self.entry_password.config(highlightbackground="red", highlightthickness=0.5)
            return False

        # hash the password
        result = hashlib.sha256(password.encode()).hexdigest()


        self.entry_password.config(highlightthickness=0)
        return result

    


    def sign_up(self):
        self.root.update()
        self.root.destroy()
        sign_up.signUpGUI()



if __name__ == "__main__":
    LoginGUI()

