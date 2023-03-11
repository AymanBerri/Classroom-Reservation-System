import hashlib
import sqlite3
import csv
from datetime import datetime
from tkinter.messagebox import showerror, showinfo
import tkinter as tk
from tkinter import ttk

# central db's name = ksu.db
db_path = "ksu.db"

def run_script():
    conn = sqlite3.connect(db_path)
    print("Connection established successfully.")



    # script for creating the table
    # try:
    conn.executescript(
        '''
        CREATE TABLE KSU 
        (
            ID          INT             PRIMARY KEY     NOT NULL,
            FIRST       TEXT                            NOT NULL,
            SECOND      TEXT                            NOT NULL,
            PASSWORD    CHAR(64)                        NOT NULL,
            EMAIL       VARCHAR(60)     UNIQUE          NOT NULL,
            PHONE       CHAR(10)        UNIQUE          NOT NULL,
            USER_TYPE   VARCHAR(20)                     NOT NULL
        );
        

        CREATE TABLE CLASSROOM
        (
            NUMBER          INT            NOT NULL,
            LOCATION        INT            NOT NULL,
            CAPACITY        INT            NOT NULL,

            PRIMARY KEY (NUMBER, LOCATION)
        );

        CREATE TABLE RESERVATION 
        (
            ID              INT             NOT NULL,
            NUMBER          INT             NOT NULL, 
            LOCATION        INT             NOT NULL,
            START           TEXT            NOT NULL,
            END             TEXT            NOT NULL,

            PRIMARY KEY (ID, NUMBER, LOCATION, START, END)
        );
        '''
    )

    add_admin()
    
    # except sqlite3.OperationalError:
        # print(f"The DB already exists")

    print("Table creation was successfull.")
    conn.close()

