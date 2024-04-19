import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import requests


def login():
    global token
    username = username_entry.get()
    password = password_entry.get()

    # URL and data for authentication
    auth_url = "http://localhost:5000/api/users/login"
    auth_data = {"email_or_username": username, "password": password}

    try:
        response = requests.post(auth_url, json=auth_data)
        response.raise_for_status()  # Raise an error for bad responses

        token = response.json().get("access_token")
        if token:
            root.deiconify()  # Show the main window
            login_window.destroy()  # Close the login window
        else:
            messagebox.showerror("Error", "Invalid token received.")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to login: {e}")


def submit():
    device_name = entry_device_name.get()
    device_mac = entry_device_mac.get()
    device_type = entry_device_type.get()

    data = {
        "name": device_name,
        "mac": device_mac,
        "type": device_type,
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    url = "http://localhost:5000/api/devices"

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        if response.status_code == 200:
            result_label.config(text="Request sent successfully!", foreground="green")
        else:
            res = response.json()
            result_label.config(
                text=f"Failed to send request: {res['message']}", foreground="red"
            )
    except requests.RequestException as e:
        result_label.config(text=f"Failed to send request: {e}", foreground="red")


# Create login window
login_window = tk.Tk()
login_window.title("Login")

tk.Label(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=5)
username_entry = tk.Entry(login_window)
username_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=5)
password_entry = tk.Entry(login_window, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=5)

login_button = tk.Button(login_window, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Global variable to store the token
token = None

# Hide the main window initially
root = tk.Tk()
root.title("Device Registration Form")
root.withdraw()

label_device_name = tk.Label(root, text="Device Name:")
label_device_name.pack(pady=5)
entry_device_name = tk.Entry(root)
entry_device_name.pack(pady=5)

label_device_mac = tk.Label(root, text="Device MAC:")
label_device_mac.pack(pady=5)
entry_device_mac = tk.Entry(root)
entry_device_mac.pack(pady=5)

label_device_type = tk.Label(root, text="Device Type:")
label_device_type.pack(pady=5)
entry_device_type = tk.Entry(root)
entry_device_type.pack(pady=5)

submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()
