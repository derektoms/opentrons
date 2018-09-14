# GSIS Opentrons Protocol
# Last Updated: September 13th, 2018

from opentrons import robot, containers, instruments
from itertools import chain

# ~~~~~~~~~~~ SET UP ~~~~~~~~~~
#max_speed_per_axis = { # Head Speed
# 'x': 2000, 'y': 1000, 'z':500, 'a':500, 'b':500, 'c':200}
#robot.head_speed(
#    combined_speed=max(max_speed_per_axis.values()), **max_speed_per_axis)
robot.head_speed(z=1200)

tipracks = [
    containers.load('tiprack-200ul', slot)
    for slot in ['D2', 'E2']]

## Tyler's custom 8-trough container (treated as 4, because of the way BD made them)
containers.create(
    'trough-8row',
    grid=(8,4),
    spacing=(9,30),
    diameter=6,
    depth=35)

## Very deep 96-well plate (2.5 ml)
containers.create(
    '96-very-deep-well',
    grid=(8,12),
    spacing=(9,9),
    diameter=6,
    depth=43)
	
## VWR 1.2-ml sample tubes
containers.create(
    '96-sample-tubes',
    grid=(8,12),
    spacing=(9,9),
    diameter=6,
    depth=44.6)

	
wastePlate = containers.load('96-very-deep-well', 'C2', 'Waste plate') #waste in deep well to see cells in case speed has an impact in disruptions 
trash = containers.load('point','D1','Tip trash')

washBasin = containers.load('trough-12row', 'A1', 'KRBH low glucose') 
reservoirs = containers.load('96-deep-well', 'B2', 'Solution reservoirs')

samplePlate = containers.load('96-sample-tubes', 'B1', 'Sample plate - place on heater') # Deep well plate with samples; hot plate beneath, 37 °C.
collectionPlate = containers.load('384-plate', 'C1', '384-well collection plate')

    
p300_multi_high_speed = instruments.Pipette( # high dispense speed, robot max, use for washing columns 7-11
    axis='a',
    name='P300 Multichannel pipette, high dispense speed',
    max_volume=300,
    min_volume=30,
    channels=8,
    tip_racks=tipracks,
    trash_container=trash,
    aspirate_speed=300,
    dispense_speed=540)

p300_multi_low_speed = instruments.Pipette( # Lowest pipette speed, use for washing and columns 0-3
    axis='a',
    name='P300 Multichannel pipette, low dispense speed',
    max_volume=300,
    min_volume=30,
    channels=8,
    tip_racks=tipracks,
    trash_container=trash,
    aspirate_speed=300,
    dispense_speed=120)

p300_multi_default_speed = instruments.Pipette( # Middle speed. This 'pipette' will operate during the rows 4-7. default speed  
    axis='a',
    name='P300 Multichannel pipette, default dispense speed',
    max_volume=300,
    min_volume=30,
    channels=8,
    tip_racks=tipracks,
    trash_container=trash,
    aspirate_speed=300,
    dispense_speed=400)
    
# ~~~~~~~~~~ PROTOCOL RUN ~~~~~~~~~
p300_multi_default_speed.pick_up_tip()


# Define number of sample rows, sample volume, height from the bottom of the islet wells (aspiration and dispensing)
sampleRows = 3
sampleVol = 500
aspHeight = 3
disHeight = 8

#Step 1. Remove existing media

robot.comment("Removing existing media from samples.")

for row in range(0, sampleRows):
    p300_multi_default_speed.transfer(sampleVol, 
        samplePlate.rows(row).bottom(aspHeight), 
        wastePlate.rows(row),
        new_tip='never',
        blow_out=True)

robot.comment("Media removed.")

# Step 2. Wash islets

def washSamples(numWashes,volWash):
    robot.comment("Beginning "+str(numWashes)+" washes, "+str(volWash)+" µl each.")
    # numWashes = 3
    # volWash = 300
    for washing in range(0, numWashes):
        for row in range(0, sampleRows):
            p300_multi_default_speed.transfer(volWash,washBasin.rows(row), samplePlate.rows(row), new_tip='never',blow_out=True,touch_tip=False)
        for row in range(0, sampleRows):
            p300_multi_default_speed.transfer(volWash, samplePlate.rows(row).bottom(aspHeight), wastePlate.rows(row), new_tip='never',blow_out=True)            
        robot.comment("Finished wash number "+str(washing+1)+" of "+str(numWashes)+".\n")
    robot.comment("Finished washing "+str(numWashes)+" times. Adding low glucose solution to wells now.\n")

washSamples(5,300)
robot.home()

# Step 3. Dynamic secretion (repeat low-high challenge N times (Steps 3A and 3B))
## currently reservoir rows are coded in (0 = low glucose, 1 = high glucose)

numChallenges = 4
## set up the 384-well plate


alternating_wells = []
for row in collectionPlate.rows():
    alternating_wells.append(row.wells('A', length=8, step=2))
    alternating_wells.append(row.wells('B', length=8, step=2))


