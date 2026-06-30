
import concurrent.futures

def time_up(current_time, time_limit= 60):
    """
    Input: 
        current_time, time_limit
    Output:
        - False if time limit has not been reached
        - True if time limit reached

    """
    return current_time >= time_limit