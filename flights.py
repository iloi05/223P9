import json

from datetime import datetime

    
def check_flight(flight_number):
        return (flight_number != 0)
        
def valid_flight(flight_number):
    return flight_number.isalnum()

def valid_origin(origin):
    return origin.isalpha()

def valid_destination(destination):
    return destination.isalpha()


class Flights:

    def __init__(self, filename, /):
        self.filename = filename
        self.data_list = []
        try:
            with open(self.filename, "r") as f:
                self.data_list = json.load(f)
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found...\n Creating new file now:{self.filename}")
        

    def add_flight(self, origin, destination, flight_number, departure, next_day, arrival, /):
        try:
            datetime.strptime(departure, "%H%M")
        except ValueError:
            return False
        
        try:
            datetime.strptime(arrival, "%H%M")
        except ValueError:
            return False

        flight = {
            "origin": origin,
            "destination": destination,
            "flight_number": flight_number,
            "departure": departure,
            "next_day": next_day,
            "arrival": arrival
        }      
        self.data_list.append(flight)
        with open(self.filename, "w") as f:
            json.dump(self.data_list, f, indent=1)
        return True
    
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

    def get_flights(self, /):
        sorted_list = sorted(self.data_list, key=lambda f: int(f["departure"]))

        formatted = []

        for flight in sorted_list:
            origin = flight["origin"]
            destination = flight["destination"]
            flight_number = flight["flight_number"]
            
            departure = flight["departure"]
            arrival = flight["arrival"]
            next_day = flight["next_day"]

            dep_fmt = self.format_time(departure)
            arr_fmt = self.format_time(arrival)
            if next_day.upper() == "Y":
                arr_fmt = "+" + arr_fmt

            duration = self.calculate_duration(departure, arrival, next_day)

            formatted.append({
                "origin": origin,
                "destination": destination,
                "flight_number": flight_number,
                "departure": dep_fmt,
                "arrival": arr_fmt,
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
            print(f"{f['origin']:<6} {f['destination']:<10} {f['flight_number']:>7} "
                  f"{f['departure']:>9} {f['arrival']:>8} {f['duration']:>8}")
        