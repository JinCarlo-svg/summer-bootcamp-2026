import customtkinter as ctk
import json
import os
import ctypes
from datetime import datetime
import shutil

# --- WIN32 TASKBAR ICON FIX ---
try:
    app_id = "portfolio.modern.taskmanager.v2"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
except Exception:
    pass

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class EnterpriseTaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("NexusTask Pro ")
        self.root.geometry("650x800")
        self.root.resizable(False, False)
        
        # Icon management
        self.icon_name = "app_icon.ico"
        if os.path.exists(self.icon_name):
            self.root.iconbitmap(self.icon_name)
        
        # File paths & Backup configurations
        self.file_name = "modern_tasks.json"
        self.backup_dir = "backups"
        self.tasks = self.load_tasks_with_recovery()
        self.current_filter = "All"

        self.setup_ui()
        self.refresh_list()
        self.show_toast("System Initialized Successfully! 💾", "#a6e3a1")

    def load_tasks_with_recovery(self):
        """Advanced engineering: Database recovery system from backups"""
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                # If primary file is corrupted, look into backups
                if os.path.exists(self.backup_dir):
                    backups = sorted(os.listdir(self.backup_dir), reverse=True)
                    if backups:
                        latest_backup = os.path.join(self.backup_dir, backups[0])
                        with open(latest_backup, "r") as f:
                            print(f"CRITICAL: Primary database corrupted! Recovered from {latest_backup}")
                            return json.load(f)
                return []
        return []

    def save_and_backup(self):
        """Saves current state and creates an archival backup file"""
        with open(self.file_name, "w") as f:
            json.dump(self.tasks, f, indent=4)
        
        # Create continuous automated backups
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(self.backup_dir, f"backup_{timestamp}.json")
        shutil.copy(self.file_name, backup_path)
        
        # Keep only the last 5 backups to optimize storage
        all_backups = sorted([os.path.join(self.backup_dir, b) for b in os.listdir(self.backup_dir)])
        while len(all_backups) > 5:
            os.remove(all_backups.pop(0))

    def setup_ui(self):
        # Header Banner
        self.title_label = ctk.CTkLabel(self.root, text=" 📊 ENTERPRISE TASK CONSOLE", font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color="#cba6f7")
        self.title_label.pack(pady=(20, 10))

        # --- DYNAMIC IN-APP NOTIFICATION BANNER (Toast System) ---
        self.toast_label = ctk.CTkLabel(self.root, text="", font=ctk.CTkFont(size=12, weight="bold"), fg_color="transparent", height=0, corner_radius=8)
        self.toast_label.pack(fill="x", padx=30, pady=(0, 10))

        # Stats Progress Tracker
        self.stats_frame = ctk.CTkFrame(self.root, fg_color="#181825", corner_radius=10)
        self.stats_frame.pack(fill="x", padx=30, pady=5)
        
        self.progress_label = ctk.CTkLabel(self.stats_frame, text="⚡ Progress: 0%", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color="#bac2de")
        self.progress_label.pack(side="left", padx=15, pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(self.stats_frame, width=380, fg_color="#313244", progress_color="#a6e3a1")
        self.progress_bar.pack(side="right", padx=15, pady=10)
        self.progress_bar.set(0)

        # Filters Controls
        filter_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        filter_frame.pack(fill="x", padx=30, pady=5)
        
        for filter_type in ["All", "Pending", "Completed"]:
            btn = ctk.CTkButton(filter_frame, text=filter_type, width=85, height=28, corner_radius=20,
                                fg_color="#89b4fa" if filter_type == "All" else "#313244",
                                text_color="#11111b" if filter_type == "All" else "#cdd6f4",
                                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                                command=lambda f=filter_type: self.set_filter(f))
            btn.pack(side="left", padx=5)

        # Input Row
        input_frame = ctk.CTkFrame(self.root, fg_color="#1e1e2e", corner_radius=15)
        input_frame.pack(pady=10, fill="x", padx=30, ipady=5)

        self.task_entry = ctk.CTkEntry(input_frame, placeholder_text="🔍 Deploy next objective script...", width=320, height=40, fg_color="#313244", border_color="#45475a", text_color="#cdd6f4", corner_radius=10)
        self.task_entry.grid(row=0, column=0, padx=15, pady=15)

        self.priority_combo = ctk.CTkComboBox(input_frame, values=["🔥 High", "⚡ Medium", "🍃 Low"], width=110, height=40, corner_radius=10, fg_color="#313244", border_color="#45475a")
        self.priority_combo.set("⚡ Medium")
        self.priority_combo.grid(row=0, column=1, padx=5, pady=15)

        self.add_btn = ctk.CTkButton(input_frame, text="➕ Deploy", width=80, height=40, corner_radius=10, font=ctk.CTkFont(weight="bold"), fg_color="#a6e3a1", hover_color="#94e2d5", text_color="#11111b", command=self.add_task)
        self.add_btn.grid(row=0, column=2, padx=15, pady=15)

        # Scrollable list view
        self.tasks_container = ctk.CTkScrollableFrame(self.root, fg_color="#181825", corner_radius=15, width=540, height=440)
        self.tasks_container.pack(pady=10, padx=30, fill="both", expand=True)

    def show_toast(self, text, color="#89b4fa"):
        """Displays a beautiful modern toast alert that clears itself dynamically"""
        self.toast_label.configure(text=text, fg_color=color, text_color="#11111b", height=30)
        self.root.after(2500, lambda: self.toast_label.configure(text="", fg_color="transparent", height=0))

    def set_filter(self, filter_type):
        self.current_filter = filter_type
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for sub_w in widget.winfo_children():
                    if isinstance(sub_w, ctk.CTkButton) and sub_w.cget("text") in ["All", "Pending", "Completed"]:
                        if sub_w.cget("text") == filter_type:
                            sub_w.configure(fg_color="#89b4fa", text_color="#11111b")
                        else:
                            sub_w.configure(fg_color="#313244", text_color="#cdd6f4")
        self.refresh_list()

    def update_progress(self):
        if not self.tasks:
            self.progress_bar.set(0)
            self.progress_label.configure(text="⚡ Progress: 0%")
            return
        completed_count = sum(1 for t in self.tasks if t["completed"])
        ratio = completed_count / len(self.tasks)
        self.progress_bar.set(ratio)
        self.progress_label.configure(text=f"⚡ Progress: {int(ratio*100)}%")

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            self.tasks.append({"title": task_text, "priority": self.priority_combo.get(), "completed": False})
            self.save_and_backup()
            self.refresh_list()
            self.task_entry.delete(0, 'end')
            self.show_toast("Task deployed successfully! ✨", "#a6e3a1")
        else:
            self.show_toast("Error: Task field is empty! ✕", "#f38ba8")

    def refresh_list(self):
        for widget in self.tasks_container.winfo_children():
            widget.destroy()

        self.update_progress()

        for index, task in enumerate(self.tasks):
            if self.current_filter == "Pending" and task["completed"]: continue
            if self.current_filter == "Completed" and not task["completed"]: continue

            task_card = ctk.CTkFrame(self.tasks_container, fg_color="#313244", corner_radius=10)
            task_card.pack(fill="x", pady=5, padx=10)

            p_text = task["priority"]
            badge_color = "#f38ba8" if "High" in p_text else ("#f9e2af" if "Medium" in p_text else "#a6e3a1")
            
            priority_label = ctk.CTkLabel(task_card, text=f" {p_text} ", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#11111b", fg_color=badge_color, corner_radius=5)
            priority_label.pack(side="left", padx=10, pady=10)

            display_title = f"✅ {task['title']}" if task["completed"] else f"📌 {task['title']}"
            task_title = ctk.CTkLabel(task_card, text=display_title, font=ctk.CTkFont(family="Segoe UI", size=13, weight="normal" if not task["completed"] else "bold"), text_color="#cdd6f4" if not task["completed"] else "#585b70")
            task_title.pack(side="left", padx=10, fill="x", expand=True, anchor="w")

            toggle_btn = ctk.CTkButton(task_card, text="✔️", width=35, height=35, fg_color="#89b4fa", text_color="#11111b", font=ctk.CTkFont(weight="bold"), command=lambda idx=index: self.toggle_task(idx))
            toggle_btn.pack(side="right", padx=5)

            del_btn = ctk.CTkButton(task_card, text="🗑️", width=35, height=35, fg_color="#f38ba8", text_color="#11111b", font=ctk.CTkFont(weight="bold"), command=lambda idx=index: self.delete_task(idx))
            del_btn.pack(side="right", padx=(0, 10))

    def toggle_task(self, index):
        self.tasks[index]["completed"] = not self.tasks[index]["completed"]
        self.save_and_backup()
        self.refresh_list()
        status_msg = "Task checked! ✔️" if self.tasks[index]["completed"] else "Task marked pending! ⏳"
        self.show_toast(status_msg, "#89b4fa")

    def delete_task(self, index):
        del self.tasks[index]
        self.save_and_backup()
        self.refresh_list()
        self.show_toast("Task purged from database! 🗑️", "#f38ba8")

if __name__ == "__main__":
    root = ctk.CTk()
    app = EnterpriseTaskManager(root)
    root.mainloop()