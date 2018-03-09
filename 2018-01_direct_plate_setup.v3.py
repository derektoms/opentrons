# 2018-01-22
# Updated the code to first add appropriate base media to each well, then pipette the drugs. Using PCR tubes now, so that was changed as well.
# 2018-01-19
# 30 factor DSD screen with human islets
# 2017-10-01
# INS-1 test for DSD experiments

# import required bits
from opentrons import robot, containers, instruments
from itertools import chain

#robot.head_speed(z=1000)

## container set up
# set tip racks

p10rack = containers.load(
    'tiprack-10ul',
    'A1',
    'p10-rack-01'
)

p1000rack = containers.load(
    'tiprack-1000ul',
    'B1',
    'p1000-rack-01'
)

# set plates
plate_mapped = containers.load(
    '96-PCR-flat',
    'C1',
    'plate_mapped'
)

plate_source = containers.load(
    'PCR-strip-tall',
    'C2',
    'plate_source'
)

tube_source = containers.load(
    'tube-rack-15_50ml',
    'E1',
    'plate_source'
)

# trash
trash = containers.load('point', 'A2')

# load pipette
p10 = instruments.Pipette(
    name="p10", # optional
    trash_container=trash,
    tip_racks=[p10rack],
    min_volume=0.2, # actual minimum volume of the pipette
    max_volume=10,
    axis="b",
    channels=1 # 
)

p1000 = instruments.Pipette(
    name="p1000", # optional
    trash_container=trash,
    tip_racks=[p1000rack],
    min_volume=50, # actual minimum volume of the pipette
    max_volume=1000,
    axis="a",
    channels=1 # 
)

## distribute commands

# first, distribute base media to each well of the mapped plate
# this needed to be split between eight commands because the p1000 axis doesn't reset to the bottom, and instead begins the next command from 'blow out', which gets progressively lower until the tip falls off

p1000.distribute(['92.02', '67.97', '69.87', '100.00', '100.00', '100.00', '100.00', '100.00', '100.00', '100.00', '100.00', '66.88'],
tube_source.wells('A3'),
plate_mapped.wells(['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'A2', 'B2', 'C2', 'D2']),
touch_tip=True
)
p1000.home()

p1000.distribute(['100.00', '57.41', '51.67', '62.14', '66.21', '100.00', '92.02', '67.08', '100.00', '55.01', '59.14', '62.06'],
tube_source.wells('A3'),
plate_mapped.wells(['E2', 'F2', 'G2', 'H2', 'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3']),
touch_tip=True
)
p1000.home()

p1000.distribute(['62.39', '100.00', '63.94', '76.01', '23.07', '58.40', '64.67', '100.00', '92.02', '92.02', '56.79', '66.28'],
tube_source.wells('A3'),
plate_mapped.wells(['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'A5', 'B5', 'C5', 'D5']),
touch_tip=True
)
p1000.home()

p1000.distribute(['59.13', '64.05', '62.41', '62.26', '100.00', '60.93', '78.33', '59.00', '100.00', '66.87', '65.53', '92.02'],
tube_source.wells('A3'),
plate_mapped.wells(['E5', 'F5', 'G5', 'H5', 'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6']),
touch_tip=True
)
p1000.home()

p1000.distribute(['92.02', '100.00', '100.00', '61.00', '67.26', '63.01', '65.61', '100.00', '60.67', '66.78', '100.00', '62.26'],
tube_source.wells('A3'),
plate_mapped.wells(['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'A8', 'B8', 'C8', 'D8']),
touch_tip=True
)
p1000.home()

p1000.distribute(['56.94', '100.00', '100.00', '60.81', '100.00', '92.02', '59.10', '56.19', '66.63', '62.27', '70.21', '59.56'],
tube_source.wells('A3'),
plate_mapped.wells(['E8', 'F8', 'G8', 'H8', 'A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9']),
touch_tip=True
)
p1000.home()

p1000.start_at_tip(p1000rack['A2']) # necessary to avoid a collision with the p10

p1000.distribute(['100.00', '69.66', '100.00', '54.46', '100.00', '63.67', '46.87', '56.93', '62.16', '66.93', '73.00', '100.00'],
tube_source.wells('A3'),
plate_mapped.wells(['A10', 'B10', 'C10', 'D10', 'E10', 'F10', 'G10', 'H10', 'A11', 'B11', 'C11', 'D11']),
touch_tip=True
)
p1000.home()

p1000.distribute(['100.00', '59.35', '100.00', '100.00', '57.80', '65.32', '64.91', '54.80', '92.02', '67.27', '51.21', '64.92'],
tube_source.wells('A3'),
plate_mapped.wells(['E11', 'F11', 'G11', 'H11', 'A12', 'B12', 'C12', 'D12', 'E12', 'F12', 'G12', 'H12']),
touch_tip=True
)


# second, dilute drugs into the mapped plate
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'C3', 'A5', 'B5', 'H6', 'A7', 'B9', 'A11', 'C12', 'E12'])]
p10.distribute(
    ['0.50'],
    plate_source.wells(0),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'C3', 'A5', 'B5', 'H6', 'A7', 'B9', 'G9', 'D10', 'E12'])]
p10.distribute(
    ['0.20'],
    plate_source.wells(1),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'C3', 'A5', 'B5', 'D6', 'H6', 'A7', 'B9', 'E12', 'F12'])]
