import os
import shutil
import logging
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD

# Logging setup
logging.basicConfig(
    filename='file_organizer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

# File categories (now modifiable)
categories = {
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Audio": [".mp3", ".wav", ".aac"]
}

# Ensure unique filenames
def get_unique_filename(filepath):
    base, extension = os.path.splitext(filepath)
    counter = 1
    while os.path.exists(filepath):
        filepath = f"{base}_{counter}{extension}"
        counter += 1
    return filepath

# Organize files logic
def organize_files_gui(target_directory):
    try:
        for folder in categories:
            os.makedirs(os.path.join(target_directory, folder), exist_ok=True)
        os.makedirs(os.path.join(target_directory, "Others"), exist_ok=True)

        for item in os.listdir(target_directory):
            item_path = os.path.join(target_directory, item)
            if os.path.isdir(item_path):
                continue

            moved = False
            for folder, extensions in categories.items():
                if item.lower().endswith(tuple(extensions)):
                    dest = os.path.join(target_directory, folder, item)
                    dest = get_unique_filename(dest)
                    shutil.move(item_path, dest)
                    logger.info(f"{item} → {folder}")
                    moved = True
                    break

            if not moved:
                dest = os.path.join(target_directory, "Others", item)
                dest = get_unique_filename(dest)
                shutil.move(item_path, dest)
                logger.info(f"{item} → Others")

        messagebox.showinfo("Success", "Files have been organized successfully.")
    except Exception as e:
        logger.error(f"Error organizing files: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

# Category management window
def open_category_manager():
    category_window = tk.Toplevel(root)
    category_window.title("Manage Categories")
    category_window.geometry("500x400")
    category_window.resizable(True, True)
    
    # Make window modal
    category_window.transient(root)
    category_window.grab_set()
    
    # Main frame
    main_frame = tk.Frame(category_window)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Categories listbox with scrollbar
    list_frame = tk.Frame(main_frame)
    list_frame.pack(fill=tk.BOTH, expand=True)
    
    tk.Label(list_frame, text="Categories and Extensions:", font=('Arial', 10, 'bold')).pack(anchor='w')
    
    listbox_frame = tk.Frame(list_frame)
    listbox_frame.pack(fill=tk.BOTH, expand=True, pady=5)
    
    scrollbar = tk.Scrollbar(listbox_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    category_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set, font=('Courier', 9))
    category_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=category_listbox.yview)
    
    def refresh_listbox():
        category_listbox.delete(0, tk.END)
        for category, extensions in categories.items():
            ext_str = ", ".join(extensions)
            category_listbox.insert(tk.END, f"{category}: {ext_str}")
    
    refresh_listbox()
    
    # Buttons frame
    button_frame = tk.Frame(main_frame)
    button_frame.pack(fill=tk.X, pady=10)
    
    # Add category function
    def add_category():
        add_window = tk.Toplevel(category_window)
        add_window.title("Add Category")
        add_window.geometry("350x200")
        add_window.transient(category_window)
        add_window.grab_set()
        
        tk.Label(add_window, text="Category Name:").pack(pady=5)
        name_entry = tk.Entry(add_window, width=30)
        name_entry.pack(pady=5)
        
        tk.Label(add_window, text="Extensions (comma-separated, with dots):").pack(pady=5)
        tk.Label(add_window, text="Example: .pdf, .docx, .txt", font=('Arial', 8), fg='gray').pack()
        ext_entry = tk.Entry(add_window, width=30)
        ext_entry.pack(pady=5)
        
        def save_category():
            name = name_entry.get().strip()
            extensions = ext_entry.get().strip()
            
            if not name or not extensions:
                messagebox.showwarning("Invalid Input", "Please fill in both fields.")
                return
            
            if name in categories:
                messagebox.showwarning("Duplicate", "Category already exists.")
                return
            
            # Parse extensions
            ext_list = [ext.strip() for ext in extensions.split(',')]
            ext_list = [ext if ext.startswith('.') else f'.{ext}' for ext in ext_list]
            
            categories[name] = ext_list
            refresh_listbox()
            add_window.destroy()
            messagebox.showinfo("Success", f"Category '{name}' added successfully.")
        
        tk.Button(add_window, text="Add Category", command=save_category, bg="green", fg="white").pack(pady=10)
        name_entry.focus()
    
    # Edit category function
    def edit_category():
        selection = category_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a category to edit.")
            return
        
        selected_text = category_listbox.get(selection[0])
        category_name = selected_text.split(':')[0]
        
        edit_window = tk.Toplevel(category_window)
        edit_window.title(f"Edit Category: {category_name}")
        edit_window.geometry("350x200")
        edit_window.transient(category_window)
        edit_window.grab_set()
        
        tk.Label(edit_window, text="Category Name:").pack(pady=5)
        name_entry = tk.Entry(edit_window, width=30)
        name_entry.pack(pady=5)
        name_entry.insert(0, category_name)
        
        tk.Label(edit_window, text="Extensions (comma-separated, with dots):").pack(pady=5)
        ext_entry = tk.Entry(edit_window, width=30)
        ext_entry.pack(pady=5)
        ext_entry.insert(0, ", ".join(categories[category_name]))
        
        def save_changes():
            new_name = name_entry.get().strip()
            extensions = ext_entry.get().strip()
            
            if not new_name or not extensions:
                messagebox.showwarning("Invalid Input", "Please fill in both fields.")
                return
            
            # Parse extensions
            ext_list = [ext.strip() for ext in extensions.split(',')]
            ext_list = [ext if ext.startswith('.') else f'.{ext}' for ext in ext_list]
            
            # Remove old category if name changed
            if new_name != category_name:
                if new_name in categories:
                    messagebox.showwarning("Duplicate", "Category name already exists.")
                    return
                del categories[category_name]
            
            categories[new_name] = ext_list
            refresh_listbox()
            edit_window.destroy()
            messagebox.showinfo("Success", f"Category '{new_name}' updated successfully.")
        
        tk.Button(edit_window, text="Save Changes", command=save_changes, bg="blue", fg="white").pack(pady=10)
    
    # Remove category function
    def remove_category():
        selection = category_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a category to remove.")
            return
        
        selected_text = category_listbox.get(selection[0])
        category_name = selected_text.split(':')[0]
        
        if messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove the '{category_name}' category?"):
            del categories[category_name]
            refresh_listbox()
            messagebox.showinfo("Success", f"Category '{category_name}' removed successfully.")
    
    # Reset to defaults function
    def reset_defaults():
        if messagebox.askyesno("Reset Categories", "Are you sure you want to reset to default categories? This will remove all custom categories."):
            global categories
            categories = {
                "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
                "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
                "Videos": [".mp4", ".mov", ".avi", ".mkv"],
                "Audio": [".mp3", ".wav", ".aac"]
            }
            refresh_listbox()
            messagebox.showinfo("Success", "Categories reset to defaults.")
    
    # Button layout
    btn_frame1 = tk.Frame(button_frame)
    btn_frame1.pack(fill=tk.X, pady=2)
    
    tk.Button(btn_frame1, text="Add Category", command=add_category, bg="green", fg="white", width=15).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame1, text="Edit Category", command=edit_category, bg="blue", fg="white", width=15).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame1, text="Remove Category", command=remove_category, bg="red", fg="white", width=15).pack(side=tk.LEFT, padx=5)
    
    btn_frame2 = tk.Frame(button_frame)
    btn_frame2.pack(fill=tk.X, pady=2)
    
    tk.Button(btn_frame2, text="Reset to Defaults", command=reset_defaults, bg="orange", fg="white", width=20).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame2, text="Close", command=category_window.destroy, width=20).pack(side=tk.RIGHT, padx=5)
    
    # Double-click to edit
    category_listbox.bind('<Double-1>', lambda e: edit_category())

