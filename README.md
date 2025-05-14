# MS SQL Server Database Manager

A GUI application for managing MS SQL Server databases, built with Python and CustomTkinter.

## Features

- Connect to MS SQL Server databases
- Create new databases
- Create and manage tables
- Insert data into tables
- View and query data
- Execute custom SQL queries
- User-friendly interface 
- Multi-language support (English and Turkish)
- Theme support (Light, Dark, and System)

## Requirements

- Windows OS
- Python 3.7 or higher
- MS SQL Server (Express edition is supported)
- ODBC Driver 17 for SQL Server
- Make sure that TCP/IP and Named Pipes are enabled in the Configuration Manager
- SQL Server (SQLEXPRESS) service should be running.


## Installation

1. Clone the repository:
```bash
git clone https://github.com/utku9012/ms_sql_database_manager.git
cd ms-sql-database-manager
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure you have ODBC Driver 17 for SQL Server installed on your system.

## Usage

1. Run the application:
```bash
python database_gui.py
```

2. In the Connection tab:
   - Enter your server name (e.g., DESKTOP-NC4C7PD\SQLEXPRESS)
   - Enter the database name
   - Click "Connect" to connect to an existing database
   - Or click "Create Database" to create a new one

3. Use the different tabs to:
   - Manage tables (create, delete)
   - Insert data
   - View and query data
   - Customize settings

## Features in Detail

### Connection Management
- Connect to existing databases
- Create new databases
- Disconnect from current database

### Table Management
- Create new tables with custom columns
- Define primary keys and constraints
- Delete existing tables
- View list of all tables

### Data Management
- Insert data into tables
- View table contents
- Execute custom SQL queries
- Real-time data display

### Settings
- Choose between Light, Dark, or System theme
- Switch between English and Turkish languages
- Settings are saved between sessions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern UI components
- [pyodbc](https://github.com/mkleehammer/pyodbc) for database connectivity 
