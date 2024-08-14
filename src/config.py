import configparser

cfg = configparser.ConfigParser()
with open("config.txt", "rt") as f: 
    cfg.read_file(f)

port = cfg["DEFAULT"]["port"]
address = cfg["DEFAULT"]["address"]

display_line1 = cfg.getboolean("display", "line1", fallback=True)
display_line2 = cfg.getboolean("display", "line2", fallback=True)
display_line3 = cfg.getboolean("display", "line3", fallback=True)
