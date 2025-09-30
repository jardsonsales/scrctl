from tkinter import *
from tkinter import ttk
import tkinter as tk
import subprocess
import os
import json
import sys

def resource_path(relative_path):
    """ Obtém o caminho absoluto para recursos empacotados """
    if hasattr(sys, '_MEIPASS'):
        # Estamos rodando em um PyInstaller bundle
        return os.path.join(sys._MEIPASS, relative_path)
    # Estamos rodando em modo de desenvolvimento normal
    return relative_path  # Corrigido aqui


home_folder = os.path.expanduser('~')
profile_folder = home_folder + "/.config/scrctl"
profile_file = profile_folder + "/profiles.json"
profiles = {}
if os.path.exists(profile_file):
    with open(profile_file, "r") as f:
        profiles = json.loads(f.read())
else:
        profiles = {
                "Profile 1": {
                    "gamma": 4500,
                    "bright": 100
                },
                "Profile 2": {
                    "gamma": 4500,
                    "bright": 100
                },
                "Profile 3": {
                    "gamma": 4500,
                    "bright": 100
                },
                "Profile 4": {
                    "gamma": 4500,
                    "bright": 100
                }
        }
        os.makedirs(profile_folder, exist_ok=True)
        with open(profile_file, "w") as f:
            f.write(json.dumps(profiles))

def apply():
    print(f"gamma={gamma.get()} bright={bright.get()} profile={combo.get()}")
    subprocess.run("pkill gammastep", shell=True, text=True, capture_output=True)
    subprocess.run(f"brightnessctl set {bright.get()}%", shell=True, text=True, capture_output=True)
    subprocess.run(f"ddcutil --verbose setvcp 10 {bright.get()}", shell=True, text=True, capture_output=True)
    subprocess.Popen(["gammastep", "-m", "wayland", "-O", str(gamma.get())], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    save()

def save():
    profiles[combo.get()] = { "gamma": int(gamma.get()), "bright": float(bright.get()) }
    with open(profile_file, "w") as f:
        f.write(json.dumps(profiles))

def profile_switch(_):
    gamma.delete(0, tk.END)
    gamma.insert(0, str(profiles[combo.get()]["gamma"]))
    bright.delete(0, tk.END)
    bright.insert(0, str(profiles[combo.get()]["bright"]))

root = Tk(baseName="x11screencontrol", className="xorgscreencontrol")
root.tk.call('source', resource_path('forest-light.tcl'))
ttk.Style().theme_use('forest-light')

root.title("X11 Screen Control")
frm = ttk.Frame(root, padding=50)
frm.grid()

ttk.Label(frm, text="Gamma Night Mode").grid(column=0, row=0)

gamma = ttk.Entry(frm)
gamma.insert(0, str(profiles["Profile 1"]["gamma"]))
gamma.grid(column=1, row=0, padx=(5,10), pady=5)


ttk.Label(frm, text="Brightness").grid(column=0, row=1)

bright = ttk.Entry(frm)
bright.insert(0, str(profiles["Profile 1"]["bright"]))
bright.grid(column=1, row=1, padx=(5,10), pady=5)


combo_profiles = ["Profile 1", "Profile 2", "Profile 3", "Profile 4"]
combo = ttk.Combobox(frm, values=combo_profiles, state="readonly")
combo.grid(column=0, row=2, padx=0, pady=5, columnspan=2)
combo.current(0)
combo.bind('<<ComboboxSelected>>', profile_switch)

ttk.Button(frm, text="Apply", command=apply).grid(column=0, row=3, columnspan=2, pady=(20,5))


root.mainloop()
