import pyautogui as type
import time
import random
import string
import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading
from tkextrafont import Font

# Constants for behavior probabilities and delays
TYPO_PROBABILITY = 0.02
PAUSE_THRESHOLD = 0.95
PUNCTUATION_DELAY_RANGE = (0.5, 3.0)
UPPERCASE_DELAY_RANGE = (0.5, 3.0)
BASE_WAIT_TIME_RANGE = (0.05, 0.3)
THINKING_DELAY_MULTIPLIER_BOTTOM = 2/0.05
THINKING_DELAY_MULTIPLIER_UPPER = 3/0.05


pause_typing = False
time_from_last_open = 0
current_file_path = None

def main(text, typo_prob=0.02, pause_threshold=0.95, punctuation_delay=(0.5, 3.0), base_wait_time=(0.05, 0.3)):
    for char in text:
        global pause_typing 
        while pause_typing:
            time.sleep(0.0002)
        interval_after = 0
        wait_time = random.uniform(*BASE_WAIT_TIME_RANGE)
        if char in string.punctuation:
            interval_after = random.uniform(*PUNCTUATION_DELAY_RANGE)
        if random.random() < TYPO_PROBABILITY:  
            type.typewrite(introduce_typo(char))  # Type a wrong letter
            time.sleep(random.uniform(0.4, 0.7))  # Short pause before correcting
            type.press('backspace')
        if random.random() > PAUSE_THRESHOLD:
            time.sleep(random.uniform(0 , 3.0  ))
        if char.isupper():
            wait_time += random.uniform(0.5, 3.0)

        time.sleep(wait_time)
        type.typewrite(char, interval=interval_after)

def introduce_typo(char):
    keyboard_map = {
    'a': 'qwsz', 'b': 'vghn', 'c': 'xdfv', 'd': 'ersfcx', 'e': 'wrsd', 
    'f': 'rtgdcv', 'g': 'tyhfvb', 'h': 'yujgbn', 'i': 'uokl', 'j': 'uikmnh', 
    'k': 'iolmj', 'l': 'opk', 'm': 'njk', 'n': 'bhjm', 'o': 'ipkl', 
    'p': 'ol', 'q': 'wa', 'r': 'etdf', 's': 'awedxz', 't': 'rfgy', 
    'u': 'yhji', 'v': 'cfgb', 'w': 'qase', 'x': 'zsdc', 'y': 'tghu', 
    'z': 'asx', 
    # Numbers and special characters
    '1': '2q', '2': '13wq', '3': '24we', '4': '35er', '5': '46rt', 
    '6': '57ty', '7': '68uy', '8': '79iu', '9': '80io', '0': '9po', 
    '-': '0p=', '=': '-[', '[': 'p]', ']': '[', ';': 'lk', "'": ';', 
    ',': 'km', '.': ',/', '/': '.', ' ': ' '}

    try:
        return random.choice(keyboard_map[char])
    except:
        return char

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import font

import tkinter as tk
import tkinter.font as tkFont
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
time_from_last_open = 0

def create_gui():
    def on_start():
        time.sleep(2)
        message = message_entry.get("1.0", tk.END).strip()
        typo_prob = float(typo_prob_spinbox.get())
        pause_threshold = float(pause_threshold_spinbox.get())
        punctuation_delay = (float(punctuation_min_spinbox.get()), float(punctuation_max_spinbox.get()))
        base_wait_time = (float(base_wait_min_spinbox.get()), float(base_wait_max_spinbox.get()))

        t1 = threading.Thread(target = main, args = (message, typo_prob, pause_threshold, punctuation_delay, base_wait_time))
        t1.start()

    def stop_typing():
        global pause_typing
        pause_typing = not pause_typing

    def open_text_editor():
        t2 = threading.Thread(target = open_new_window, args = ())
        t2.start()
        
    
    
    def open_new_window():
        new_window = tk.Toplevel(root)
        menubar = tk.Menu(new_window)
    

