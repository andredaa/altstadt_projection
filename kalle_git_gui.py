#! /usr/bin/env python3
import tkinter as tk
from tkinter import *
import subprocess as sub
import os

os.chdir("/home/pi/scripts/altstadt_projection")

# TODO set permissions for reboot
#  http://www.ridgesolutions.ie/index.php/2013/02/22/raspberry-pi-restart-shutdown-your-pi-from-python-code/
def reboot():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)


def update_git():
    with sub.Popen(["git", "pull"], stdout=sub.PIPE) as proc:
        #  output = process.communicate()[0]   #  sub.check_call("touch test")
        output =  proc.stdout.read().decode("utf-8")
        print(output)

    # Keine Änderungen
    if "Bereits aktuell" in output:
        button = tk.Button(frame,
                           text="Keine Updates verfuegbar, Fenster schliessen",
                           fg="black",
                           command=quit)
    # erfolgreich aktualisiert
    elif "Aktualisiere" in output:
        button = tk.Button(frame,
                           text="Updates empfangen! Jetzt neu starten",
                           fg="green",
                           command=reboot)
    # es gab warhscheinlich eine Errormeldung
    else:
        with sub.Popen(["git", "status"], stdout=sub.PIPE) as proc:
            #  output = process.communicate()[0]   #  sub.check_call("touch test")
            output = proc.stdout.read().decode("utf-8")
            print(output)

        T = Text(root, height=40, width=100)
        T.pack()
        T.insert(END, "Da ist eventuell was schief gegangen.\n\n\n", "Foto von Text machen, Andre schicken.\n", output)
        button = tk.Button(frame,
                           text="Man kann nix kaputt machen. Wir gucken morgen mal",
                           fg="black",
                           command=quit)


    # display new button
    button.pack(side=tk.LEFT)
    root.mainloop()


WINDOW_SIZE = "500x200"

root = tk.Tk(className="Projection - update")
root.geometry(WINDOW_SIZE)

frame = tk.Frame(root)
frame.pack()

refresh_button = tk.Button(frame,
                           text="Aktualisieren",
                           fg="black",
                           command=update_git)

refresh_button.pack(side=tk.LEFT)

root.mainloop()
