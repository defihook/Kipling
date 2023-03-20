import json
import os


def getJson(path):
    return json.load(open(path))


def writeJson(path, content):
    with open(path, 'w') as file:
        file.write(json.dumps(content, indent=4))


def doesFileExist(path):
    return os.path.isfile(path)


def doesDirExist(path):
    return os.path.isdir(path)


def getString(prompt):
    return input(f"{prompt}: ")


def getNumber(prompt):
    while True:
        try:
            return int(input(f"{prompt}: "))
        except ValueError:
            pass


def getFloat(prompt):
    while True:
        try:
            return float(input(f"{prompt}: "))
        except ValueError:
            pass


def getOptions(prompt, stop):
    options = []
    while True:
        options_joined = ', '.join(options)
        option = input(f"{prompt} (Type '{stop.upper()}' to end) - [{options_joined}]: ")
        if option.upper() == stop.upper():
            break
        options.append(option)
    return options
