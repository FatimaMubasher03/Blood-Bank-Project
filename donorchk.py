import tkinter as tk
from tkinter import messagebox, StringVar
from tkinter.ttk import Combobox
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import sqlite3
import random
from datetime import datetime,timedelta
import string
def convert_blood_group(blood_group_input):
    blood_group_mapping = {
        'A+': '00A',
        'A-': '01A',
        'B+': '00B',
        'B-': '01B',
        'O+': '00O',
        'O-': '01B',
        'AB+': '0AB',
        'AB-': '1AB'
    }
    return blood_group_mapping.get(blood_group_input, '')

class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.insert("0", self.placeholder)
        self.config(fg="white")
        self.bind("<FocusIn>", self.on_entry_click)
        self.bind("<FocusOut>", self.on_focus_out)

    def on_entry_click(self, event):
        if self.get() == self.placeholder:
            self.delete(0, "end")
            self.config(fg="black")  # Change text color when typing

    def on_focus_out(self, event):
        if not self.get():
            self.insert("0", self.placeholder)
            self.config(fg="white")

class DonorPromptApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Donor Prompt")
        self.master.geometry("800x600")  # Adjusted the window size
        self.master.configure(bg="white")

        # Load and blur the image
        original_image = Image.open("grid.png")

        # Resize the image to fit the window
        resized_image = original_image.resize((800, 600), Image.LANCZOS)

        # Apply GaussianBlur with a specific radius to control blurriness
        blurred_image = resized_image.filter(ImageFilter.GaussianBlur(radius=2))  # Adjust the radius as needed

        # Convert the image to a Tkinter-compatible format
        self.bg_image = ImageTk.PhotoImage(blurred_image)

        # Create a Canvas widget to display the image
        self.canvas = tk.Canvas(self.master, width=800, height=600, highlightthickness=0)
        self.canvas.grid(row=0, column=0, rowspan=19, columnspan=2)

        # Display the resized image on the Canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)

        # Heading label
        text_message = "In serving humanity, we find the true essence of our existence!"
        self.canvas.create_text(370, 20, text=text_message, font=("Georgia", 14), fill="white")

        self.create_widgets()

    def create_widgets(self):
        # Customize font options
        custom_font = ("Georgia", 12)  # Change font type and size as needed
        custom_font_color = "white"  # Change font color as needed

        # Label for Membership ID
        self.label_membership_id = tk.Label(self.master, text="DONOR ID:", bg="crimson", font=custom_font,
                                            fg=custom_font_color)
        self.label_membership_id.grid(row=3, column=0, pady=5, padx=10, sticky="w")

        # Entry for Membership ID with placeholder
        self.membership_id_var = StringVar()
        self.entry_membership_id = EntryWithPlaceholder(self.master, textvariable=self.membership_id_var,
                                                        placeholder="ENTER ID e.g BKD000", width=30, font=('Times new roman',12),bg='crimson')
        self.entry_membership_id.grid(row=3, column=1, pady=5, padx=10, sticky="w")

        # Label for Name
        self.label_name = tk.Label(self.master, text="Name:", bg="crimson", font=custom_font, fg=custom_font_color)
        self.label_name.grid(row=4, column=0, pady=5, padx=10, sticky="w")

        # Entry for Name
        self.name_var = StringVar()
        self.entry_name = tk.Entry(self.master, textvariable=self.name_var, font=custom_font,bg='crimson')
        self.entry_name.grid(row=4, column=1, pady=5, padx=10, sticky="w")

        # Label for Age
        self.label_age = tk.Label(self.master, text="Age:", bg="crimson", font=custom_font, fg=custom_font_color)
        self.label_age.grid(row=5, column=0, pady=5, padx=10, sticky="w")

        # Entry for Age
        self.age_var = StringVar()
        self.entry_age = tk.Entry(self.master, textvariable=self.age_var, font=custom_font,bg='crimson')
        self.entry_age.grid(row=5, column=1, pady=5, padx=10, sticky="w")

        # Label for Blood Type
        self.label_blood_type = tk.Label(self.master, text="Blood Type:", bg="crimson", font=custom_font,
                                         fg=custom_font_color)
        self.label_blood_type.grid(row=6, column=0, pady=5, padx=10, sticky="w")

        blood_types = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
        self.blood_type_var = StringVar()
        self.blood_type_dropdown = Combobox(self.master, textvariable=self.blood_type_var, values=blood_types,
                                            state="readonly", font=custom_font)
        self.blood_type_dropdown.grid(row=6, column=1, pady=5, padx=10, sticky="w")
        self.blood_type_dropdown.current(0)

        # Label for Contact Number
        self.label_contact_number = tk.Label(self.master, text="Contact Number:", bg="crimson", font=custom_font,
                                             fg=custom_font_color)
        self.label_contact_number.grid(row=7, column=0, pady=5, padx=10, sticky="w")

        # Entry for Contact Number
        self.contact_number_var = StringVar()
        self.entry_contact_number = tk.Entry(self.master, textvariable=self.contact_number_var, font=custom_font,bg='crimson')
        self.entry_contact_number.grid(row=7, column=1, pady=5, padx=10, sticky="w")

        # Label for Amount Required
        self.label_amount_required = tk.Label(self.master, text="Amount Donated:", bg="crimson", font=custom_font,
                                              fg=custom_font_color)
        self.label_amount_required.grid(row=8, column=0, pady=5, padx=10, sticky="w")

        # Entry for Amount Required with placeholder
        self.amount_required_var = StringVar()
        self.entry_amount_required = EntryWithPlaceholder(self.master, textvariable=self.amount_required_var,
                                                          placeholder="Enter no. of units", width=30, font=custom_font,bg='crimson')
        self.entry_amount_required.grid(row=8, column=1, pady=5, padx=10, sticky="w")

        # Label for Status
        self.label_status = tk.Label(self.master, text="Status:", bg="crimson", font=custom_font, fg=custom_font_color)
        self.label_status.grid(row=9, column=0, pady=5, padx=10, sticky="w")

        # Radio buttons for Status
        self.status_var = StringVar()
        self.status_buttons = []
        status_options = ["Eligible", "Not Eligible"]
        for i, status_option in enumerate(status_options):
            button = tk.Radiobutton(self.master, text=status_option, variable=self.status_var, value=status_option,
                                    bg="crimson", font=custom_font, fg=custom_font_color)
            button.grid(row=9, column=1, pady=5, padx=(10 + i * 120), sticky="w")  # Adjusted padx for separation
            self.status_buttons.append(button)


        # Submit Button
        self.submit_button = tk.Button(self.master, text="Submit", command=self.submit_form, bg="crimson", fg="white",
                                       font=custom_font, width=7, height=1)
        self.submit_button.grid(row=11, column=0, columnspan=2, pady=10)

    def insert_donor_data_into_db(self, data):
        conn = sqlite3.connect('Blood_Bank.db')
        cursor = conn.cursor()
        cursor.execute('''
                INSERT INTO donors (
                    DONOR_ID, NAME, AGE, BLOOD_TYPE, CONTACT_NUMBER, AMOUNT_DONATED, STATUS
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', data)
        conn.commit()
    def get_last_row(self, cur, table_name):
        cur.execute(f'SELECT * FROM {table_name}')
        rows = cur.fetchall()
        return rows[-1] if rows else None

    def generate_bag_id(self, cur):
        last_row = self.get_last_row(cur, 'BloodInventory')

        if last_row is None:
            bag_id = 'bg01'
        else:
            last_id = last_row[0]
            last_number = int(last_id[2:])
            new_number = last_number + 1
            bag_id = f"bg{new_number:02d}"

        return bag_id

    def calculate_expiry_date(self, collection_date):
        collection_date_obj = datetime.strptime(collection_date, '%Y-%m-%d')
        expiry_date_obj = collection_date_obj + timedelta(days=42)
        return expiry_date_obj.date().strftime('%Y-%m-%d')


    def insert_blood_inventory(self, donor_id, blood_type, status):
        bloodbank_db = sqlite3.connect("Blood_Bank.db")
        bloodbank_cur = bloodbank_db.cursor()

        current_datetime = datetime.now()
        collection_date = current_datetime.strftime("%Y-%m-%d")
        expiry_date = self.calculate_expiry_date(collection_date)
        bag_id = self.generate_bag_id(bloodbank_cur)
        recipient_id = ''

        bloodbank_cur.execute('''
            INSERT INTO BloodInventory (
                BagID, DonorID, BloodType, CollectionDate, ExpiryDate, RecipientID, Status
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (bag_id, donor_id, blood_type, collection_date, expiry_date, recipient_id, status))
        bloodbank_db.commit()
        bloodbank_db.close()

    def submit_form(self):
        # Validate the input fields
        if not self.validate_input():
            messagebox.showerror("Error", "Invalid input. Please check the fields.")
            return

        # Get data from the input fields
        donor_id = self.membership_id_var.get()
        name = self.name_var.get()
        age = self.age_var.get()
        blood_group_input = self.blood_type_var.get()
        blood_type = convert_blood_group(blood_group_input)
        contact_number = self.contact_number_var.get()
        amount_donated = self.amount_required_var.get()
        status_input = self.status_var.get().lower()
        status = "1" if status_input == "eligible" else "0"
        # Display the information in a messagebox
        message = (
            f"Donor ID: {donor_id}\n"
            f"Name: {name}\n"
            f"Age: {age}\n"
            f"Blood Type: {blood_type}\n"
            f"Contact Number: {contact_number}\n"
            f"Amount Donated: {amount_donated}\n"
            f"Status: {status}"
        )

        # Prepare the data for insertion into the database
        donor_data = (donor_id, name, age, blood_type, contact_number, amount_donated, status)
        status_2=0

        # Insert data into the database
        self.insert_blood_inventory(donor_id, blood_type, status_2)
        self.insert_donor_data_into_db(donor_data)
        inventory_message = f"Inventory updated for donor ID: {donor_id}"
        messagebox.showinfo("Inventory Updated", inventory_message)

            # Prepare donor information message
        donor_message = (
                f"Donor ID: {donor_id}\n"
                f"Name: {name}\n"
                f"Age: {age}\n"
                f"Blood Type: {blood_type}\n"
                f"Contact Number: {contact_number}\n"
                f"Amount Donated: {amount_donated}\n"
                f"Status: {status}"
            )

            # Show the donor information message
        messagebox.showinfo("Donor Information", donor_message)

            # Rest of your code...

    # ... (Rest of your code)

    def validate_input(self):
        # Validate the length of Membership ID
        if len(self.membership_id_var.get()) ==0:
            return False

        # Validate that Age is an integer
        try:
            int(self.age_var.get())
        except ValueError:
            return False

        # Validate that Contact Number is 11 characters long
        if len(self.contact_number_var.get()) ==0:
            return False

        # Validate that Amount Required is an integer
        try:
            int(self.amount_required_var.get())
        except ValueError:
            return False

        # You can add more validation as needed

        return True


if __name__ == "__main__":
    root = tk.Tk()
    app = DonorPromptApp(root)
    root.mainloop()



