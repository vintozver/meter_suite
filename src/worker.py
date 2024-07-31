import datetime
import json
import os
import sys
import time
import ekmmeters
import sqlite3
from . import db
from . import config


def main():
    port = ekmmeters.SerialPort(config.port)
    if port.initPort() == True:
        meter = ekmmeters.V4Meter(config.address)
        meter.attachPort(port)
    else:
        print("Cannot open port")
        return

    db_connection = sqlite3.connect("meter.db")
    raw = open("meter.raw", "wt")
 
    while True:
        if meter.request():
            read_buffer = meter.getReadBuffer()
            json_str = meter.jsonRender(read_buffer)
            raw.seek(0)
            raw.write(json_str)
            raw.truncate()
            raw.flush()
            bucket = json.loads(json_str)
            db_connection.execute(db.instant_reads_insert, (
                datetime.datetime.utcnow(),
                float(bucket["kWh_Ln_1"]), float(bucket["kWh_Ln_2"]), float(bucket["kWh_Ln_3"]), float(bucket["kWh_Tot"]), float(bucket["Reactive_Energy_Tot"]),
                float(bucket["RMS_Volts_Ln_1"]), float(bucket["RMS_Volts_Ln_2"]), float(bucket["RMS_Volts_Ln_3"]),
                float(bucket["Amps_Ln_1"]), float(bucket["Amps_Ln_2"]), float(bucket["Amps_Ln_3"]),
                float(bucket["RMS_Watts_Ln_1"]), float(bucket["RMS_Watts_Ln_2"]), float(bucket["RMS_Watts_Ln_3"]), float(bucket["RMS_Watts_Tot"]),
                int(bucket["Power_Factor_Ln_1"]), int(bucket["Power_Factor_Ln_2"]), int(bucket["Power_Factor_Ln_3"]),
                float(bucket["Reactive_Pwr_Ln_1"]), float(bucket["Reactive_Pwr_Ln_2"]), float(bucket["Reactive_Pwr_Ln_3"]), float(bucket["Reactive_Pwr_Tot"]),
            ))
            db_connection.commit()
            print("Total " + bucket["kWh_Tot"])
            time.sleep(4)  # 5 seconds read interval, including one second to read
        
if __name__ == '__main__':
    main()


