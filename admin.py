import login
import db_handler
import tkinter as tk
from tkinter.messagebox import showerror

class AdminGUI:
    def __init__(self, active_user) -> None:
        id, name = active_user[0], active_user[1]

        self.classroom = {}

        self.root = tk.Tk()
        self.root.title(f"Howdy, {name}")
        self.root.geometry("500x400")
        self.root.resizable(False,False)

        self.font = ("Arial", 11)

        # label frame
        self.labelFrame = tk.LabelFrame(self.root, text=f"Admin Window", borderwidth=2, labelanchor="n", font=("Arial", 12))
        

        # Widgets
        self.class_num = tk.Label(self.labelFrame, text="Classroom Number", font=self.font)
        self.entry_class_num = tk.Entry(self.labelFrame, width=30)

        self.class_loc = tk.Label(self.labelFrame, text="Classroom Location", font=self.font)
        self.entry_class_loc = tk.Entry(self.labelFrame, width=30)

        self.class_cap = tk.Label(self.labelFrame, text="Classroom Capacity", font=self.font)
        self.entry_class_cap = tk.Entry(self.labelFrame, width=30)

        self.create_button = tk.Button(self.root, text="Create", width=20, font=("Arial", 9, "bold"), command=self.create)
        self.backup_button = tk.Button(self.root, text="Backup", width=20, font=("Arial", 9, "bold"), command=self.backup)
        self.logout_button = tk.Button(self.root, text="Logout", width=20, font=("Arial", 9, "bold"), command=self.logout)
        



        # grid
        self.labelFrame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Labels
        self.labels_padx = (60,10)
        self.labels_pady = (10, 10)
        self.class_num.grid(column=0, row=0, padx=self.labels_padx, pady=(self.labels_pady[0]+40 ,self.labels_pady[1]))
        self.class_loc.grid(column=0, row=1, padx=self.labels_padx, pady=self.labels_pady)
        self.class_cap.grid(column=0, row=2, padx=self.labels_padx, pady=self.labels_pady)


        # entries
        self.entry_padx = (10, 0)
        self.entry_pady = (10, 10)
        self.entry_ipady = (2,2)
        self.entry_class_num.grid(column=2, row=0, padx=self.entry_padx, pady=(self.entry_pady[0]+40 ,self.entry_pady[1]), ipady=2)
        self.entry_class_loc.grid(column=2, row=1, padx=self.entry_padx, pady=self.entry_pady, ipady=2)
        self.entry_class_cap.grid(column=2, row=2, padx=self.entry_padx, pady=self.entry_pady, ipady=2)

        
        # button
        self.create_button.place(relx=.5, rely=.6, anchor= tk.CENTER)
        self.backup_button.place(relx=.5, rely=.69, anchor= tk.CENTER)
        self.logout_button.place(relx=.5, rely=.78, anchor= tk.CENTER)


        self.root.mainloop()


    def create(self):
        number_check = self.validate_number(self.entry_class_num.get())
        location_check = self.validate_loaction(self.entry_class_loc.get())
        capacity_check = self.validate_capacity(self.entry_class_cap.get())

        if(number_check and location_check and capacity_check):
            if not (db_handler.add_classroom(self.classroom)):
                # showerror("Class already exists", "This class already exists")
                pass
            else:
                self.entry_class_num.delete(0, tk.END)
                self.entry_class_loc.delete(0, tk.END)
                self.entry_class_cap.delete(0, tk.END)
            
        pass

    def backup(self):
        db_handler.backup_db()

    def logout(self):
        self.root.update()
        self.root.destroy()
        login.LoginGUI()

    def validate_number(self, num):
        try: 
            int(num)
            self.classroom["number"] = num
            self.entry_class_num.config(highlightthickness=0)
            return num

        except:
            self.entry_class_num.config(highlightbackground="red", highlightthickness=0.5)
            showerror("Invalid class number", "Please enter a valid class number\nFor example '65'")
            return False
        
        

    def validate_loaction(self, loc):
        try: 
            int(loc)
            self.classroom["location"] = loc
            self.entry_class_loc.config(highlightthickness=0)
            return loc

        except:
            self.entry_class_loc.config(highlightbackground="red", highlightthickness=0.5)
            showerror("Invalid class location", "Please enter a valid class location\nA valid class location would be the building number like '31'")
            return False


    def validate_capacity(self, cap):
        try: 
            cap = int(cap)

            if cap < 1: raise Exception

            self.classroom["capacity"] = cap
            self.entry_class_cap.config(highlightthickness=0)
            return cap

        except:
            self.entry_class_cap.config(highlightbackground="red", highlightthickness=0.5)
            showerror("Invalid Class Capacity", "Please enter a valid class capacity.")
            return False

        


if __name__ == "__main__":
    AdminGUI((111111111, "admin", "admin"))
