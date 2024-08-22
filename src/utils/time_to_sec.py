def time_to_sec(time_str):
    time_str = time_str.lower()
    if'm' in time_str:
        time_num = int(time_str.split('m')[0])
        time_sec = time_num * 60
    elif 'h' in time_str:
        time_num = int(time_str.split('h')[0])
        time_sec = time_num * 60 * 60
    elif 'd' in time_str:
        time_num = int(time_str.split('d')[0])
        time_sec = time_num * 24 * 60 * 60
    elif 'w' in time_str:
        time_num = int(time_str.split('w')[0])
        time_sec = time_num * 7 * 24 * 60 * 60
    elif 'y' in time_str:
        time_num = int(time_str.split('y')[0])
        time_sec = time_num * 365 * 24 * 60 * 60
    else:
        time_sec = int(time_str)
    return time_sec