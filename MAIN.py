import tkinter as tk
from donorchk import DonorPromptApp
from Recipient_final import RecipientPromptApp
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
from inventory import BloodDonationApp

class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Recipient Prompt")
        self.master.geometry("400x400")  # Adjusted the window size
        self.master.configure(bg="white")

        # Load and blur the image
        original_image = Image.open("mainpic1.png")

        # Resize the image to fit the window
        resized_image = original_image.resize((400, 400), Image.LANCZOS)

        # Apply GaussianBlur with a specific radius to control blurriness
        blurred_image = resized_image.filter(ImageFilter.GaussianBlur(radius=4))  # Adjust the radius as needed

        # Convert the image to a Tkinter-compatible format
        self.bg_image = ImageTk.PhotoImage(blurred_image)

        # Create a Canvas widget to display the image
        self.canvas = tk.Canvas(self.master, width=400, height=400, highlightthickness=0)
        self.canvas.grid(row=0, column=0, rowspan=19, columnspan=2, sticky="w")

        # Display the resized image on the Canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)

        # Heading label
        text_message = "Welcome! Choose one of the following options:"
        self.canvas.create_text(200, 20, text=text_message, font=("Georgia", 14), fill="white")

        # Buttons
        self.donate_button = tk.Button(self.master, text="Donate Blood", command=self.open_donor_page, bg="white", fg="red",
                                       font=("Georgia", 12), width=15, height=2)
        self.donate_button.grid(row=6, column=1, pady=10, sticky="w")

        self.request_button = tk.Button(self.master, text="Request Blood", command=self.open_recipient_page, bg="white", fg="red",
                                         font=("Georgia", 12), width=15, height=2)
        self.request_button.grid(row=7, column=1, pady=10, sticky="w")

        self.show_inventory_button = tk.Button(self.master, text="Show Inventory", command=self.open_storage_page, bg="white", fg="red",
                                          font=("Georgia", 12), width=15, height=2)
        self.show_inventory_button.grid(row=8, column=1, pady=10, sticky="w")

    def open_donor_page(self):
        donor_root = tk.Toplevel(self.master)
        donor_app = DonorPromptApp(donor_root)

    def open_recipient_page(self):
        recipient_root = tk.Toplevel(self.master)
        recipient_app = RecipientPromptApp(recipient_root)

    def open_storage_page(self):
        storage_root = tk.Toplevel(self.master)
        storage_app = BloodDonationApp(storage_root,'Blood_bank.db')

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
