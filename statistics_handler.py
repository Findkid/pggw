import tkinter as tk
import pandas as pd

class Statistics:
    def __init__(self, parent, data_handler):
        self.parent = parent
        self.data_handler = data_handler
        self.distance_threshold_var = tk.IntVar()

    def show_statistics(self):
        """Displays statistics in the provided frame."""
        for widget in self.parent.winfo_children():
            widget.destroy()

        df = pd.DataFrame(self.data_handler.data)

        df['Distance'] = pd.to_numeric(df['Distance'], errors='coerce')

        input_frame = tk.Frame(self.parent)
        input_frame.pack(fill="x")

        tk.Label(input_frame, text="Enter the distance threshold:").pack(side="left")
        distance_entry = tk.Entry(input_frame, textvariable=self.distance_threshold_var)
        distance_entry.pack(side="left")
        tk.Button(input_frame, text="Update", command=lambda: self.update_statistics(df)).pack(side="left")

        self.stats_frame = tk.Frame(self.parent)
        self.stats_frame.pack(fill="both", expand=True)

        # Initial statistics display
        self.update_statistics(df)

    def update_statistics(self, df):
        """Updates the statistics based on the distance threshold."""
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        distance_threshold = self.distance_threshold_var.get()
        if distance_threshold:
            traveled_more = df[df['Distance'] > distance_threshold]
            percentage_traveled_more = (len(traveled_more) / len(df)) * 100
            tk.Label(self.stats_frame, text=f"Percentage of people who traveled more than {distance_threshold} km: {percentage_traveled_more:.2f}%").pack()

        # Calculate the percentages of people with different combinations of accommodation and ticket type
        combinations = df.groupby(['Accommodation', 'Ticket']).size().unstack(fill_value=0)
        percentages = combinations.div(combinations.sum(axis=1), axis=0) * 100


        tk.Label(self.stats_frame, text="Percentages of people with different combinations of accommodation and ticket type:").pack()
        for accommodation in percentages.index:
            for ticket in percentages.columns:
                percentage = percentages.loc[accommodation, ticket]
                tk.Label(self.stats_frame, text=f"{accommodation} - {ticket}: {percentage:.2f}%").pack()