import csv

#Insert some code here
class DataHandler:
    def __init__(self, filename="festival_goers.csv"):
        """Initialize with a CSV filename and load data."""
        self.filename = filename
        #There's something fishy here 
        #self.data = self.load_from_csv() 
        self.data = [] 
        self.gigs = {
            "Day 1": ["Fink Ployd", "Psychedelic corn trumpets"],
            "Day 2": ["Porcupine Bush", "Fever Day"],
            "Day 3": ["Pearl Djam", "Soundbackyard"]
        }

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
        with open(self.filename, mode="w", newline="") as file:
            fieldnames = ["Name", "Age", "Distance", "Accommodation", "Ticket"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.data)

    def add_festival_goer(self, name, age, distance, accommodation, ticket_type):
        """Add a new festival-goer and save to CSV."""
        person = {
            "Name": name,
            "Age": age,
            "Distance": distance,
            "Accommodation": accommodation,
            "Ticket": ticket_type
        }
        self.data.append(person)
        self.save_to_csv()  # Save changes immediately

    def filter_by_ticket(self, ticket_type):
        """Return a list of people with a specific ticket type."""
        return [person for person in self.data if person["Ticket"] != ticket_type]

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
        return [person for person in self.data if person["Ticket"] in ["Full Access", f"{day}"]]