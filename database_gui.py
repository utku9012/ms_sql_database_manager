import pyodbc 
import customtkinter as ctk
from tkinter import messagebox, ttk
import json
import os

class DatabaseGUI:
    def __init__(self):
        # Load settings
        self.load_settings()
        
        # Set theme
        ctk.set_appearance_mode(self.settings.get("theme", "system"))
        ctk.set_default_color_theme("blue")
        
        self.app = ctk.CTk()
        self.app.geometry("800x600")
        self.app.title("MS SQL Server Database Manager")
        
        # Create Tabview
        self.tabview = ctk.CTkTabview(self.app)
        self.tabview.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Create tabs
        self.tab_connection = self.tabview.add("Connection")
        self.tab_tables = self.tabview.add("Table Management")
        self.tab_insert = self.tabview.add("Insert Data")
        self.tab_view = self.tabview.add("View Data")
        self.tab_settings = self.tabview.add("Settings")
        
        # Connection Tab
        self.setup_connection_tab()
        
        # Table Management Tab
        self.setup_table_tab()
        
        # Insert Data Tab
        self.setup_insert_tab()
        
        # View Data Tab
        self.setup_view_tab()
        
        # Settings Tab
        self.setup_settings_tab()
        
        self.connection = None
    
    def load_settings(self):
        self.settings_file = "settings.json"
        default_settings = {
            "theme": "system",
            "language": "en"
        }
        
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    self.settings = json.load(f)
            except:
                self.settings = default_settings
        else:
            self.settings = default_settings
            self.save_settings()

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def setup_connection_tab(self):
        # Main Frame
        self.main_frame = ctk.CTkFrame(self.tab_connection)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Server Entry
        self.server_label = ctk.CTkLabel(self.main_frame, text="Server Name:")
        self.server_label.pack(pady=(20,5))
        self.server_entry = ctk.CTkEntry(self.main_frame, width=300, placeholder_text="Enter server name (e.g., DESKTOP-NC4C7PD\\SQLEXPRESS)")
        self.server_entry.pack(pady=(0,10))
        self.server_entry.insert(0, "DESKTOP-NC4C7PD\\SQLEXPRESS")
        
        # Database Entry
        self.db_label = ctk.CTkLabel(self.main_frame, text="Database Name:")
        self.db_label.pack(pady=(10,5))
        self.db_entry = ctk.CTkEntry(self.main_frame, width=300, placeholder_text="Enter database name")
        self.db_entry.pack(pady=(0,10))
        
        # Buttons Frame
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(pady=20)
        
        # Connect Button
        self.connect_btn = ctk.CTkButton(
            self.button_frame, 
            text="Connect", 
            command=self.connect_db,
            width=120,
            fg_color="#2E7D32"
        )
        self.connect_btn.pack(side="left", padx=10)
        
        # Create DB Button
        self.create_btn = ctk.CTkButton(
            self.button_frame, 
            text="Create Database", 
            command=self.create_db,
            width=120,
            fg_color="#1976D2"
        )
        self.create_btn.pack(side="left", padx=10)

        # Disconnect Button
        self.disconnect_btn = ctk.CTkButton(
            self.button_frame,
            text="Disconnect",
            command=self.disconnect_db,
            width=120,
            fg_color="#D32F2F"
        )
        self.disconnect_btn.pack(side="left", padx=10)
        
        # Status Label
        self.status_label = ctk.CTkLabel(
            self.main_frame, 
            text="Status: Not Connected",
            text_color="#D32F2F"
        )
        self.status_label.pack(pady=20)

    def setup_table_tab(self):
        # Main Frame for Table Management
        self.table_frame = ctk.CTkFrame(self.tab_tables)
        self.table_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Table Name Entry
        self.table_name_label = ctk.CTkLabel(self.table_frame, text="Table Name:")
        self.table_name_label.pack(pady=(20,5))
        self.table_name_entry = ctk.CTkEntry(self.table_frame, width=300, placeholder_text="Enter table name")
        self.table_name_entry.pack(pady=(0,10))
        
        # Columns Frame
        self.columns_frame = ctk.CTkFrame(self.table_frame)
        self.columns_frame.pack(pady=10, fill="x")
        
        # Column List
        self.column_list = []
        self.add_column_fields()
        
        # Add Column Button
        self.add_column_btn = ctk.CTkButton(
            self.table_frame,
            text="Add Column",
            command=self.add_column_fields,
            width=120,
            fg_color="#1976D2"
        )
        self.add_column_btn.pack(pady=10)
        
        # Table Management Buttons
        self.table_buttons_frame = ctk.CTkFrame(self.table_frame)
        self.table_buttons_frame.pack(pady=10)
        
        # Create Table Button
        self.create_table_btn = ctk.CTkButton(
            self.table_buttons_frame,
            text="Create Table",
            command=self.create_table,
            width=120,
            fg_color="#2E7D32"
        )
        self.create_table_btn.pack(side="left", padx=10)
        
        # Delete Table Button
        self.delete_table_btn = ctk.CTkButton(
            self.table_buttons_frame,
            text="Delete Table",
            command=self.delete_table,
            width=120,
            fg_color="#D32F2F"
        )
        self.delete_table_btn.pack(side="left", padx=10)
        
        # Existing Tables List
        self.tables_label = ctk.CTkLabel(self.table_frame, text="Existing Tables:")
        self.tables_label.pack(pady=(20,5))
        
        self.tables_listbox = ctk.CTkTextbox(self.table_frame, height=100)
        self.tables_listbox.pack(pady=10, fill="x")
        
        # Refresh Tables Button
        self.refresh_tables_btn = ctk.CTkButton(
            self.table_frame,
            text="Refresh Tables List",
            command=self.refresh_tables_list,
            width=120,
            fg_color="#1976D2"
        )
        self.refresh_tables_btn.pack(pady=10)

    def add_column_fields(self):
        column_frame = ctk.CTkFrame(self.columns_frame)
        column_frame.pack(pady=5, fill="x")
        
        # Column Name
        name_entry = ctk.CTkEntry(column_frame, placeholder_text="Column Name", width=150)
        name_entry.pack(side="left", padx=5)
        
        # Data Type
        data_type = ctk.CTkComboBox(column_frame, values=[
            "INT", "VARCHAR(50)", "VARCHAR(100)", "VARCHAR(255)",
            "DATETIME", "DECIMAL(10,2)", "BIT", "TEXT"
        ], width=150)
        data_type.pack(side="left", padx=5)
        
        # Primary Key Checkbox
        is_primary = ctk.CTkCheckBox(column_frame, text="Primary Key")
        is_primary.pack(side="left", padx=5)
        
        # Not Null Checkbox
        not_null = ctk.CTkCheckBox(column_frame, text="Not Null")
        not_null.pack(side="left", padx=5)
        
        # Remove Button
        remove_btn = ctk.CTkButton(
            column_frame,
            text="Remove",
            command=lambda: self.remove_column(column_frame),
            width=80,
            fg_color="#D32F2F"
        )
        remove_btn.pack(side="right", padx=5)
        
        self.column_list.append({
            "frame": column_frame,
            "name": name_entry,
            "type": data_type,
            "primary": is_primary,
            "not_null": not_null
        })

    def remove_column(self, column_frame):
        for column in self.column_list:
            if column["frame"] == column_frame:
                column_frame.destroy()
                self.column_list.remove(column)
                break

    def create_table(self):
        if not self.connection:
            messagebox.showerror("Error", "Please connect to database first!")
            return
            
        table_name = self.table_name_entry.get().strip()
        if not table_name:
            messagebox.showerror("Error", "Please enter table name!")
            return
            
        if not self.column_list:
            messagebox.showerror("Error", "Please add at least one column!")
            return
            
        try:
            # Build CREATE TABLE query
            columns = []
            for column in self.column_list:
                name = column["name"].get().strip()
                data_type = column["type"].get()
                is_primary = column["primary"].get()
                not_null = column["not_null"].get()
                
                if not name:
                    messagebox.showerror("Error", "All columns must have names!")
                    return
                    
                column_def = f"[{name}] {data_type}"
                if is_primary:
                    column_def += " PRIMARY KEY"
                if not_null:
                    column_def += " NOT NULL"
                    
                columns.append(column_def)
            
            query = f"CREATE TABLE [{table_name}] (\n    " + ",\n    ".join(columns) + "\n)"
            
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            
            messagebox.showinfo("Success", f"Table {table_name} created successfully!")
            self.refresh_tables_list()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create table: {str(e)}")

    def delete_table(self):
        if not self.connection:
            messagebox.showerror("Error", "Please connect to database first!")
            return
            
        table_name = self.table_name_entry.get().strip()
        if not table_name:
            messagebox.showerror("Error", "Please enter table name!")
            return
            
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete table {table_name}?"):
            try:
                cursor = self.connection.cursor()
                cursor.execute(f"DROP TABLE [{table_name}]")
                self.connection.commit()
                
                messagebox.showinfo("Success", f"Table {table_name} deleted successfully!")
                self.refresh_tables_list()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete table: {str(e)}")

    def refresh_tables_list(self):
        if not self.connection:
            messagebox.showerror("Error", "Please connect to database first!")
            return
            
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_NAME
            """)
            
            tables = cursor.fetchall()
            self.tables_listbox.delete("1.0", "end")
            for table in tables:
                self.tables_listbox.insert("end", f"{table[0]}\n")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh tables list: {str(e)}")

    def connect_db(self):
        server = self.server_entry.get().strip()
        database = self.db_entry.get().strip()
        
        if not server or not database:
            messagebox.showerror("Error", "Please enter both server and database names!")
            return
            
        try:
            conn_str = (
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={server};'
                f'DATABASE={database};'
                'Trusted_Connection=yes'
            )
            self.connection = pyodbc.connect(conn_str)
            self.status_label.configure(
                text="Status: Connected Successfully",
                text_color="#2E7D32"
            )
            messagebox.showinfo("Success", f"Successfully connected to {database} on {server}!")
            self.refresh_tables_list()
        except Exception as e:
            self.status_label.configure(
                text="Status: Connection Failed",
                text_color="#D32F2F"
            )
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
    
    def create_db(self):
        server = self.server_entry.get().strip()
        database = self.db_entry.get().strip()
        
        if not server or not database:
            messagebox.showerror("Error", "Please enter both server and database names!")
            return
            
        try:
            conn_str = (
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={server};'
                f'DATABASE=master;'
                'Trusted_Connection=yes'
            )
            conn = pyodbc.connect(conn_str)
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(f'CREATE DATABASE [{database}]')
            self.status_label.configure(
                text=f"Status: Database {database} Created",
                text_color="#2E7D32"
            )
            messagebox.showinfo("Success", f"Database {database} created successfully!")
        except Exception as e:
            self.status_label.configure(
                text="Status: Creation Failed",
                text_color="#D32F2F"
            )
            messagebox.showerror("Creation Error", f"Failed to create database: {str(e)}")
    
    def setup_insert_tab(self):
        # Main Frame for Insert Data
        self.insert_frame = ctk.CTkFrame(self.tab_insert)
        self.insert_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Table Selection
        self.table_select_label = ctk.CTkLabel(self.insert_frame, text="Select Table:")
        self.table_select_label.pack(pady=(20,5))
        
        self.table_select_frame = ctk.CTkFrame(self.insert_frame)
        self.table_select_frame.pack(fill="x", pady=(0,10))
        
        self.table_combo = ctk.CTkComboBox(self.table_select_frame, width=200)
        self.table_combo.pack(side="left", padx=5)
        
        self.refresh_tables_combo_btn = ctk.CTkButton(
            self.table_select_frame,
            text="Refresh",
            command=self.refresh_tables_combo,
            width=100
        )
        self.refresh_tables_combo_btn.pack(side="left", padx=5)
        
        # Create a frame for the scrollable area
        self.scrollable_frame = ctk.CTkScrollableFrame(self.insert_frame, height=300)
        self.scrollable_frame.pack(fill="both", expand=True, pady=10)
        
        # Data Entry Frame (now inside scrollable frame)
        self.data_entry_frame = ctk.CTkFrame(self.scrollable_frame)
        self.data_entry_frame.pack(fill="both", expand=True)
        
        # Column entries will be added here dynamically
        self.column_entries = {}
        
        # Insert Button
        self.insert_btn = ctk.CTkButton(
            self.insert_frame,
            text="Insert Data",
            command=self.insert_data,
            width=120,
            fg_color="#2E7D32"
        )
        self.insert_btn.pack(pady=10)
        
        # Bind table selection change
        self.table_combo.configure(command=self.on_table_selected)

    def refresh_tables_combo(self):
        if not self.connection:
            messagebox.showerror("Error", "Please connect to database first!")
            return
            
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_NAME
            """)
            
            tables = [table[0] for table in cursor.fetchall()]
            self.table_combo.configure(values=tables)
            if tables:
                self.table_combo.set(tables[0])
                self.on_table_selected(tables[0])
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh tables list: {str(e)}")

    def on_table_selected(self, table_name):
        if not table_name:
            return
            
        # Clear previous entries
        for widget in self.data_entry_frame.winfo_children():
            widget.destroy()
        self.column_entries.clear()
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""
                SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table_name}'
                ORDER BY ORDINAL_POSITION
            """)
            
            columns = cursor.fetchall()
            
            for column in columns:
                col_name, data_type, is_nullable = column
                
                # Create frame for each column
                col_frame = ctk.CTkFrame(self.data_entry_frame)
                col_frame.pack(fill="x", pady=5)
                
                # Column name label
                label = ctk.CTkLabel(col_frame, text=f"{col_name} ({data_type}):")
                label.pack(side="left", padx=5)
                
                # Create appropriate input widget based on data type
                if data_type in ('int', 'bigint', 'smallint', 'tinyint'):
                    entry = ctk.CTkEntry(col_frame, placeholder_text="Enter number")
                elif data_type in ('decimal', 'numeric', 'float', 'real'):
                    entry = ctk.CTkEntry(col_frame, placeholder_text="Enter decimal number")
                elif data_type == 'bit':
                    entry = ctk.CTkCheckBox(col_frame, text="")
                elif data_type == 'datetime':
                    entry = ctk.CTkEntry(col_frame, placeholder_text="YYYY-MM-DD HH:MM:SS")
                else:
                    entry = ctk.CTkEntry(col_frame, placeholder_text=f"Enter {data_type}")
                
                entry.pack(side="left", padx=5, fill="x", expand=True)
                
                # Add to column entries dictionary
                self.column_entries[col_name] = {
                    'widget': entry,
                    'type': data_type
                }
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load table structure: {str(e)}")

    def insert_data(self):
        if not self.connection:
            messagebox.showerror("Error", "Please connect to database first!")
            return
            
        table_name = self.table_combo.get()
        if not table_name:
            messagebox.showerror("Error", "Please select a table!")
            return
            
        try:
            # Build column names and values
            columns = []
            values = []
            params = []
            
            for col_name, col_info in self.column_entries.items():
                widget = col_info['widget']
                data_type = col_info['type']
                
                if isinstance(widget, ctk.CTkEntry):
                    value = widget.get().strip()
                    if value:  # Only include non-empty values
                        columns.append(f"[{col_name}]")
                        if data_type in ('int', 'bigint', 'smallint', 'tinyint'):
                            values.append("?")
                            params.append(int(value))
                        elif data_type in ('decimal', 'numeric', 'float', 'real'):
                            values.append("?")
                            params.append(float(value))
                        elif data_type == 'datetime':
                            values.append("?")
                            params.append(value)
                        else:
                            values.append("?")
                            params.append(value)
                elif isinstance(widget, ctk.CTkCheckBox):
                    columns.append(f"[{col_name}]")
                    values.append("?")
                    params.append(1 if widget.get() else 0)
            
            if not columns:
                messagebox.showerror("Error", "Please enter at least one value!")
                return
            
            # Build and execute INSERT query
            query = f"INSERT INTO [{table_name}] ({', '.join(columns)}) VALUES ({', '.join(values)})"
            
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            
            messagebox.showinfo("Success", "Data inserted successfully!")
            
            # Clear all entries
            for col_info in self.column_entries.values():
                widget = col_info['widget']
                if isinstance(widget, ctk.CTkEntry):
                    widget.delete(0, "end")
                elif isinstance(widget, ctk.CTkCheckBox):
                    widget.deselect()
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to insert data: {str(e)}")

    def disconnect_db(self):
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
                self.status_label.configure(
                    text="Status: Disconnected",
                    text_color="#D32F2F"
                )
                messagebox.showinfo("Success", "Successfully disconnected from database!")
                
                # Clear table combo box
                self.table_combo.configure(values=[])
                self.table_combo.set("")
                
                # Clear data entry frame
                for widget in self.data_entry_frame.winfo_children():
                    widget.destroy()
                self.column_entries.clear()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error while disconnecting: {str(e)}")
        else:
            messagebox.showinfo("Info", "Not connected to any database.")

    def setup_settings_tab(self):
        # Main Frame for Settings
        self.settings_frame = ctk.CTkFrame(self.tab_settings)
        self.settings_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Theme Selection
        self.theme_label = ctk.CTkLabel(self.settings_frame, text="Theme:")
        self.theme_label.pack(pady=(20,5))
        
        self.theme_combo = ctk.CTkComboBox(
            self.settings_frame,
            values=["System", "Light", "Dark"],
            width=200,
            command=self.change_theme
        )
        self.theme_combo.pack(pady=(0,20))
        self.theme_combo.set(self.settings.get("theme", "system").capitalize())
        
        # Language Selection
        self.language_label = ctk.CTkLabel(self.settings_frame, text="Language:")
        self.language_label.pack(pady=(20,5))
        
        self.language_combo = ctk.CTkComboBox(
            self.settings_frame,
            values=["English", "Türkçe"],
            width=200,
            command=self.change_language
        )
        self.language_combo.pack(pady=(0,20))
        self.language_combo.set("English" if self.settings.get("language", "en") == "en" else "Türkçe")
        
        # Save Button
        self.save_settings_btn = ctk.CTkButton(
            self.settings_frame,
            text="Save Settings",
            command=self.save_settings,
            width=120,
            fg_color="#2E7D32"
        )
        self.save_settings_btn.pack(pady=20)
        
        # Restart Required Label
        self.restart_label = ctk.CTkLabel(
            self.settings_frame,
            text="Note: Some changes may require restarting the application",
            text_color="gray"
        )
        self.restart_label.pack(pady=10)

    def change_theme(self, choice):
        theme = choice.lower()
        ctk.set_appearance_mode(theme)
        self.settings["theme"] = theme
        self.save_settings()

    def change_language(self, choice):
        lang = "en" if choice == "English" else "tr"
        self.settings["language"] = lang
        self.save_settings()
        self.update_language()

    def update_language(self):
        # Update all text elements based on selected language
        lang = self.settings.get("language", "en")
        translations = {
            "en": {
                "app_title": "MS SQL Server Database Manager",
                "connection": "Connection",
                "table_management": "Table Management",
                "insert_data": "Insert Data",
                "settings": "Settings",
                "server_name": "Server Name:",
                "database_name": "Database Name:",
                "connect": "Connect",
                "create_database": "Create Database",
                "disconnect": "Disconnect",
                "status": "Status:",
                "not_connected": "Not Connected",
                "connected": "Connected Successfully",
                "disconnected": "Disconnected",
                "theme": "Theme:",
                "language": "Language:",
                "save_settings": "Save Settings",
                "restart_note": "Note: Some changes may require restarting the application",
                "edit_selected": "Edit Selected",
                "delete_selected": "Delete Selected",
                "save_changes": "Save Changes",
                "changes_saved": "Changes saved. Click 'Save Changes' to update database.",
                "row_deleted": "Row marked for deletion. Click 'Save Changes' to update database.",
                "all_changes_saved": "All changes saved successfully!",
                "no_changes": "No changes to save!",
                "view_data": "View Data",
                "select_table": "Select Table:",
                "refresh": "Refresh",
                "view_table": "View Table",
                "sql_query": "SQL Query:",
                "execute_query": "Execute Query",
                "displaying_rows": "Displaying {} rows from {}",
                "query_executed": "Query executed successfully. {} rows returned."
            },
            "tr": {
                "app_title": "MS SQL Server Veritabanı Yöneticisi",
                "connection": "Bağlantı",
                "table_management": "Tablo Yönetimi",
                "insert_data": "Veri Ekle",
                "settings": "Ayarlar",
                "server_name": "Sunucu Adı:",
                "database_name": "Veritabanı Adı:",
                "connect": "Bağlan",
                "create_database": "Veritabanı Oluştur",
                "disconnect": "Bağlantıyı Kes",
                "status": "Durum:",
                "not_connected": "Bağlı Değil",
                "connected": "Bağlantı Başarılı",
                "disconnected": "Bağlantı Kesildi",
                "theme": "Tema:",
                "language": "Dil:",
                "save_settings": "Ayarları Kaydet",
                "restart_note": "Not: Bazı değişiklikler uygulamanın yeniden başlatılmasını gerektirebilir",
                "edit_selected": "Seçileni Düzenle",
                "delete_selected": "Seçileni Sil",
                "save_changes": "Değişiklikleri Kaydet",
                "changes_saved": "Değişiklikler kaydedildi. Veritabanını güncellemek için 'Değişiklikleri Kaydet'e tıklayın.",
                "row_deleted": "Satır silinmek üzere işaretlendi. Veritabanını güncellemek için 'Değişiklikleri Kaydet'e tıklayın.",
                "all_changes_saved": "Tüm değişiklikler başarıyla kaydedildi!",
                "no_changes": "Kaydedilecek değişiklik yok!",
                "view_data": "Veri Görüntüle",
                "select_table": "Tablo Seç:",
                "refresh": "Yenile",
                "view_table": "Tabloyu Görüntüle",
                "sql_query": "SQL Sorgusu:",
                "execute_query": "Sorguyu Çalıştır",
                "displaying_rows": "{} satır {} tablosundan görüntüleniyor",
                "query_executed": "Sorgu başarıyla çalıştırıldı. {} satır döndürüldü."
            }
        }
        
        # Update window title
        self.app.title(translations[lang]["app_title"])
        
        # Update tab names
        self.tabview.set("Connection")
        self.tabview.set("Table Management")
        self.tabview.set("Insert Data")
        self.tabview.set("Settings")
        
        # Update labels and buttons
        self.server_label.configure(text=translations[lang]["server_name"])
        self.db_label.configure(text=translations[lang]["database_name"])
        self.connect_btn.configure(text=translations[lang]["connect"])
        self.create_btn.configure(text=translations[lang]["create_database"])
        self.disconnect_btn.configure(text=translations[lang]["disconnect"])
        
        # Update status label
        current_status = self.status_label.cget("text")
        if "Not Connected" in current_status:
            self.status_label.configure(text=f"{translations[lang]['status']} {translations[lang]['not_connected']}")
        elif "Connected Successfully" in current_status:
            self.status_label.configure(text=f"{translations[lang]['status']} {translations[lang]['connected']}")
        elif "Disconnected" in current_status:
            self.status_label.configure(text=f"{translations[lang]['status']} {translations[lang]['disconnected']}")
        
        # Update settings tab
        self.theme_label.configure(text=translations[lang]["theme"])
        self.language_label.configure(text=translations[lang]["language"])
        self.save_settings_btn.configure(text=translations[lang]["save_settings"])
        self.restart_label.configure(text=translations[lang]["restart_note"])
        
        # Update data management buttons
        self.edit_btn.configure(text=translations[lang]["edit_selected"])
        self.delete_btn.configure(text=translations[lang]["delete_selected"])
        self.save_changes_btn.configure(text=translations[lang]["save_changes"])

    def setup_view_tab(self):
        # Main Frame for View Data
        self.view_frame = ctk.CTkFrame(self.tab_view)
        self.view_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Top Frame for Controls
        self.view_controls_frame = ctk.CTkFrame(self.view_frame)
        self.view_controls_frame.pack(fill="x", pady=(0, 10))
        
        # Table Selection
        self.view_table_label = ctk.CTkLabel(self.view_controls_frame, text="Select Table:")
        self.view_table_label.pack(side="left", padx=5)
        
        self.view_table_combo = ctk.CTkComboBox(self.view_controls_frame, width=200)
        self.view_table_combo.pack(side="left", padx=5)
        
        self.view_refresh_btn = ctk.CTkButton(
            self.view_controls_frame,
            text="Refresh",
            command=self.refresh_view_tables,
            width=100
        )
        self.view_refresh_btn.pack(side="left", padx=5)
        
        self.view_table_btn = ctk.CTkButton(
            self.view_controls_frame,
            text="View Table",
            command=self.view_table_data,
            width=100,
            fg_color="#1976D2"
        )
        self.view_table_btn.pack(side="left", padx=5)
        
        # SQL Query Frame
        self.query_frame = ctk.CTkFrame(self.view_frame)
        self.query_frame.pack(fill="x", pady=10)
        
        self.query_label = ctk.CTkLabel(self.query_frame, text="SQL Query:")
        self.query_label.pack(anchor="w", padx=5)
        
        self.query_text = ctk.CTkTextbox(self.query_frame, height=100)
        self.query_text.pack(fill="x", padx=5, pady=5)
        
        self.execute_query_btn = ctk.CTkButton(
            self.query_frame,
            text="Execute Query",
            command=self.execute_query,
            width=120,
            fg_color="#2E7D32"
        )
        self.execute_query_btn.pack(pady=5)
        
        # Results Frame
        self.results_frame = ctk.CTkFrame(self.view_frame)
        self.results_frame.pack(fill="both", expand=True, pady=10)
        
        # Create Treeview for results
        self.results_tree = ttk.Treeview(self.results_frame)
        self.results_tree.pack(fill="both", expand=True)
        
        # Add scrollbars
        self.vsb = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.results_tree.yview)
        self.hsb = ttk.Scrollbar(self.results_frame, orient="horizontal", command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        
        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")
        
        # Status Label
        self.view_status_label = ctk.CTkLabel(
            self.view_frame,
            text="",
            text_color="gray"
        )
        self.view_status_label.pack(pady=5)

    def refresh_view_tables(self):
        if not self.connection:
            messagebox.showerror("Error", "Please connect to database first!")
            return
            
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_NAME
            """)
            
            tables = [table[0] for table in cursor.fetchall()]
            self.view_table_combo.configure(values=tables)
            if tables:
                self.view_table_combo.set(tables[0])
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh tables list: {str(e)}")

    def view_table_data(self):
        if not self.connection:
            messagebox.showerror("Error", "Please connect to database first!")
            return
            
        table_name = self.view_table_combo.get()
        if not table_name:
            messagebox.showerror("Error", "Please select a table!")
            return
            
        try:
            # Clear existing items
            self.results_tree.delete(*self.results_tree.get_children())
            
            # Get column information
            cursor = self.connection.cursor()
            cursor.execute(f"""
                SELECT COLUMN_NAME, DATA_TYPE
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table_name}'
                ORDER BY ORDINAL_POSITION
            """)
            
            columns = cursor.fetchall()
            
            # Configure treeview columns
            self.results_tree["columns"] = [col[0] for col in columns]
            self.results_tree["show"] = "headings"
            
            # Set column headings and widths
            for col in columns:
                col_name = col[0]
                self.results_tree.heading(col_name, text=col_name)
                # Adjust column width based on data type
                if col[1] in ('varchar', 'nvarchar', 'char', 'nchar', 'text', 'ntext'):
                    self.results_tree.column(col_name, width=150, minwidth=100)
                elif col[1] in ('datetime', 'date', 'time'):
                    self.results_tree.column(col_name, width=150, minwidth=120)
                elif col[1] in ('decimal', 'numeric', 'float', 'real'):
                    self.results_tree.column(col_name, width=100, minwidth=80)
                else:
                    self.results_tree.column(col_name, width=100, minwidth=80)
            
            # Fetch and display data
            cursor.execute(f"SELECT * FROM [{table_name}]")
            rows = cursor.fetchall()
            
            # Insert data into treeview
            for row in rows:
                # Convert all values to strings to ensure proper display
                row_values = [str(value) if value is not None else "" for value in row]
                self.results_tree.insert("", "end", values=row_values)
            
            # Update status label
            self.view_status_label.configure(
                text=f"Displaying {len(rows)} rows from {table_name}",
                text_color="#2E7D32"
            )
            
        except Exception as e:
            self.view_status_label.configure(
                text=f"Error: {str(e)}",
                text_color="#D32F2F"
            )
            messagebox.showerror("Error", f"Failed to view table data: {str(e)}")

    def execute_query(self):
        if not self.connection:
            messagebox.showerror("Error", "Please connect to database first!")
            return
            
        query = self.query_text.get("1.0", "end-1c").strip()
        if not query:
            messagebox.showerror("Error", "Please enter a SQL query!")
            return
            
        try:
            # Clear existing items
            self.results_tree.delete(*self.results_tree.get_children())
            
            # Execute query
            cursor = self.connection.cursor()
            cursor.execute(query)
            
            # Get column names from cursor description
            columns = [column[0] for column in cursor.description]
            
            # Configure treeview columns
            self.results_tree["columns"] = columns
            self.results_tree["show"] = "headings"
            
            for col in columns:
                self.results_tree.heading(col, text=col)
                self.results_tree.column(col, width=100)
            
            # Fetch and display results
            rows = cursor.fetchall()
            
            for row in rows:
                self.results_tree.insert("", "end", values=row)
            
            self.view_status_label.configure(
                text=f"Query executed successfully. {len(rows)} rows returned.",
                text_color="#2E7D32"
            )
            
        except Exception as e:
            self.view_status_label.configure(
                text=f"Error: {str(e)}",
                text_color="#D32F2F"
            )
            messagebox.showerror("Error", f"Failed to execute query: {str(e)}")

    def run(self):
        self.app.mainloop()

# Create and run the application
if __name__ == "__main__":
    app = DatabaseGUI()
    app.run() 