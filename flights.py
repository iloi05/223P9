import json

class Flights:

    def __init__(self, filename, /):
        self.filename = filename
        self.data_list = []
        try:
            with open(self.filename, "r") as f:
                self.data_list = json.load(f)
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")

    def add_flight(self, origin_string, destination, flight_number, departure, next_day, arrival, /):
        if not (departure.isdigit() and len(departure) == 4):
            return False
        if not(arrival.isdigit() and len(arrival) == 4):
            return False

        flight = {
            "origin": origin_string,
            "destination": destination,
            "flight_number": flight_number,
            "departure": departure,
            "next day": next_day,
            "arrival": arrival
        }      
        self.data_list.append(flight)
        with open(self.filename, "w") as f:
            json.dump(self.data_list, f, indent=4)
        return True
    
    def get_flights(self, /):
        formatted = []

        for flight in self.data_list:
            origin = flight["origin"]
            destination = flight["destination"]
            flight_number = flight["flight_number"]
            
            departure = flight["departure"]
            arrival = flight["arrival"]
            next_day = flight["next_day"]

            departure_fmt = self.format_time(departure)
            arrival_fmt = self.format_time(arrival)
            if next_day.upper() == "Y":
                arrival_fmt = "+" + arrival_fmt

            duration = self.calculate_duration(departure, arrival, next_day)

            formatted.append({
                "origin": origin,
                "destination": destination,
                "flight_number": flight_number,
                "departure": departure_fmt,
                "arrival": arrival_fmt,
                "duration": duration
            })
        return formatted
    
    def print_flight_schedule(self):
        flights = self.get_flights()

        if not flights:
            print("No flights scheduled, please schedule one first.")
            return
        
        print("================== FLIGHT SCHEDULE ==================")
        print("Origin Destination Number Departure  Arrival Duration")
        print("====== =========== ====== ========= ======== ========")

        for f in flights:
            print(f"{f['origin']:<6} {f['destination']:<11} {f['flight_number']:<6} "
                  f"{f['departure']:<9} {f['arrival']:<9} {f['duration']:<7}")
        