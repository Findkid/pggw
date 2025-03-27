import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

class Visualization:
    def __init__(self, parent, data_handler):
        self.parent = parent
        self.data_handler = data_handler
        self.canvas = None
    
    def update_graphs(self, ticket_type):
        """Updates and displays graphs based on the selected ticket type."""
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        figure, ax = plt.subplots()
        distribution = self.data_handler.get_distribution_by_accommodation(ticket_type)
        
        labels = list(distribution.keys())
        sizes = list(distribution.values())
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title(f"Accommodation Distribution for {ticket_type} Ticket Holders")
        
        self.canvas = FigureCanvasTkAgg(figure, master=self.parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)