import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox, StringVar
from tkinter.ttk import Combobox
import sqlite3
from tkinter import simpledialog


def map_blood_type(blood_type_code):
    mapping = {'01A': 'A+', '00A': 'A-', '01B': 'B+', '00B': 'B-', '01O': 'O+', '00O': 'O-', '1AB': 'AB+',
               '0AB': 'AB-'}
    return mapping.get(blood_type_code, "Unknown")
class BloodDonationApp:
    def __init__(self, master, db_path):
        self.master = master
        self.master.title("Blood Donation App")
        self.master.geometry("400x400")
        self.master.configure(bg="white")

        style = ttk.Style()
        style.configure("TNotebook.Tab", padding=(10, 8), font=('Times new roman', 10), bg='red')

        self.notebook = ttk.Notebook(self.master)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        donor_tab = ttk.Frame(self.notebook)
        recipient_tab = ttk.Frame(self.notebook)
        storage_tab = ttk.Frame(self.notebook)

        self.notebook.add(donor_tab, text="  DONOR INFO  ")
        self.notebook.add(recipient_tab, text="  RECIPIENT INFO  ")
        self.notebook.add(storage_tab, text=" BLOOD STORAGE ")

        self.create_tab_with_image_and_buttons(donor_tab, "crumbled.png", self.search_donor, self.show_all_donors)
        self.create_tab_with_image_and_buttons(recipient_tab, "crumbled.png", self.search_recipient, self.show_all_recipients)
        self.create_tab_with_image_and_buttons(storage_tab, "crumbled.png", self.search_blood_bag, self.show_blood_storage)

        # Connect to the database
        self.conn = sqlite3.connect('Blood_Bank.db')
        self.cursor = self.conn.cursor()

    def create_tab_with_image_and_buttons(self, tab, image_path, search_command, show_all_command):
        # Open the image with Pillow
        img = Image.open(image_path)
        img = ImageTk.PhotoImage(img)

        # Create a Label to display the image
        image_label = tk.Label(tab, image=img)
        image_label.image = img
        image_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Configure row and column weights for resizing
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(0, weight=1)

        # Options
        button_search = tk.Button(tab, text="Search", command=search_command, bg="white", fg="red",
                                  font=("Georgia", 12), width=15, height=2)
        button_search.grid(row=1, column=0, pady=(2, 0))

        button_show_all = tk.Button(tab, text="Show All", command=show_all_command, bg="white",
                                    fg="red", font=("Georgia", 12), width=15, height=2)
        button_show_all.grid(row=2, column=0, pady=(0, 2))

    def search_donor(self):
        # Prompt the user to enter the donor ID
        donor_id = simpledialog.askstring("Search Donor", "Enter Donor ID:")

        if not donor_id:
            # User clicked Cancel or entered an empty string
            return

        # Example query: Retrieve donor information from the "donors" table
        self.cursor.execute("SELECT * FROM donors WHERE DONOR_ID = ?", (donor_id,))
        donor_info = self.cursor.fetchone()

        # Display donor information in the new window
        result_text = self.format_donor_result(donor_info)

        # Create a Text widget to display the result
        self.display_result(result_text, "Search Donor Result")

    def format_donor_result(self, donor_info):
        if donor_info:
            if donor_info[6] == 1:
                status_readable = 'ELIGIBLE'
            else:
                status_readable = "INELIGIBLE"
            blood_type_readable = map_blood_type(donor_info[3])
            result_text = (
                f"{'DONOR_ID':<10} {'NAME':<15} {'AGE':^4} {'BLOOD_TYPE':^2} "
                f"{'CONTACT_NUMBER':^15} {'AMOUNT DONATED':^13}  {'STATUS':<10}\n"
                '========== ============== ==== =========== =============== =============   =======\n'
                f"{donor_info[0]:<10} {donor_info[1]:<15} {str(donor_info[2]):^2} "
                f"{blood_type_readable:^11} {donor_info[4]:^16} "
                f"{str(donor_info[5]) + ' ml':<16}{status_readable:<5}"
            )
        else:
            result_text = "No information found for the specified donor ID."

        return result_text

    def show_all_donors(self):
        donor_root = tk.Toplevel(self.master)
        donor_root.geometry("900x600")
        donor_root.title("Show All Donors")

        try:
            # Example query: Retrieve all donor information from the "donors" table
            self.cursor.execute("SELECT * FROM donors")
            donors_info = self.cursor.fetchall()

            # Display donor information in the new window (you can customize this part)
            result_text = f"{'DONOR_ID':<10} {'NAME':<15} {'AGE':^4} {'BLOOD_TYPE':^2} {'CONTACT_NUMBER':^15} {'AMOUNT DONATED':^13}  {'STATUS':<10}\n"
            result_text += '========== ============== ==== =========== =============== =============   =======\n'
            for donor_info in donors_info:
                if donor_info[6] == 1:
                    status_readable = 'ELIGIBLE'
                else:
                    status_readable = "INELIGIBLE"
                blood_type_readable = map_blood_type(donor_info[3])
                result_text += f"{donor_info[0]:<10} {donor_info[1]:<15} {str(donor_info[2]):^2} {blood_type_readable:^11} {donor_info[4]:^16} {str(donor_info[5]) + ' ml':<16}{status_readable:<5}\n"

            # Create a Text widget to display the result with a larger size
            result_display = tk.Text(donor_root, wrap=tk.WORD, height=40, width=120)  # Adjust height and width as needed
            result_display.insert(tk.END, result_text)
            result_display.pack()


        except sqlite3.Error as e:
            print(f"Error fetching donor data: {e}")
            tk.messagebox.showerror("Error", "Error fetching donor data")

    def search_recipient(self):
        # Prompt the user to enter the recipient ID
        recipient_id = simpledialog.askstring("Search Recipient", "Enter Recipient ID:")

        if not recipient_id:
            # User clicked Cancel or entered an empty string
            return

        # Example query: Retrieve recipient information from the "recipients" table
        self.cursor.execute("SELECT * FROM RECIPIENT WHERE recipientid = ?", (recipient_id,))
        recipient_info = self.cursor.fetchone()

        # Display recipient information in the new window
        result_text = self.format_recipient_result(recipient_info)

        # Create a Text widget to display the result
        self.display_result(result_text, "Search Recipient Result")

    def format_recipient_result(self, recipient_info):
        if recipient_info:
            if recipient_info[6] == 1:
                status_readable = 'ACCEPTED'
            else:
                status_readable = "PENDING"
            blood_type_readable = map_blood_type(recipient_info[3])
            result_text = (
                f"{'RECIPIENT_ID':<13} {'NAME':<15} {'AGE':^4} {'BLOOD_TYPE':^2} "
                f"{'CONTACT_NUMBER':^15} {'AMOUNT RECEIVED':^16}  {'STATUS':<10} {'DATE_OF_REQUEST':<10}\n"
                '============ ============    ==== =========== =============== ================  =======     ==============\n'
                f"{recipient_info[0]:<13} {recipient_info[1]:<15} {str(recipient_info[2]):^4} "
                f"{blood_type_readable:^11} {recipient_info[4]:^16} "
                f"{str(recipient_info[5]) + ' ml':<16}{status_readable:<10}  {str(recipient_info[7]):11}"
            )
        else:
            result_text = "No information found for the specified recipient ID."

        return result_text

    def show_all_recipients(self):
        recipient_root = tk.Toplevel(self.master)
        recipient_root.geometry("900x600")
        recipient_root.title("Show All Recipients")

        try:
            # Example query: Retrieve all recipient information from the "recipients" table
            self.cursor.execute("SELECT * FROM RECIPIENT")
            recipients_info = self.cursor.fetchall()

            # Display recipient information in the new window (you can customize this part)
            result_text = f"{'RECIPIENT_ID':<13} {'NAME':<15} {'AGE':^4} {'BLOOD_TYPE':^2}  {'CONTACT_NUMBER':^15} {'AMOUNT RECEIVED':^16}  {'STATUS':<10} {'DATE_OF_REQUEST':<10}\n"
            result_text += '============ ============    ==== =========== =============== ================  =======     ==============\n'
            for recipient_info in recipients_info:
                if recipient_info[6] == 1:
                    status_readable = 'ACCEPTED'
                else:
                    status_readable = "PENDING"
                blood_type_readable = map_blood_type(recipient_info[3])
                result_text += f"{recipient_info[0]:<13} {recipient_info[1]:<15} {str(recipient_info[2]):^4} {blood_type_readable:^11} {recipient_info[4]:^16} {str(recipient_info[5]) + ' ml':<16}{status_readable:<10}  {str(recipient_info[7]):11}\n"

            # Create a Text widget to display the result with a larger size
            result_display = tk.Text(recipient_root, wrap=tk.WORD, height=40,
                                     width=120)  # Adjust height and width as needed
            result_display.insert(tk.END, result_text)
            result_display.pack()


        except sqlite3.Error as e:
            print(f"Error fetching recipient data: {e}")
            tk.messagebox.showerror("Error", "Error fetching recipient data")

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from tkinter.ttk import Combobox
import sqlite3
from PIL import Image, ImageTk

