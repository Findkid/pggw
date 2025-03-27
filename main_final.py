import tkinter as tk
from tkinter import ttk
from data_handler import DataHandler
from visualization import Visualization
from poster import Poster
from statistics_handler import Statistics


data_handler = DataHandler("festival_goers.csv")

# window?
root = tk.Tk()
root.title("Festival Goers Manager")
root.geometry("1000x600")
root.configure(bg="#2E8B57")  

# ==================== HEADER (Data Entry) ====================
header_frame = tk.Frame(root, padx=10, pady=10, bg="#3CB371")  # Medium green
header_frame.pack(fill="x")

tk.Label(header_frame, text="Name", bg="#3CB371", fg="white").grid(row=0, column=0)
tk.Label(header_frame, text="Age", bg="#3CB371", fg="white").grid(row=0, column=1)
tk.Label(header_frame, text="Distance", bg="#3CB371", fg="white").grid(row=0, column=2)
tk.Label(header_frame, text="Accommodation", bg="#3CB371", fg="white").grid(row=0, column=3)
tk.Label(header_frame, text="Ticket Type", bg="#3CB371", fg="white").grid(row=0, column=4)


name_entry = tk.Entry(header_frame)
name_entry.grid(row=1, column=0)
age_entry = tk.Entry(header_frame)
age_entry.grid(row=1, column=1)
distance_entry = tk.Entry(header_frame)
distance_entry.grid(row=1, column=2)

accommodation_var = tk.StringVar(value="Camping")
accommodation_dropdown = ttk.Combobox(header_frame, textvariable=accommodation_var, values=["Camping", "Hotel", "Accommodation"])
accommodation_dropdown.grid(row=1, column=3)

ticket_var = tk.StringVar(value="Full Access")
ticket_dropdown = ttk.Combobox(header_frame, textvariable=ticket_var, values=["Full Access", "1 Day", "2 Day"])
ticket_dropdown.grid(row=1, column=4)

def add_festival_goer():
    """Adds a new festival-goer and updates the display."""
    name = name_entry.get()
    age = age_entry.get()
    distance = distance_entry.get()
    accommodation = accommodation_var.get()
    ticket_type = ticket_var.get()

    if name and age and distance and accommodation and ticket_type:
        data_handler.add_festival_goer(name, int(age), int(distance), accommodation, ticket_type)
        update_festival_list()
    else:
        print("Please fill in all fields!")

tk.Button(header_frame, text="Add Festival Goer", command=add_festival_goer).grid(row=1, column=5)

# ==================== LEFT PANE (Filter Buttons) ====================
left_frame = tk.Frame(root, padx=10, pady=10, bg="#8FBC8F")  
left_frame.pack(side="left", fill="y")

tk.Label(left_frame, text="Filter by Ticket Type", bg="#8FBC8F", fg="black").pack()

def filter_and_display(ticket_type):
    filtered_data = data_handler.filter_by_ticket(ticket_type)
    update_festival_list(filtered_data)

for ticket_type, color in zip(["Full Access", "1 Day", "2 Day"], ["#B22222", "#2E8B57", "#DC143C"]):
    tk.Button(left_frame, text=ticket_type, command=lambda t=ticket_type: filter_and_display(t), bg=color, fg="white").pack(fill="x")

# ==================== RIGHT PANE (Graph Visualizations and Statistics) ====================
right_frame = tk.Frame(root, padx=10, pady=10, bg="green")
right_frame.pack(side="right", fill="both", expand=True)

visualization = Visualization(right_frame, data_handler)
statistics = Statistics(right_frame, data_handler)

tk.Label(right_frame, text="Graph Visualization").pack()

def show_accommodation_distribution(ticket_type):
    visualization.update_graphs(ticket_type)
    back_button.pack(fill="x")

def go_back():
    visualization.parent.pack_forget()
    visualization.canvas.get_tk_widget().pack_forget()
    back_button.pack_forget()
    update_festival_list()

back_button = tk.Button(right_frame, text="Back to Festival Goers", command=go_back)

for ticket_type in ["Full Access", "1 Day", "2 Day"]:
    tk.Button(right_frame, text=f"Show {ticket_type} Distribution", command=lambda t=ticket_type: show_accommodation_distribution(t)).pack(fill="x")

# Button to show visualisation
tk.Button(right_frame, text="Show Festival Statistics", command=statistics.show_statistics).pack(fill="x")

# ==================== CENTER (Festival Goers List) ====================
center_frame = tk.Frame(root, padx=10, pady=10, bg = "#ba3c3e")
center_frame.pack(expand=True, fill="both")

festival_listbox = tk.Listbox(center_frame, width=80, height=15, bg = "#ba2c3e")
festival_listbox.pack(fill="both", expand=True)

def update_festival_list(filtered_data=None):
    """Updates the festival-goers list."""
    festival_listbox.delete(0, tk.END)
    data_to_display = filtered_data if filtered_data else data_handler.data
    for person in data_to_display:
        festival_listbox.insert(tk.END, f"{person['Name']} - {person['Ticket']} - {person['Accommodation']}")

update_festival_list()  # Load initial data

# ==================== BOTTOM PANE (Gigs) ====================
bottom_frame = tk.Frame(root, padx=10, pady=10)
bottom_frame.pack(side="bottom", fill="x")

tk.Label(bottom_frame, text="Gigs").pack()

def show_gigs(day):
    """Displays gigs for the selected day."""
    gigs_listbox.delete(0, tk.END)
    gigs = data_handler.gigs[day]
    for gig in gigs:
        gigs_listbox.insert(tk.END, gig)

def show_eligible_festival_goers(event):
    """Displays festival-goers eligible for the selected gig."""
    selected_gig = gigs_listbox.get(gigs_listbox.curselection())
    day = day_var.get()
    eligible_festival_goers = data_handler.get_eligible_festival_goers(day)
    festival_listbox.delete(0, tk.END)
    for person in eligible_festival_goers:
        festival_listbox.insert(tk.END, f"{person['Name']} - {person['Ticket']} - {person['Accommodation']}")

day_var = tk.StringVar(value="Day 1")
day_dropdown = ttk.Combobox(bottom_frame, textvariable=day_var, values=["Day 1", "Day 2", "Day 3"])
day_dropdown.pack(side="left")
day_dropdown.bind("<<ComboboxSelected>>", lambda event: show_gigs(day_var.get()))

gigs_listbox = tk.Listbox(bottom_frame, width=50, height=5)
gigs_listbox.pack(side="left", fill="both", expand=True)
gigs_listbox.bind("<<ListboxSelect>>", show_eligible_festival_goers)


show_gigs("Day 1")


poster = Poster(data_handler)

def show_poster():
    """Displays the festival poster in a new window."""
    poster.create_poster()

tk.Button(root, text="Show Festival Poster", command=show_poster).pack(side="bottom", fill="x")


root.mainloop()