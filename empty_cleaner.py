import os
import sys
import time
import winshell
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from datetime import datetime
from send2trash import send2trash

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class EmptyCleaner:
    def __init__(self, root):
        self.root = root
        self.root.title("Empty Cleaner")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)
        
        # Set application icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clean.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        
        # Configure the grid layout
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(root, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        # App logo/title
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Empty Cleaner",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
          # Directory selection
        self.dir_label = ctk.CTkLabel(self.sidebar_frame, text="Target Directory:")
        self.dir_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.dir_var = ctk.StringVar()
        self.dir_entry = ctk.CTkEntry(self.sidebar_frame, textvariable=self.dir_var, width=160)
        self.dir_entry.grid(row=2, column=0, padx=20, pady=(5, 0), sticky="ew")
        
        self.browse_button = ctk.CTkButton(
            self.sidebar_frame, 
            text="Browse...",
            command=self.browse_directory,
            corner_radius=8
        )
        self.browse_button.grid(row=3, column=0, padx=20, pady=(5, 0), sticky="ew")
          # Action buttons
        self.button_frame = ctk.CTkFrame(self.sidebar_frame)
        self.button_frame.grid(row=5, column=0, padx=20, pady=20, sticky="ew")
        
        self.scan_button = ctk.CTkButton(
            self.button_frame,
            text="Scan Directory",
            command=self.scan_directory,
            fg_color="#3a7ebf",
            hover_color="#2a6da8",
            corner_radius=8
        )
        self.scan_button.pack(fill="x", pady=(0, 5))
        
        self.delete_button = ctk.CTkButton(
            self.button_frame,
            text="Move to Recycle Bin",
            command=self.delete_empty,
            fg_color="#2d8659",
            hover_color="#1d7549",
            corner_radius=8
        )
        self.delete_button.pack(fill="x", pady=5)
        
        self.empty_rb_button = ctk.CTkButton(
            self.button_frame,
            text="Empty Recycle Bin",
            command=self.empty_recycle_bin,
            fg_color="#963a3a",
            hover_color="#862a2a",
            corner_radius=8
        )
        self.empty_rb_button.pack(fill="x", pady=(5, 0))
          # About button
        self.about_button = ctk.CTkButton(
            self.sidebar_frame,
            text="About",
            command=self.show_about,
            fg_color="#555555",
            hover_color="#444444",
            corner_radius=8
        )
        self.about_button.grid(row=6, column=0, padx=20, pady=(30, 0), sticky="ew")
        
        # Appearance mode option
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(20, 0))
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.sidebar_frame, 
            values=["Dark", "Light", "System"],
            command=self.change_appearance_mode
        )
        self.appearance_mode_menu.grid(row=8, column=0, padx=20, pady=(5, 20))
        self.appearance_mode_menu.set("Dark")
        
        # Create main frame with color matching the title bar
        self.main_frame = ctk.CTkFrame(root, fg_color=("#333333", "#1e1e1e"))
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Header in main frame
        self.header_label = ctk.CTkLabel(
            self.main_frame, 
            text="Scan results:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.header_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
        
        # Create the results frame with tabview
        self.results_frame = ctk.CTkTabview(self.main_frame)
        self.results_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Add tabs for files and folders
        self.tab_files = self.results_frame.add("Empty Files")
        self.tab_folders = self.results_frame.add("Empty Folders")
        
        # Configure tabs
        self.tab_files.grid_columnconfigure(0, weight=1)
        self.tab_files.grid_rowconfigure(0, weight=1)
        self.tab_folders.grid_columnconfigure(0, weight=1)
        self.tab_folders.grid_rowconfigure(0, weight=1)
        
        # Create scrollable frames for each tab
        self.files_scrollable_frame = ctk.CTkScrollableFrame(self.tab_files)
        self.files_scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.files_scrollable_frame.grid_columnconfigure(0, weight=1)
        
        self.folders_scrollable_frame = ctk.CTkScrollableFrame(self.tab_folders)
        self.folders_scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.folders_scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # Status and progress
        self.status_frame = ctk.CTkFrame(self.main_frame)
        self.status_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.status_frame.grid_columnconfigure(0, weight=1)
        
        self.status_var = ctk.StringVar(value="Ready")
        self.status_label = ctk.CTkLabel(
            self.status_frame, 
            textvariable=self.status_var,
            anchor="w"
        )
        self.status_label.grid(row=0, column=0, sticky="w", padx=5, pady=(5, 0))
        
        self.progress = ctk.CTkProgressBar(self.status_frame)
        self.progress.grid(row=1, column=0, sticky="ew", padx=5, pady=(5, 5))
        self.progress.set(0)
        
        # Empty files and folders lists
        self.empty_files = []
        self.empty_folders = []
        self.file_widgets = []
        self.folder_widgets = []
    
    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode.lower())
    
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_var.set(directory)
    
    def scan_directory(self):
        directory = self.dir_var.get()
        if not directory:
            messagebox.showwarning("Warning", "Please select a directory first.")
            return
        
        if not os.path.exists(directory):
            messagebox.showerror("Error", "The selected directory does not exist.")
            return
        
        # Clear previous results
        self.clear_results()
        
        # Start scanning in a separate thread
        threading.Thread(target=self._scan_thread, args=(directory,), daemon=True).start()
    
    def clear_results(self):
        # Clear file results
        for widget in self.file_widgets:
            widget.destroy()
        self.file_widgets = []
        
        # Clear folder results
        for widget in self.folder_widgets:
            widget.destroy()
        self.folder_widgets = []
        
        # Reset lists
        self.empty_files = []
        self.empty_folders = []
    
    def _scan_thread(self, directory):
        self.status_var.set("Scanning...")
        self.progress.set(0)
        self.root.update_idletasks()
        
        try:
            # Get all files and folders
            all_items = []
            for root, dirs, files in os.walk(directory):
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    all_items.append(dir_path)
                
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    all_items.append(file_path)
            
            total_items = len(all_items)
            processed = 0
            
            # Check each item
            for item_path in all_items:
                if os.path.isfile(item_path):
                    if os.path.getsize(item_path) == 0:
                        self.empty_files.append(item_path)
                        # Add to UI in the main thread
                        self.root.after(0, lambda p=item_path: self._add_file_to_ui(p))
                else:  # It's a directory
                    # Check if directory is empty (no files or subdirectories)
                    if not os.listdir(item_path):
                        self.empty_folders.append(item_path)
                        # Add to UI in the main thread
                        self.root.after(0, lambda p=item_path: self._add_folder_to_ui(p))
                
                # Update progress
                processed += 1
                progress_value = processed / total_items
                self.root.after(0, lambda v=progress_value: self.progress.set(v))
                
                # Update status every 100 items to avoid GUI freezing
                if processed % 100 == 0 or processed == total_items:
                    self.root.after(0, lambda p=processed, t=total_items: 
                                   self.status_var.set(f"Scanned {p} of {t} items..."))
            
            # Final update
            total_empty = len(self.empty_files) + len(self.empty_folders)
            self.root.after(0, lambda: self.status_var.set(
                f"Scan complete. Found {total_empty} empty items ({len(self.empty_files)} files, {len(self.empty_folders)} folders)."))
            
            if total_empty == 0:
                self.root.after(0, lambda: messagebox.showinfo("Scan Complete", "No empty files or folders were found."))
        
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error during scan: {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred during scanning:\n{str(e)}"))
        
        finally:
            self.root.after(0, lambda: self.progress.set(1))
    
    def _add_file_to_ui(self, file_path):
        try:
            # Create frame for this item
            frame = ctk.CTkFrame(self.files_scrollable_frame)
            frame.pack(fill="x", padx=5, pady=2)
            
            # Get file details
            stats = os.stat(file_path)
            mod_time = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            # Add file info
            label = ctk.CTkLabel(
                frame, 
                text=file_path,
                anchor="w",
                wraplength=500,
                justify="left"
            )
            label.pack(fill="x", padx=5, pady=2, anchor="w")
            
            # Add details in smaller font
            details_label = ctk.CTkLabel(
                frame,
                text=f"Modified: {mod_time}",
                font=ctk.CTkFont(size=10),
                anchor="w"
            )
            details_label.pack(fill="x", padx=5, pady=(0, 2), anchor="w")
            
            # Store the widget reference
            self.file_widgets.append(frame)
            
            # Switch to files tab
            self.results_frame.set("Empty Files")
            
        except Exception:
            # Handle case where item might have been deleted/moved during scan
            pass
    
    def _add_folder_to_ui(self, folder_path):
        try:
            # Create frame for this item
            frame = ctk.CTkFrame(self.folders_scrollable_frame)
            frame.pack(fill="x", padx=5, pady=2)
            
            # Get folder details
            stats = os.stat(folder_path)
            mod_time = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            # Add folder info
            label = ctk.CTkLabel(
                frame, 
                text=folder_path,
                anchor="w",
                wraplength=500,
                justify="left"
            )
            label.pack(fill="x", padx=5, pady=2, anchor="w")
            
            # Add details in smaller font
            details_label = ctk.CTkLabel(
                frame,
                text=f"Modified: {mod_time}",
                font=ctk.CTkFont(size=10),
                anchor="w"
            )
            details_label.pack(fill="x", padx=5, pady=(0, 2), anchor="w")
            
            # Store the widget reference
            self.folder_widgets.append(frame)
            
            # Switch to folders tab if this is the first folder
            if len(self.folder_widgets) == 1 and len(self.file_widgets) == 0:
                self.results_frame.set("Empty Folders")
            
        except Exception:
            # Handle case where item might have been deleted/moved during scan
            pass
    
    def delete_empty(self):
        if not self.empty_files and not self.empty_folders:
            messagebox.showwarning("Warning", "No empty files or folders to delete. Run a scan first.")
            return
        
        total_items = len(self.empty_files) + len(self.empty_folders)
        result = messagebox.askyesno(
            "Confirm Action", 
            f"Are you sure you want to move {total_items} empty items to the recycle bin?\n\n"
            f"- {len(self.empty_files)} empty files\n"
            f"- {len(self.empty_folders)} empty folders"
        )
        
        if result:
            # Start deletion in a separate thread
            threading.Thread(target=self._delete_thread, daemon=True).start()
    
    def _delete_thread(self):
        self.status_var.set("Moving items to recycle bin...")
        self.progress.set(0)
        
        total_items = len(self.empty_files) + len(self.empty_folders)
        processed = 0
        failed = 0
        
        # Delete empty files first
        for file_path in self.empty_files[:]:
            try:
                if os.path.exists(file_path):
                    # Normalize path - replace forward slashes with backslashes for Windows
                    normalized_path = os.path.abspath(os.path.normpath(file_path))
                    # Use send2trash to move to recycle bin
                    send2trash(normalized_path)
                    self.empty_files.remove(file_path)
                    
                    # Remove from UI in main thread
                    if self.file_widgets:
                        widget = self.file_widgets.pop(0)
                        self.root.after(0, lambda w=widget: w.destroy())
            except Exception as e:
                print(f"Failed to delete file {file_path}: {str(e)}")
                failed += 1
            
            processed += 1
            progress_value = processed / total_items
            self.root.after(0, lambda v=progress_value: self.progress.set(v))
            
            if processed % 5 == 0:
                self.root.after(0, lambda p=processed, t=total_items: 
                               self.status_var.set(f"Processed {p} of {t} items..."))
        
        # Delete empty folders (in reverse order to handle nested folders)
        for folder_path in sorted(self.empty_folders, reverse=True):
            try:
                if os.path.exists(folder_path) and not os.listdir(folder_path):
                    # Normalize path - replace forward slashes with backslashes for Windows
                    normalized_path = os.path.abspath(os.path.normpath(folder_path))
                    # Use send2trash to move to recycle bin
                    send2trash(normalized_path)
                    self.empty_folders.remove(folder_path)
                    
                    # Remove from UI in main thread
                    if self.folder_widgets:
                        widget = self.folder_widgets.pop(0)
                        self.root.after(0, lambda w=widget: w.destroy())
            except Exception as e:
                print(f"Failed to delete folder {folder_path}: {str(e)}")
                failed += 1
            
            processed += 1
            progress_value = processed / total_items
            self.root.after(0, lambda v=progress_value: self.progress.set(v))
            
            if processed % 5 == 0:
                self.root.after(0, lambda p=processed, t=total_items: 
                               self.status_var.set(f"Processed {p} of {t} items..."))
        
        # Final update
        if failed > 0:
            self.root.after(0, lambda: self.status_var.set(
                f"Complete. {processed - failed} items moved to recycle bin, {failed} items failed."))
            self.root.after(0, lambda f=failed, s=processed-failed: messagebox.showwarning(
                "Operation Complete", 
                f"{s} empty items were moved to the recycle bin.\n{f} items could not be processed."
            ))
        else:
            self.root.after(0, lambda: self.status_var.set(
                f"Complete. {processed} items moved to recycle bin."))
            self.root.after(0, lambda p=processed: messagebox.showinfo(
                "Operation Complete", 
                f"{p} empty items were moved to the recycle bin."
            ))
        
        self.root.after(0, lambda: self.progress.set(1))
    
    def empty_recycle_bin(self):
        result = messagebox.askyesno(
            "Confirm Action", 
            "Are you sure you want to permanently empty the recycle bin?\n\nThis action cannot be undone."
        )
        
        if result:
            try:
                self.status_var.set("Emptying recycle bin...")
                winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
                self.status_var.set("Recycle bin emptied successfully.")
                messagebox.showinfo("Success", "Recycle bin emptied successfully.")
            except Exception as e:
                self.status_var.set(f"Error emptying recycle bin: {str(e)}")
                messagebox.showerror("Error", f"Could not empty recycle bin:\n{str(e)}")
    
    def show_about(self):
        # Clear current content
        self.clear_results()
        
        # Update header
        self.header_label.configure(text="About Empty Cleaner")
        
        # Hide the tabview
        self.results_frame.grid_remove()
        
        # Create about frame
        self.about_frame = ctk.CTkFrame(self.main_frame)
        self.about_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.about_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            self.about_frame, 
            text="Empty Cleaner",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 5))
        
        # Version
        version_label = ctk.CTkLabel(
            self.about_frame, 
            text="Version 1.0",
            font=ctk.CTkFont(size=14)
        )
        version_label.pack(pady=(0, 20))
          # Description
        desc_text = (
            "Empty Cleaner is a powerful utility designed to efficiently identify and manage empty files and folders "
            "within your file system. It safely sends items to the recycle bin rather than permanently deleting them, "
            "allowing you to clean up unnecessary empty items while maintaining the ability to recover them if needed."
        )
        desc_label = ctk.CTkLabel(
            self.about_frame, 
            text=desc_text,
            font=ctk.CTkFont(size=12),
            wraplength=460,
            justify="center"
        )
        desc_label.pack(pady=10)
        
        # Creator info
        creator_label = ctk.CTkLabel(
            self.about_frame, 
            text="Created by: Christlieb Dela",
            font=ctk.CTkFont(size=12),
            justify="center"
        )
        creator_label.pack(pady=(20, 5))
        
        # GitHub link
        github_text = "GitHub: https://github.com/christliebdela"
        github_label = ctk.CTkLabel(
            self.about_frame, 
            text=github_text,
            font=ctk.CTkFont(size=12),
            justify="center"
        )
        github_label.pack(pady=5)
          # Open source notice
        opensource_text = (
            "This is an open source tool. Contributions are welcome!\n"
            "Repository: https://github.com/christliebdela/Empty-Cleaner"
        )
        opensource_label = ctk.CTkLabel(
            self.about_frame, 
            text=opensource_text,
            font=ctk.CTkFont(size=12),
            wraplength=460,
            justify="center"
        )
        opensource_label.pack(pady=20)
        
        # Back button to return to scan view
        back_button = ctk.CTkButton(            self.about_frame,
            text="Back to Scan",
            command=self.show_scan_view,
            width=120,
            corner_radius=8
        )
        back_button.pack(pady=10)
        
        # Update status
        self.status_var.set("About Empty Cleaner")
    
    def show_scan_view(self):
        # Remove the about frame if it exists
        if hasattr(self, 'about_frame'):
            self.about_frame.destroy()
        
        # Update header
        self.header_label.configure(text="Scan Results")
        
        # Show the tabview again
        self.results_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Update status
        self.status_var.set("Ready to scan.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = EmptyCleaner(root)
    root.mainloop()
