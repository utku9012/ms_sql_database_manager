import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["customtkinter", "pyodbc"],
    "excludes": [],
    "include_files": []
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="MS SQL Server Database Manager",
    version="1.0",
    description="A GUI application for managing MS SQL Server databases",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "database_gui.py",
            base=base,
            target_name="DatabaseManager.exe",
            icon=None  # You can add an icon file here
        )
    ]
) 