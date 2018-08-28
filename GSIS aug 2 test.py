#GSIS Opentrons Protocol
#Last Updated: July 27, 2018

from opentrons import robot, containers, instruments
from itertools import chain

# ~~~~~~~~~~~ SET UP ~~~~~~~~~~
# max_speed_per_axis = { # Head Speed
 # 'x': 2000, 'y': 1000, 'z':500, 'a':500, 'b':500, 'c':200}
# robot.head_speed(
    # combined_speed=max(max_speed_per_axis.values()), **max_speed_per_axis)

tiprack = containers.load('tiprack-200ul', 'A2', 'tiprack')
waste = containers.load('96-deep-well', 'D2', 'waste') #waste in deep well to see cells in case speed has an impact in disruptions 
wash_basin = containers.load('point', 'B2', 'wash basin')
cellwell = containers.load('96-PCR-flat', 'C1', 'cells') #microwell plate with cells in it #place hot plate beneath, 37 degrees.
output_low = containers.load('96-PCR-flat', 'B1', 'output low')
output_high = containers.load('96-PCR-flat', 'A1', 'output high')

containers.create(
    'troughrow',
    grid=(8,4),
    spacing=(10,30),
    diameter=6,
    depth=35)

glucose_medium = containers.load('troughrow', 'D1', 'glucose medium')

LOW_GLUCOSE_MEDIUM_ROWS = '1' #'2', '3']
#1st & 2nd rows of trough (from front to back) require 15mL low glucose medium
#3rd row requires 16mL low glucose medium

HIGH_GLUCOSE_MEDIUM_LOCATION = '4'
#4th row requires 16mL low glucose medium

p200_multi_low_speed = instruments.Pipette( # Lowest pipette speed, use for washing
    axis='a',
    name='pip200low',
    max_volume=200,
    min_volume=20,
    channels=8,
    tip_racks=[tiprack],
    trash_container=waste,
    aspirate_speed=300,
    dispense_speed=150)

p200_multi_default_speed = instruments.Pipette( # Middle speed 
    axis='a',
    name='pip200default',
    max_volume=200,
    min_volume=20,
    channels=8,
    tip_racks=[tiprack],
    trash_container=waste,
    aspirate_speed=300,
    dispense_speed=400)
    
p200_multi_high_speed = instruments.Pipette( # high dispense speed, robot max
    axis='a',
    name='pip200high',
    max_volume=200,
    min_volume=20,
    channels=8,
    tip_racks=[tiprack],
    trash_container=waste,
    aspirate_speed=300,
    dispense_speed=1200)


    
                                        ########## transfer command removed and approved 
p200_multi_low_speed.aspirate(200, wash_basin.rows(0))
p200_multi_low_speed.dispense(200, cellwell.rows(0))
        
                                        ########## transfer command removed and approved 
p200_multi_default_speed.aspirate(200, wash_basin.rows(0))
p200_multi_default_speed.dispense(200, cellwell.rows(0))

p200_multi_high_speed.aspirate(200, wash_basin.rows(0))
p200_multi_high_speed.dispense(200, cellwell.rows(0))
robot.home()




