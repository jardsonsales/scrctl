default:
	pyinstaller main.spec

new:
	pyinstaller --hidden-import=tkinter --hidden-import=tkinter.filedialog --windowed --add-data "forest-light.tcl:." --add-data "forest-light:forest-light" main.py

new-spec:
	pyi-makespec main.py
