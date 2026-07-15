import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import json
import os
import time

FILE = "tasks.json"

# Initialize CustomTkinter settings
ctk.set_appearance_mode("System")  # Adapts beautifully to user's OS dark/light mode
ctk.set_default_color_theme("blue")

def load_tasks():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_tasks():
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=2)

tasks = load_tasks()


root = ctk.CTk()
root.title("To-Do-List")
root.geometry("600x750")
root.resizable(False, False)

# --- Real-Time Animated Clock ---
def update_clock():
    current_time = time.strftime("📅 %A, %d %b %Y   🕒 %I:%M:%S %p")
    clock_label.configure(text=current_time)
    root.after(1000, update_clock)

# --- UI Header ---
header_frame = ctk.CTkFrame(root, fg_color="transparent")
header_frame.pack(pady=(30, 10), fill="x", padx=40)

title_label = ctk.CTkLabel(
    header_frame, 
    text="To-Do-List", 
    font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"),
    text_color=("#4F46E5", "#818CF8") # Light mode / Dark mode contrast
)
title_label.pack()

subtitle_label = ctk.CTkLabel(
    header_frame, 
    text="✨ Organize your day beautifully ✨", 
   font=ctk.CTkFont(family="Segoe UI", size=13, slant="italic"),
    text_color=("#6B7280", "#9CA3AF")
)
subtitle_label.pack(pady=(2, 5))

clock_label = ctk.CTkLabel(
    header_frame, 
    font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
    text_color=("#EC4899", "#F472B6")
)
clock_label.pack()

# --- Input Area ---
input_frame = ctk.CTkFrame(root, fg_color="transparent")
input_frame.pack(pady=15, padx=30, fill="x")

task_entry = ctk.CTkEntry(
    input_frame, 
    placeholder_text="What's your next breakthrough step?...",
    font=ctk.CTkFont(family="Segoe UI", size=14),
    height=45,
    corner_radius=12,
    border_width=2,
    border_color=("#D8B4FE", "#4C1D95")
)
task_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

# --- Scrollable Modern List Frame ---
# CustomTkinter's ScrollableFrame removes the ugly standard legacy listbox look
scroll_frame = ctk.CTkScrollableFrame(
    root, 
    width=500, 
    height=380, 
    corner_radius=16,
    fg_color=("#F5F3FF", "#1E1B4B"),
    border_width=1,
    border_color=("#E0E7FF", "#312E81")
)
scroll_frame.pack(pady=15, padx=30, fill="both", expand=True)

status_label = ctk.CTkLabel(
    root, 
    text="Total Tasks: 0", 
    font=ctk.CTkFont(family="Segoe UI", size=12),
    text_color=("#4B5563", "#9CA3AF")
)
status_label.pack(pady=(0, 10))

# --- Task Engine and Refresh Layout ---
def refresh_ui():
    # Clear the layout
    for widget in scroll_frame.winfo_children():
        widget.destroy()
        
    for index, task in enumerate(tasks):
        # Frame container for each list item
        item_bg = ("#FFFFFF", "#2E2A72") if not task["done"] else ("#EEF2FF", "#16133A")
        item_frame = ctk.CTkFrame(scroll_frame, fg_color=item_bg, corner_radius=10, height=50)
        item_frame.pack(fill="x", pady=5, padx=5)
        item_frame.pack_propagate(False)
        
        # Checkbox for marking completion status
        cb_var = tk.BooleanVar(value=task["done"])
        cb = ctk.CTkCheckBox(
            item_frame, 
            text=task["task"], 
            variable=cb_var,
            command=lambda i=index: toggle_complete(i),
            font=ctk.CTkFont(
    family="Segoe UI", 
    size=13, 
    weight="normal", 
    overstrike=True if task["done"] else False
),
            checkbox_width=22,
            checkbox_height=22,
            corner_radius=6,
            fg_color="#6366F1",
            hover_color="#4F46E5"
        )
        cb.pack(side="left", padx=15, fill="x", expand=True)
        
        # Action Buttons for individual item controls
        del_btn = ctk.CTkButton(
            item_frame, 
            text="🗑️", 
            width=35, 
            height=30, 
            fg_color="transparent", 
            text_color=("#EF4444", "#F87171"),
            hover_color=("#FEE2E2", "#7F1D1D"),
            corner_radius=8,
            command=lambda i=index: delete_task(i)
        )
        del_btn.pack(side="right", padx=(0, 10))
        
        edit_btn = ctk.CTkButton(
            item_frame, 
            text="✏️", 
            width=35, 
            height=30, 
            fg_color="transparent", 
            text_color=("#3B82F6", "#60A5FA"),
            hover_color=("#DBEAFE", "#1E3A8A"),
            corner_radius=8,
            command=lambda i=index: prep_edit_task(i)
        )
        edit_btn.pack(side="right", padx=(0, 5))

    status_label.configure(text=f"Total Tasks: {len(tasks)}  |  Completed: {sum(1 for t in tasks if t['done'])}")

# --- Actions Engine ---
def add_task():
    txt = task_entry.get().strip()
    if not txt:
        messagebox.showwarning("Empty Task", "Please write a task down before adding.")
        return
    tasks.append({"task": txt, "done": False})
    save_tasks()
    refresh_ui()
    task_entry.delete(0, tk.END)

def toggle_complete(index):
    tasks[index]["done"] = not tasks[index]["done"]
    save_tasks()
    refresh_ui()

def delete_task(index):
    tasks.pop(index)
    save_tasks()
    refresh_ui()

def prep_edit_task(index):
    # Inserts current task back into text entry for quick updating
    task_entry.delete(0, tk.END)
    task_entry.insert(0, tasks[index]["task"])
    
    # Smooth temporary override to prompt user action update
    add_button.configure(text="💾 Update", fg_color="#10B981", hover_color="#059669", command=lambda: save_edit_task(index))

def save_edit_task(index):
    txt = task_entry.get().strip()
    if not txt: return
    tasks[index]["task"] = txt
    save_tasks()
    task_entry.delete(0, tk.END)
    # Reset adding capabilities back to button default state
    add_button.configure(text="➕ Add Task", fg_color="#6366F1", hover_color="#4F46E5", command=add_task)
    refresh_ui()

# --- Main Action Adding Button ---
add_button = ctk.CTkButton(
    input_frame, 
    text="➕ Add Task", 
    font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
    width=110,
    height=45,
    corner_radius=12,
    fg_color="#6366F1",
    hover_color="#4F46E5"
)
add_button.configure(command=add_task)
add_button.pack(side="right")

# --- Footer Decorator ---
footer_label = ctk.CTkLabel(
    root, 
    text="✔ Stay Consistent • Every Task Counts", 
    font=ctk.CTkFont(family="Segoe UI", size=11),
    text_color=("#9CA3AF", "#4B5563")
)
footer_label.pack(side="bottom", pady=15)

# --- App Initialization Engine Loops ---
refresh_ui()
update_clock()
root.mainloop()