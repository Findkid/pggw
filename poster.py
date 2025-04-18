import tkinter as tk
import os

# import the tkinter module to create GUI and renamed it as tk.

class Poster:
    def __init__(self, data_handler):
        self.data_handler = data_handler
# define a new class called poster. input the data_handler file and store it.
    def create_poster(self):
        # Creates and displays the festival poster in a toplevel window.
        poster_window = tk.Toplevel()
        poster_window.title("Festival Poster")
        poster_window.geometry("800x600")
        # set the title of the poster and the dimensions of the poster.
        canvas = tk.Canvas(poster_window, width=800, height=600)
        canvas.pack(fill=tk.BOTH, expand=True)
        # create a Canvas widget with the same size of the poster,
        # and allows the widget to expand to match any size of the poster.

        # Dynamically determine the path to the image
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, "festival_background.png")

        if not os.path.exists(image_path):
            print("Error: festival_background.png not found!")
            return
        # Load the image named festival_background and draw it onto the canvas widget.
        background_image = tk.PhotoImage(file=image_path)
        canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
        canvas.image = background_image
        # Keep a reference to avoid garbage collection (may display nothing without this step)

        y_position = 200
        for day, gigs in self.data_handler.gigs.items():
            # original code: for day, gigs in self.data_handler.gigs.values():
            # edited: change values to items to avoid possible value-error
            canvas.create_text(400, y_position, text=day, font=("Arial", 24, "bold"), fill="white", anchor=tk.NW)
            y_position += 50
            # connect each day with its gigs and create text of days on poster with settings(ex.font size 24).
            for i, gig in enumerate(gigs):
                font_size = 20 
                canvas.create_text(400, y_position, text=gig, font=("Arial", font_size), fill="white", anchor=tk.NW)
                y_position += 40
                # create text of gigs with settings. only first gig have font size of 20(headliner). else 16.
            y_position += 30  # add empty space between days
