import tkinter as tk
import pandas as pd

class Statistics:
    def __init__(self, parent, data_handler):
        self.parent = parent
        self.data_handler = data_handler
        self.distance_threshold_var = tk.StringVar()  # EDIT: Changed from tk.IntVar() to tk.StringVar() to allow manual validation and prevent app crash when non-integer input is entered

    def show_statistics(self):
        """Displays statistics in the provided frame."""
        for widget in self.parent.winfo_children():
            widget.destroy()

        df = pd.DataFrame(self.data_handler.data)
        df['Distance'] = pd.to_numeric(df['Distance'], errors='coerce')  # Keep original logic for converting distance safely

        # Input section for the user to set a distance threshold
        input_frame = tk.Frame(self.parent)
        input_frame.pack(fill="x")

        tk.Label(input_frame, text="Enter the distance threshold (km):").pack(side="left")
        # EDIT: Updated label text to be more descriptive and user-friendly, adding "(km)" for clarity

        distance_entry = tk.Entry(input_frame, textvariable=self.distance_threshold_var)
        distance_entry.pack(side="left")
        # EDIT: Entry now uses tk.StringVar() so we can validate and provide custom error messages instead of crashing on invalid input

        tk.Button(input_frame, text="Update", command=lambda: self.update_statistics(df)).pack(side="left")
        # EDIT: No logic changed here, but pairing with the new validation logic in update_statistics()

        self.stats_frame = tk.Frame(self.parent)
        self.stats_frame.pack(fill="both", expand=True)

        self.update_statistics(df)  # Initial load

    def update_statistics(self, df):
        """Updates the statistics based on the distance threshold."""
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        try:
            threshold = int(self.distance_threshold_var.get())
            valid_threshold = True
            # EDIT: Replaced IntVar direct access with manual conversion from StringVar using int()
            #       This allows catching invalid input (e.g. text or empty strings) and prevents crashes
        except ValueError:
            valid_threshold = False
            # EDIT: If conversion fails, we can now show a friendly error instead of breaking the app

        if valid_threshold:
            traveled_more = df[df['Distance'] > threshold]
            if len(df) > 0:
                percentage_traveled_more = (len(traveled_more) / len(df)) * 100
            else:
                percentage_traveled_more = 0
            # EDIT: Added safe check for division by zero (if dataset is empty)

            tk.Label(
                self.stats_frame,
                text=f"📍 {percentage_traveled_more:.2f}% of attendees traveled more than {threshold} km"
            ).pack()
            # EDIT: Rephrased output string to be more descriptive and visual (added 📍 icon for clarity during presentation)
        else:
            tk.Label(self.stats_frame, text="⚠️ Please enter a valid number for distance.").pack()
            # EDIT: New validation message added to guide the user when they enter invalid data (e.g. letters, symbols, or empty input)

        # Calculate the percentages of people with different combinations of accommodation and ticket type
        tk.Label(self.stats_frame, text="🎟 Accommodation + Ticket Type Breakdown:").pack(pady=(10, 0))
        # EDIT: Modified label to include emoji and clearer text for better UI and more engaging presentation (especially useful during demo)

        if not df.empty:
            combinations = df.groupby(['Accommodation', 'Ticket']).size().unstack(fill_value=0)
            # EDIT: No logic change — this line creates a table counting each Accommodation+Ticket combination

            percentages = combinations.div(combinations.sum(axis=1), axis=0) * 100
            # EDIT: No logic change — calculates row-wise percentages of ticket types within each accommodation group

            for accommodation in percentages.index:
                for ticket in percentages.columns:
                    percentage = percentages.loc[accommodation, ticket]
                    tk.Label(
                        self.stats_frame,
                        text=f"• {accommodation} - {ticket}: {percentage:.2f}%"
                    ).pack(anchor="w")
                    # EDIT: Added bullet symbol • to improve readability and visual structure
                    # EDIT: Set anchor="w" to left-align all stat labels for a neater, column-like look
