from time import sleep
import threading
import multiprocessing

import tkinter as tk
from tkinter import ttk

from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode
import ctypes

TOGGLE_KEY = KeyCode(char='k')

DELAY = 1.5
mouse = Controller()


class AutoClicker:
    global tk_status

    def __init__(self, process_s, thread_s, status):
        self.delay = DELAY
        self.clicking = False
        self.process_enable = process_s
        self.thread_enable = thread_s
        self.status = status
        print(self.process_enable, self.thread_enable)

    def clicker(self):
        while bool(self.thread_enable.value):  # CHECK FOR ENABLE
            if self.clicking:
                print('Clicking is true')
                mouse.click(Button.left, 1)
                sleep(self.delay)
            else:
                print('Clicking is not true')
                sleep(self.delay)
        else:
            print("clicker thread killed!")

    def toggle_event(self, key):
        if bool(self.thread_enable.value):
            if key == TOGGLE_KEY:
                self.clicking = not self.clicking
        else:
            return False
        if self.clicking:
            self.status.value = "AutoClicker is on"

        else:
            self.status.value = "AutoClicker is off, Press [k] to toggle"

    def start_thread(self):
        print("Starting clicker thread")
        clicker_thread = threading.Thread(target=self.clicker)
        clicker_thread.start()
        print("Starting listener thread")
        with Listener(on_press=self.toggle_event) as listener:
            while bool(self.thread_enable.value) is True:
                pass
            else:
                listener.stop()
            listener.join()
        print("Listener thread killed!")

        print("Process was killed")


def run_autoclicker():
    if process_status.value == 1:
        print("Killing process")
        thread_status.value = 0
        process_status.value = 0
        tk_status.set("Autoclicker [Disabled]")
    else:
        print("Starting process")
        process_status.value = 1
        thread_status.value = 1
        auto_clicker_obj = AutoClicker(process_status, thread_status, c_tk_status)
        p1 = multiprocessing.Process(target=auto_clicker_obj.start_thread)
        p1.start()
        tk_status.set("Autoclicker [Enabled]")


def validate_time(time_delay):
    global DELAY
    try:
        time_delay = float(time_delay)
        if time_delay >= 0.1:
            DELAY = time_delay
            tk_status.set(f"Time delay set to {time_delay} sec(s)")
        else:
            tk_status.set(f"Time delay should be >= 0.1")

    except ValueError:
        tk_status.set(f"Invalid Time Delay")


def status_update():
    global tk_status
    tk_status.set(c_tk_status.value)


if __name__ == "__main__":

    process_status = multiprocessing.Value('i', int(False))
    thread_status = multiprocessing.Value('i', int(False))

    window = tk.Tk()

    tk_delay = tk.StringVar()
    tk_status = tk.StringVar()
    c_tk_status = multiprocessing.Value(ctypes.c_wchar_p, str(tk_status))
    tk_delay.set(str(DELAY))  # Sets delay on the window
    tk_status.set(f"Time delay set to {tk_delay.get()} sec(s)")  # Updates status of main window

    window.title('AutoClicker')
    window.geometry("400x300")
    window.resizable(False, False)

    style = ttk.Style()

    # Label and string_var to display status and delay settings
    ttk.Label(window, text="Status:", style='TLabel').place(x=30, y=30)
    ttk.Label(window, textvariable=tk_status, style='TLabel').place(x=110, y=30)

    ttk.Label(window, text="Time delay(sec):", style='TLabel').place(x=40, y=100)
    ttk.Entry(window, textvariable=tk_delay, font=('calibre', 15, 'normal'), width=8, ).place(x=220, y=100)
    # Submit button
    ttk.Button(window, text="Submit", style='TButton', width=8, command=lambda: validate_time(tk_delay.get())) \
        .place(x=220, y=150)
    # Run
    ttk.Button(window, text="Listener", style='TButton', width=8, command=run_autoclicker) \
        .place(x=290, y=250)

    style.configure('TButton', font=(None, 15))
    style.configure('TLabel', font=(None, 15))

    window.mainloop()
