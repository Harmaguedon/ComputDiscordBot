import re
import os

def capitalize(argument):
    return str(argument)[0].upper() + str(argument)[1:]

def lower(argument):
    return str(argument).lower()

def anti_capitalize(argument):
    return str(argument)[0].lower() + str(argument)[1:]

def find_matching_files(path, *args):
    regex = "(.)*"
    matching_files = []
    for arg in args:
        regex += "{}(.)*".format(arg)
    regex = re.compile(regex)
    files = os.listdir(path)
    files_sorted = sorted(files)
    for f in files_sorted:
        if re.match(regex, f):
            matching_files.append(f)
    return matching_files