def display_db():
    ws = tk.Tk()
    ws.title('TreeView')
    ws.geometry('1150x600')

    conn = sqlite3.connect(db_path)

    # TREEVIEW FOR THE KSU TABLE
    
    tv_ksu = ttk.Treeview(ws, columns=(1, 2, 3, 4, 5, 6, 7), show='headings', height=8)
    # creating columns to change their width
    for col in range(8):
        tv_ksu.column(col, width=150, anchor='center')
    tv_ksu.heading(1, text="ID")
    tv_ksu.heading(2, text="FIRST")
    tv_ksu.heading(3, text="SECOND")
    tv_ksu.heading(4, text="PASSWORD")
    tv_ksu.heading(5, text="EMAIL")
    tv_ksu.heading(6, text="PHONE")
    tv_ksu.heading(7, text="USER_TYPE")

    cursor_ksu = conn.execute(f"SELECT * from KSU")
    count = 0

    for row in cursor_ksu:
        tv_ksu.insert(parent='', index=count, text='', values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        count+=1
    # print ("KSU TABLE display successful.")

    # TREEVIEW FOR THE CLASSROOM TABLE
    
    tv_classroom = ttk.Treeview(ws, columns=(1,2,3), show='headings', height=8)
    # creating columns to change their width
    for col in range(4):
        tv_classroom.column(col, width=150, anchor='center')
    tv_classroom.heading(1, text="NUMBER")
    tv_classroom.heading(2, text="LOCATION")
    tv_classroom.heading(3, text="CAPACITY")


    cursor_classroom = conn.execute(f"SELECT * from CLASSROOM")
    count = 0

    for row in cursor_classroom:
        tv_classroom.insert(parent='', index=count, text='', values=(row[0], row[1], row[2]))
        count+=1
    # print ("CLASSROOM TABLE display successful.")

    # TREEVIEW FOR THE RESERVATION TABLE
    tv_reservation = ttk.Treeview(ws, columns=(1,2,3,4,5), show='headings', height=8)
    # creating columns to change their width
    for col in range(6):
        tv_reservation.column(col, width=150, anchor='center')
    tv_reservation.heading(1, text="ID")
    tv_reservation.heading(2, text="NUMBER")
    tv_reservation.heading(3, text="LOCATION")
    tv_reservation.heading(4, text="START")
    tv_reservation.heading(5, text="END")

    cursor_reservation = conn.execute(f"SELECT * from RESERVATION")
    count = 0

    for row in cursor_reservation:
        tv_reservation.insert(parent='', index=count, text='', values=(row[0], row[1], row[2], row[3], row[4]))
        count+=1


    conn.close()
    tk.Label(ws, text="User Table", anchor=tk.CENTER, font=30).pack()
    tv_ksu.pack()
    tk.Label(ws, text="Classroom Table", anchor=tk.CENTER, font=30).pack()
    tv_classroom.pack()
    tk.Label(ws, text="Reservation Table", anchor=tk.CENTER, font=30).pack()
    tv_reservation.pack()
    ws.mainloop()


def add_admin():
    # this method is static, AND ONLY FOR THE USE IN THE BACK-END
    with sqlite3.connect(db_path) as conn:
        try:
            # put your password here    \/\/
            password = hashlib.sha256("admin1".encode()).hexdigest()

            conn.execute(f"INSERT INTO KSU VALUES(111111111, 'admin', 'admin', '{password}', 'admin@admin.admin', '0500000000', 'admin')")
            conn.commit()
        except sqlite3.IntegrityError:
            print("[ERROR] This admin already exists.")

# instead of showerror, let it return False
def add_student(acc):
    with sqlite3.connect(db_path) as conn:
        try:
            conn.execute(f"INSERT INTO KSU VALUES({acc['id']}, '{acc['first']}', '{acc['second']}', '{acc['password']}', '{acc['email']}', '{acc['phone']}', 'student')")
            conn.commit()

            # True declares that the student was created.
            showinfo("User created", "User creation was successful.")
            return True
        except sqlite3.IntegrityError as e:
            # to get the attribute that failed
            att = str(e).split(".",1)[1].title()
            showerror(f"{att} already exists", f"A student with the same {att} already exists.")
            
        except sqlite3.OperationalError as e:
            print(e)

            
            
def check_user_exists(id, password):
    '''this method checks if the id and password of a user exists and are identical'''
    with sqlite3.connect(db_path) as conn:
        query = conn.execute(f"SELECT * FROM KSU WHERE ID = '{id}' LIMIT 1;")
        user = query.fetchone()

        # if the user doesn't exist
        if not user:
            print("[ERROR] User doesn't exist")
            return False
        
        # password check
        if(user[3] != password):
            print("[ERROR] Wrong password")
            return False

        # print((user[0], user[1], user[6]))
        # Returning     (id, firstname, usertype)
        return          (user[0], user[1], user[6])

def add_classroom(cour):
    with sqlite3.connect(db_path) as conn:
        try:
            conn.execute(f"INSERT INTO CLASSROOM VALUES({cour['number']}, {cour['location']}, {cour['capacity']})")
            conn.commit()
            showinfo("Classroom created", "Classroom creation was successful.")

            # True declares that the CLASSROOM was created.
            return True
        except sqlite3.IntegrityError:
            showerror("Classroom already exists", "The classroom already exists.")
            return False

            

def add_reservation(res):
    with sqlite3.connect(db_path) as conn:   

        if(check_valid_reservation(res)):
            try:
                conn.execute(f"INSERT INTO RESERVATION VALUES({res['id']},{res['number']}, {res['location']},'{res['start']}','{res['end']}')")
                conn.commit()
                showinfo("Reservation Successfull", f"Your reservation was successfull.")
                return True 

            except sqlite3.IntegrityError:
                showerror("Reservation exists", "This exact reservation already exists.")
                return False
            

def check_valid_reservation(res):
    with sqlite3.connect(db_path) as conn:

        # getting all the reservations of the class from the DB using the number and location
        try:
            cursor_reservation = conn.execute(f"SELECT * FROM RESERVATION WHERE NUMBER={res['number']} AND LOCATION={res['location']}")
        except KeyError:
            # when the program doesn't know what is 'number' and 'location', mostly the user didn't select a CLASSROOM from the list.
            showerror("Select classroom", "You must select the classroom you wish to reserve.")


        # converting input dates to datetime object
        startA = convert_datetime_obj(res['start'])
        endA = convert_datetime_obj(res['end'])

        # print(startA)
        # VALID DATE CHECKING

        # check if user entered a start date from the future:
        # getting the date time now
        today = datetime.now()
        # converting it to our agreed format
        today = datetime.strptime(str(today), "%Y-%m-%d %H:%M:%S.%f")
        today = today.strftime("%d-%m-%Y %H:%M")
        # turning it to a datetime obj for comparing
        today = convert_datetime_obj(today)

        # compare
        if startA < today:
            showerror("Invalid start date", f"The start date must be after {today.strftime('%d-%m-%Y %H:%M')}")
            return False

        # check if user entered start date before the end
        if startA >= endA:
            showerror("Invalid end date", "The end date must come after the start date.")
            return False


    for row in cursor_reservation:
        # converting the date string to a datetime object
        startB = convert_datetime_obj(row[3])
        endB = convert_datetime_obj(row[4])


        # OVERLAP CHECKING
        # can't start or end inside another reservation
        if(startA >= startB and startA < endB): 
            showerror("Start error", f"Existing reservation:\n    Start: {startB.strftime('%d-%m-%Y %H:%M')}\n    End: {endB.strftime('%d-%m-%Y %H:%M')}\n\nPlease modify your start date accordingly.")
            return False
        if(endA <= endB and endA > startB): 
            showerror("End error", f"Existing reservation:\n    Start: {startB.strftime('%d-%m-%Y %H:%M')}\n    End: {endB.strftime('%d-%m-%Y %H:%M')}\n\nPlease modify your end date accordingly.")
            return False

        # can't start a reservation araound an existing one
        if(startA < startB and endA > endB): 
            showerror("Around error", f"Existing reservation:\n    Start: {startB.strftime('%d-%m-%Y %H:%M')}\n    End: {endB.strftime('%d-%m-%Y %H:%M')}\n\nPlease modify your start or end accordingly.")
            return False
      
    # if reservation is a go-go
    return True
    

def convert_datetime_obj(dt):
    # in: <str>
    # creating returning a datetime object
    return datetime.strptime(dt, "%d-%m-%Y %H:%M")
    
        
def backup_db():
    # must first clear the file before saving, as to not have duplicate data
    open("backup.csv", "w+")

    # connect to DB
    conn = sqlite3.connect(db_path)
    for table in ["KSU", "CLASSROOM", "RESERVATION"]:
        # retrieving all the data of the table
        cursor = conn.execute(f"SELECT * FROM {table}")

        # getting all the headers of the table
        headers = []
        for i in cursor.description:
            headers.append(i[0])
        
        # getting all the entries
        data = cursor.fetchall()
        
        # finally, calling another method to save them to the csv
        save_to_csv(headers, data)
    
    showinfo("Backup", "The backup was successfull.")

def save_to_csv(header, data):
    with open('backup.csv', 'a', newline='') as bf:
        writer = csv.writer(bf)

        # write the header
        writer.writerow(header)

        # write the data
        writer.writerows(data)

        
            

def drop_tables():
    with sqlite3.connect(db_path) as conn:
        # # Dropping KSU table if already exists.
        conn.execute("DROP TABLE IF EXISTS KSU")
        conn.commit()
        conn.execute("DROP TABLE IF EXISTS CLASSROOM")
        conn.commit()
        conn.execute("DROP TABLE IF EXISTS RESERVATION")
        conn.commit()
        print("Tables Dropped")
def clear_table(table):
    with sqlite3.connect(db_path) as conn:
        # # Dropping KSU table if already exists.
        conn.execute(f"DELETE FROM {table.upper()};")

        print(f"Table {table.upper()} Cleared")



if __name__ == "__main__":

    # put your password here    \/\/
    password = hashlib.sha256("ayman1".encode()).hexdigest()
    test_user = {'email': 'a_b@gmail.com','first': 'a','id': '442105433','password': password,'phone': '0555555955','second': 'b'}
    test_classroom = {'number': 45, 'location': 31, 'capacity': 100}
    test_classroom1 = {'number': 44, 'location': 31, 'capacity': 100}
    test_reservation = {'id': 111222333, 'number': 123, 'location':456, 'start':'11-2-2024 13:00', 'end':'11-2-2024 16:00'}
    test_reservation1 = {'id': 111222334, 'number': 123, 'location':456, 'start':'11-2-2000 12:00', 'end':'10-2-2023 12:00'}
    # test_reservation2 = {'id': 111222335, 'number': 123, 'location':456, 'start':'11-2-2023 13:00', 'end':'11-2-2023 13:11'}

    # drop_tables()
    # clear_table("classroom")
    # clear_table("ksu")
    # clear_table("reservation")
    add_admin()
    # run_script()
    # backup_db()

    # add_student(test_user)
    # add_classroom(test_classroom)
    # add_classroom(test_classroom1)
    # add_reservation(test_reservation)
    # add_reservation(test_reservation1)
    # add_reservation(test_reservation2)
   

    display_db()

