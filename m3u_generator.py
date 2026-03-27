import sys
import os
import re
import threading
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QFileDialog, QTextEdit, QProgressBar, QListWidget, QListWidgetItem, QCheckBox,
    QScrollArea, QFrame, QDialog, QButtonGroup, QRadioButton, QStatusBar, QGroupBox,
    QAction, QMenuBar, QMenu, QMainWindow, QTreeWidget, QTreeWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QColor, QPalette, QFont

# Theme management
class ThemeManager:
    @staticmethod
    def get_light_theme():
        return """
        QWidget {
            background-color: #f5f5f5;
            color: #333333;
        }
        QPushButton {
            background-color: #e0e0e0;
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 6px 12px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #d0d0d0;
        }
        QPushButton:pressed {
            background-color: #c0c0c0;
        }
        QPushButton:disabled {
            background-color: #f0f0f0;
            color: #999999;
        }
        QLineEdit {
            background-color: white;
            border: 1px solid #cccccc;
            border-radius: 3px;
            padding: 4px;
        }
        QLineEdit:focus {
            border: 2px solid #4a90e2;
        }
        QTextEdit {
            background-color: white;
            border: 1px solid #cccccc;
            border-radius: 3px;
        }
        QTreeWidget {
            background-color: white;
            border: 1px solid #cccccc;
            border-radius: 3px;
            alternate-background-color: #f9f9f9;
        }
        QTreeWidget::item {
            padding: 4px;
        }
        QTreeWidget::item:selected {
            background-color: #e3f2fd;
            color: #1976d2;
        }
        QHeaderView::section {
            background-color: #e0e0e0;
            color: #333333;
            border: 1px solid #cccccc;
            padding: 6px;
            font-weight: bold;
        }
        QHeaderView::section:hover {
            background-color: #d0d0d0;
        }
        QScrollBar:horizontal {
            background-color: #f0f0f0;
            border: 1px solid #cccccc;
            height: 12px;
        }
        QScrollBar::handle:horizontal {
            background-color: #c0c0c0;
            border-radius: 6px;
            min-width: 20px;
        }
        QScrollBar::handle:horizontal:hover {
            background-color: #b0b0b0;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            background-color: #f0f0f0;
            border: none;
            width: 0px;
        }
        QScrollBar:vertical {
            background-color: #f0f0f0;
            border: 1px solid #cccccc;
            width: 12px;
        }
        QScrollBar::handle:vertical {
            background-color: #c0c0c0;
            border-radius: 6px;
            min-height: 20px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #b0b0b0;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background-color: #f0f0f0;
            border: none;
            height: 0px;
        }
        QProgressBar {
            border: 1px solid #cccccc;
            border-radius: 3px;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #4caf50;
            border-radius: 2px;
        }
        QStatusBar {
            background-color: #e0e0e0;
            border-top: 1px solid #cccccc;
        }
        QMenuBar {
            background-color: #f5f5f5;
            border-bottom: 1px solid #cccccc;
        }
        QMenuBar::item {
            background-color: transparent;
            padding: 4px 8px;
        }
        QMenuBar::item:selected {
            background-color: #e0e0e0;
        }
        QMenu {
            background-color: white;
            border: 1px solid #cccccc;
        }
        QMenu::item {
            padding: 6px 20px;
        }
        QMenu::item:selected {
            background-color: #e3f2fd;
        }
        QCheckBox {
            color: #333333;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
        }
        QCheckBox::indicator:unchecked {
            border: 2px solid #cccccc;
            background-color: white;
        }
        QCheckBox::indicator:checked {
            border: 2px solid #4a90e2;
            background-color: #1976d2;
        }
        QLabel {
            color: #333333;
        }
        QGroupBox {
            font-weight: bold;
            border: 1px solid #cccccc;
            border-radius: 4px;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        """

    @staticmethod
    def get_dark_theme():
        return """
        QWidget {
            background-color: #2d2d2d;
            color: #e0e0e0;
        }
        QPushButton {
            background-color: #404040;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 6px 12px;
            font-weight: bold;
            color: #e0e0e0;
        }
        QPushButton:hover {
            background-color: #505050;
        }
        QPushButton:pressed {
            background-color: #353535;
        }
        QPushButton:disabled {
            background-color: #353535;
            color: #666666;
        }
        QLineEdit {
            background-color: #404040;
            border: 1px solid #555555;
            border-radius: 3px;
            padding: 4px;
            color: #e0e0e0;
        }
        QLineEdit:focus {
            border: 2px solid #64b5f6;
        }
        QTextEdit {
            background-color: #404040;
            border: 1px solid #555555;
            border-radius: 3px;
            color: #e0e0e0;
        }
        QTreeWidget {
            background-color: #404040;
            border: 1px solid #555555;
            border-radius: 3px;
            alternate-background-color: #353535;
        }
        QTreeWidget::item {
            padding: 4px;
        }
        QTreeWidget::item:selected {
            background-color: #1976d2;
            color: white;
        }
        QHeaderView::section {
            background-color: #505050;
            color: #e0e0e0;
            border: 1px solid #555555;
            padding: 6px;
            font-weight: bold;
        }
        QHeaderView::section:hover {
            background-color: #606060;
        }
        QScrollBar:horizontal {
            background-color: #404040;
            border: 1px solid #555555;
            height: 16px;
        }
        QScrollBar::handle:horizontal {
            background-color: #707070;
            border-radius: 8px;
            min-width: 30px;
        }
        QScrollBar::handle:horizontal:hover {
            background-color: #808080;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            background-color: #404040;
            border: none;
            width: 0px;
        }
        QScrollBar:vertical {
            background-color: #404040;
            border: 1px solid #555555;
            width: 16px;
        }
        QScrollBar::handle:vertical {
            background-color: #707070;
            border-radius: 8px;
            min-height: 30px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #808080;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background-color: #404040;
            border: none;
            height: 0px;
        }
        QProgressBar {
            border: 1px solid #555555;
            border-radius: 3px;
            text-align: center;
            background-color: #404040;
        }
        QProgressBar::chunk {
            background-color: #4caf50;
            border-radius: 2px;
        }
        QStatusBar {
            background-color: #404040;
            border-top: 1px solid #555555;
        }
        QMenuBar {
            background-color: #2d2d2d;
            border-bottom: 1px solid #555555;
        }
        QMenuBar::item {
            background-color: transparent;
            padding: 4px 8px;
        }
        QMenuBar::item:selected {
            background-color: #404040;
        }
        QMenu {
            background-color: #404040;
            border: 1px solid #555555;
        }
        QMenu::item {
            padding: 6px 20px;
        }
        QMenu::item:selected {
            background-color: #1976d2;
        }
        QCheckBox {
            color: #e0e0e0;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
        }
        QCheckBox::indicator:unchecked {
            border: 2px solid #555555;
            background-color: #404040;
        }
        QCheckBox::indicator:checked {
            border: 2px solid #64b5f6;
            background-color: #1976d2;
        }
        QLabel {
            color: #e0e0e0;
        }
        QGroupBox {
            font-weight: bold;
            border: 1px solid #555555;
            border-radius: 4px;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        """

