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

        #========== ZONE 2:  COMPRESSOR SETTINGS ==========#

        self.frame_settings = ctk.CTkFrame(self)
        self.frame_settings.grid(row=1, column=0, sticky="ew", padx=20, pady=10)#Stick to east and west

        #Slider for compression level
        self.label_quality = ctk.CTkLabel(self.frame_settings, text="Quality Level:80%")# Label for the slider
        self.label_quality.grid(row=0, column=0, padx=20, pady=20)# Padding around the label
        self.slider_quality = ctk.CTkSlider(self.frame_settings, from_=0, to=100, number_of_steps=90, width=300)# Slider widget
        self.slider_quality.set(80)# Default value at 80%
        self.slider_quality.grid(row=0, column=1, padx=10, pady=20, sticky="ew")# Padding and stick to east and west
        self.frame_settings.grid_columnconfigure(1, weight=1)# Make the slider column expandable

        #Checkbox for resizing images
        self.check_resize = ctk.CTkCheckBox(self.frame_settings, text="Resize Images to 1920px")# Checkbox widget
        self.check_resize.grid(row=0, column=2, padx=20, pady=20)# Padding around the checkbox

        #========== END ZONE 2 ==========#

        #========== ZONE 3:  ACTION BUTTONS ==========#

        self.frame_actions = ctk.CTkFrame(self, fg_color="transparent")# Transparent frame to blend with background
        self.frame_actions.grid(row=2, column=0, sticky="ew", padx=20, pady=10)#Stick to east and west

        #Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.frame_actions)
        self.progress_bar.set(0)# Initialize at 0%
        self.progress_bar.pack(fill="x", pady=(0,10))# Fill horizontally with bottom padding

        #Compress button
        self.button_compress = ctk.CTkButton(self.frame_actions, text="START COMPRESSION", height=50, font=("Arial", 16, "bold"), fg_color="#2A2DC2FF", hover_color="#2A2DC2FF")# Blue button with hover effect
        self.button_compress.pack(fill="x")# Fill horizontally

        #Status label
        self.label_status = ctk.CTkLabel(self.frame_actions, text="Ready")# Status label
        self.label_status.pack(pady=10)# Add some vertical padding

        #========== END ZONE 3 ==========#

