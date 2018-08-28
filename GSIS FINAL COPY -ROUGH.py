#GSIS Opentrons Protocol
#Last Updated: August 3rd, 2018

from opentrons import robot, containers, instruments
from itertools import chain

# ~~~~~~~~~~~ SET UP ~~~~~~~~~~
#max_speed_per_axis = { # Head Speed
# 'x': 2000, 'y': 1000, 'z':500, 'a':500, 'b':500, 'c':200}
#robot.head_speed(
#    combined_speed=max(max_speed_per_axis.values()), **max_speed_per_axis)

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

p200_multi_default_speed = instruments.Pipette( # Middle speed. This 'pipette' will operate during the rows 4-7. default speed  
    axis='a',
    name='pip200default',
    max_volume=200,
    min_volume=20,
    channels=8,
    tip_racks=[tiprack],
    trash_container=waste,
    aspirate_speed=300,
    dispense_speed=400)
    
p200_multi_high_speed = instruments.Pipette( # high dispense speed, robot max, use for washing columns 7-11
    axis='a',
    name='pip200high',
    max_volume=200,
    min_volume=20,
    channels=8,
    tip_racks=[tiprack],
    trash_container=waste,
    aspirate_speed=300,
    dispense_speed=1200)

p200_multi_low_speed = instruments.Pipette( # Lowest pipette speed, use for washing and columns 0-3
    axis='a',
    name='pip200low',
    max_volume=200,
    min_volume=20,
    channels=8,
    tip_racks=[tiprack],
    trash_container=waste,
    aspirate_speed=300,
    dispense_speed=150)

# ~~~~~~~~~~ PROTOCOL RUN ~~~~~~~~~
p200_multi_low_speed.pick_up_tip(tiprack.wells('A1'))


#Step 1.
for row in range(0, 11):
    p200_multi_low_speed.transfer(200, cellwell.rows(row), waste.rows(row)) #remove medium from microwells

# Step 2. Wash with 200 ul DPBS 
num_washes = 4
for washing in range(0, num_washes):
    for row in range(0, 11): #using low speed pipette
        p200_multi_low_speed.dispense(wash_basin.rows(0))
        p200_multi_low_speed.aspirate(200, wash_basin.rows(0))
        p200_multi_low_speed.dispense(200, cellwell.rows(row).bottom(5))
        p200_multi_low_speed.touch_tip(cellwell.rows(row)) 
        p200_multi_low_speed.move_to(cellwell.rows(row).top())
        p200_multi_low_speed.aspirate() 
        p200_multi_low_speed.new_tip='never'	#got approved did this work? -yes	#dispensing DPBS
    for row in range(0, 11): 	
        p200_multi_low_speed.dispense(cellwell.rows(row))	
        p200_multi_low_speed.aspirate(200, cellwell.rows(row))
        p200_multi_low_speed.dispense(200,waste.rows(row).bottom(5)) 
        p200_multi_low_speed.move_to(waste.rows(row).top())
        p200_multi_low_speed.aspirate()
        p200_multi_low_speed.new_tip='never' #Removing DPBS 
    
	
    robot.comment("Finished wash number "+str(washing)+"of "+str(num_washes)+" washes")
robot.comment("finished five washes. Adding low glucose solution to wells now...")




#Step 3. Low Glucose
#100 ul of low glucose solution to microwell plate. Incubate @ 37 C for 60 minutes.
#dispensing low glucose medium into microwells
for low_row in range(0, 3): #low plunging speed
    p200_multi_low_speed,dispense(glucose_medium.rows(LOW_GLUCOSE_MEDIUM_ROWS))
    p200_multi_low_speed.aspirate(100, glucose_medium.rows(LOW_GLUCOSE_MEDIUM_ROWS))
    p200_multi_low_speed.dispense(100, cellwell.rows(low_row).bottom(5)) 
    p200_multi_low_speed.touch_tip(cellwell.rows(low_row))
    p200_multi_low_speed.move_to(cellwell.rows(low_row).top())
    p200_multi_low_speed.aspirate()
    p200_multi_low_speed.new_tip='never'

