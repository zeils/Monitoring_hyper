def check_and_append_log(filename, string):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            last_line = lines[-1].strip() if lines else None
    except FileNotFoundError:
        last_line = None

    if last_line != string:
        with open(filename, 'a') as file:
            file.write(string + '\n')