class ScanWorker(QThread):
    scan_progress = pyqtSignal(str)
    scan_complete = pyqtSignal(dict)
    scan_error = pyqtSignal(str)

    def __init__(self, folder_path=None, file_paths=None):
        super().__init__()
        self.folder_path = folder_path
        self.file_paths = file_paths

    def run(self):
        try:
            self.scan_progress.emit("Scanning for multi-disc games...")
            if self.file_paths:
                games = self.find_multidisc_games_from_files(self.file_paths)
            else:
                games = self.find_multidisc_games(self.folder_path)
            self.scan_complete.emit(games)
        except Exception as e:
            self.scan_error.emit(f"Error scanning games: {str(e)}")

    def find_multidisc_games_from_files(self, file_paths):
        games = {}
        disc_pattern = re.compile(
            r'(?i)(?P<basename>.*?)'  # Everything before the disc pattern (non-greedy)
            r'[\s\-_]*[\(\[]*'
            r'(disc|cd|disk|diskette)[\s\-_]*'
            r'(?P<discnum>\d+)'
            r'[\s\-_]*[\)\]]*'
            r'(?:[^\w\d]|$)'
        )
        for file_path in file_paths:
            filename = os.path.basename(file_path)
            match = disc_pattern.search(filename)
            if match:
                base_name = match.group('basename').strip(' -_')
                if not base_name:
                    base_name = filename
                if base_name not in games:
                    games[base_name] = []
                games[base_name].append((filename, Path(file_path)))
        for game_name in games:
            games[game_name].sort(key=lambda x: self.extract_disc_number(x[0]))
        return games

    def extract_disc_number(self, filename):
        match = re.search(r'(?i)(disc|cd|disk|diskette)[\s\-_]*([0-9]+)', filename)
        if match:
            return int(match.group(2))
        return 0

    def find_multidisc_games(self, folder):
        games = {}
        # Improved pattern: supports disc pattern anywhere in the filename, with region tags or other info after
        disc_pattern = re.compile(
            r'(?i)(?P<basename>.*?)'  # Everything before the disc pattern (non-greedy)
            r'[\s\-_]*[\(\[]*'
            r'(disc|cd|disk|diskette)[\s\-_]*'
            r'(?P<discnum>\d+)'
            r'[\s\-_]*[\)\]]*'
            r'(?:[^\w\d]|$)'
        )
        for file_path in Path(folder).rglob('*'):
            if file_path.is_file():
                filename = file_path.name
                match = disc_pattern.search(filename)
                if match:
                    base_name = match.group('basename').strip(' -_')
                    if not base_name:
                        base_name = filename  # fallback
                    # Include relative subfolder path in key to preserve folder structure
                    rel_parent = file_path.parent.relative_to(folder)
                    if str(rel_parent) != '.':
                        game_key = f"{rel_parent.as_posix()}/{base_name}"
                    else:
                        game_key = base_name
                    if game_key not in games:
                        games[game_key] = []
                    games[game_key].append((filename, file_path))
        for game_name in games:
            games[game_name].sort(key=lambda x: self.extract_disc_number(x[0]))
        return games