# Create the File menu

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=new_file)
        file_menu.add_command(label="Open", command=open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save", command=save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Save As", command = save_as_file)
        menubar.add_cascade(label="Save", menu=file_menu)

        # Configure the menu bar
        new_window.config(menu=menubar)
        new_window.title("Autotyper editor")
        new_window.geometry("600x600")
        global text_editor
        style = ttk.Style(theme="darkly")  # Use a dark theme
        text_editor = tk.Text(new_window, wrap="word", height=15, width=70, font = ("Inter", 9
        ),selectbackground="#382d53", fg = "#f8f5ff",   # Change the selection background color
    selectforeground="white", undo = True)
        text_editor.config(selectbackground= "#382d53", selectforeground="#f8f5ff")
        text_editor.tag_configure("highlight", background="#d7c4ff")
        
        

    # Insert some sample text
        text_editor.insert(tk.END, "This is some sample text.\nHighlight this text.\nAnother line of text.")

        # Apply the highlight tag to specific text (e.g., highlight the second line)        
            

        text_editor.pack(padx=10, pady=5, fill="both", expand=True)
    current_file_path = None
    global time_from_last_open
    time_from_last_open = 0
    def autosave():
        global current_file_path
        global new_window
        global time_from_last_open
        if current_file_path != None:
            if current_file_path and (time.time() - time_from_last_open) > 5:
                print("file autosaved")
                save_file()
        root.after(1000, autosave) 
    
    def save_file():
        global current_file_path
        try:
            if current_file_path:
                try:
                    with open(current_file_path, "w") as file:
                        content = text_editor.get(1.0, tk.END).rstrip()  # Get content from editor
                        file.write(content)  # Write content to the file
                        print("file saved")
                        global time_from_last_open
                        time_from_last_open = time.time()
                except Exception as e:
                    save_as_file()
            else:
                save_as_file()
        except NameError:
            pass
    def save_as_file():
        global time_from_last_open
        time_from_last_open = time.time()
        global current_file_path
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        current_file_path = file_path
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(text_editor.get("1.0", tk.END).strip())  # Get all text from the editor
                print(f"File saved successfully to {file_path}")
                time_from_last_open = time.time()
            except Exception as e:
                print(f"Error saving file: {e}")
        
        
                
                
            
       
    def new_file():
        text_editor.delete("1.0", tk.END)  # Clear the current content
         


    

    def open_file():
        global time_from_last_open
        time_from_last_open= time.time()
        file_path = filedialog.askopenfilename()
        if file_path:
            file = open(file_path, "r")
            global current_file_path 
            content = file.read()
            text_editor.delete("1.0", tk.END)  # Clear the current content
            text_editor.insert(tk.END, content)
            current_file_path = file_path

    def load_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            file = open(file_path, "r")
            content = file.read()
            message_entry.delete("1.0", tk.END)  # Clear the current content
            message_entry.insert(tk.END, content)

    def clear_message():
        message_entry.delete("1.0", tk.END)

    root = tk.Tk()
    root.title("Autotyper GUI")

    root.after(1000, autosave)
    print("begin autosave")


    # Register the custom font
    root.option_add('*Font', 'Inter-Regular 12')  # This can point to the custom font name

    # Initialize ttkbootstrap theme and style
    style = ttk.Style(theme="flatly")

    # Set rounded style for Entry and Button widgets
    style.configure('TButton', font=("Inter", 12), width=20, padding=6, relief=SOLID, borderwidth=1, corner_radius=12)
    style.configure('TEntry', font=("Inter", 12), padding=6, relief=SOLID, borderwidth=1, corner_radius=12)
    style.configure('TSpinbox', font=("Inter", 12), padding=6, relief=SOLID, borderwidth=1, corner_radius=12)
    style.configure('TLabel', font=("Inter", 12))

    # Message input
    tk.Label(root, text="Message to Type:", font=("Inter", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
    message_entry = tk.Text(root, height=5, width=40, font=("Inter", 8), wrap="word")
    message_entry.grid(row=0, column=1, padx=10, pady=10)

    # Typo probability
    tk.Label(root, text="Typo Probability:", font=("Inter", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
    typo_prob_spinbox = ttk.Spinbox(root, from_=0.0, to=1.0, increment=0.01)
    typo_prob_spinbox.set(TYPO_PROBABILITY)
    typo_prob_spinbox.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    # Pause threshold
    tk.Label(root, text="Pause Threshold:", font=("Inter", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
    pause_threshold_spinbox = ttk.Spinbox(root, from_=0.0, to=1.0, increment=0.01)
    pause_threshold_spinbox.set(PAUSE_THRESHOLD)
    pause_threshold_spinbox.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    # Punctuation delay range
    tk.Label(root, text="Punctuation Delay Range (s):", font=("Inter", 12)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
    punctuation_min_spinbox = ttk.Spinbox(root, from_=0.0, to=5.0, increment=0.1)
    punctuation_min_spinbox.set(PUNCTUATION_DELAY_RANGE[0])
    punctuation_min_spinbox.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    punctuation_max_spinbox = ttk.Spinbox(root, from_=0.0, to=5.0, increment=0.1)
    punctuation_max_spinbox.set(PUNCTUATION_DELAY_RANGE[1])
    punctuation_max_spinbox.grid(row=3, column=1, padx=10, pady=35, sticky="e")

    # Base wait time range
    tk.Label(root, text="Base Wait Time Range (s):", font=("Inter", 12)).grid(row=4, column=0, padx=10, pady=10, sticky="w")
    base_wait_min_spinbox = ttk.Spinbox(root, from_=0.0, to=1.0, increment=0.1)
    base_wait_min_spinbox.set(BASE_WAIT_TIME_RANGE[0])
    base_wait_min_spinbox.grid(row=4, column=1, padx=10, pady=5, sticky="w")
    base_wait_max_spinbox = ttk.Spinbox(root, from_=0.0, to=1.0, increment=0.1)
    base_wait_max_spinbox.set(BASE_WAIT_TIME_RANGE[1])
    base_wait_max_spinbox.grid(row=4, column=1, padx=10, pady=35, sticky="e")

    button_frame = ttk.Frame(root)
    button_frame.grid(row=5, column=0, columnspan=4, pady=20, padx=10, sticky="w")

    button_clear_message = ttk.Button(button_frame, text="Clear message", command=clear_message)
    button_clear_message.grid(row=0, column=3, padx=10, pady=10)

    # Load file button
    load_file_button = ttk.Button(button_frame, text="Load File", command=load_file)
    load_file_button.grid(row=0, column=0, padx=10, pady=10)

    # Start button
    start_button = ttk.Button(button_frame, text="Start Typing", command=on_start)
    start_button.grid(row=0, column=1, padx=10, pady=10)

    # Stop button
    stop_button = ttk.Button(button_frame, text="Stop Typing", command=stop_typing)
    stop_button.grid(row=0, column=2, padx=10, pady=10)

    # Text editor button (aligned below the other buttons)
    text_editor_button = ttk.Button(button_frame, text="Text Editor", command=open_text_editor)
    text_editor_button.grid(row=1, column=0, columnspan=4, pady=10, sticky="ew")

    root.mainloop()


if __name__ == "__main__":
    create_gui()