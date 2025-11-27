import json

from datetime import datetime

def valid_time(time, fmt_string = "%H%M"):
    try:
        datetime.strptime(time, fmt_string)
        return True
    except ValueError:
        return False

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
            "next_day": next_day,
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
    
    def format_time(self, hhmm):
        hour = int(hhmm[:2])
        minute = int(hhmm[2:4])

        suffix = "am"
        if hour == 0:
            hour = 12
        elif hour == 12:
            suffix = "pm"
        elif hour > 12:
            hour -= 12
            suffix = "pm"
        return f"{hour}:{minute:02d}{suffix}"
    
    def calculate_duration(self, departure, arrival, next_day):
        dep_h = int(departure[:2])
        dep_m = int(departure[2:4])
        arr_h = int(arrival[:2])
        arr_m = int(arrival[2:4])

        dep_total = dep_h * 60 + dep_m
        arr_total = arr_h * 60 + arr_m

        if next_day.upper() == "Y":
            arr_total += 24 * 60

        duration = arr_total - dep_total
        hours = duration // 60
        minutes = duration % 60

        return f"{hours}:{minutes:02d}"
    
    def print_flight_schedule(self):
        flights = self.get_flights()

        if not flights:
            print("No flights scheduled, please schedule one first.")
            return
        
        print("================== FLIGHT SCHEDULE ==================")
        print("Origin Destination Number Departure  Arrival Duration")
        print("====== =========== ====== ========= ======== ========")

        for f in flights:
            print(f"{f['origin']:<6} {f['destination']:<10} {f['flight_number']:>7} "
                  f"{f['departure']:>9} {f['arrival']:>8} {f['duration']:>8}")
        