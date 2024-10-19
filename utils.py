from datetime import timedelta

def add_time(start_time_str, minutes_to_add):
        start_time_obj = timedelta(hours=int(start_time_str.split(":")[0]), 
                                   minutes=int(start_time_str.split(":")[1]), 
                                   seconds=int(start_time_str.split(":")[2]))
        end_time_obj = start_time_obj + timedelta(seconds=minutes_to_add*60)
        return str(end_time_obj)