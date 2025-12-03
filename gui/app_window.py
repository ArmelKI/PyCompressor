import customtkinter as ctk
import os 
from tkinter import filedialog 

class PyCompressorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.selected_files = [] 
        
        # Window setup
        self.title("PyCompressor - Online File Compressor")
        self.geometry("800x600")
        ctk.set_appearance_mode("System") 
        ctk.set_default_color_theme("blue")

        # Grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ============================================================
        # ZONE 1: IMPORTATION
        # ============================================================
        self.frame_import = ctk.CTkFrame(self)
        self.frame_import.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))
        
        self.label_import = ctk.CTkLabel(master=self.frame_import, text="Files to import", font=("Arial", 16,"bold"))
        self.label_import.pack(pady=10)

        # File list area
        self.scroll_files = ctk.CTkScrollableFrame(self.frame_import, label_text="List empty")
        self.scroll_files.pack(fill="both", expand=True, padx=10, pady=10)

        self.button_add_file = ctk.CTkButton(
            self.frame_import, 
            text="+ Add Files", 
            width=200, 
            command=self.open_file_dialog
        )
        self.button_add_file.pack(pady=10)


        # ============================================================
        # ZONE 2: SETTINGS
        # ============================================================
        self.frame_settings = ctk.CTkFrame(self)
        self.frame_settings.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

        # Quality Slider
        self.label_quality = ctk.CTkLabel(self.frame_settings, text="Quality Level: 80%")
        self.label_quality.grid(row=0, column=0, padx=20, pady=20)
        
        self.slider_quality = ctk.CTkSlider(self.frame_settings, from_=10, to=100, number_of_steps=90, width=300)
        self.slider_quality.set(80)
        self.slider_quality.grid(row=0, column=1, padx=10, pady=20, sticky="ew")
        
        self.frame_settings.grid_columnconfigure(1, weight=1)

        # Checkbox
        self.check_resize = ctk.CTkCheckBox(self.frame_settings, text="Resize to HD (1920px)")
        self.check_resize.grid(row=0, column=2, padx=20, pady=20)


        # ============================================================
        # ZONE 3: ACTIONS
        # ============================================================
        self.frame_actions = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_actions.grid(row=2, column=0, sticky="ew", padx=20, pady=20)

        self.progress_bar = ctk.CTkProgressBar(self.frame_actions)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(0,10))

        self.button_compress = ctk.CTkButton(self.frame_actions, text="START COMPRESSION", height=50, font=("Arial", 16, "bold"))
        self.button_compress.pack(fill="x")

        self.label_status = ctk.CTkLabel(self.frame_actions, text="Ready", text_color="gray")
        self.label_status.pack(pady=5)


    def open_file_dialog(self):
        """Open file dialog to select files and update the UI."""
        filetypes = [
            ("All supported files", "*.*"), 
            ("Images", "*.jpg"),
            ("Images", "*.jpeg"), 
            ("Images", "*.png"), 
            ("PDF Files", "*.pdf")
        ]
        
        filepaths = filedialog.askopenfilenames(title="Select Files", filetypes=filetypes)

        if filepaths:
            for path in filepaths:
                if path not in self.selected_files: 
                    self.selected_files.append(path)
            
            self.update_file_list_ui()
    
    def update_file_list_ui(self):
        # 1. Clear the list
        for widget in self.scroll_files.winfo_children():
            widget.destroy()

        # 2. Add files
        for path in self.selected_files:
            filename = os.path.basename(path) 
            extension = os.path.splitext(filename)[1].lower()
            
            # Create a specific frame for this row (transparent)
            row_frame = ctk.CTkFrame(self.scroll_files, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            
            # Determine Icon
            if extension in [".jpg", ".jpeg", ".png"]:
                icon = "🖼️"
            elif extension == ".pdf":
                icon = "📄"
            else:
                icon = "❓"

            # Create the label INSIDE the row_frame
            label = ctk.CTkLabel(row_frame, text=f"{icon}  {filename}", anchor="w")
            label.pack(side="left", padx=5)

        # 3. Update status text
        count = len(self.selected_files)
        self.label_status.configure(text=f"{count} file(s) selected")
        
        if count > 0:
            self.scroll_files.configure(label_text=f"{count} Files")
        else:
            self.scroll_files.configure(label_text="List empty")

    