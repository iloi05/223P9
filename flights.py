# Name: Ivy Loi
# Date: 12/2/25
# Purpose of file: Create functions to be used in main file
import json

from datetime import datetime


class Flights:

    def __init__(self, filename, /):
        '''Initializing filename variable and opening json file'''
        self.filename = filename
        self.data_list = []
        try:
            with open(self.filename, "r") as f:
                self.data_list = json.load(f)
        except FileNotFoundError:
          print(f"Error: {self.filename} was not found.")
        

    def add_flight(self, origin, destination, flight_number, departure, next_day, arrival, /):
        '''Adding flight information to json file'''
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
        '''Used to calculate flight duration for get_flights'''
        d_h = int(departure[:2])
        d_m = int(departure[2:4])
        a_h = int(arrival[:2])
        a_m = int(arrival[2:4])

        d_tot = d_h * 60 + d_m
        a_tot = a_h * 60 + a_m

        if next_day.upper() == "Y":
            a_tot += 24 * 60

        duration = a_tot - d_tot
        h = duration // 60
        m = duration % 60

        return f"{h}:{m:02d}"
    
    def format_time(self, hhmm):
        '''Used to format time for get_flights'''
        h = int(hhmm[:2])
        m = int(hhmm[2:4])

        ampm = "am"
        if h == 0:
            h = 12
        elif h == 12:
            ampm = "pm"
        elif h > 12:
            h -= 12
            ampm = "pm"
        return f"{h}:{m:02d}{ampm}"

    def get_flights(self, /):
        '''Retrieves information stored in json file'''
        sorted_list = sorted(self.data_list, key=lambda f: int(f["departure"]))

        formatted = []

        for flight in sorted_list:
            origin = flight["origin"]
            destination = flight["destination"]
            flight_number = flight["flight_number"]
            
            departure = flight["departure"]
            arrival = flight["arrival"]
            next_day = flight["next_day"]

            dep_f = self.format_time(departure)
            arr_f = self.format_time(arrival)
            if next_day.upper() == "Y":
                arr_f = "+" + arr_f

            duration = self.calculate_duration(departure, arrival, next_day)

            formatted.append({
                "origin": origin,
                "destination": destination,
                "flight_number": flight_number,
                "departure": dep_f,
                "arrival": arr_f,
                "duration": duration
            })
        return formatted
    
    
    def print_flight_schedule(self):
        '''Used to print out information stored in json file'''
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

    def check_flight(self, flight_number):
        '''Checks if input is empty for flight_number'''
        return (len(flight_number) != 0)
        
    def valid_flight(self, flight_number):
        '''Checks if flight_number is just letters and numbers'''
        return flight_number.isalnum()

    def valid_origin(self, origin):
        '''Checks if origin is just letters'''
        if origin.isalpha() and origin.isupper():
            return True

    def valid_destination(self, destination):
        '''Checks if destination is just letters'''
        if destination.isalpha() and destination.isupper():
            return True   