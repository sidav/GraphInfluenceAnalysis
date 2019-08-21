def progressBar(title, value, endvalue, bar_length=20):
    import sys
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\r" + title + " [{0}] {1}% ({2} out of {3})".format(arrow + spaces, int(round(percent * 100)), value, endvalue))
    if value == endvalue:
        sys.stdout.write("\n")
    sys.stdout.flush()
