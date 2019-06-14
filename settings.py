# configuration and preferences
from main import location

def get_settings():
    print("loading settings from file...")
    settings = dict()
    with open(location+"settings.conf", "r") as f:
        for pair in f.readlines():
            key, value = pair.split("=")
            value = value.strip()  
            
            try:
                value = {"true":True, "false":False}[value.lower()]
            except KeyError:
                try:
                    value = int(value)
                except ValueError:
                    pass

            settings[key] = value
    print("settings loaded!")
    return settings

def set_settings():
    print("saving settings to file...")
    with open(location+"settings.conf", "w+") as f:
        for key, value in settings:
            f.write(f"{key}={value}\n")
    print("settings exported!")