p10.distribute(
    ['0.40'],
    plate_source.wells(2),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'C3', 'A5', 'B5', 'H6', 'A7', 'G7', 'D8', 'B9', 'E12'])]
p10.distribute(
    ['0.60'],
    plate_source.wells(3),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'B1', 'C3', 'A5', 'B5', 'H6', 'A7', 'B9', 'C9', 'E12'])]
p10.distribute(
    ['0.50'],
    plate_source.wells(4),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'C3', 'A5', 'B5', 'H6', 'A7', 'E8', 'B9', 'B11', 'E12'])]
p10.distribute(
    ['0.20'],
    plate_source.wells(5),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'D2', 'C3', 'A5', 'B5', 'H6', 'A7', 'B9', 'D9', 'E12'])]
p10.distribute(
    ['0.20'],
    plate_source.wells(6),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'C3', 'A5', 'B5', 'G5', 'H6', 'A7', 'B9', 'E12', 'H12'])]
p10.distribute(
    ['0.53'],
    plate_source.wells(7),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'F2', 'C3', 'A5', 'B5', 'H6', 'A7', 'E7', 'B9', 'E12'])]
p10.distribute(
    ['0.20'],
    plate_source.wells(8),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'C3', 'D4', 'A5', 'B5', 'H6', 'A7', 'B9', 'E12', 'G12'])]
p10.distribute(
    ['0.52'],
    plate_source.wells(9),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'C3', 'A5', 'B5', 'H6', 'A7', 'B9', 'E9', 'H9', 'E12'])]
p10.distribute(
    ['0.24'],
    plate_source.wells(10),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'C3', 'A5', 'B5', 'H6', 'A7', 'F7', 'B9', 'F9', 'E12'])]
p10.distribute(
    ['0.74'],
    plate_source.wells(11),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'C3', 'F3', 'A5', 'B5', 'H6', 'A7', 'B9', 'B10', 'E12'])]
p10.distribute(
    ['0.20'],
    plate_source.wells(12),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'C3', 'A5', 'B5', 'H6', 'A7', 'B8', 'B9', 'H10', 'E12'])]
p10.distribute(
    ['0.80'],
    plate_source.wells(13),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'C3', 'A5', 'B5', 'H6', 'A7', 'D7', 'B9', 'F10', 'E12'])]
p10.distribute(
    ['0.20'],
    plate_source.wells(14),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'A3', 'C3', 'H3', 'A5', 'B5', 'H6', 'A7', 'B9', 'E12'])]
p10.distribute(
    ['0.40'],
    plate_source.wells(15),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'C3', 'A5', 'B5', 'C6', 'H6', 'A7', 'B9', 'G10', 'E12'])]