def map_blood_type(blood_type_code):
    mapping = {'01A': 'A+', '00A': 'A-', '01B': 'B+', '00B': 'B-', '01O': 'O+', '00O': 'O-', '1AB': 'AB+',
               '0AB': 'AB-'}
    return mapping.get(blood_type_code, "Unknown")

class BloodDonationApp:
    def __init__(self, master, db_path):
        self.master = master
        self.master.title("Blood Donation App")
        self.master.geometry("400x400")
        self.master.configure(bg="white")

        style = ttk.Style()
        style.configure("TNotebook.Tab", padding=(10, 8), font=('Times new roman', 10), bg='red')

        # Initialize the notebook
        self.notebook = ttk.Notebook(self.master)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        # Create tabs
        donor_tab = ttk.Frame(self.notebook)
        recipient_tab = ttk.Frame(self.notebook)
        storage_tab = ttk.Frame(self.notebook)

        # Add tabs to the notebook
        self.notebook.add(donor_tab, text="  DONOR INFO  ")
        self.notebook.add(recipient_tab, text="  RECIPIENT INFO  ")
        self.notebook.add(storage_tab, text=" BLOOD STORAGE ")

        # Connect to the database
        self.conn = sqlite3.connect('Blood_bank.db')
        self.cursor = self.conn.cursor()

        # Create tabs with images and buttons
        self.create_tab_with_image_and_buttons(donor_tab, "bdboy.png", self.search_donor, self.show_all_donors)
        self.create_tab_with_image_and_buttons(recipient_tab, "dbrec2.png", self.search_recipient, self.show_all_recipients)
        self.create_tab_with_image_and_buttons(storage_tab, "stg3.png", self.search_blood_bag, self.show_blood_storage)

    def create_tab_with_image_and_buttons(self, tab, image_path, search_command, show_all_command):
        # Open the image with Pillow
        img = Image.open(image_path)
        img = ImageTk.PhotoImage(img)

        # Create a Label to display the image
        image_label = tk.Label(tab, image=img)
        image_label.image = img
        image_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Configure row and column weights for resizing
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(0, weight=1)

        # Options
        button_search = tk.Button(tab, text="Search", command=search_command, bg="white", fg="red",
                                  font=("Georgia", 12), width=15, height=2)
        button_search.grid(row=1, column=0, pady=(2, 0))

        button_show_all = tk.Button(tab, text="Show All", command=show_all_command, bg="white",
                                    fg="red", font=("Georgia", 12), width=15, height=2)
        button_show_all.grid(row=2, column=0, pady=(0, 2))

    def search_donor(self):
        donor_id = simpledialog.askstring("Search Donor", "Enter Donor ID:")
        if not donor_id:
            return

        self.cursor.execute("SELECT * FROM donors WHERE DONOR_ID = ?", (donor_id,))
        donor_info = self.cursor.fetchone()

        result_text = self.format_donor_result(donor_info)
        self.display_result(result_text, "Search Donor Result")

    def format_donor_result(self, donor_info):
        if donor_info:
            status_readable = 'ELIGIBLE' if donor_info[6] == 1 else 'INELIGIBLE'
            blood_type_readable = map_blood_type(donor_info[3])
            result_text = (
                f"{'DONOR_ID':<10} {'NAME':<15} {'AGE':^4} {'BLOOD_TYPE':^2} "
                f"{'CONTACT_NUMBER':^15} {'AMOUNT DONATED':^13}  {'STATUS':<10}\n"
                '========== ============== ==== =========== =============== =============   =======\n'
                f"{donor_info[0]:<10} {donor_info[1]:<15} {str(donor_info[2]):^2} "
                f"{blood_type_readable:^11} {donor_info[4]:^16} "
                f"{str(donor_info[5]) + ' ml':<16}{status_readable:<5}"
            )
        else:
            result_text = "No information found for the specified donor ID."

        return result_text

    def show_all_donors(self):
        donor_root = tk.Toplevel(self.master)
        donor_root.geometry("900x600")
        donor_root.title("Show All Donors")

        try:
            self.cursor.execute("SELECT * FROM donors")
            donors_info = self.cursor.fetchall()

            result_text = f"{'DONOR_ID':<10} {'NAME':<15} {'AGE':^4} {'BLOOD_TYPE':^2} {'CONTACT_NUMBER':^15} {'AMOUNT DONATED':^13}  {'STATUS':<10}\n"
            result_text += '========== ============== ==== =========== =============== =============   =======\n'
            for donor_info in donors_info:
                status_readable = 'ELIGIBLE' if donor_info[6] == 1 else 'INELIGIBLE'
                blood_type_readable = map_blood_type(donor_info[3])
                result_text += f"{donor_info[0]:<10} {donor_info[1]:<15} {str(donor_info[2]):^2} {blood_type_readable:^11} {donor_info[4]:^16} {str(donor_info[5]) + ' ml':<16}{status_readable:<5}\n"

            result_display = tk.Text(donor_root, wrap=tk.WORD, height=40, width=120)
            result_display.insert(tk.END, result_text)
            result_display.pack()

        except sqlite3.Error as e:
            print(f"Error fetching donor data: {e}")
            tk.messagebox.showerror("Error", "Error fetching donor data")

    def search_recipient(self):
        recipient_id = simpledialog.askstring("Search Recipient", "Enter Recipient ID:")
        if not recipient_id:
            return

        self.cursor.execute("SELECT * FROM RECIPIENT WHERE recipientid = ?", (recipient_id,))
        recipient_info = self.cursor.fetchone()

        result_text = self.format_recipient_result(recipient_info)
        self.display_result(result_text, "Search Recipient Result")


    def format_recipient_result(self, recipient_info):
        if recipient_info:
            status_readable = 'ACCEPTED' if recipient_info[6] == 1 else 'PENDING'
            blood_type_readable = map_blood_type(recipient_info[3])
            result_text = (
                f"{'RECIPIENT_ID':<13} {'NAME':<15} {'AGE':^4} {'BLOOD_TYPE':^2} "
                f"{'CONTACT_NUMBER':^15} {'AMOUNT RECEIVED':^16}  {'STATUS':<10} {'DATE_OF_REQUEST':<10}\n"
                '============ ============    ==== =========== =============== ================  =======     ==============\n'
                f"{recipient_info[0]:<13} {recipient_info[1]:<15} {str(recipient_info[2]):^4} "
                f"{blood_type_readable:^11} {recipient_info[4]:^16} "
                f"{str(recipient_info[5]) + ' ml':<16}{status_readable:<10}  {str(recipient_info[7]):11}"
            )
        else:
            result_text = "No information found for the specified recipient ID."

        return result_text

    def show_all_recipients(self):
        recipient_root = tk.Toplevel(self.master)
        recipient_root.geometry("900x600")
        recipient_root.title("Show All Recipients")

        try:
            self.cursor.execute("SELECT * FROM RECIPIENT")
            recipients_info = self.cursor.fetchall()

            result_text = f"{'RECIPIENT_ID':<13} {'NAME':<15} {'AGE':^4} {'BLOOD_TYPE':^2}  {'CONTACT_NUMBER':^15} {'AMOUNT RECEIVED':^16}  {'STATUS':<10} {'DATE_OF_REQUEST':<10}\n"
            result_text += '============ ============    ==== =========== =============== ================  =======     ==============\n'
            for recipient_info in recipients_info:
                status_readable = 'ACCEPTED' if recipient_info[6] == 1 else 'PENDING'
                blood_type_readable = map_blood_type(recipient_info[3])
                result_text += f"{recipient_info[0]:<13} {recipient_info[1]:<15} {str(recipient_info[2]):^4} {blood_type_readable:^11} {recipient_info[4]:^16} {str(recipient_info[5]) + ' ml':<16}{status_readable:<10}  {str(recipient_info[7]):11}\n"

            result_display = tk.Text(recipient_root, wrap=tk.WORD, height=40, width=120)
            result_display.insert(tk.END, result_text)
            result_display.pack()

        except sqlite3.Error as e:
            print(f"Error fetching recipient data: {e}")
            tk.messagebox.showerror("Error", "Error fetching recipient data")

    def search_blood_bag(self):
        bag_id = simpledialog.askstring("Search Blood Bag", "Enter Blood Bag ID:")
        if not bag_id:
            return

        self.cursor.execute("SELECT * FROM BloodInventory WHERE BagID = ?", (bag_id,))
        bag_info = self.cursor.fetchone()

        result_text = self.format_blood_bag_result(bag_info)
        header = (
            f"{'Bag_ID':<12} {'DONOR_ID':<12} {'BLOOD_TYPE':<12} {'COLLECTION_DATE':<15} "
                f"{'EXPIRY_DATE':<15} {'RECIPIENT_ID':<12} {'STATUS':<10}\n"
                f'=========   ==========    ========     ===========     ===========     ===========  ========\n'
            )
        self.display_result(header + result_text, "Search Blood Bag Result")

    def format_blood_bag_result(self, bag_info):
        if bag_info:
            blood_type_mapping = map_blood_type(bag_info[2])
            status_mapping = {0: 'Available', 1: 'Donated', 2: 'Disposed'}
            st = status_mapping.get(int(bag_info[6]))

            result_text = (
                f"{bag_info[0]:<12} {bag_info[1]:<12} {blood_type_mapping:<12} {bag_info[3]:<15} "
                f"{bag_info[4]:<15} {bag_info[5]:<12} {st:<10}"
            )
        else:
            result_text = "No information found for the specified blood bag ID."

        return result_text

    def show_blood_storage(self):
        storage_root = tk.Toplevel(self.master)
        storage_root.geometry("900x600")
        storage_root.title("Show Blood Storage")

        try:
            self.cursor.execute("SELECT * FROM BloodInventory")
            bags_info = self.cursor.fetchall()

            bag_header = (
                f"{'Bag_ID':<12} {'DONOR_ID':<12} {'BLOOD_TYPE':<12} {'COLLECTION_DATE':<15} "
                f"{'EXPIRY_DATE':<15} {'RECIPIENT_ID':<12} {'STATUS':<10}\n"
                f'=========   ==========    ========     ===========     ===========     ===========  ========\n'
            )

            result_text = bag_header
            for bag_info in bags_info:
                blood_type_mapping = map_blood_type(bag_info[2])
                status_mapping = {0: 'Available', 1: 'Donated', 2: 'Disposed'}
                st = status_mapping.get(int(bag_info[6]))

                result_text += f"{bag_info[0]:<12} {bag_info[1]:<12} {blood_type_mapping:<12} {bag_info[3]:<15} {bag_info[4]:<15} {bag_info[5]:<12} {st:<10}\n"

            result_display = tk.Text(storage_root, wrap=tk.WORD, height=40, width=120)
            result_display.insert(tk.END, result_text)
            result_display.pack()

        except sqlite3.Error as e:
            print(f"Error fetching blood storage data: {e}")
            tk.messagebox.showerror("Error", "Error fetching blood storage data")

    def display_result(self, result_text, title):
        result_root = tk.Toplevel(self.master)
        result_root.geometry("1000x300")
        result_root.title(title)

        result_display = tk.Text(result_root, wrap=tk.WORD, height=20, width=140)
        result_display.insert(tk.END, result_text)
        result_display.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = BloodDonationApp(root, 'Blood_Bank.db')
    root.mainloop()

    def display_result(self, result_text, title):
        result_root = tk.Toplevel(self.master)
        result_root.geometry("900x600")
        result_root.title(title)

        # Create a Text widget to display the result
        result_display = tk.Text(result_root, wrap=tk.WORD)
        result_display.insert(tk.END, result_text)
        result_display.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = BloodDonationApp(root,'Blood_Bank.db')
    root.mainloop()

