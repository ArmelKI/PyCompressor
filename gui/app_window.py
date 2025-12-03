import customtkinter as ctk
import os
import threading
from tkinter import filedialog

# Logic Imports
from logic.file_manager import get_unique_output_path, get_size_mb, format_size, calculate_savings
from logic.compressor_img import compress_image
from logic.compressor_pdf import compress_pdf

class PyCompressorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.selected_files = [] 
        
        # --- WINDOW SETUP ---
        self.title("PyCompressor - English Edition")
        self.geometry("800x600")
        ctk.set_appearance_mode("System") 
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ================= ZONE 1: IMPORT =================
        self.frame_import = ctk.CTkFrame(self)
        self.frame_import.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))
        
        self.label_import = ctk.CTkLabel(self.frame_import, text="Files to import", font=("Arial", 16,"bold"))
        self.label_import.pack(pady=10)

        self.scroll_files = ctk.CTkScrollableFrame(self.frame_import, label_text="List empty")
        self.scroll_files.pack(fill="both", expand=True, padx=10, pady=10)

        self.button_add_file = ctk.CTkButton(self.frame_import, text="+ Add Files", width=200, command=self.open_file_dialog)
        self.button_add_file.pack(pady=10)

        # ================= ZONE 2: SETTINGS =================
        self.frame_settings = ctk.CTkFrame(self)
        self.frame_settings.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

        # Quality Label (Updates dynamically now)
        self.label_quality = ctk.CTkLabel(self.frame_settings, text="Quality Level: 80%")
        self.label_quality.grid(row=0, column=0, padx=20, pady=20)
        
        # Slider with 'command' to update the label
        self.slider_quality = ctk.CTkSlider(
            self.frame_settings, 
            from_=10, to=100, 
            number_of_steps=90, 
            width=300,
            command=self.update_quality_label # <--- FIX 1: Updates label on drag
        )
        self.slider_quality.set(80)
        self.slider_quality.grid(row=0, column=1, padx=10, pady=20, sticky="ew")
        
        self.frame_settings.grid_columnconfigure(1, weight=1)

        self.check_resize = ctk.CTkCheckBox(self.frame_settings, text="Resize to HD (1920px)")
        self.check_resize.grid(row=0, column=2, padx=20, pady=20)

        # ================= ZONE 3: ACTIONS =================
        self.frame_actions = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_actions.grid(row=2, column=0, sticky="ew", padx=20, pady=20)

        self.progress_bar = ctk.CTkProgressBar(self.frame_actions)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(0,10))

        self.button_compress = ctk.CTkButton(
            self.frame_actions, 
            text="START COMPRESSION", 
            height=50, 
            font=("Arial", 16, "bold"),
            command=self.start_compression_thread
        )
        self.button_compress.pack(fill="x")

        self.label_status = ctk.CTkLabel(self.frame_actions, text="Ready", text_color="gray")
        self.label_status.pack(pady=5)


    # ================= FUNCTIONS =================

    def update_quality_label(self, value):
        """Updates the label text when the slider moves."""
        val_int = int(value)
        self.label_quality.configure(text=f"Quality Level: {val_int}%")

    def open_file_dialog(self):
        print("DEBUG: Opening File Dialog...") 
        
        # FIX 2: Simplified filters for Linux compatibility
        # Using "*.*" ensures the OS doesn't hide files because of casing (jpg vs JPG)
        filepaths = filedialog.askopenfilenames(
            title="Select Files",
            filetypes=[("All Files", "*.*")] 
        )

        print(f"DEBUG: Dialog returned: {filepaths}") 

        if filepaths:
            # Check if list is valid
            if len(filepaths) > 0:
                for path in filepaths:
                    if path not in self.selected_files: 
                        self.selected_files.append(path)
                self.update_file_list_ui()
            else:
                print("DEBUG: Filepaths is empty list")
        else:
            print("DEBUG: User cancelled or nothing selected")
    
    def update_file_list_ui(self):
        # 1. Clean UI
        for widget in self.scroll_files.winfo_children():
            widget.destroy()

        # 2. Add files to UI
        for path in self.selected_files:
            filename = os.path.basename(path) 
            extension = os.path.splitext(filename)[1].lower()
            
            row_frame = ctk.CTkFrame(self.scroll_files, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            
            # Icon logic
            icon = "❓"
            if extension in [".jpg", ".jpeg", ".png"]: icon = "🖼️"
            if extension == ".pdf": icon = "📄"

            label = ctk.CTkLabel(row_frame, text=f"{icon}  {filename}", anchor="w")
            label.pack(side="left", padx=5)

        # 3. Update status
        count = len(self.selected_files)
        print(f"DEBUG: Total files in memory: {count}") 
        
        self.label_status.configure(text=f"{count} file(s) ready")
        
        if count > 0:
            self.scroll_files.configure(label_text=f"{count} Files Selected")
        else:
            self.scroll_files.configure(label_text="List empty")

    def start_compression_thread(self):
        print("DEBUG: Start button clicked") 
        if not self.selected_files:
            self.label_status.configure(text="No files selected!", text_color="#ff5555")
            print("DEBUG: ERROR - No files in list")
            return

        self.button_compress.configure(state="disabled", text="Processing...")
        self.progress_bar.set(0)
        
        threading.Thread(target=self.run_compression_process, daemon=True).start()

    def run_compression_process(self):
        total_files = len(self.selected_files)
        success_count = 0
        total_size_before = 0
        total_size_after = 0
        
        # Get settings from UI
        quality_val = int(self.slider_quality.get())
        do_resize = bool(self.check_resize.get())
        
        print(f"DEBUG: Starting compression with Quality={quality_val}, Resize={do_resize}")

        for index, file_path in enumerate(self.selected_files):
            try:
                # Measure size BEFORE
                size_before = get_size_mb(file_path)
                total_size_before += size_before

                # Update Status
                filename = os.path.basename(file_path)
                self.label_status.configure(text=f"Processing: {filename}...")
                
                # Output Path
                output_path = get_unique_output_path(file_path, suffix="_min")
                extension = os.path.splitext(file_path)[1].lower()
                result = False
                
                # Processing
                if extension == ".pdf":
                    result = compress_pdf(file_path, output_path)
                elif extension in [".jpg", ".jpeg", ".png"]:
                    # max_w is int or None
                    max_w = 1920 if do_resize else None
                    result = compress_image(file_path, output_path, quality=quality_val, max_width=max_w)
                
                if result:
                    success_count += 1
                    size_after = get_size_mb(output_path)
                    total_size_after += size_after
                    print(f"DEBUG: Success on {filename}")
                else:
                    print(f"DEBUG: Failed on {filename}")

                # Progress
                progress = (index + 1) / total_files
                self.progress_bar.set(progress)
            except Exception as e:
                print(f"DEBUG: CRITICAL ERROR on {file_path}: {e}")

        # FINISHED
        saved_mb = total_size_before - total_size_after
        saved_percent = calculate_savings(total_size_before, total_size_after)
        
        final_message = (
            f"Done! {success_count}/{total_files} files.\n"
            f"Saved: {format_size(saved_mb)} (-{saved_percent}%)"
        )
        
        self.label_status.configure(text=final_message, text_color="#55ff55") 
        self.button_compress.configure(state="normal", text="START COMPRESSION")
        
        # Clear list
        self.selected_files = [] 
        self.update_file_list_ui()