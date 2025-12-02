import customtkinter as ctk

class PyCompressorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set window title
        self.title("PyCompressor")
        self.geometry("700x500")#length x height
        #theme settings
        ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

        # Verification label
        self.label = ctk.CTkLabel(master=self, text="PyCompressor is running!", font=("Arial", 20))# Set font size to 20
        self.label.pack(pady=20)# Add some vertical padding