class GenerateWorker(QThread):
    progress_updated = pyqtSignal(str)
    generation_complete = pyqtSignal(list, int)
    generation_error = pyqtSignal(str)

    def __init__(self, games, selected_games, roms_folder):
        super().__init__()
        self.games = games
        self.selected_games = selected_games
        self.roms_folder = roms_folder

    def run(self):
        try:
            created_folders = []
            moved_files = []
            
            for game_name in self.selected_games:
                if game_name in self.games:
                    discs = self.games[game_name]
                    self.progress_updated.emit(f"Processing {game_name}...")
                    
                    # Extract the base game name and subfolder path
                    if '/' in game_name:
                        subfolder_path, base_game_name = game_name.rsplit('/', 1)
                        target_folder = self.roms_folder / subfolder_path
                        folder_name = f"{base_game_name}.m3u"
                        game_folder = target_folder / folder_name
                    else:
                        # Game is in the root folder
                        base_game_name = game_name
                        target_folder = self.roms_folder
                        folder_name = f"{base_game_name}.m3u"
                        game_folder = target_folder / folder_name
                    
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
            
            self.generation_complete.emit(created_folders, len(moved_files))
            
        except Exception as e:
            self.generation_error.emit(f"Error processing games: {str(e)}")

class ESDE_M3UGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ES-DE Multi-Disc M3U Generator")
        self.setGeometry(100, 100, 1000, 800)
        self.setMinimumSize(900, 750)
        self.setAcceptDrops(True)
        
        # Variables
        self.roms_folder_path = ""
        self.games_found = {}
        self.selected_games = set()
        
        # Theme management
        self.current_theme = 'dark'  # Default to dark theme
        
        self.init_ui()
        self.setup_menu_bar()
        self.apply_theme(self.current_theme)

    def setup_menu_bar(self):
        """Setup the menu bar with theme switching options"""
        menubar = self.menuBar()
        
        # View menu
        view_menu = menubar.addMenu('View')
        
        # Theme submenu
        theme_menu = view_menu.addMenu('Theme')
        
        # Light theme action
        light_action = QAction('Light Theme', self)
        light_action.setCheckable(True)
        light_action.setChecked(self.current_theme == 'light')
        light_action.triggered.connect(lambda: self.switch_theme('light'))
        theme_menu.addAction(light_action)
        
        # Dark theme action
        dark_action = QAction('Dark Theme', self)
        dark_action.setCheckable(True)
        dark_action.setChecked(self.current_theme == 'dark')
        dark_action.triggered.connect(lambda: self.switch_theme('dark'))
        theme_menu.addAction(dark_action)
        
        # Store actions for later use
        self.light_theme_action = light_action
        self.dark_theme_action = dark_action

    def switch_theme(self, theme):
        """Switch between light and dark themes"""
        if theme != self.current_theme:
            self.current_theme = theme
            self.apply_theme(theme)
            
            # Update menu checkmarks
            if hasattr(self, 'light_theme_action'):
                self.light_theme_action.setChecked(theme == 'light')
            if hasattr(self, 'dark_theme_action'):
                self.dark_theme_action.setChecked(theme == 'dark')

    def apply_theme(self, theme):
        """Apply the specified theme to the application"""
        if theme == 'dark':
            self.setStyleSheet(ThemeManager.get_dark_theme())
        else:
            self.setStyleSheet(ThemeManager.get_light_theme())

    def init_ui(self):
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("ES-DE Multi-Disc M3U Generator")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        main_layout.addWidget(title_label)
        
        # Description
        desc_text = """This tool creates ES-DE compatible multi-disc game folders.

For each multi-disc game, it will:
• Create a folder named 'Game Name.m3u'
• Move all disc files into that folder
• Create an M3U file inside the folder listing the discs

This allows ES-DE to show only one entry per game while supporting disc switching."""
        
        desc_label = QLabel(desc_text)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("margin-bottom: 15px;")
        main_layout.addWidget(desc_label)
        
        # Folder selection group
        folder_group = QGroupBox("Folder Selection")
        folder_layout = QVBoxLayout(folder_group)
        
        folder_frame = QHBoxLayout()
        self.folder_edit = QLineEdit()
        self.folder_edit.setPlaceholderText("Select your games folder...")
        folder_frame.addWidget(self.folder_edit)
        
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_folder)
        folder_frame.addWidget(browse_btn)
        
        folder_layout.addLayout(folder_frame)
        main_layout.addWidget(folder_group)
        
        # Scan button
        self.scan_btn = QPushButton("Scan for Multi-Disc Games")
        self.scan_btn.clicked.connect(self.scan_games)
        self.scan_btn.setStyleSheet("font-size: 14px; padding: 10px;")
        main_layout.addWidget(self.scan_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Results group
        results_group = QGroupBox("Multi-Disc Games Found")
        results_layout = QVBoxLayout(results_group)
        
        # Selection buttons
        selection_frame = QHBoxLayout()
        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.clicked.connect(self.select_all_games)
        self.select_all_btn.setEnabled(False)
        selection_frame.addWidget(self.select_all_btn)
        
        self.select_none_btn = QPushButton("Select None")
        self.select_none_btn.clicked.connect(self.select_none_games)
        self.select_none_btn.setEnabled(False)
        selection_frame.addWidget(self.select_none_btn)
        
        results_layout.addLayout(selection_frame)
        
        # Tree widget for games
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Selected", "Game Name", "Discs", "Folder Name"])
        self.tree_widget.setAlternatingRowColors(True)
        self.tree_widget.itemClicked.connect(self.on_tree_item_clicked)
        
        # Set column widths and resizing modes
        header = self.tree_widget.header()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Interactive)  # Allow horizontal scroll
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.setSectionResizeMode(3, QHeaderView.Interactive)  # Allow horizontal scroll
        self.tree_widget.setColumnWidth(0, 100)  # Wider for "Selected" title
        self.tree_widget.setColumnWidth(2, 60)
        self.tree_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tree_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # (No setMaximumWidth)
        results_layout.addWidget(self.tree_widget)
        main_layout.addWidget(results_group)
        
        # Generate button
        self.generate_btn = QPushButton("Create ES-DE Multi-Disc Folders")
        self.generate_btn.clicked.connect(self.generate_esde_folders)
        self.generate_btn.setEnabled(False)
        self.generate_btn.setStyleSheet("font-size: 14px; padding: 10px;")
        main_layout.addWidget(self.generate_btn)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready to scan")

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Games Folder")
        if folder:
            self.folder_edit.setText(folder)
            self.roms_folder_path = folder

    def scan_games(self, file_paths=None):
        if not file_paths and not self.folder_edit.text():
            self.status_bar.showMessage("Please select a games folder first!")
            return
        self.roms_folder_path = self.folder_edit.text() if not file_paths else None
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.status_bar.showMessage("Scanning for multi-disc games...")
        self.scan_btn.setEnabled(False)
        self.generate_btn.setEnabled(False)
        self.select_all_btn.setEnabled(False)
        self.select_none_btn.setEnabled(False)
        # Start scanning in background
        if file_paths:
            self.scan_worker = ScanWorker(None, file_paths)
        else:
            self.scan_worker = ScanWorker(self.roms_folder_path)
        self.scan_worker.scan_progress.connect(self.update_scan_progress)
        self.scan_worker.scan_complete.connect(self.scan_completed)
        self.scan_worker.scan_error.connect(self.scan_error)
        self.scan_worker.start()

    def update_scan_progress(self, message):
        self.status_bar.showMessage(message)

    def scan_completed(self, games):
        self.games_found = games
        self.progress_bar.setVisible(False)
        self.scan_btn.setEnabled(True)
        
        if games:
            self.populate_tree_widget(games)
            self.select_all_btn.setEnabled(True)
            self.select_none_btn.setEnabled(True)
            self.generate_btn.setEnabled(True)
            self.status_bar.showMessage(f"Found {len(games)} multi-disc game(s) - Select which ones to process")
        else:
            self.status_bar.showMessage("No multi-disc games found")

    def scan_error(self, error_msg):
        self.progress_bar.setVisible(False)
        self.scan_btn.setEnabled(True)
        self.status_bar.showMessage(f"Error: {error_msg}")

    def populate_tree_widget(self, games):
        self.tree_widget.clear()
        self.selected_games.clear()
        
        for game_name, discs in games.items():
            # Extract display name and folder name
            if '/' in game_name:
                subfolder_path, base_game_name = game_name.rsplit('/', 1)
                display_name = f"{base_game_name} (in {subfolder_path})"
                folder_name = f"{subfolder_path}/{base_game_name}.m3u"
            else:
                display_name = game_name
                folder_name = f"{game_name}.m3u"
            
            item = QTreeWidgetItem()
            item.setText(0, "☐")  # Unchecked checkbox
            item.setText(1, display_name)
            item.setText(2, str(len(discs)))
            item.setText(3, folder_name)
            item.setData(0, Qt.UserRole, game_name)  # Store original game name
            
            self.tree_widget.addTopLevelItem(item)
        
        # Select all by default
        self.select_all_games()

        # Force columns to be wide to trigger horizontal scroll bar
        self.tree_widget.setColumnWidth(1, 600)  # Game Name
        self.tree_widget.setColumnWidth(3, 800)  # Folder Name

    def on_tree_item_clicked(self, item, column):
        if column == 0:  # Checkbox column
            game_name = item.data(0, Qt.UserRole)
            if item.text(0) == "☐":
                item.setText(0, "☑")
                self.selected_games.add(game_name)
            else:
                item.setText(0, "☐")
                self.selected_games.discard(game_name)

    def select_all_games(self):
        for i in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(i)
            item.setText(0, "☑")
            game_name = item.data(0, Qt.UserRole)
            self.selected_games.add(game_name)

    def select_none_games(self):
        for i in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(i)
            item.setText(0, "☐")
            game_name = item.data(0, Qt.UserRole)
            self.selected_games.discard(game_name)

    def generate_esde_folders(self):
        if not self.selected_games:
            self.status_bar.showMessage("Please select at least one game to process!")
            return
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.status_bar.showMessage("Creating ES-DE multi-disc folders...")
        
        # Disable buttons during generation
        self.generate_btn.setEnabled(False)
        self.scan_btn.setEnabled(False)
        
        # Start generation in background
        self.generate_worker = GenerateWorker(self.games_found, self.selected_games, Path(self.roms_folder_path))
        self.generate_worker.progress_updated.connect(self.update_generation_progress)
        self.generate_worker.generation_complete.connect(self.generation_completed)
        self.generate_worker.generation_error.connect(self.generation_error)
        self.generate_worker.start()

    def update_generation_progress(self, message):
        self.status_bar.showMessage(message)

    def generation_completed(self, created_folders, moved_files_count):
        self.progress_bar.setVisible(False)
        self.generate_btn.setEnabled(True)
        self.scan_btn.setEnabled(True)
        
        message = f"Successfully created {len(created_folders)} ES-DE multi-disc folder(s) and moved {moved_files_count} disc file(s)"
        self.status_bar.showMessage(message)

    def generation_error(self, error_msg):
        self.progress_bar.setVisible(False)
        self.generate_btn.setEnabled(True)
        self.scan_btn.setEnabled(True)
        self.status_bar.showMessage(f"Error: {error_msg}")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        paths = [url.toLocalFile() for url in event.mimeData().urls()]
        if not paths:
            return
        if any(os.path.isdir(path) for path in paths):
            # If any folder is dropped, use the first folder
            folder = next(path for path in paths if os.path.isdir(path))
            self.folder_edit.setText(folder)
            self.roms_folder_path = folder
            self.status_bar.showMessage(f"Dropped folder: {os.path.basename(folder)} - Scanning...")
            self.scan_games()
        else:
            # Only files dropped: process only those files
            self.folder_edit.setText("")  # Clear folder field so scan_games doesn't use it
            self.roms_folder_path = None
            self.status_bar.showMessage(f"Dropped {len(paths)} file(s) - Scanning...")
            self.scan_games(file_paths=paths)

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("ES-DE Multi-Disc M3U Generator")
    
    window = ESDE_M3UGenerator()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 