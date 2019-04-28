# assuming Python3
import tkinter as tk
import subprocess as sub

# TODO set permissions for reboot
#  http://www.ridgesolutions.ie/index.php/2013/02/22/raspberry-pi-restart-shutdown-your-pi-from-python-code/
def reboot():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)


def write_slogan():
    # Git pull im ordner des git repos ausführen
    with sub.Popen(["git", "pull"], stdout=sub.PIPE) as proc:
        #  output = process.communicate()[0]   #  sub.check_call("touch test")
        output =  proc.stdout.read().decode("utf-8")
        print(output)

    # Give the option to either reboot or quit the window
    if "Already up-to-date." in output:
        button = tk.Button(frame,
                           text="Keine Updates verfügbar, Fenster schließen",
                           fg="black",
                           command=quit)
    else:
        button = tk.Button(frame,
                           text="Updates empfangen! Jetzt neu starten",
                           fg="green",
                           command=reboot)

    # display new button

    button.pack(side=tk.LEFT)
    root.mainloop()


WINDOW_SIZE = "600x400"

root = tk.Tk()
root.geometry(WINDOW_SIZE)

frame = tk.Frame(root)
frame.pack()

refresh_button = tk.Button(frame,
                   text="Aktualisieren",
                   fg="black",
                   command=write_slogan)

refresh_button.pack(side=tk.LEFT)

root.mainloop()
