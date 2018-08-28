# Pipette Accuracy test for Auguest 7th
# 
from opentrons import robot, containers, instruments
from itertools import chain



tiprack = containers.load('tiprack-200ul', 'A2', 'tiprack')
wash_basin = containers.load('point', 'B2', 'wash basin')
cellwell = containers.load('96-PCR-flat', 'C1', 'cells')

p50_multi = instruments.Pipette(
    axis='a',
    name='small volume pipette',
    max_volume=50,
    min_volume=5,
    channels=8)
	
p50_multi.pick_up_tip(tiprack.wells('A1'))

p50_multi.aspirate(50, wash_basin(0)) 
p50_multi.dispense(50, cellwell('A1'))
p50_multi.touch_tip()
p50_multi.blow_out()