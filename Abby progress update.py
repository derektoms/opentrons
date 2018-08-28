# imports
from opentrons import robot, containers, load, insturments
from intertools import chains

# robot settings
robot.head_speed(z=1000) 


# container set up 

# set tip racks
tiprack = containers.load('tiprack-200ul', 'A1') 

# waste 
waste = containers.load('point', 'C2', 'waste') 
liquid_waste = containers.load('96-PCR-flat', 'D1', 'liquid waste') 

# wash basin 
wash_basin = containers.load('trash-box', 'B1', 'wash basin') 

# microwell plate
uwell = containers.load('96-PCR-flat', 'C1') 


# load pipette
p200_multi = insturments.Pipette(
    axis='a'
    name='p200_multi',
    max_volume=200,
    min_volume=20, 
    channels=8
    tip_racks=[tiprack], 
    trash_container=trash) 
	
# starting tip row
p200_multi.start_at_tip(tiprack.rows(0)) 

# first remove media from the wells
# p200_multi.transfer(200, uwell.rows(), liquid_waste.rows()) 

# then wash the plate n times
num_washes = 5 

# loop wash 
for washing in range(0,num_washes):
    for platecolumn in range(0, 11):
        p200_multi.transfer(
		    200, 
		    wash_basin.rows(0), 
	        uwell.rows(platecolumn),
			blow_out=True,    # blow out every time
			new_tip=False,    # never pick up or drop tip
			hjfjyfiydidkycjyku
			
			
			
	    
		
	