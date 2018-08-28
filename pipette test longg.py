# 
from opentrons import robot, containers, instruments
from itertools import chain



tiprack = containers.load('tiprack-200ul', 'A2', 'tiprack')
wash_basin = containers.load('point', 'B2', 'wash basin')
cellwell = containers.load('96-PCR-flat', 'C1', 'cells')

p200_multi = instruments.Pipette(
    axis='a',
    name='small volume pipette',
    max_volume=200,
    min_volume=50,
    channels=8)
	
p200_multi.pick_up_tip(tiprack.wells('A1'))

lots_of_pipetting = 200
for pipetting in range(0, lots_of_pipetting):
    p200_multi.transfer(200, wash_basin.rows(), cellwell.rows(0)) 