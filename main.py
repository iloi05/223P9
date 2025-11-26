import flights

flights_list = flights.Flights("flights.json")

options = ["1", "2", "3", "9"]

while True:
    print("      *** TUFFY TITAN FLIGHT SCHEDULE MAIN MENU")
    print("1. Add flight")
    print("2. Print flight schedule")
    print("3. Set flight scedule filename")
    print("9. Exit the program")
    prompt = input("Enter menu choice: ")
    if prompt == "1":
        origin = input("Enter origin: ")
        destination = input("Enter destinaton: ")
        flight_number = input("Enter fligh number: ")
        departure_time = input("Enter departure time (HHMM): ")
        arrival_time = input("Enter arrival time (HHMM): ")
        next_day = input("Is arrival next day (Y/N): ")

        success = flights_list.add_flight(origin, destination, flight_number, departure_time, next_day, arrival_time)

        if success:
            print("Flight added.\n")
        else:
            print("Error: Invalid time format.\n")
    elif prompt == "2":
        flights_list.print_flight_schedule()
        print()
    elif prompt == "3":
        new_file = input("Enter new flight schedule filename: ")
        flights_list = flights.Flights(new_file)
        print(f"Filename set to {new_file}\n")
    
    elif prompt == "9":
        break

    if prompt not in options:
        print("That is not a valid menu option, try again")
        continue