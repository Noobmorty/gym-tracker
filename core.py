from storage import HISTORY_FILE, load_history

def get_max_volume(exercise):
    max_volume = 0
    history = load_history()
    for session in history:
        for workout in session['exercises']:
            if workout['exercise'] == exercise:
                volume = (workout['weight'] *
                          workout['sets'] *
                          workout['reps'])
                if volume > max_volume:
                    max_volume = volume
    return max_volume

def get_max_weight(exercise):
    max_weight = 0
    history = load_history()
    for session in history:
        for workout in session['exercises']:
            if workout['exercise'] == exercise:
                weight = workout['weight']
                if weight > max_weight:
                    max_weight = weight
    return max_weight

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"
