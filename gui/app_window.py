import customtkinter as ctk

class PyCompressorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set window title
        self.title("PyCompressor - Online File Compressor")
        self.geometry("800x600")#length x height
        #theme settings
        ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        self.grid_columnconfigure(0, weight=1)# Make the first column expandable
        self.grid_rowconfigure(0, weight=1)# Make the first row take all extra space

        #========== ZONE 1:  IMPORTATION ==========#
        
        self.frame_import = ctk.CTkFrame(self)
        self.frame_import.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        #Title of the zone
        self.label_import = ctk.CTkLabel(master=self.frame_import, text="Files to import", font=("Arial", 16,"bold"))# Set font size to 16 and bold for the title
        self.label_import.pack(pady=10)# Add some vertical padding

        #File list area (scrollable)
        self.scroll_files = ctk.CTkScrollableFrame(self.frame_import, label_text="List empty")# Create a scrollable frame with a label
        self.scroll_files.pack(fill="both", expand=True, padx=10, pady=10)# Fill both directions and expand

        #Add file button
        self.button_add_file = ctk.CTkButton(self.frame_import, text="+Add File", width=200)
        self.button_add_file.pack(pady=10)# Add some vertical padding

        #========== END ZONE 1 ==========#
