import krpc
import time
import csv

conn = krpc.connect(name = "logger")
vessel = conn.space_center.active_vessel
frame = vessel.orbit.body.reference_frame

f = open("shuttleAbort.csv", "w")
csvwriter = csv.writer(f)

met = conn.add_stream(getattr, vessel, 'met')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
latitude = conn.add_stream(getattr, vessel.flight(), 'latitude')
longitude = conn.add_stream(getattr, vessel.flight(), 'longitude')
atmosphereDensity = conn.add_stream(getattr, vessel.flight(), 'atmosphere_density')
dynamicPressure = conn.add_stream(getattr, vessel.flight(), 'dynamic_pressure')
totalAirTemp = conn.add_stream(getattr, vessel.flight(), 'total_air_temperature')
staticAirTemp = conn.add_stream(getattr, vessel.flight(), 'static_air_temperature')

fields = ['time', 'altitude', 'latitude', 'longitude', 'atmosphereDensity',
'dynamicPressure', 'totalAirTemp', 'staticAirTemp', 'speed', 'acceleration', 'jerk', 'gForce']

csvwriter.writerow(fields)

speed = 0
acceleration = 0

i = 0

while True:
    oldSpeed = speed
    oldAccel = acceleration

    time.sleep(1)

    speed = vessel.flight(frame).speed
    acceleration = speed - oldSpeed
    jerk = acceleration - oldAccel
    gForce = acceleration / 9.81

    row = [met(), altitude(), latitude(), longitude(), atmosphereDensity(), dynamicPressure(), totalAirTemp(), staticAirTemp(),
    speed, acceleration, jerk, gForce]

    csvwriter.writerow(row)

    i = i + 1
    print(str(i) + " write successful!")