# Browse folder dialog
def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, folder_selected)

# Start organizing from input
def start_organizing():
    folder_path = entry_path.get()
    if not os.path.isdir(folder_path):
        messagebox.showwarning("Invalid Path", "Please select a valid directory.")
        return
    organize_files_gui(folder_path)

# Handle drag and drop
def drop_event(event):
    dropped_path = event.data.strip('{}')  # Clean up the dropped path
    if os.path.isdir(dropped_path):
        entry_path.delete(0, tk.END)
        entry_path.insert(0, dropped_path)
        organize_files_gui(dropped_path)
    else:
        messagebox.showwarning("Invalid Drop", "Please drop a folder only.")

# Create GUI window with drag and drop
root = TkinterDnD.Tk()
root.title("File Organizer")
root.geometry("450x200")
root.resizable(False, False)

tk.Label(root, text="Select or drag a folder to organize:", font=('Arial', 10)).pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=5)

entry_path = tk.Entry(frame, width=45)
entry_path.pack(side=tk.LEFT, padx=5)

browse_button = tk.Button(frame, text="Browse", command=browse_folder)
browse_button.pack(side=tk.LEFT)

# Button frame for organize and manage categories
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

organize_button = tk.Button(button_frame, text="Organize Files", command=start_organizing, bg="green", fg="white", width=15)
organize_button.pack(side=tk.LEFT, padx=5)

manage_button = tk.Button(button_frame, text="Manage Categories", command=open_category_manager, bg="purple", fg="white", width=15)
manage_button.pack(side=tk.LEFT, padx=5)

# Add drag and drop
entry_path.drop_target_register(DND_FILES)
entry_path.dnd_bind('<<Drop>>', drop_event)

root.mainloop()