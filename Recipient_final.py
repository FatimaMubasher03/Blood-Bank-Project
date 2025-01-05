import tkinter as tk
from tkinter import messagebox, StringVar
from tkinter.ttk import Combobox
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import sqlite3

def convert_blood_group(blood_group_input):
    blood_group_mapping = {
        'A+': '00A',
        'A-': '01A',
        'B+': '00B',
        'B-': '01B',
        'O+': '00O',
        'O-': '01B',  # Corrected mapping for 'O-'
        'AB+': '0AB',
        'AB-': '1AB'
    }
    return blood_group_mapping.get(blood_group_input, '')

class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.insert("0", self.placeholder)
        self.config(fg="grey")
        self.bind("<FocusIn>", self.on_entry_click)
        self.bind("<FocusOut>", self.on_focus_out)

    def on_entry_click(self, event):
        if self.get() == self.placeholder:
            self.delete(0, "end")
            self.config(fg="black")  # Change text color when typing

    def on_focus_out(self, event):
        if not self.get():
            self.insert("0", self.placeholder)
            self.config(fg="grey")

class RecipientPromptApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Recipient Prompt")
        self.master.geometry("800x600")  # Adjusted the window size
        self.master.configure(bg="white")

        # Load and blur the image
        original_image = Image.open("w111.png")

        # Resize the image to fit the window
        resized_image = original_image.resize((800, 600), Image.LANCZOS)

        # Apply GaussianBlur with a specific radius to control blurriness
        blurred_image = resized_image.filter(ImageFilter.GaussianBlur(radius=1))  # Adjust the radius as needed

        # Convert the image to a Tkinter-compatible format
        self.bg_image = ImageTk.PhotoImage(blurred_image)

        # Create a Canvas widget to display the image
        self.canvas = tk.Canvas(self.master, width=800, height=600, highlightthickness=0)
        self.canvas.grid(row=0, column=0, rowspan=19, columnspan=2)

        # Display the resized image on the Canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)

        # Heading label
        text_message = "Welcome! We're happy to serve you."
        self.canvas.create_text(350, 20, text=text_message, font=("Georgia", 14), fill="white")

        self.create_widgets()

    def create_widgets(self):
        # Customize font options
        custom_font = ("Georgia", 12)  # Change font type and size as needed
        custom_font_color = "black"  # Change font color as needed

        # Label for Membership ID
        self.label_membership_id = tk.Label(self.master, text="Membership ID:", bg="white", font=custom_font,
                                            fg=custom_font_color)
        self.label_membership_id.grid(row=3+1, column=0, pady=5, padx=10, sticky="w")

        # Entry for Membership ID with placeholder
        self.membership_id_var = StringVar()
        self.entry_membership_id = EntryWithPlaceholder(self.master, textvariable=self.membership_id_var,
                                                        placeholder="ENTER ID e.g BKR000", width=30, font=custom_font)
        self.entry_membership_id.grid(row=3+1, column=1, pady=5, padx=10, sticky="w")

        # Label for Name
        self.label_name = tk.Label(self.master, text="Name:", bg="white", font=custom_font, fg=custom_font_color)
        self.label_name.grid(row=4+1, column=0, pady=5, padx=10, sticky="w")

        # Entry for Name
        self.name_var = StringVar()
        self.entry_name = tk.Entry(self.master, textvariable=self.name_var, font=custom_font)
        self.entry_name.grid(row=4+1, column=1, pady=5, padx=10, sticky="w")

        # Label for Age
        self.label_age = tk.Label(self.master, text="Age:", bg="white", font=custom_font, fg=custom_font_color)
        self.label_age.grid(row=5+1, column=0, pady=5, padx=10, sticky="w")

        # Entry for Age
        self.age_var = StringVar()
        self.entry_age = tk.Entry(self.master, textvariable=self.age_var, font=custom_font)
        self.entry_age.grid(row=5+1, column=1, pady=5, padx=10, sticky="w")

        # Label for Blood Type
        self.label_blood_type = tk.Label(self.master, text="Blood Type:", bg="white", font=custom_font,
                                         fg=custom_font_color)
        self.label_blood_type.grid(row=6+1, column=0, pady=5, padx=10, sticky="w")

        blood_types = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
        self.blood_type_var = StringVar()
        self.blood_type_dropdown = Combobox(self.master, textvariable=self.blood_type_var, values=blood_types,
                                            state="readonly", font=custom_font)
        self.blood_type_dropdown.grid(row=6+1, column=1, pady=5, padx=10, sticky="w")
        self.blood_type_dropdown.current(0)

        # Label for Contact Number
        self.label_contact_number = tk.Label(self.master, text="Contact Number:", bg="white", font=custom_font,
                                             fg=custom_font_color)
        self.label_contact_number.grid(row=7+1, column=0, pady=5, padx=10, sticky="w")

        # Entry for Contact Number
        self.contact_number_var = StringVar()
        self.entry_contact_number = tk.Entry(self.master, textvariable=self.contact_number_var, font=custom_font)
        self.entry_contact_number.grid(row=7+1, column=1, pady=5, padx=10, sticky="w")

        # Label for Amount Required
        self.label_amount_required = tk.Label(self.master, text="Amount Required:", bg="white", font=custom_font,
                                              fg=custom_font_color)
        self.label_amount_required.grid(row=8+1, column=0, pady=5, padx=10, sticky="w")

        # Entry for Amount Required with placeholder
        self.amount_required_var = StringVar()
        self.entry_amount_required = EntryWithPlaceholder(self.master, textvariable=self.amount_required_var,
                                                          placeholder="Enter no. of units", width=30, font=custom_font)
        self.entry_amount_required.grid(row=8+1, column=1, pady=5, padx=10, sticky="w")

        # Label for Status
        self.label_status = tk.Label(self.master, text="Status:", bg="white", font=custom_font, fg=custom_font_color)
        self.label_status.grid(row=9+1, column=0, pady=5, padx=10, sticky="w")

        # Radio buttons for Status
        self.status_var = StringVar()
        self.status_buttons = []
        status_options = ["Received", "Pending"]
        for i, status_option in enumerate(status_options):
            button = tk.Radiobutton(self.master, text=status_option, variable=self.status_var, value=status_option,
                                    bg="white", font=custom_font, fg=custom_font_color)
            button.grid(row=9+1, column=1, pady=5, padx=(10 + i * 120), sticky="w")  # Adjusted padx for separation
            self.status_buttons.append(button)

        # Label for Date of Request
        self.label_date_of_request = tk.Label(self.master, text="Date of Request:", bg="white", font=custom_font,
                                              fg=custom_font_color)
        self.label_date_of_request.grid(row=10+1, column=0, pady=5, padx=10, sticky="w")

        # Entry for Date of Request
        self.date_of_request_var = StringVar()
        self.entry_date_of_request = tk.Entry(self.master, textvariable=self.date_of_request_var, font=custom_font)
        self.entry_date_of_request.grid(row=10+1, column=1, pady=5, padx=10, sticky="w")

        # Label for Additional Information
        self.label_additional_info = tk.Label(self.master, text="Additional Information:", bg="white", font=custom_font,
                                              fg=custom_font_color)
        self.label_additional_info.grid(row=11+1, column=0, pady=5, padx=10, sticky="w")

        # Text area for Additional Information
        self.additional_info_var = tk.StringVar()
        self.entry_additional_info = tk.Entry(self.master, textvariable=self.additional_info_var, font=custom_font)
        self.entry_additional_info.grid(row=11+1, column=1, pady=5, padx=10, sticky="w")

        # Label for Address
        self.label_address = tk.Label(self.master, text="Address:", bg="white", font=custom_font, fg=custom_font_color)
        self.label_address.grid(row=12+1, column=0, pady=5, padx=10, sticky="w")

        # Entry for Address
        self.address_var = StringVar()
        self.entry_address = tk.Entry(self.master, textvariable=self.address_var, font=custom_font)
        self.entry_address.grid(row=12+1, column=1, pady=5, padx=10, sticky="w")

        # Label for Email
        self.label_email = tk.Label(self.master, text="Email:", bg="white", font=custom_font, fg=custom_font_color)
        self.label_email.grid(row=13+1, column=0, pady=5, padx=10, sticky="w")

        # Entry for Email
        self.email_var = StringVar()
        self.entry_email = tk.Entry(self.master, textvariable=self.email_var, font=custom_font)
        self.entry_email.grid(row=13+1, column=1, pady=5, padx=10, sticky="w")

        # Checkbutton for Agreement
        self.agreement_var = tk.IntVar()
        self.checkbutton_agreement = tk.Checkbutton(self.master, text="I agree to the terms and conditions",
                                                    variable=self.agreement_var, bg="white", font=custom_font,
                                                    fg=custom_font_color)
        self.checkbutton_agreement.grid(row=14+1, column=0, columnspan=2, pady=5, padx=10, sticky="w")

        # ... (you can continue adding more input fields as needed)

        # Submit Button
        self.submit_button = tk.Button(self.master, text="Submit", command=self.submit_form, bg="white", fg="red",
                                       font=custom_font, width=7, height=1)
        self.submit_button.grid(row=17+1, column=0, columnspan=2, pady=10)


    def submit_form(self):
    # Validate the input fields
        if not self.validate_input():
            messagebox.showerror("Error", "Invalid input. Please check the fields.")
            return

        # Get data from the input fields
        membership_id = self.membership_id_var.get()
        name = self.name_var.get()
        age = self.age_var.get()
        blood_group_input = self.blood_type_var.get()
        blood_type = convert_blood_group(blood_group_input)
        contact_number = self.contact_number_var.get()
        amount_required = self.amount_required_var.get()
        status_input = self.status_var.get().lower()
        status = "0" if status_input == "pending" else "1"
        date_of_request = self.date_of_request_var.get()
        additional_info = self.additional_info_var.get()
        address = self.address_var.get()
        email = self.email_var.get()


        # Prepare the data for insertion into the database
        user_data = (
            self.membership_id_var.get(), self.name_var.get(), int(self.age_var.get()),
            blood_type, self.contact_number_var.get(),
            int(self.amount_required_var.get()), status, self.date_of_request_var.get()
        )

        # Insert data into the database
        self.insert_data_into_db(user_data)

        message = (
            f"Membership ID: {membership_id}\n"
            f"Name: {name}\n"
            f"Age: {age}\n"
            f"Blood Type: {blood_type}\n"
            f"Contact Number: {contact_number}\n"
            f"Amount Required: {amount_required}\n"
            f"Status: {status}\n"
            f"Date of Request: {date_of_request}\n"
            f"Additional Information: {additional_info}\n"
            f"Address: {address}\n"
            f"Email: {email}"
        )

        messagebox.showinfo("Form Submission", message)


    def insert_data_into_db(self, data):
        conn = sqlite3.connect('Blood_Bank.db')
        cursor = conn.cursor()

        # Assuming you have a table named 'RECIPIENT' in your database
        cursor.execute('''
            INSERT INTO RECIPIENT (recipientid, name, age, blood_type, contact_number,
            amount_required, status, date_of_request)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)

        conn.commit()
        conn.close()

    # The rest of your Tkinter code...


    def validate_input(self):
        # Validate the length of Membership ID
        if len(self.membership_id_var.get()) != 6:
            return False

        # Validate that Age is an integer
        try:
            int(self.age_var.get())
        except ValueError:
            return False

        # Validate that Contact Number is 11 characters long
        if len(self.contact_number_var.get()) != 11:
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
    app = RecipientPromptApp(root)
    root.mainloop()


