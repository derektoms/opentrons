# 2018-02-12

# import required bits
from opentrons import robot, containers, instruments
from itertools import chain

#robot.head_speed(z=1000)

## container set up
# set tip racks

p10rack = containers.load('tiprack-10ul', 'A1', 'p10-rack')
p10rack2 = containers.load('tiprack-10ul', 'A2', 'p10-rack')

# set plates
plate_mapped_low = containers.load(
    'PCR-strip-tall',
    'C1',
    'plate_mapped_low'
)

plate_mapped_high = containers.load(
    'PCR-strip-tall',
    'D1',
    'plate_mapped_high'
)

plate_source_low = containers.load(
    'PCR-strip-tall',
    'C2',
    'plate_source_low'
)

plate_source_high = containers.load(
    'PCR-strip-tall',
    'D2',
    'plate_source_high'
)



# trash
trash = containers.load('point', 'E2')

# load pipette
p10 = instruments.Pipette(
    name="p10", # optional
    trash_container=trash,
    tip_racks=[p10rack, p10rack2],
    min_volume=0.2, # actual minimum volume of the pipette
    max_volume=10,
    axis="b",
    channels=1 # 
)


## transfer
## low plate
source_wells = [well.bottom(2) for well in plate_source_low.wells(['A1', 'B1', 'C1', 'D1', 'F1', 'H1', 'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'A4', 'B4', 'D4', 'E4', 'F4', 'G4', 'H4', 'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'A6', 'B6', 'D6', 'E6', 'F6', 'H6', 'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'A9', 'B9', 'C9', 'D9', 'F9', 'G9', 'H9', 'B10', 'C10', 'D10', 'E10', 'F10', 'H10', 'A11', 'C11', 'D11', 'E11', 'F11', 'G11', 'H11', 'A12', 'C12', 'D12', 'E12', 'F12', 'G12', 'H12'])]
destination_wells = [well.bottom(2) for well in plate_mapped_low.wells(['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9', 'A10', 'B10', 'C10', 'D10', 'E10', 'F10', 'G10', 'H10', 'A11', 'B11', 'C11', 'D11', 'E11', 'F11'])]
p10.transfer(
    ['10'],
    source_wells,
    destination_wells
    )
## high plate
source_wells = [well.bottom(2) for well in plate_source_high.wells(['A1', 'B1', 'C1', 'D1', 'F1', 'H1', 'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'A4', 'B4', 'D4', 'E4', 'F4', 'G4', 'H4', 'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'A6', 'B6', 'D6', 'E6', 'F6', 'H6', 'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'A9', 'B9', 'C9', 'D9', 'F9', 'G9', 'H9', 'B10', 'C10', 'D10', 'E10', 'F10', 'H10', 'A11', 'C11', 'D11', 'E11', 'F11', 'G11', 'H11', 'A12', 'C12', 'D12', 'E12', 'F12', 'G12', 'H12'])]
destination_wells = [well.bottom(2) for well in plate_mapped_high.wells(['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9', 'A10', 'B10', 'C10', 'D10', 'E10', 'F10', 'G10', 'H10', 'A11', 'B11', 'C11', 'D11', 'E11', 'F11'])]
p10.transfer(
    ['10'],
    source_wells,
    destination_wells
    )