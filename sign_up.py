import login
import db_handler
import hashlib
import re
from tkinter.messagebox import showerror
# must install
from email_validator import validate_email, EmailNotValidError
import tkinter as tk

class signUpGUI:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Sign Up")
        self.root.geometry("500x450")
        self.root.resizable(False,False)

        self.font = ("Arial", 11)
        # dictionary that will be passed to the DB
        self.acc = {}

        # label frame
        self.labelFrame = tk.LabelFrame(self.root, text="Sign Up Form", borderwidth=2, labelanchor="n", font=("Arial", 12))
        

        # Widgets
        self.first_name = tk.Label(self.labelFrame, text="First Name", font=self.font)
        self.entry_first_name = tk.Entry(self.labelFrame, width=30)

        self.second_name = tk.Label(self.labelFrame, text="Second Name", font=self.font)
        self.entry_second_name = tk.Entry(self.labelFrame, width=30)

        self.id = tk.Label(self.labelFrame, text="Student ID", font=self.font)
        self.entry_id = tk.Entry(self.labelFrame, width=30)

        self.password = tk.Label(self.labelFrame, text="Password", font=self.font)
        self.entry_password = tk.Entry(self.labelFrame, width=30, show="*")

        self.email = tk.Label(self.labelFrame, text="Email", font=self.font)
        self.entry_email = tk.Entry(self.labelFrame, width=30)

        self.phone_num = tk.Label(self.labelFrame, text="Phone Number", font=self.font)
        self.entry_phone_num = tk.Entry(self.labelFrame, width=30)

        self.submit_button = tk.Button(self.root, text="Submit", width=20, font=("Arial", 9, "bold"), command=self.submit)
        self.login_button = tk.Button(self.root, text="Login instead", width=20, font=("Arial", 9, "bold"), command=self.login)




        # grid
        self.labelFrame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Labels
        self.labels_padx = (100,10)
        self.labels_pady = (10, 10)
        self.first_name.grid(column=0, row=0, padx=self.labels_padx, pady=(self.labels_pady[0]+40 ,self.labels_pady[1]))
        self.second_name.grid(column=0, row=1, padx=self.labels_padx, pady=self.labels_pady)
        self.id.grid(column=0, row=2, padx=self.labels_padx, pady=self.labels_pady)
        self.password.grid(column=0, row=3, padx=self.labels_padx, pady=self.labels_pady)
        self.email.grid(column=0, row=4, padx=self.labels_padx, pady=self.labels_pady)
        self.phone_num.grid(column=0, row=5, padx=self.labels_padx, pady=self.labels_pady)

        # entries
        self.entry_padx = (10, 0)
        self.entry_pady = (10, 10)
        self.entry_ipady = (2,2)
        self.entry_first_name.grid(column=2, row=0, padx=self.entry_padx, pady=(self.entry_pady[0]+40 ,self.entry_pady[1]), ipady=2)
        self.entry_second_name.grid(column=2, row=1, padx=self.entry_padx, pady=self.entry_pady, ipady=2)
        self.entry_id.grid(column=2, row=2, padx=self.entry_padx, pady=self.entry_pady, ipady=2)
        self.entry_password.grid(column=2, row=3, padx=self.entry_padx, pady=self.entry_pady, ipady=2)
        self.entry_email.grid(column=2, row=4, padx=self.entry_padx, pady=self.entry_pady, ipady=2)
        self.entry_phone_num.grid(column=2, row=5, padx=self.entry_padx, pady=self.entry_pady, ipady=2)
        
        # button
        self.submit_button.place(relx=.5, rely=.8, anchor= tk.CENTER)
        self.login_button.place(relx=.5, rely=.87, anchor= tk.CENTER)


        self.root.mainloop()


    def submit(self):
        name_check = self.validate_name(self.entry_first_name.get(), self.entry_second_name.get())
        id_check = self.validate_id(self.entry_id.get())
        pass_check = self.validate_password(self.entry_password.get())
        email_check = self.validate_email(self.entry_email.get())
        phone_check = self.validate_phone(self.entry_phone_num.get())


        if(name_check and id_check and pass_check and email_check and phone_check):
            
            # after checking if the entered info is complete, we check if the student already exists using nested if statement
            if(db_handler.add_student(self.acc)):
                self.entry_first_name.delete(0, tk.END)
                self.entry_second_name.delete(0, tk.END)
                self.entry_id.delete(0, tk.END)
                self.entry_password.delete(0, tk.END)
                self.entry_email.delete(0, tk.END)
                self.entry_phone_num.delete(0, tk.END)             
                self.login_button["bg"] = "#adffc8"
                self.login_button["text"] = "Login"

                

            

    def login(self):
        # Database handling goes here
        self.root.update()
        self.root.destroy()
        login.LoginGUI()
            
    def validate_name(self, first, second):
        flagFirst = True
        flagSecond = True

        if first == "":
            self.entry_first_name.config(highlightbackground="red", highlightthickness=0.5)
            showerror("Invalid First Name", "Please enter first name.")
            flagFirst = False
        if second == "":
            self.entry_second_name.config(highlightbackground="red", highlightthickness=0.5)
            showerror("Invalid Second Name", "Please enter second name.")
            flagSecond = False

        # update the account dictionary
        
        if(flagFirst): self.entry_first_name.config(highlightthickness=0)
        if(flagSecond): self.entry_second_name.config(highlightthickness=0)
        if(flagFirst and flagSecond): 
            self.acc['first'], self.acc['second'] = first, second
            return True


    def validate_id(self, id):
        if id == "" or not (re.search(r"^(\d){9}$", id)):
            self.entry_id.config(highlightbackground="red", highlightthickness=0.5)
            showerror("Invalid Student ID", "Please enter a valid Student Id of 9 digits.")
            return False

        # update the account dictionary
        self.acc['id'] = id


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

        # update the account dictionary
        
        
        self.acc['password'] = result


        self.entry_password.config(highlightthickness=0)
        return result

    def validate_email(self, email):
        try:
            # validate and get info
            v = validate_email(email)
            # replace with normalized form
            email = v["email"] 

            # update the account dictionary
            self.acc['email'] = email
            self.entry_email.config(highlightthickness=0)
            return True
        except EmailNotValidError as e:
            # highlight the error
            self.entry_email.config(highlightbackground="red", highlightthickness=0.5)

            # email is not valid, exception message is human-readable
            if email == "": 
                showerror("No email", "Please enter an email.")
                return False
            else: 
                showerror("Invalid Email", str(e)+" Please try again.")
                return False

    def validate_phone(self, phone):
        if phone == "" or not (re.search("^05(\d){8}$", phone)):
            self.entry_phone_num.config(highlightbackground="red", highlightthickness=0.5)
            showerror("Invalid Phone", "Please enter a valid Saudi phone - 05XXXXXXXX")
            return False

        ## update the account dictionary
        self.acc['phone'] = phone
        self.entry_phone_num.config(highlightthickness=0)
        return True            

    
        

            

if __name__ == "__main__":
    sign_up = signUpGUI()