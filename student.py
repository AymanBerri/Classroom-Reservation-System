import login
import logging
import db_handler
import re
from datetime import datetime
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror

logging.basicConfig(filename='student.log', filemode='a', format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)



class StudentGUI:
    def __init__(self, active_user) -> None:
        self.id, self.name = active_user[0], active_user[1]

        # reservation dictionary holding all details for reserving a class
        self.reservation = {}

        self.root = tk.Tk()
        self.root.title(f"Howdy, {self.name}")
        self.root.geometry("500x500")
        self.root.resizable(False,False)

        self.font = ("Arial", 11)


        # Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(padx=5, pady=2, fill="both", expand=True)

        # labelFrames
        self.reserve_frame = tk.LabelFrame(self.root, borderwidth=2)
        self.view_frame = tk.LabelFrame(self.root, borderwidth=2)

        # Treeviews
        ### RESERVE TREEVIEW
        self.tv_classroom = ttk.Treeview(self.reserve_frame, columns=(1,2,3), show='headings', height=8)
        # creating columns to change their width
        for col in range(4):
            self.tv_classroom.column(col, width=125, anchor='center')
        self.tv_classroom.heading(1, text="NUMBER")
        self.tv_classroom.heading(2, text="LOCATION")
        self.tv_classroom.heading(3, text="CAPACITY")

        # getting the data and displaying it
        conn = sqlite3.connect("ksu.db")
        cursor_classroom = conn.execute(f"SELECT * from CLASSROOM")
        count = 0

        for row in cursor_classroom:
            self.tv_classroom.insert(parent='', index=count, text='', values=(row[0], row[1], row[2]))
            count+=1

        ### VIEW TREEVIEW
        self.tv_view = ttk.Treeview(self.view_frame, columns=(1,2,3,4), show='headings', height=8)
        # creating columns to change their width
        for col in range(5):
            self.tv_view.column(col, width=100, anchor='center')
        self.tv_view.heading(1, text="NUMBER")
        self.tv_view.heading(2, text="LOCATION")
        self.tv_view.heading(3, text="FROM")
        self.tv_view.heading(4, text="TO")

        # # getting the data and displaying it
        # conn = sqlite3.connect("ksu.db")
        # cursor_course = conn.execute(f"SELECT * FROM RESERVATION WHERE id={self.id}")
        # count = 0

        # for row in cursor_course:
        #     self.tv_view.insert(parent='', index=count, text='', values=(row[0], row[1], row[2], row[3]))
        #     count+=1


        # widgets - reserve frame
        self.desc = tk.Label(self.reserve_frame, text="Select the class you wish to reserve:", font=self.font)

        self.start = tk.Label(self.reserve_frame, text="Start time & date:", font=self.font)
        self.entry_start = tk.Entry(self.reserve_frame, width=30)

        self.end = tk.Label(self.reserve_frame, text="End time & date:", font=self.font)
        self.entry_end = tk.Entry(self.reserve_frame, width=30)

        self.reserve_button = tk.Button(self.reserve_frame, text="Reserve", width=20, font=("Arial", 9, "bold"), command=self.reserve)
        self.logout_reserve_button = tk.Button(text="Logout", width=20, font=("Arial", 9, "bold"), command=self.logout_reserve)

        # widgets - view frame
        self.show_reservations_button = tk.Button(self.view_frame, text="Refresh Reservations", width=20, font=("Arial", 9, "bold"), command=self.show_reservations)
        self.logout_view_button = tk.Button(text="Logout", width=20, font=("Arial", 9, "bold"), command=self.logout_view)



        # packing
        self.reserve_frame.pack()
        self.view_frame.pack()

        # Treeview
        self.tv_classroom.grid(column=0, row=1, columnspan=5, padx=50, pady=5)

        self.tv_view.grid(column=0, row=1, columnspan=5, padx=50, pady=5)


        # Labels
        self.labels_padx = (60,10)
        self.labels_pady = (10, 10)

        self.desc.grid(column=0, row=0, padx=5, pady=(30, 0))

        self.start.grid(column=0, row=2, padx=self.labels_padx, pady=self.labels_pady)
        self.end.grid(column=0, row=3, padx=self.labels_padx, pady=self.labels_pady)

        # entries
        self.entry_padx = (10, 0)
        self.entry_pady = (10, 10)
        self.entry_ipady = (2,2)
        self.entry_start.grid(column=2, row=2, padx=self.entry_padx, pady=self.entry_pady, ipady=2)
        self.entry_end.grid(column=2, row=3, padx=self.entry_padx, pady=self.entry_pady, ipady=2)

        # Buttons
        self.reserve_button.place(relx=.5, rely=.8, anchor= tk.CENTER)
        self.logout_reserve_button.place(in_=self.reserve_frame, relx=.5, rely=.89, anchor= tk.CENTER)

        self.show_reservations_button.place(relx=.5, rely=.8, anchor= tk.CENTER)
        self.logout_view_button.place(in_=self.view_frame,relx=.5, rely=.89, anchor= tk.CENTER)


        self.notebook.add(self.reserve_frame, text='    Reserve    ')
        self.notebook.add(self.view_frame, text='    View Reservations    ')
        
        # took it off the internet. :)
        self.tv_classroom.bind('<ButtonRelease-1>', self.select_item)


        
        self.root.mainloop()

    def show_reservations(self):
        # clearing the shown reservations to avoid appending them again
        for item in self.tv_view.get_children():
            self.tv_view.delete(item)

        # getting the reservations and displaying it
        conn = sqlite3.connect("ksu.db")
        cursor_reservation = conn.execute(f"SELECT * FROM RESERVATION WHERE id={self.id}")
        count = 0

        for row in cursor_reservation:
            self.tv_view.insert(parent='', index=count, text='', values=(row[1], row[2], row[3], row[4]))
            count+=1
        
        
    def reserve(self):
        self.reservation['id'] = self.id

        # Validating the start and end time and date format and getting them
        if start_date := self.validate_date_time_format(self.entry_start.get()):
            self.entry_start.config(highlightthickness=0)
            self.reservation['start'] = start_date
        else:
            self.entry_start.config(highlightbackground="red", highlightthickness=0.5)
            showerror("Invalid start date format", "Please enter a valid start date and time following the Day-Month-Year format for the date and the 24 hour format for the time.\nAccepted format\n\
                \t'dd-mm-yyyy hh:mm'\n\nex:\n'8-12-2023 00:30'\n'08-2-2023 13:00'")

        if end_date := self.validate_date_time_format(self.entry_end.get()):
            self.entry_end.config(highlightthickness=0)
            self.reservation['end'] = end_date
        else:
            self.entry_end.config(highlightbackground="red", highlightthickness=0.5)
            showerror("Invalid end date format", "Please enter a valid start date and time following the Day-Month-Year format for the date and the 24 hour format for the time.\nAccepted format\n\
                \t'dd-mm-yyyy hh:mm'\n\nex:\n'8-12-2023 00:30'\n'08-2-2023 13:00'")



        # adding the reservation using the db.add_reservation, that will first check if the reservation is valid.
        if (db_handler.add_reservation(self.reservation)):
            logging.info(f"The student with the id '{self.reservation['id']}' made a new reservation: Class Number:{self.reservation['number']}, Location:{self.reservation['location']}, From:{self.reservation['start']}, To:{self.reservation['end']}")

            
        
    def select_item(self, event):        
        selected_record = self.tv_classroom.selection()
        selected_class = {"number":self.tv_classroom.item(selected_record)['values'][0],
                            "location":self.tv_classroom.item(selected_record)['values'][1],
                            "capacity": self.tv_classroom.item(selected_record)['values'][2]}

        # print(f"Number:{selected_class['number']}, LOCATION:{selected_class['location']}, CAPACITY:{selected_class['capacity']}")

        # adding the chosen class's number and location to the dictionary that will be passed to the db_handler
        self.reservation['number'] = selected_class['number']
        self.reservation['location'] = selected_class['location']
        # return selected row's detail as a dict
        return selected_class
    


    def validate_date_time_format(self, date_time):
        # validating using regex
        if(result := re.search(r"^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4} ([0-1]?[0-9]|2[0-3]):[0-5][0-9]$", date_time)):
            # converting the result to a datetime object
            date_time_obj = datetime.strptime(date_time, "%d-%m-%Y %H:%M")
            # ???????????????????????????????????????????????????????????????
            # converting the previous object to our standard date and time format
            date_time_obj = date_time_obj.strftime("%d-%m-%Y %H:%M")
            # returning the datetime obj just like what the user entered.
            return date_time_obj
        else:
            return False
    

    
    def logout_reserve(self):
        self.go_login()
    def logout_view(self):
        self.go_login()
    def go_login(self):
        self.root.destroy()
        login.LoginGUI()



if __name__ == "__main__":
    
    s = StudentGUI((111111111, "Ayman", "student"))
    