robot.comment("Finished adding low glucose to wells, low speed.")

for middle_row in range(4, 7): #default (middle) plunging speed
    p200_multi_default_speed.dispense(glucose_medium.rows(LOW_GLUCOSE_MEDIUM_ROWS))
    p200_multi_default_speed.aspirate(100, glucose_medium.rows(LOW_GLUCOSE_MEDIUM_ROWS))
    p200_multi_default_speed.dispense(100, cellwell.rows(middle_row).bottom(5)) 
    p200_multi_default_speed.touch_tip(cellwell.rows(middle_row))
    p200_multi_default_speed.move_to(cellwell.rows(middle_row).top())
    p200_multi_default_speed.aspirate()
    p200_multi_default_speed.new_tip='never'
	
robot.comment("Finished adding low glucose to wells, default speed.")  
 
for high_row in range(8, 11): #high, max plunging speed
    p200_multi_high_speed.aspirate(100, glucose_medium.rows(LOW_GLUCOSE_MEDIUM_ROWS))
    p200_multi_high_speed.dispense(100, cellwell.rows(high_row).bottom(5)) 
    #p200_multi_high_speed.blow_out(cellwell.rows(high_row))
    p200_multi_high_speed.touch_tip(cellwell.rows(high_row))
    p200_multi_high_speed.new_tip='never'
    
robot.comment("Finished adding low glucose to wells, high speed.")


robot.home('a') # homing to remove stress on pipette

p200_multi_high_speed.delay(minutes=60) # 1 h incubation

robot.comment("Starting 1 h low glucose incubation")

###############################################################################################
    # for row in range(3, 5):
        # p200_multi.aspirate(150, cellwell.rows(row))
        # p200_multi.dispense(150, waste)
        # p200_multi.blow_out(waste)
        # p200_multi.new_tip='never'            ################### ^^^^^^^^^^ not needed

# 160ul of low glucose solution to wells.
# for row in range(3, 5):
    # p200_multi.aspirate(160, glucose_medium.rows('3'))
    # p200_multi.dispense(160, cellwell.rows(row))
    # p200_multi.blow_out(cellwell.rows(row))
    # p200_multi.touch_tip(cellwell.rows(row))
    # p200_multi.new_tip='never'

#p200_multi.delay(minutes=60) # Incubate for 1 hour    ############## ^^^^^^^^ not needed

############################################################################################

robot.comment("Delay complete, now beginning transfer to low glucose plate")

for low_row in range(0, 3): #Transfer 50 ul to U 96 well plate #low plunging speed
    p200_multi_low_speed.aspirate(50, cellwell.rows(low_row))
    p200_multi_low_speed.dispense(50, output_low.rows(low_row).bottom(5)) 
    #p200_multi_low_speed.blow_out(output_low.rows(low_row))
    p200_multi_low_speed.touch_tip(output_low.rows(low_row)) 
    p200_multi_low_speed.new_tip='never'
    
robot.comment("Finished tranferring to low glucose plate, low speed.")

for middle_row in range(4, 7): #Transfer 50 ul to U 96 well plate #default plunging speed
    p200_multi_default_speed.aspirate(50, cellwell.rows(middle_row))
    p200_multi_default_speed.dispense(50, output_low.rows(middle_row).bottom(5)) 
    #p200_multi_default_speed.blow_out(output_low.rows(middle_row))
    p200_multi_default_speed.touch_tip(output_low.rows(middle_row)) 
    p200_multi_default_speed.new_tip='never'
    
robot.comment("Finished tranferring to low glucose plate, default speed.")

for high_row in range(8, 11): #Transfer 50 ul to U 96 well plate #high plunging speed
    p200_multi_high_speed.aspirate(50, cellwell.rows(high_row))
    p200_multi_high_speed.dispense(50, output_low.rows(high_row).bottom(5)) 
    #p200_multi_high_speed.blow_out(output_low.rows(high_row))
    p200_multi_high_speed.touch_tip(output_low.rows(high_row)) 
    p200_multi_high_speed.new_tip='never'

