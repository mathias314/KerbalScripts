import krpc
import time
import csv

conn = krpc.connect(name = "logger")
vessel = conn.space_center.active_vessel
frame = vessel.orbit.body.reference_frame

fileName = input("Enter csv file name (with .csv appended): ")

f = open(fileName, "w")
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

acceleration = 0
jerk = 0
gForce = 0
speed = 0

epsilon = .0000000000001

i = 1

while True:
    oldSpeed = speed
    oldAccel = acceleration
    oldTime = met()

    time.sleep(1)

    speed = vessel.flight(frame).speed
    acceleration = (speed - oldSpeed) / (met() - oldTime + epsilon) #causes problems if the craft has slight movement on the pad
    jerk = (acceleration - oldAccel) / (met() - oldTime + epsilon) #have to add epsilon to prevent divide from 0 error when on pad
    gForce = acceleration / 9.81

    row = [met(), altitude(), latitude(), longitude(), atmosphereDensity(), dynamicPressure(), totalAirTemp(), staticAirTemp(),
    speed, acceleration, jerk, gForce]

    csvwriter.writerow(row)

    i = i + 1
    print(str(i) + " write successful!")
