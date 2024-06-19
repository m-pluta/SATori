def printTime(time):
    if time == 0:
        return
    
    out = ''
    for unit in ['s', 'ms', 'us', 'ns']:
        if time >= 1:
            num = int(time)
            out += f'{num}{unit} '
            time -= num
        time *= 1000
    
    print(out.strip())