robot.comment("Finished tranferring to low glucose plate, high speed.")	
	
	
#Step 4. High Glucose
#Add 50 ul, wait 60 min, remove 50 ul to U plate High glucose medium.

robot.comment("Starting high glucose steps")

for low_row in range(0, 3): #trough to microwell plate #low plunging speed
    p200_multi_low_speed.aspirate(50, glucose_medium.rows(HIGH_GLUCOSE_MEDIUM_LOCATION))
    p200_multi_low_speed.dispense(50, cellwell.rows(low_row).bottom(5))
    #p200_multi_low_speed.blow_out(cellwell.rows(low_row))
    p200_multi_low_speed.touch_tip(cellwell.rows(low_row))
    p200_multi_low_speed.new_tip='never' # set the right trough row (high glucose now)
  
robot.comment("Finished adding high glucose to wells, low speed.")
  
for middle_row in range(4, 7): #trough to microwell plate #default plunging speed
    p200_multi_default_speed.aspirate(50, glucose_medium.rows(HIGH_GLUCOSE_MEDIUM_LOCATION))
    p200_multi_default_speed.dispense(50, cellwell.rows(middle_row).bottom(5))
    #p200_multi_default_speed.blow_out(cellwell.rows(middle_row))
    p200_multi_default_speed.touch_tip(cellwell.rows(middle_row))
    p200_multi_default_speed.new_tip='never'
    
robot.comment("Finished adding high glucose to wells, default speed.")

for high_row in range(8, 11): #trough to microwell plate  #high plunging speed
    p200_multi_high_speed.aspirate(50, glucose_medium.rows(HIGH_GLUCOSE_MEDIUM_LOCATION))
    p200_multi_high_speed.dispense(50, cellwell.rows(high_row).bottom(5))
    #p200_multi_high_speed.blow_out(cellwell.rows(high_row))
    p200_multi_high_speed.touch_tip(cellwell.rows(high_row))
    p200_multi_high_speed.new_tip='never'
	
robot.comment("Finished adding high glucose to wells, default speed.")

robot.home('a') #homing to remove stress on pipette


p200_multi_high_speed.delay(minutes=60) #1h incubation
robot.comment("Starting 1 h high glucose incubation")

robot.comment("Delay complete, now beginning transfer to high glucose plate")

for low_row in range(0, 3): #transfer to U 96 well plate #low plunging speed
    p200_multi_low_speed.aspirate(50, cellwell.rows(low_row))
    p200_multi_low_speed.dispense(output_high.rows(low_row).bottom(5)) 
    #p200_multi_low_speed.blow_out(output_high.rows(low_row))
    p200_multi_low_speed.touch_tip(output_high.rows(low_row))
    new_tip='never'
    
robot.comment("Finished tranferring to high glucose plate, low speed.")

for middle_row in range(4, 7): #transfer to U 96 well plate #default plunging speed
    p200_multi_default_speed.aspirate(50, cellwell.rows(middle_row))
    p200_multi_default_speed.dispense(output_high.rows(middle_row).bottom(5)) 
    #p200_multi_default_speed.blow_out(output_high.rows(middle_row))
    p200_multi_default_speed.touch_tip(output_high.rows(middle_row))
    new_tip='never'
    
robot.comment("Finished tranferring to high glucose plate, default speed.")

for high_row in range(8, 11): #transfer to U 96 well plate  #high plunging speed
    p200_multi_high_speed.aspirate(50, cellwell.rows(high_row))
    p200_multi_high_speed.dispense(output_high.rows(high_row).bottom(5)) 
    #p200_multi_high_speed.blow_out(output_high.rows(high_row))
    p200_multi_high_speed.touch_tip(output_high.rows(high_row))
    new_tip='never'
    
robot.comment("Finished tranferring to high glucose plate, high speed.")
    
    
robot.home()

robot.comment("Protocol complete, place cells plates in correct location.")