p10.distribute(
    ['0.27'],
    plate_source.wells(16),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'C3', 'A5', 'B5', 'F5', 'H6', 'A7', 'A8', 'B9', 'E12'])]
p10.distribute(
    ['0.21'],
    plate_source.wells(17),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'C3', 'A5', 'B5', 'F6', 'H6', 'A7', 'B9', 'A12', 'E12'])]
p10.distribute(
    ['0.20'],
    plate_source.wells(18),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'G2', 'C3', 'A5', 'B5', 'H6', 'A7', 'B9', 'C11', 'E12'])]
p10.distribute(
    ['0.20'],
    plate_source.wells(19),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'C3', 'A5', 'B5', 'H6', 'A7', 'B9', 'F11', 'B12', 'E12'])]
p10.distribute(
    ['0.20'],
    plate_source.wells(20),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'C1', 'C3', 'A5', 'B5', 'H6', 'A7', 'B9', 'D12', 'E12'])]
p10.distribute(
    ['0.20'],
    plate_source.wells(21),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'C3', 'D3', 'A4', 'A5', 'B5', 'H6', 'A7', 'B9', 'E12'])]
p10.distribute(
    ['0.80'],
    plate_source.wells(22),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A1', 'C3', 'G3', 'A5', 'B5', 'G6', 'H6', 'A7', 'B9', 'E12'])]
p10.distribute(
    ['0.20'],
    plate_source.wells(23),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['B1', 'G2', 'A3', 'D3', 'F3', 'G3', 'C4', 'E4', 'F4', 'D5', 'H5', 'B6', 'D7', 'E7', 'A8', 'D8', 'D9', 'E9', 'F9', 'G9', 'G10', 'H10', 'B11', 'A12', 'B12', 'D12', 'F12', 'G12', 'H12'])]
p10.distribute(
    ['5.00'],
    plate_source.wells(0),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['C1', 'F2', 'G2', 'H2', 'A3', 'F3', 'G3', 'A4', 'C4', 'D4', 'E4', 'G4', 'D5', 'F5', 'H5', 'C6', 'D6', 'B8', 'D8', 'C9', 'D9', 'F9', 'H9', 'F10', 'B11', 'F11', 'A12', 'C12', 'H12'])]
p10.distribute(
    ['2.00'],
    plate_source.wells(1),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['F2', 'G2', 'H2', 'D3', 'F3', 'H3', 'C4', 'E4', 'G4', 'C5', 'H5', 'C6', 'F6', 'G6', 'D7', 'F7', 'G7', 'A8', 'B8', 'E8', 'C9', 'D9', 'E9', 'G9', 'A11', 'F11', 'D12', 'G12', 'H12'])]
p10.distribute(
    ['4.00'],
    plate_source.wells(2),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['B1', 'D2', 'F2', 'H2', 'A3', 'G3', 'A4', 'C4', 'E4', 'F4', 'C5', 'D6', 'D7', 'A8', 'B8', 'E8', 'H8', 'F9', 'H9', 'B10', 'D10', 'G10', 'A11', 'C11', 'F11', 'A12', 'D12', 'G12', 'H12'])]
p10.distribute(
    ['6.00'],
    plate_source.wells(3),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['D2', 'F2', 'G2', 'H2', 'A3', 'F3', 'A4', 'E4', 'F4', 'C5', 'E5', 'F5', 'G5', 'H5', 'C6', 'G6', 'D7', 'F7', 'G7', 'H9', 'D10', 'H10', 'B11', 'A12', 'B12', 'C12', 'D12', 'F12', 'G12'])]
p10.distribute(
    ['5.00'],
    plate_source.wells(4),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['B1', 'C1', 'G2', 'A3', 'A4', 'C4', 'E4', 'F4', 'C5', 'G5', 'B6', 'C6', 'F6', 'G6', 'E7', 'F7', 'A8', 'B8', 'D8', 'H8', 'D9', 'G9', 'H9', 'B10', 'F10', 'F11', 'C12', 'F12', 'G12'])]
