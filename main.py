import flights

flights_list = flights.Flights("flights.json")

options = ["1", "2", "3", "9"]
nd_input = ["Y", "y", "N", "n"]

while True:
    print("      *** TUFFY TITAN FLIGHT SCHEDULE MAIN MENU")
    print("1. Add flight")
    print("2. Print flight schedule")
    print("3. Set flight scedule filename")
    print("9. Exit the program")
    prompt = input("Enter menu choice: ")
    if prompt == "1":
        origin = input("Enter origin: ")
        if len(origin) == 0:
            print("Origin not provided, returning to main menu...")
            continue
        if not flights.valid_origin(origin):
            print("Airport does not exist, please only input letters. Returning to main menu...")
            continue
        destination = input("Enter destinaton: ")
        if len(destination) == 0:
            print("Origin not provided, returning to main menu...")
            continue
        if not flights.valid_destination(destination):
            print("Airport does not exist, please only input letters. Returning to main menu...")
            continue
        flight_number = input("Enter flight number: ")
        if not flights.check_flight(flight_number):
            print("Flight number not provided, up to six characters must be provided. Returning to main menu...")
            continue
        if not flights.valid_flight(flight_number):
            print("Invalid flight number given, only letters and numbers accepted. Returning to main menu...")
            continue
        departure_time = input("Enter departure time (HHMM): ")
        if len(departure_time) != 4:
            print("Invalid time length, enter only four digits (HHMM), military time is used.")
            continue
        arrival_time = input("Enter arrival time (HHMM): ")
        if len(arrival_time) != 4:
            print("Invalid time length, enter only four digits (HHMM), military time is used.")
            continue
        next_day = input("Is arrival next day (Y/N): ")
        if next_day not in nd_input:
            print("Not a valid answer, only input Y or N (lowercase is accepted), returning to main menu...")
            continue
        success = flights_list.add_flight(origin, destination, flight_number, departure_time, next_day, arrival_time)
        if not success:
            print("Unable to add flight. An invalid departure or arrival time was given... returning to main menu.")
            continue
        print("Flight succesfully added to system.\n")
    elif prompt == "2":
        flights_list.print_flight_schedule()
        print()
    elif prompt == "3":
        new_file = input("Enter flight schedule filename: ")
        flights_list = flights.Flights(new_file)
        if not flights_list:
            print(f"New file: {new_file} being made\n")
    elif prompt == "9":
        break

    if prompt not in options:
        print("That is not a valid menu option, try again")
        continue