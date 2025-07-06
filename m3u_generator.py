import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import re
from pathlib import Path
import threading

class ESDE_M3UGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("ES-DE Multi-Disc M3U Generator")
        self.root.geometry("1000x800")
        self.root.minsize(900, 750)
        
        # Variables
        self.roms_folder_path = tk.StringVar()
        self.games_found = {}
        self.game_vars = {}  # Dictionary to store checkbox variables
        self.tree_items = {}  # Map tree item IDs to game names
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="ES-DE Multi-Disc M3U Generator", 
                               font=("TkDefaultFont", 14, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Description
        desc_text = """This tool creates ES-DE compatible multi-disc game folders.
        
For each multi-disc game, it will:
• Create a folder named 'Game Name.m3u'
• Move all disc files into that folder
• Create an M3U file inside the folder listing the discs

This allows ES-DE to show only one entry per game while supporting disc switching."""
        
        desc_label = ttk.Label(main_frame, text=desc_text, justify=tk.LEFT, 
                              font=("TkDefaultFont", 9))
        desc_label.pack(pady=(0, 15))
        
        # ROMs Folder selection
        ttk.Label(main_frame, text="ROMs Folder:").pack(anchor=tk.W)
        
        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill=tk.X, pady=5)
        
        ttk.Entry(folder_frame, textvariable=self.roms_folder_path).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(folder_frame, text="Browse", command=self.browse_folder).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Scan button
        ttk.Button(main_frame, text="Scan for Multi-Disc Games", command=self.scan_games).pack(pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Multi-Disc Games Found", padding="5")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Selection buttons frame
        selection_frame = ttk.Frame(results_frame)
        selection_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.select_all_btn = ttk.Button(selection_frame, text="Select All", 
                                        command=self.select_all_games, state='disabled')
        self.select_all_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.select_none_btn = ttk.Button(selection_frame, text="Select None", 
                                         command=self.select_none_games, state='disabled')
        self.select_none_btn.pack(side=tk.LEFT)
        
        # Treeview frame (for grid layout)
        treeview_frame = ttk.Frame(results_frame)
        treeview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for games list (created ONCE here)
        columns = ("selected", "game_name", "discs", "folder_name")
        self.tree = ttk.Treeview(treeview_frame, columns=columns, show="headings", selectmode="none")
        self.tree.heading("selected", text="■")
        self.tree.heading("game_name", text="Game Name")
        self.tree.heading("discs", text="Discs")
        self.tree.heading("folder_name", text="Folder Name")
        self.tree.column("selected", width=40, anchor="center", stretch=False)
        self.tree.column("game_name", width=350, anchor="w")
        self.tree.column("discs", width=60, anchor="center", stretch=False)
        self.tree.column("folder_name", width=300, anchor="w")
        
        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(treeview_frame, orient="vertical", command=self.tree.yview)
        tree_scroll_x = ttk.Scrollbar(treeview_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
        
        # Use grid for Treeview and scrollbars inside treeview_frame
        self.tree.grid(row=0, column=0, sticky="nsew")
        tree_scroll_y.grid(row=0, column=1, sticky="ns")
        tree_scroll_x.grid(row=1, column=0, sticky="ew")
        treeview_frame.grid_rowconfigure(0, weight=1)
        treeview_frame.grid_columnconfigure(0, weight=1)
        
        # Bind click on the first column to toggle selection
        self.tree.bind("<Button-1>", self.on_tree_click)
        
        # Bottom section
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Generate button
        self.generate_btn = ttk.Button(bottom_frame, text="Create ES-DE Multi-Disc Folders", 
                                      command=self.generate_esde_folders, state='disabled')
        self.generate_btn.pack(pady=5)
        
        # Status bar at the bottom of the window
        self.status_var = tk.StringVar(value="Ready to scan")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, anchor='w', relief='sunken')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def set_status(self, text):
        self.status_var.set(text)
        self.status_bar.update_idletasks()
    
    def select_all_games(self):
        for game_name in self.game_vars:
            self.game_vars[game_name].set(True)
        self.update_tree_checks()
    
    def select_none_games(self):
        for game_name in self.game_vars:
            self.game_vars[game_name].set(False)
        self.update_tree_checks()
    
    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select ROMs Folder")
        if folder:
            self.roms_folder_path.set(folder)
    
    def scan_games(self):
        if not self.roms_folder_path.get():
            messagebox.showerror("Error", "Please select a ROMs folder first!")
            return
        self.progress.start()
        self.set_status("Scanning for multi-disc games...")
        self.generate_btn.config(state='disabled')
        self.select_all_btn.config(state='disabled')
        self.select_none_btn.config(state='disabled')
        # Run scanning in a separate thread
        thread = threading.Thread(target=self._scan_games_thread)
        thread.daemon = True
        thread.start()
    
    def _scan_games_thread(self):
        try:
            folder = self.roms_folder_path.get()
            games = self.find_multidisc_games(folder)
            print(f"DEBUG: Found {len(games)} games: {list(games.keys())}")
            self.root.after(0, self._update_results, games)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error scanning games: {str(e)}"))
        finally:
            self.root.after(0, self._scan_complete)
    
    def _scan_complete(self):
        self.progress.stop()
        self.set_status("Scan complete")
    
    def _update_results(self, games):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.games_found = games
        self.game_vars.clear()
        self.tree_items.clear()
        print(f"DEBUG: _update_results called with {len(games)} games.")
        if games:
            for game_name, discs in games.items():
                print(f"DEBUG: Inserting {game_name} with {len(discs)} discs.")
                var = tk.BooleanVar(value=True)
                self.game_vars[game_name] = var
                
                # Extract display name and folder name
                if '/' in game_name:
                    subfolder_path, base_game_name = game_name.rsplit('/', 1)
                    display_name = f"{base_game_name} (in {subfolder_path})"
                    folder_name = f"{subfolder_path}/{base_game_name}.m3u"
                else:
                    display_name = game_name
                    folder_name = f"{game_name}.m3u"
                
                item_id = self.tree.insert("", "end", values=("■", display_name, str(len(discs)), folder_name))
                self.tree_items[item_id] = game_name
            self.tree.update_idletasks()
            # Ensure the first item is visible
            children = self.tree.get_children()
            if children:
                self.tree.see(children[0])
            self.generate_btn.config(state='normal')
            self.select_all_btn.config(state='normal')
            self.select_none_btn.config(state='normal')
            self.set_status(f"Found {len(games)} multi-disc game(s) - Select which ones to process")
        else:
            self.set_status("No multi-disc games found")
    
    def update_tree_checks(self):
        for item_id, game_name in self.tree_items.items():
            checked = self.game_vars[game_name].get()
            self.tree.set(item_id, "selected", "■" if checked else "☐")
    
    def on_tree_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "heading":
            return
        col = self.tree.identify_column(event.x)
        if col == "#1":  # First column (checkbox)
            row_id = self.tree.identify_row(event.y)
            if row_id:
                game_name = self.tree_items.get(row_id)
                if game_name:
                    var = self.game_vars[game_name]
                    var.set(not var.get())
                    self.update_tree_checks()
    
    def find_multidisc_games(self, folder):
        games = {}
        disc_pattern = re.compile(r'^(.+?)\s*\(Disc\s*\d+\)\s*(.+)$', re.IGNORECASE)
        for file_path in Path(folder).rglob('*'):
            if file_path.is_file():
                filename = file_path.name
                match = disc_pattern.match(filename)
                if match:
                    base_name = match.group(1).strip()
                    extension = match.group(2).strip()
                    # Use the subfolder path as part of the key to keep games separate by location
                    subfolder = file_path.parent.relative_to(Path(folder))
                    game_key = f"{subfolder}/{base_name}" if str(subfolder) != "." else base_name
                    if game_key not in games:
                        games[game_key] = []
                    games[game_key].append((filename, file_path))
        for game_name in games:
            games[game_name].sort(key=lambda x: self.extract_disc_number(x[0]))
        return games
    
    def extract_disc_number(self, filename):
        match = re.search(r'\(Disc\s*(\d+)\)', filename, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return 0
    
    def generate_esde_folders(self):
        if not self.games_found:
            messagebox.showwarning("Warning", "No multi-disc games found!")
            return
        selected_games = {game_name: discs for game_name, discs in self.games_found.items() 
                         if self.game_vars[game_name].get()}
        if not selected_games:
            messagebox.showwarning("Warning", "Please select at least one game to process!")
            return
        roms_folder = Path(self.roms_folder_path.get())
        created_folders = []
        moved_files = []
        for game_name, discs in selected_games.items():
            # Extract the base game name and subfolder path
            if '/' in game_name:
                subfolder_path, base_game_name = game_name.rsplit('/', 1)
                target_folder = roms_folder / subfolder_path
                folder_name = f"{base_game_name}.m3u"
                game_folder = target_folder / folder_name
            else:
                # Game is in the root folder
                base_game_name = game_name
                target_folder = roms_folder
                folder_name = f"{base_game_name}.m3u"
                game_folder = target_folder / folder_name
            
            try:
                # Ensure the target folder exists
                target_folder.mkdir(parents=True, exist_ok=True)
                game_folder.mkdir(exist_ok=True)
                disc_filenames = []
                for disc_filename, disc_path in discs:
                    new_disc_path = game_folder / disc_filename
                    disc_path.rename(new_disc_path)
                    disc_filenames.append(disc_filename)
                    moved_files.append(disc_filename)
                m3u_filename = f"{base_game_name}.m3u"
                m3u_path = game_folder / m3u_filename
                with open(m3u_path, 'w', encoding='utf-8') as f:
                    for disc_filename in disc_filenames:
                        f.write(f"{disc_filename}\n")
                created_folders.append(f"{subfolder_path}/{folder_name}" if '/' in game_name else folder_name)
            except Exception as e:
                messagebox.showerror("Error", f"Error processing {game_name}: {str(e)}")
                return
        if created_folders:
            message = f"Successfully created {len(created_folders)} ES-DE multi-disc folder(s):\n\n"
            message += "\n".join(created_folders) + "\n\n"
            message += f"Moved {len(moved_files)} disc file(s) into the folders.\n\n"
            message += "Each folder contains:\n"
            message += "• All disc files for the game\n"
            message += "• An M3U file listing the discs in order\n\n"
            message += "ES-DE will now show only one entry per game with disc switching support."
            messagebox.showinfo("Success", message)
            self.set_status(f"Created {len(created_folders)} ES-DE multi-disc folders")

def main():
    root = tk.Tk()
    app = ESDE_M3UGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main() 