p10.distribute(
    ['1.20'],
    plate_source.wells(5),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['H2', 'D3', 'H3', 'D4', 'E4', 'F4', 'D5', 'E5', 'C6', 'D6', 'G6', 'D7', 'E7', 'F7', 'A8', 'D8', 'H8', 'C9', 'G9', 'H9', 'B10', 'H10', 'B11', 'C11', 'F11', 'A12', 'C12', 'D12', 'H12'])]
p10.distribute(
    ['0.40'],
    plate_source.wells(6),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['F2', 'G2', 'A3', 'G3', 'A4', 'D4', 'E4', 'G4', 'C5', 'E5', 'B6', 'D6', 'F7', 'G7', 'A8', 'E8', 'H8', 'C9', 'D9', 'E9', 'G9', 'B10', 'F10', 'G10', 'H10', 'A12', 'B12', 'C12', 'D12'])]
p10.distribute(
    ['5.33'],
    plate_source.wells(7),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['B1', 'C1', 'D2', 'G2', 'H3', 'A4', 'E4', 'F4', 'D5', 'E5', 'F5', 'H5', 'B6', 'C6', 'D6', 'G6', 'G7', 'E8', 'E9', 'F9', 'G9', 'B10', 'F10', 'H10', 'A11', 'F11', 'A12', 'G12', 'H12'])]
p10.distribute(
    ['2.00'],
    plate_source.wells(8),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['B1', 'D2', 'F2', 'G2', 'D3', 'F3', 'H3', 'C4', 'E4', 'G4', 'D5', 'G5', 'B6', 'D6', 'F6', 'G6', 'G7', 'A8', 'H8', 'F9', 'H9', 'D10', 'F10', 'G10', 'H10', 'B11', 'F11', 'C12', 'D12'])]
p10.distribute(
    ['5.19'],
    plate_source.wells(9),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['B1', 'H2', 'F3', 'G3', 'H3', 'A4', 'E4', 'G4', 'D5', 'E5', 'F5', 'G5', 'E7', 'F7', 'G7', 'B8', 'H8', 'D9', 'G9', 'F10', 'G10', 'A11', 'B11', 'C11', 'F11', 'A12', 'D12', 'F12', 'G12'])]
p10.distribute(
    ['3.60'],
    plate_source.wells(10),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['B1', 'G2', 'H3', 'A4', 'D4', 'E4', 'G4', 'C5', 'E5', 'F5', 'H5', 'B6', 'D6', 'F6', 'G6', 'D7', 'E7', 'B8', 'D8', 'D9', 'H9', 'B10', 'D10', 'G10', 'A11', 'B11', 'B12', 'D12', 'H12'])]
p10.distribute(
    ['3.68'],
    plate_source.wells(11),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['C1', 'F2', 'A3', 'A4', 'C4', 'D4', 'E4', 'F4', 'D5', 'F5', 'B6', 'F6', 'G6', 'D7', 'F7', 'G7', 'H8', 'C9', 'D9', 'E9', 'D10', 'G10', 'H10', 'A11', 'B11', 'C11', 'F11', 'F12', 'H12'])]
p10.distribute(
    ['2.00'],
    plate_source.wells(12),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['B1', 'F2', 'H2', 'A3', 'D3', 'E4', 'G4', 'D5', 'E5', 'F5', 'C6', 'F6', 'G6', 'D8', 'E8', 'H8', 'D9', 'E9', 'F9', 'B10', 'D10', 'F10', 'C11', 'B12', 'C12', 'D12', 'F12', 'G12', 'H12'])]
p10.distribute(
    ['8.00'],
    plate_source.wells(13),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['C1', 'D2', 'F2', 'F3', 'G3', 'H3', 'A4', 'E4', 'G4', 'C5', 'E5', 'B6', 'C6', 'F6', 'A8', 'D8', 'H8', 'C9', 'F9', 'G9', 'H9', 'H10', 'A11', 'B11', 'C11', 'B12', 'F12', 'G12', 'H12'])]
