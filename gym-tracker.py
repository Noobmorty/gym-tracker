import json

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

def add_workout():
    while True:
        exercise = input("Exercise name: ")
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

        option = input("Add another workout? (y/n)")
        if option == "n":
            routineyn = input("Save this workout as a routine? (y/n)")
            if routineyn == "y":
                with open("routine_history.json", "w") as f:
                    json.dump(workouts, f)
                with open("routine_template.json", "w") as f:
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
        
    option = int(input("Enter the number of the exercise to remove: "))
    if 1 <= option <= len(workouts):
        workouts.pop(option-1)
        print("Exercise removed.")
    else:
        print("Invalid option.")

def start_routine():
    try:
        with open("routine_template.json", "r") as f:
            routine = json.load(f)
    except FileNotFoundError:
        print("No saved routine template is found.")
        return
    except json.JSONDecodeError:
        print("Routine template file is corrupted.")
        return

    try:
        with open("routine_history.json", "r") as f:
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
        print(f"Previous weight:", next((e['weight'] for e in previous_session if e['exercise'] == ex), None), end=" ")
        weight = get_float("|| Weight: ")
        print(f"Previous set:", next((e['sets'] for e in previous_session if e['exercise'] == ex), None), end=" ")
        sets = get_int("|| Number of sets: ")
        print(f"Previous rep:", next((e['reps'] for e in previous_session if e['exercise'] == ex), None), end=" ")
        reps = get_int("|| Number of reps: ")
    
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

        choice = input("Choose: ")

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
