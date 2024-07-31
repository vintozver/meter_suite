# EKM metering local suite

This software is intended to run on the Raspberry Pi, installed on Andino X1 or similar platform.
It's expected that you already have the hardware set up:
* installed EKM v3 or v4 meter, current transformeters etc.
* wired RS485 bus to the Andino or similar interface
* set up necessary drivers, overlays - to expose RS485 serial (tty) interface in the OS
* install supervisord or similar process management software, to run fetch process, HTTP service

## Installation
```
pip3 install meter_suite
```

Then, create the *meter_suite_data* (or similar) configuration folder, which must be set as a current folder - when running the parts of the suite.

Create *config.txt* configuration file inside of the *meter_suite_data* folder:

```
[DEFAULT]
# ttyS file to the RS485 interface
port = /dev/ttySC0
# your meter address
address = 300003101
```

Create database
```
$ python3
>>> import sqlite3
>>> import meter_suite.db
>>> db = sqlite3.connect("meter.db")
>>> db.execute(meter_suite.db.instant_reads)
>>> db.commit()
```

Copy *supervisor.conf* file to your supervisord config, and adjust the settings accordingly.

Lastly, hook up your reverse proxy to the *meter_suite_data/http.socket* - this will be serving the interface.

You're all set!

### Multiple instances
If you have multiple meters, create a unique *meter_suite_data* folder and config per meter.
Multiple meters on the same bus support is planned.

## Usage
Meter will be read every 5 seconds automatically, and the data will be dumped into the *meter_suite_data/meter.db*
Requests to the */latest* uri will produce last 24h of datetime/kWh reads.
Requests to all other uris will produce last good raw read.

