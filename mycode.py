import tkinter as tk
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
import io

# Function to convert binary data to image
def convertBinaryToImage(binarydata):
    image = Image.open(io.BytesIO(binarydata))
    return image

# MySQL connection configuration
host = "localhost"
user = "root"
password = "1234"
database = "images"

# Define actual_image_name as a global variable
actual_image_name = ""
incorrect_attempts = 0
# Custom key mappings
key_mappings = {
    'Â': 'A', 'B²': 'B', 'Č': 'C', 'Ð': 'D', 'Ë': 'E',
    'Fⁿ': 'F', '/G': 'G', 'Ĥ': 'H', 'I³': 'I', 'J_': 'J',
    'K*': 'K', 'Ł': 'L', '[:M]': 'M', 'Ṅ': 'N', "'O": 'O',
    'P⅞': 'P', '`Q': 'Q', '{R}': 'R', '$': 'S', 'Ṭ': 'T',
    'Ű': 'U', 'V⁴': 'V', '!W!': 'W', '¿X': 'X', '|Ÿ': 'Y', '<Z>': 'Z', 
    'Backspace': '<-', 'Space': ' '
}

def display_new_image():
    global actual_image_name
    try:
        connection = mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )
        cursor = connection.cursor()
        select_sql_query = "SELECT img, name FROM image ORDER BY RAND() LIMIT 1"
        cursor.execute(select_sql_query)
        result = cursor.fetchone()
        if result:
            image_data, actual_image_name = result
            img = convertBinaryToImage(image_data)
            img = img.resize((300, 300))
            photo = ImageTk.PhotoImage(img)
            image_label.config(image=photo)
            image_label.image = photo
            name_entry.delete(0, tk.END)
            result_label.config(text="", fg="black")
    except Error as e:
        print("Error occurred:", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection is closed")

def check_guess():
    global actual_image_name
    guessed_name = name_entry.get().strip().lower()
    if guessed_name == actual_image_name.lower():
        result_label.config(text="Correct Guess!", fg="green", bg='gray')
        name_entry.config(state=tk.DISABLED)
        root.after(2000, root.destroy)
    else:
        display_new_image()
        result_label.config(text="Incorrect Guess. Try again!", fg="red", bg='gray')

def check_guess():
    global actual_image_name, incorrect_attempts
    guessed_name = name_entry.get().strip().lower()
    if guessed_name == actual_image_name.lower():
        result_label.config(text="Correct Guess!", fg="green", bg='gray')
        name_entry.config(state=tk.DISABLED)
        root.after(2000, root.destroy)  # Close window after 2 seconds
    else:
        incorrect_attempts += 1
        if incorrect_attempts >= 5:
            start_cooldown()
            incorrect_attempts = 0  # Reset counter after cooldown starts
        else:
            display_new_image()
            result_label.config(text=f"Incorrect Guess. Attempts: {incorrect_attempts}. Try again!", fg="red", bg='gray')

def start_cooldown():
    disable_input()
    result_label.config(text="Cooldown: Wait for 60 seconds before trying again.", fg="orange", bg='gray')
    root.after(60000, enable_input)  # Enable input after 60 seconds


def disable_input():
    name_entry.config(state=tk.DISABLED)
    check_button.config(state=tk.DISABLED)

def enable_input():
    name_entry.config(state=tk.NORMAL)
    check_button.config(state=tk.NORMAL)
    result_label.config(text="")

def update_label_position(event=None):
    label_width = result_label.winfo_reqwidth()
    window_width = root.winfo_width()
    label_x = (window_width - label_width) // 2
    result_label.place(x=label_x, y=595)

def key_pressed(char):
    if char == "Backspace":
        current_text = name_entry.get()[:-1]  # Remove the last character
    elif char == "Space":
        current_text = name_entry.get() + " "  # Add a space
    elif char in key_mappings:
        char = key_mappings[char]
        current_text = name_entry.get() + char
    else:
        return  # Do nothing if it's an unhandled key

    name_entry.config(state=tk.NORMAL)  # Temporarily enable the Entry widget to allow text insertion
    name_entry.delete(0, tk.END)
    name_entry.insert(0, current_text)
    name_entry.config(state=tk.DISABLED)  # Disable the Entry widget again

# Create the root window
root = tk.Tk()
root.title("Guess the Image Name")
root.geometry("1350x760+10+10")
root.resizable(False, False)

# Load and set the background image
bg_image = Image.open("images/GUI.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create GUI elements
image_label = tk.Label(root, font=("Microsoft Yehei UI Light", 10, "bold"), bg="black")
image_label.place(x=300, y=150)

name_entry = tk.Entry(root, width=27, relief="solid", font=("Microsoft Yehei UI Light", 12, "bold"), fg="black", bg="grey", state=tk.DISABLED)
name_entry.place(x=550, y=550)

result_label = tk.Label(root, text="", font=("Microsoft Yehei UI Light", 10, "bold"), bg="black", fg="black", activebackground="black", activeforeground="black")
root.bind("<Configure>", update_label_position)

display_new_image()

check_button = tk.Button(root, text="Check Guess", relief="solid", font=("Microsoft Yehei UI Light", 10, "bold"), bd=0, fg="black", bg="white", activebackground="gray", cursor="hand2", command=check_guess)
check_button.place(x=630, y=630)

# Create the virtual keyboard
keyboard_frame = tk.Frame(root, bg='white', bd=2, relief='raised')
keyboard_frame.place(x=600, y=200)

# Define custom keyboard layout including Backspace and Space
custom_keyboard_layout = [
    ['Â', 'B²', 'Č', 'Ð', 'Ë', 'Fⁿ', '/G', 'Ĥ', 'I³', 'J_', 'K*', 'Ł'],
    ['[:M]', 'Ṅ', "'O", 'P⅞', '`Q', '{R}', '$', 'Ṭ', 'Ű', 'V⁴', '!W!', '¿X'],
    ['|Ÿ', '<Z>', 'Space','Backspace'],
]

for row_index, row in enumerate(custom_keyboard_layout):
    for col_index, char in enumerate(row):
        btn = tk.Button(keyboard_frame, text=char, width=12 if char == "Space" else 4, bg='lightgray', command=lambda c=char: key_pressed(c))
        btn.grid(row=row_index, column=col_index, padx=5, pady=5)

root.mainloop()