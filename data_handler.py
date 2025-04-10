import csv

#Insert some code here
class DataHandler:
    def __init__(self, filename="festival_goers.csv"):
        """Initialize with a CSV filename and load data."""
        self.filename = filename
        # I have uncommented the self.data so it can load data from the CSV. 
        self.data = self.load_from_csv() 
        self.data = [] 
        self.gigs = {
            "Day 1": ["Fink Ployd", "Psychedelic corn trumpets"],
            "Day 2": ["Porcupine Bush", "Fever Day"],
            "Day 3": ["Pearl Djam", "Soundbackyard"]
        }       
        self.ticket_index = {}  ## Initialize ticket_index as an empty dictionary

    def load_from_csv(self):
        """Load festival-goers from the CSV file."""
        try:
            with open(self.filename, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                return [row for row in reader]  # Load all rows as dictionaries
        except FileNotFoundError:
            return []

    def save_to_csv(self):
        """Save the current festival-goer data back to the CSV file."""
        with open(self.filename, mode="a", newline="") as file:
            fieldnames = ["Name", "Age", "Distance", "Accommodation", "Ticket"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.data)
        # Changed to open file with "a" so the file does rewrite itself and instead just adds the new festival goer

    def add_festival_goer(self, name, age, distance, accommodation, ticket_type):
        """Add a new festival-goer and save to CSV."""
        person = {
            "Name": name,
            "Age": int(age),
            "Distance": int(distance),
            "Accommodation": accommodation,
            "Ticket": ticket_type
        }
        self.data.append(person)
        self.ticket_index.setdefault(ticket_type, []).append(person) 
        # Updates index for faster ffiltering

        with open(self.filename, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Name", "Age", "Distance", "Accommodation", "Ticket"])
            writer.writerow(person)
        # Opens file in append mode and ensures that only the new entry is written and not the entire file again

    
    def filter_by_ticket(self, ticket_type):
        """Return a list of people with a specific ticket type."""
        return [person for person in self.data if person["Ticket"] == ticket_type]
# I have removed the ! (not) function so that it now searches for a specific ticket type
    def get_distribution_by_accommodation(self, ticket_type):
        """Get the distribution of accommodations for a specific ticket type."""
        filtered = self.filter_by_ticket(ticket_type)
        distribution = {}
        for person in filtered:
            accommodation = person["Accommodation"]
            distribution[accommodation] = distribution.get(accommodation, 0) + 1
        return distribution

    def get_eligible_festival_goers(self, day):
        """Get festival-goers eligible for gigs on a specific day."""
        if day == "Day 1":
            return self.data
# Allows for more flexible ticket names, as currently assumes ticket names will exactly match Day 2/Day 3
        valid_tickets = {"Full Access", day}
        return [person for person in self.data if person["Ticket"] in valid_tickets]



