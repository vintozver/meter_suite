import configparser

cfg = configparser.ConfigParser()
with open("config.txt", "rt") as f: 
    cfg.read_file(f)

port = cfg["DEFAULT"]["port"]
address = cfg["DEFAULT"]["address"]
