import json
import datetime
import time

HISTORY_FILE = "data/routine_history.json"
TEMPLATE_FILE = "data/routine_template.json"

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
    workouts = []
    session_record = 0
    session_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    start_time = time.perf_counter()
    while True:
        exercise = get_str("Exercise name: ")
        weight = get_float("Weight: ")
        sets = get_int("Number of sets: ")
        reps = get_int("Number of reps: ")

        workout = {
                "exercise": exercise,
                "weight": weight,
                "sets": sets,
                "reps": reps
                }
        workouts.append(workout)

        current_volume = weight * sets * reps
        
        try:
            with open(HISTORY_FILE, "r") as f:
                for line in f:
                    if not line.strip():
                        continue
                    session = json.loads(line)
                    for workout in session['exercises']:
                        if workout['exercise'] == exercise:
                            if weight > get_max_weight(exercise):
                                session_record += 1
                            if current_volume > get_max_volume(exercise):
                                session_record += 1
        except FileNotFoundError:
            previous_session = {
                    "date": None,
                    "time": None,
                    "records": None,
                    "exercises": []
                    }
        except json.JSONDecodeError:
            print("Workout history file is corrupted.")
            return

        option = get_str("Add another workout? (y/n)")
        if option == "n":
            end_time = time.perf_counter()
            total_seconds = int(end_time - start_time)
            workouts = {
                    "date": session_date,
                    "time": total_seconds,
                    "records": session_record,
                    "exercises": workouts
                    }
            with open(HISTORY_FILE, "a") as f:
                json.dump(workouts, f)
                f.write("\n")
            break

def view_workout():
    if not workouts:
        print("No workout has been added yet.")
    else:
        for i, w in enumerate(workouts, start=1):
            print("---------------------------------")
            print(f"{i}. {w['exercise']} - "
            f"{w['sets']}x{w['reps']} @ {w['weight']}kg")
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

def view_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            lines = f.readlines()
            for line in reversed(lines):
                if not line.strip():
                    continue
                session = json.loads(line)
                print("------------------------------------------")
                print(f"Session date: {session['date']}")
                print("------------------------------------------")
                total_seconds = session['time']
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                if hours > 0:
                    print(f"Time: {hours}h {minutes}m {seconds}s", end="")
                elif minutes > 0:
                    print(f"Time: {minutes}m {seconds}s", end="")
                else:
                    print(f"Time: {seconds}s", end="")
                for ex in session['exercises']:
                    total_volume = sum(ex['weight'] *
										ex['sets'] *
										ex['reps'] for ex in
										session['exercises'])
                print(f" | Volume: {total_volume}kg | "
                f"Records: {session['records']}")
                print("------------------------------------------")
                for i, w in enumerate(session['exercises'], start=1):
                    print(f"{i}. {w['exercise']} - "
                          f"{w['sets']}x{w['reps']} @ {w['weight']}kg")
                print("------------------------------------------")
	
    except FileNotFoundError:
        print("No previous workout history is found.")
        return
    except json.JSONDecodeError:
        print("Workout history file is corrupted.")
        return

def get_max_volume(exercise):
    max_volume = 0
    try:
        with open(HISTORY_FILE, "r") as f:
            for line in f:
                if not line.strip():
                    continue
                session = json.loads(line)
                for workout in session['exercises']:
                    if workout['exercise'] == exercise:
                        volume = (workout['weight'] *
							workout['sets'] *
							workout['reps'])
                        if volume > max_volume:
                            max_volume = volume
    except FileNotFoundError:
        print("No previous workout history is found.")
        return 0
    except json.JSONDecodeError:
        print("Workout history file is corrupted.")
        return 0

    return max_volume

def get_max_weight(exercise):
    max_weight = 0
    try:
        with open(HISTORY_FILE, "r") as f:
            for line in f:
                if not line.strip():
                    continue
                session = json.loads(line)
                for workout in session['exercises']:
                    if workout['exercise'] == exercise:
                        weight = workout['weight']
                        if weight > max_weight:
                            max_weight = weight
    except FileNotFoundError:
        print("No previous workout history is found.")
        return 0
    except json.JSONDecodeError:
        print("Workout history file is corrupted.")
        return 0

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
            previous_session = {
                    "date": None,
                    "time": None,
                    "records": None,
                    "exercises": []
                    }
        else:
            previous_session = json.loads(lines[-1])
    except FileNotFoundError:
        previous_session = {
                "date": None,
                "time": None,
                "records": None,
                "exercises": []
                }
    except json.JSONDecodeError:
        print("Workout history file is corrupted.")
        return

    session_records = 0
    session_workout = []

    start_time = time.perf_counter()
    for ex in routine:
        print(f"Exercise: {ex}")
        previous_weight = next((e['weight']
                                for e in previous_session['exercises']
                                if e['exercise'] == ex), None)
        previous_set = next((e['sets']
                             for e in previous_session['exercises']
                             if e['exercise'] == ex), None)
        previous_rep = next((e['reps']
                             for e in previous_session['exercises']
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

        if weight > max_weight:
            print("Congratulations! You've hit a new weight PR!")
            session_records += 1
        if current_volume > max_volume:
            print("Congratulations! You've hit a new volume PR!")
            session_records += 1

        workout = {
                "exercise": ex,
                "weight": weight,
                "sets": sets,
                "reps": reps
                }
        session_workout.append(workout)
    
    end_time = time.perf_counter()
    total_seconds = int(end_time - start_time)
    session_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    session_data = {
            "date": session_date,
            "time": total_seconds,
            "records": session_records,
            "exercises": session_workout
            }

    with open(HISTORY_FILE, "a") as f:
        json.dump(session_data, f)
        f.write("\n")

    total_volume = sum(w['weight']
                       * w['sets']
                       * w['reps'] for w in session_workout)
    print("------------------------------------------")
    print("Session summary:")
    print("------------------------------------------")
    print(f"{session_date}")
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    if hours > 0:
        print(f"Time: {hours}h {minutes}m {seconds}s", end="")
    elif minutes > 0:
        print(f"Time: {minutes}m {seconds}s", end="")
    else:
        print(f"Time: {seconds}s", end="")
    print(f" | Volume: {total_volume}kg | "
    f"Records: {session_records}")
    print("------------------------------------------")
    for i, w in enumerate(session_workout, start=1):
        print(f"{i}. {w['exercise']} - "
              f"{w['sets']}x{w['reps']} @ {w['weight']}kg")
    print("------------------------------------------")

def clear_history():
    open("data/routine_history.json", "w").close()

def main():
    print("Welcome to gym tracker 101")
    while True:
        print("1. Add workout")
        print("2. Remove workout")
        print("3. View workouts")
        print("4. Start routine")
        print("5. View workout history")
        print("6. Clear workout history")
        print("7. Exit")

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
            view_history()

        elif choice == "6":
            clear_history()

        elif choice == "7":
            break

        else:
            print("Please choose a valid option.")

main()
