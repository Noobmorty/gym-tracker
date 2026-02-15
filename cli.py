import datetime
import time
from core import get_max_volume, get_max_weight, format_time
import storage as s

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

def print_session_summary(session):
    total_volume = sum(w['weight'] * 
                       w['sets'] * 
                       w['reps'] 
                       for w in session['exercises'])
    print("------------------------------------------")
    print("Session summary:")
    print("------------------------------------------")
    print(f"{session['date']}")
    print(f"Time: {format_time(session['time'])} | Volume: {total_volume}kg "
          f"| Records: {session['records']}")
    print("------------------------------------------")
    for i, w in enumerate(session['exercises'], start=1):
        print(f"{i}. {w['exercise']} - "
              f"{w['sets']}x{w['reps']} @ {w['weight']}kg")
    print("------------------------------------------")

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

        if weight > get_max_weight(exercise):
            session_record += 1
        if weight * sets * reps > get_max_volume(exercise):
            session_record += 1

        option = get_str("Add another workout? (y/n) ")
        if option == "n":
            break

    end_time = time.perf_counter()
    total_seconds = int(end_time - start_time)
    session_data = {
            "date": session_date,
            "time": total_seconds,
            "records": session_record,
            "exercises": workouts
            }
    s.save_session(session_data)
    print_session_summary(session_data)

def new_routine():
    exercises = []
    routine_name = get_str("Routine title: ")
    while True:
        exercise = get_str("Exercise name: ")
        exercises.append(exercise)
        opt = get_str("Add another exercise? (y/n) ")
        if opt == "n":
            routine_template = {
                    routine_name: exercises
                    }
            s.save_template(routine_template)
            break

def view_history():
    history = s.load_history()

    if not history:
        print("No previous workout history is found.")
        return

    for session in reversed(history):
        print_session_summary(session)

def start_routine():
    routines = s.load_templates()
    if not routines:
        print("No saved routine template is found.")
        return

    routine_list = []
    for r in routines:
        for routine_name, exercises in r.items():
            routine_list.append((routine_name, exercises))
            print(f"{len(routine_list)}. {routine_name}")

    history = s.load_history()
    if history:
        previous_session = history[-1]
    else:
        previous_session = {
                "date": None,
                "time": None,
                "records": None,
                "exercises": []
                }

    while True:
        opt = get_int("Choose the routine number you want to proceed with. ")
        if 1 <= opt <= len(routine_list):
            break
        print("Please enter a valid routine number!")

    routine_name, routine = routine_list[opt-1]
    
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

    s.save_session(session_data)
    print_session_summary(session_data)
    
def main():
    print("Welcome to gym tracker 101")
    while True:
        print("1. Start new workout")
        print("2. New routine")
        print("3. Start routine")
        print("4. View workout history")
        print("5. Clear workout history")
        print("6. Exit")

        choice = get_str("Choose: ")

        if choice == "1":
            add_workout()

        elif choice == "2":
            new_routine()

        elif choice == "3":
            start_routine()

        elif choice == "4":
            view_history()

        elif choice == "5":
            s.clear_history()

        elif choice == "6":
            break

        else:
            print("Please choose a valid option.")
