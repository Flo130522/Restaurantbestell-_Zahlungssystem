from cx_Freeze import setup, Executable

executables = [Executable("grundgerüst.py", base=None)]

setup(
    name="Golden Seagull OrderSystem", 
    version="1.0",
    description="Beschreibung Ihrer Anwendung",
    executables=executables,
    options={
        "build_exe": {
            "includes": ["tkinter", "pandas", "datetime"],  
            "include_files": ["speisekarte.csv"], 
        }
    }
)
