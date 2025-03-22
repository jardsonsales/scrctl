default:
	pyinstaller main.spec

new:
	pyinstaller --windowed --add-data "forest-light.tcl:." --add-data "forest-light:forest-light" main.py

new-spec:
	pyi-makespec main.py
