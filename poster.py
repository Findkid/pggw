import tkinter as tk

class Poster:
    def __init__(self, data_handler):
        self.data_handler = data_handler

    def create_poster(self):
        """Creates and displays the festival poster in a new window."""
        poster_window = tk.Toplevel()
        poster_window.title("Festival Poster")
        poster_window.geometry("800x600")

        canvas = tk.Canvas(poster_window, width=800, height=600)
        canvas.pack(fill=tk.BOTH, expand=True)

        # We need to contact the devs, not sure what this does 
        background_image = tk.PhotoImage(file="festival_background.png")
        canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
        canvas.image = background_image  # Keep a reference to avoid garbage collection

        y_position = 200
        for day, gigs in self.data_handler.gigs.values():
            canvas.create_text(500, y_position, text=day, font=("Arial", 24, "bold"), fill="white", anchor=tk.NW)
            y_position += 50
            for i, gig in enumerate(gigs):
                font_size = 20 if i == 0 else 16
                canvas.create_text(500, y_position, text=gig, font=("Arial", font_size), fill="white", anchor=tk.NW)
                y_position += 40
            y_position += 30