for cNum in range(0,numChallenges):
# Step 3A. Low Glucose solution to pseudoislets. Incubate @ 37 C for 30 minutes.
    robot.comment("Starting low glucose steps, challege "+str(cNum+1)+":")
    volGluc = 200
## lists of rows to be treated
    slowRows = [0]
    medRows = [1]
    fastRows = [2]
    p300_multi_low_speed.transfer(volGluc,reservoirs.rows(0), samplePlate.rows(slowRows).bottom(disHeight), new_tip='never',blow_out=True,touch_tip=True)
    p300_multi_default_speed.transfer(volGluc,reservoirs.rows(0), samplePlate.rows(medRows).bottom(disHeight), new_tip='never',blow_out=True,touch_tip=True)
    p300_multi_high_speed.transfer(volGluc,reservoirs.rows(0), samplePlate.rows(fastRows).bottom(disHeight), new_tip='never',blow_out=True,touch_tip=True)
    robot.comment("Finished adding low glucose to wells.")
    robot.home() # homing to remove stress on pipette, but also because it's good for the robot
### 30 min incubation
    robot.comment("Starting 30 min low glucose incubation.\n")
    p300_multi_default_speed.delay(minutes=20) # 1 incubation
    robot.comment("10 min remaining")
    p300_multi_default_speed.delay(minutes=8) # 1 incubation
    robot.comment("2 min remaining")
    p300_multi_default_speed.delay(minutes=2) # 1 incubation
    robot.comment("Incubation complete, now beginning transfer to collection plate.\n")
## Collect low glucose supernatant, split it into a 384-well plate and the remainder into the waste
    dest = [alternating_wells[cNum*12+0],alternating_wells[cNum*12+1],wastePlate.rows(slowRows)]
    p300_multi_default_speed.distribute([50,50,100],samplePlate.rows(slowRows),dest, new_tip='never',blow_out=True,touch_tip=True,disposal_vol=0)
    dest = [alternating_wells[cNum*12+2],alternating_wells[cNum*12+3],wastePlate.rows(medRows)]
    p300_multi_default_speed.distribute([50,50,100],samplePlate.rows(medRows),dest, new_tip='never',blow_out=True,touch_tip=True,disposal_vol=0)
    dest = [alternating_wells[cNum*12+4],alternating_wells[cNum*12+5],wastePlate.rows(fastRows)]
    p300_multi_default_speed.distribute([50,50,100],samplePlate.rows(fastRows),dest, new_tip='never',blow_out=True,touch_tip=True,disposal_vol=0)
    washSamples(3,100)
# Step 3B. High Glucose solution to pseudoislets. Incubate @ 37 C for 30 minutes.
    robot.comment("Starting high glucose steps, challege "+str(cNum+1)+":")
    p300_multi_low_speed.transfer(volGluc,reservoirs.rows(1), samplePlate.rows(slowRows).bottom(disHeight), new_tip='never',blow_out=True,touch_tip=True)
    p300_multi_default_speed.transfer(volGluc,reservoirs.rows(1), samplePlate.rows(medRows).bottom(disHeight), new_tip='never',blow_out=True,touch_tip=True)
    p300_multi_high_speed.transfer(volGluc,reservoirs.rows(1), samplePlate.rows(fastRows).bottom(disHeight), new_tip='never',blow_out=True,touch_tip=True)
    robot.comment("Finished adding high glucose to wells.")
    robot.home() # homing to remove stress on the robot
### 30 min incubation
    robot.comment("Starting 30 min high glucose incubation.\n")
    p300_multi_default_speed.delay(minutes=20) # 1 incubation
    robot.comment("2 min remaining")
    p300_multi_default_speed.delay(minutes=8) # 1 incubation
    robot.comment("1 min remaining")
    p300_multi_default_speed.delay(minutes=2) # 1 incubation
    robot.comment("Incubation complete, now beginning transfer to collection plate.\n")
## Collect high glucose supernatant, split it into a 384-well plate and the remainder into the waste
    dest = [alternating_wells[cNum*12+6],alternating_wells[cNum*12+7],wastePlate.rows(slowRows)]
    p300_multi_default_speed.distribute([50,50,100],samplePlate.rows(slowRows),dest, new_tip='never',blow_out=True,touch_tip=True,disposal_vol=0)
    dest = [alternating_wells[cNum*12+8],alternating_wells[cNum*12+9],wastePlate.rows(medRows)]
    p300_multi_default_speed.distribute([50,50,100],samplePlate.rows(medRows),dest, new_tip='never',blow_out=True,touch_tip=True,disposal_vol=0)
    dest = [alternating_wells[cNum*12+10],alternating_wells[cNum*12+11],wastePlate.rows(fastRows)]
    p300_multi_default_speed.distribute([50,50,100],samplePlate.rows(fastRows),dest, new_tip='never',blow_out=True,touch_tip=True,disposal_vol=0)
    robot.comment("Challenge "+str(cNum+1)+" of "+str(numChallenges)+" completed.\n")
    washSamples(3,100)

robot.comment("Protocol complete.")
robot.home()