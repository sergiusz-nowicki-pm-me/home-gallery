PyInstaller --onefile --noconfirm dirs_rename.py
PyInstaller --onefile --noconfirm dirs.py
PyInstaller --onefile --noconfirm unzip-all.py

copy dist\* c:\tools