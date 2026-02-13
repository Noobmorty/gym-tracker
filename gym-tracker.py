import json

HISTORY_FILE = "data/routine_history.json"
TEMPLATE_FILE = "data/routine_template.json"

workouts = []
routine_template = []

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a number!")

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a number!")

def get_str(prompt):
    while True:
        try:
            return str(input(prompt))
        except ValueError:
            print("Please enter a string!")

def add_workout():
    while True:
        exercise = get_str("Exercise name: ")
        weight = get_float("Weight: ")
        sets = get_int("Number of sets: ")
        reps = get_int("Number of reps: ")

        routine_template.append(exercise)
        workout = {
                "exercise": exercise,
                "weight": weight,
                "sets": sets,
                "reps": reps
                }

        workouts.append(workout)

        option = get_str("Add another workout? (y/n)")
        if option == "n":
            routineyn = get_str("Save this workout as a routine? (y/n)")
            if routineyn == "y":
                with open(HISTORY_FILE, "w") as f:
                    json.dump(workouts, f)
                with open(TEMPLATE_FILE, "w") as f:
                    json.dump(routine_template, f)
                break
            elif routineyn == "n":
                break

def view_workout():
    if not workouts:
        print("No workout has been added yet.")
    else:
        for i, w in enumerate(workouts, start=1):
            print("---------------------------------")
            print(f"{i}. {w['exercise']} - {w['sets']}x{w['reps']} @ {w['weight']}kg")
            print("---------------------------------")

def remove_workout():
    if not workouts:
        print("No workout has been added yet.")

    for i, w in enumerate(workouts, start=1):
        print("-----------------")
        print(f"{i}. {w['exercise']}")
        print("-----------------")
        
    option = get_int("Enter the number of the exercise to remove: ")
    if 1 <= option <= len(workouts):
        workouts.pop(option-1)
        print("Exercise removed.")
    else:
        print("Invalid option.")

def get_max_volume(exercise):
    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("No previous workout history is found.")
        return 0
    except json.JSONDecodeError:
        print("Workout history file is corrupted.")
        return 0

    max_volume = 0

    for workout in data:
        if workout['exercise'] == exercise:
            volume = workout['weight'] * workout['sets'] * workout['reps']
            if volume > max_volume:
                max_volume = volume
    
    return max_volume

def get_max_weight(exercise):
    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("No previous workout history is found.")
        return 0
    except json.JSONDecodeError:
        print("Workout history file is corrupted.")
        return 0

    max_weight = 0

    for workout in data:
        if workout['exercise'] == exercise:
            weight = workout['weight']
            if weight > max_weight:
                max_weight = weight

    return max_weight

def start_routine():
    try:
        with open(TEMPLATE_FILE, "r") as f:
            routine = json.load(f)
    except FileNotFoundError:
        print("No saved routine template is found.")
        return
    except json.JSONDecodeError:
        print("Routine template file is corrupted.")
        return

    try:
        with open(HISTORY_FILE, "r") as f:
            lines = f.readlines()

        if not lines:
            print("No previous workout history is found.")
        previous_session = json.loads(lines[-1])
    except FileNotFoundError:
        print("No workout history file is found.")
        return
    except json.JSONDecodeError:
        print("Workout history file is corrupted.")
        return

    session_workout = []
    for ex in routine:
        print(f"Exercise: {ex}")
        previous_weight = next((e['weight']
                                for e in previous_session
                                if e['exercise'] == ex), None)
        previous_set = next((e['sets']
                             for e in previous_session
                             if e['exercise'] == ex), None)
        previous_rep = next((e['reps']
                             for e in previous_session
                             if e['exercise'] == ex), None)

        print(f"Previous weight:", previous_weight, "|", end=" ")
        print(f"Previous set:", previous_set, "|", end=" ")
        print(f"Previous rep:", previous_rep)
        weight = get_float("Weight: ")
        sets = get_int("Number of sets: ")
        reps = get_int("Number of reps: ")

        current_volume = weight * sets * reps
        max_volume = get_max_volume(ex)
        max_weight = get_max_weight(ex)

        if (weight > max_weight) or
        (weight == previous_weight and reps > previous_rep) or
        (current_volume > max_volume):
            print("Congratulations! You hit a new personal record!")

        workout = {
                "exercise": ex,
                "weight": weight,
                "sets": sets,
                "reps": reps
                }
        session_workout.append(workout)
    
    with open("routine_history.json", "a") as f:
        json.dump(session_workout, f)
        f.write("\n")

def clear_history():
    open("routine_history.json", "w").close()

def main():
    print("Welcome to gym tracker 101")
    while True:
        print("1. Add workout")
        print("2. Remove workout")
        print("3. View workouts")
        print("4. Start routine")
        print("5. Clear routine history")
        print("6. Exit")

        choice = get_str("Choose: ")

        if choice == "1":
            add_workout()

        elif choice == "2":
            remove_workout()

        elif choice == "3":
            view_workout()

        elif choice == "4":
            start_routine()

        elif choice == "5":
            clear_history()

        elif choice == "6":
            break

        else:
            print("Please choose a valid option.")

main()
