import tkinter as tk
import requests


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
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMzE0MTU2NSwianRpIjoiZTk1MDBjZWYtYWVkYS00OWJlLTlhOTItZDE3YmEyMjIwZTZjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6IjY1ZjY0YTUzNzY3MTc4ZGY1MDAxODRlYyIsInR5cGUiOjJ9LCJuYmYiOjE3MTMxNDE1NjUsImNzcmYiOiIyOWE5NGM5ZS1lMzdkLTQzYmUtOGI0My0yMWVjODcyOWE2ZWYiLCJleHAiOjE3MTMyMjc5NjV9.GCAENiWHaz5T0JiHogYAnnjO5TEM_2N447Hmz-q7wpk",
        "Content-Type": "application/json",
    }

    url = "http://localhost:5000/api/devices"

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        result_label.config(text="Request sent successfully!", foreground="green")
    else:
        res = response.json()
        result_label.config(
            text=f"Failed to send request: {res['message']}", foreground="red"
        )


root = tk.Tk()
root.title("Device Registration Form")

label_device_name = tk.Label(root, text="Device Name:")
label_device_name.grid(row=0, column=0, padx=10, pady=10)
entry_device_name = tk.Entry(root)
entry_device_name.grid(row=0, column=1, padx=10, pady=10)

label_device_mac = tk.Label(root, text="Device MAC:")
label_device_mac.grid(row=1, column=0, padx=10, pady=10)
entry_device_mac = tk.Entry(root)
entry_device_mac.grid(row=1, column=1, padx=10, pady=10)

label_device_type = tk.Label(root, text="Device Type:")
label_device_type.grid(row=2, column=0, padx=10, pady=10)
entry_device_type = tk.Entry(root)
entry_device_type.grid(row=2, column=1, padx=10, pady=10)

submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

result_label = tk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=2)

root.mainloop()