p10.distribute(
    ['2.00'],
    plate_source.wells(14),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['C1', 'F2', 'D3', 'F3', 'E4', 'F4', 'D5', 'E5', 'G5', 'H5', 'B6', 'D6', 'G6', 'F7', 'A8', 'B8', 'D8', 'E8', 'C9', 'D9', 'H9', 'D10', 'F10', 'G10', 'A11', 'C11', 'A12', 'B12', 'G12'])]
p10.distribute(
    ['6.00'],
    plate_source.wells(15),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['C1', 'D2', 'G2', 'D3', 'G3', 'H3', 'C4', 'E4', 'G4', 'D5', 'F5', 'B6', 'D7', 'E7', 'F7', 'G7', 'B8', 'E8', 'H8', 'C9', 'H9', 'B10', 'D10', 'A12', 'B12', 'C12', 'F12', 'G12', 'H12'])]
p10.distribute(
    ['2.67'],
    plate_source.wells(16),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['B1', 'C1', 'D2', 'F2', 'G2', 'H2', 'A3', 'D3', 'G3', 'D4', 'E4', 'G4', 'D5', 'E5', 'G5', 'H5', 'F6', 'D7', 'F7', 'D8', 'E8', 'G9', 'H9', 'B10', 'G10', 'H10', 'A11', 'F11', 'F12'])]
p10.distribute(
    ['2.06'],
    plate_source.wells(17),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['D2', 'A3', 'D3', 'G3', 'C4', 'E4', 'G4', 'C5', 'F5', 'G5', 'H5', 'B6', 'C6', 'D6', 'E7', 'F7', 'D8', 'C9', 'E9', 'B10', 'D10', 'F10', 'H10', 'A11', 'B11', 'C11', 'F11', 'D12', 'G12'])]
p10.distribute(
    ['2.00'],
    plate_source.wells(18),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['H2', 'G3', 'H3', 'A4', 'C4', 'D4', 'E4', 'F4', 'D5', 'G5', 'H5', 'C6', 'F6', 'E7', 'G7', 'A8', 'E8', 'C9', 'D9', 'F9', 'H9', 'B10', 'D10', 'F10', 'H10', 'A11', 'B12', 'D12', 'F12'])]
p10.distribute(
    ['2.00'],
    plate_source.wells(19),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['B1', 'C1', 'D2', 'H2', 'F3', 'H3', 'A4', 'C4', 'D4', 'E4', 'G4', 'C5', 'H5', 'G6', 'E7', 'F7', 'A8', 'D8', 'E8', 'E9', 'D10', 'F10', 'G10', 'H10', 'C11', 'A12', 'C12', 'F12', 'H12'])]
p10.distribute(
    ['2.00'],
    plate_source.wells(20),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['D2', 'F2', 'G2', 'H2', 'D3', 'H3', 'C4', 'D4', 'E4', 'F4', 'C5', 'F5', 'G5', 'G6', 'B8', 'D8', 'H8', 'C9', 'E9', 'F9', 'G9', 'B10', 'F10', 'G10', 'A11', 'B11', 'A12', 'B12', 'F12'])]
p10.distribute(
    ['2.00'],
    plate_source.wells(21),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['C1', 'G2', 'H2', 'F3', 'G3', 'H3', 'E4', 'F4', 'C5', 'E5', 'F5', 'G5', 'D6', 'F6', 'D7', 'E7', 'D8', 'E8', 'H8', 'C9', 'D9', 'E9', 'F9', 'D10', 'G10', 'H10', 'F11', 'C12', 'G12'])]
p10.distribute(
    ['8.00'],
    plate_source.wells(22),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['D2', 'A3', 'D3', 'F3', 'D4', 'E4', 'F4', 'C5', 'E5', 'F5', 'H5', 'B6', 'F6', 'E7', 'G7', 'B8', 'E8', 'C9', 'F9', 'G9', 'H9', 'F10', 'G10', 'C11', 'F11', 'C12', 'D12', 'F12', 'H12'])]
p10.distribute(
    ['2.00'],
    plate_source.wells(23),
destination_wells
    )

robot.home()