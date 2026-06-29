import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import random
import os

ctk.set_appearance_mode("dark")

class InfiniteZoo(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.state("zoomed") 
        self.title("Infinite Pokémon Zoo")

        self.inventory = {} 
        
        # --- 1. SETUP BACKGROUND ---
        # Make sure field.png is in the same folder
        bg_image = Image.open("field.png").resize((1920, 1080))
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # --- 2. DYNAMIC AUTO-LOADER ---
        # This will automatically find all your new .png files!
        self.pet_images = {}
        for filename in os.listdir('.'):
            if filename.endswith(".png") and filename != "field.png":
                pet_name = filename.replace(".png", "").capitalize()
                # Loading and resizing images for the game
                img = ImageTk.PhotoImage(Image.open(filename).resize((80, 80)))
                self.pet_images[pet_name] = img
        
        # --- 3. UI ---
        self.status_label = ctk.CTkLabel(self, text="Catch your favorite Pokémon!", font=("Roboto", 32, "bold"), text_color="white")
        self.status_label.place(relx=0.5, rely=0.05, anchor="center")

        self.bag_btn = ctk.CTkButton(self, text="🎒 Open Backpack", command=self.open_backpack)
        self.bag_btn.place(relx=0.5, rely=0.9, anchor="center")

        # --- 4. START GAME (10 PETS ON SCREEN) ---
        for _ in range(10):
            self.spawn_pet()

    def spawn_pet(self):
        pet_name = random.choice(list(self.pet_images.keys()))
        x = random.randint(100, 1400)
        y = random.randint(100, 700)
        
        img = self.pet_images[pet_name]
        pet_id = self.canvas.create_image(x, y, image=img)
        
        # Bind the click to catch
        self.canvas.tag_bind(pet_id, "<Button-1>", lambda e, n=pet_name, i=pet_id: self.catch_pet(n, i))

    def catch_pet(self, name, pet_id):
        self.inventory[name] = self.inventory.get(name, 0) + 1
        self.canvas.delete(pet_id)
        self.status_label.configure(text=f"Caught a {name}! 🐾")
        self.spawn_pet()

    def open_backpack(self):
        bag_window = ctk.CTkToplevel(self)
        bag_window.title("Your Collection")
        bag_window.geometry("300x400")
        
        ctk.CTkLabel(bag_window, text="YOUR COLLECTION", font=("Roboto", 20, "bold")).pack(pady=20)
        for pet, count in self.inventory.items():
            ctk.CTkLabel(bag_window, text=f"• {pet}: {count}", font=("Roboto", 16)).pack()

if __name__ == "__main__":
    app = InfiniteZoo()
    app.mainloop()