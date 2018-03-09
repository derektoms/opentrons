# 2018-02-06

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

# media first
p1000.distribute(['90.86', '82.17', '88.83', '92.54', '100', '79.09', '100', '82.73', '95.32', '94.5', '88.08', '90.79'],
tube_source.wells('A3'),
plate_mapped.wells(['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'A2', 'B2', 'C2', 'D2']),
touch_tip=True
)
p1000.home()

p1000.distribute(['88.9', '84.69', '87.26', '84.44', '85.51', '88.01', '88.01', '95.32', '94.5', '90.04', '84.69', '87.15'],
tube_source.wells('A3'),
plate_mapped.wells(['E2', 'F2', 'G2', 'H2', 'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3']),
touch_tip=True
)
p1000.home()

p1000.distribute(['84.17', '88.08', '86.17', '86.17', '86.33', '86.17', '81.05', '90.17', '86.17', '82.73', '89.97', '83.55'],
tube_source.wells('A3'),
plate_mapped.wells(['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'A5', 'B5', 'C5', 'D5']),
touch_tip=True
)
p1000.home()

p1000.distribute(['85.19', '84.37', '91.68', '84.37', '79.91', '81.87', '86.17', '93.36', '89.72', '86.4', '100', '86.17'],
tube_source.wells('A3'),
plate_mapped.wells(['E5', 'F5', 'G5', 'H5', 'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6']),
touch_tip=True
)
p1000.home()

p1000.distribute(['90.04', '81.87', '93.36', '79.91', '91.68', '86.17', '85.19', '83.62', '84.44', '87.26', '86.17', '89.97'],
tube_source.wells('A3'),
plate_mapped.wells(['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'A8', 'B8', 'C8', 'D8']),
touch_tip=True
)
p1000.home()

p1000.distribute(['88.83', '92.54', '86.17', '86.17', '86.33', '89.72', '86.17', '82.73', '86.17', '83.77', '86.17', '86.17'],
tube_source.wells('A3'),
plate_mapped.wells(['E8', 'F8', 'G8', 'H8', 'A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9']),
touch_tip=True
)

p1000.home()
p1000.start_at_tip(p1000rack['A2']) # necessary to avoid a collision with the p10

p1000.distribute(['100', '89.22', '90.79', '82.17', '79.09', '90.17', '100', '88.9', '87.15', '86.17', '86.17', '81.05'],
tube_source.wells('A3'),
plate_mapped.wells(['A10', 'B10', 'C10', 'D10', 'E10', 'F10', 'G10', 'H10', 'A11', 'B11', 'C11', 'D11']),
touch_tip=True
)
p1000.home()

p1000.distribute(['85.51', '89.6', '90.86', '88.57', '85.58', '100', '86.4', '83.62', '83.55', '85.58', '89.22', '86.17'],
tube_source.wells('A3'),
plate_mapped.wells(['E11', 'F11', 'G11', 'H11', 'A12', 'B12', 'C12', 'D12', 'E12', 'F12', 'G12', 'H12']),
touch_tip=True
)
p1000.home()

# then drugs
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['D3', 'A2', 'E7', 'G5', 'A7', 'F3', 'C12', 'F6', 'D6', 'C7', 'E6', 'B9', 'B4', 'C2', 'A8', 'H2', 'C10', 'D2', 'H3', 'A11', 'E11', 'A3', 'B7', 'B6', 'C1', 'E8', 'E5', 'G7', 'E12', 'D5', 'D7', 'A6'])]
p10.distribute(
    ['0.59'],
    plate_source.wells(0),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['C9', 'H12', 'F4', 'H6', 'G8', 'G9', 'C8', 'F7', 'A5', 'C11', 'H4', 'B1', 'F10', 'D10', 'H11', 'F9', 'F11', 'H1', 'H8', 'H9', 'B11', 'C6', 'C4', 'E9'])]
p10.distribute(
    ['1'],
    plate_source.wells(0),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['E3', 'B2', 'A1', 'G11', 'B10', 'G12', 'A12', 'F12', 'D1', 'F8', 'E2', 'H10', 'G2', 'B8', 'H7', 'D12', 'C5', 'D8', 'A9', 'E4', 'F2', 'G3', 'G4', 'D11', 'B3', 'C3', 'F5', 'H5', 'B5', 'D9', 'E10', 'F1'])]
p10.distribute(
    ['1.41'],
    plate_source.wells(0),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A4'])]
p10.distribute(
    ['2'],
    plate_source.wells(0),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['D3', 'A2', 'E3', 'B2', 'A7', 'F3', 'B10', 'G12', 'D6', 'C7', 'D1', 'F8', 'B4', 'C2', 'G2', 'B8', 'C10', 'D2', 'C5', 'D8', 'E11', 'A3', 'F2', 'G3', 'C1', 'E8', 'B3', 'C3', 'E12', 'D5', 'B5', 'D9'])]
p10.distribute(
    ['0.36'],
    plate_source.wells(1),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['C9', 'H12', 'F4', 'H6', 'G8', 'G9', 'C8', 'F7', 'A5', 'C11', 'D4', 'A4', 'F10', 'D10', 'H11', 'F9', 'F11', 'H1', 'H8', 'H9', 'B11', 'C6', 'C4', 'E9'])]
p10.distribute(
    ['4'],
    plate_source.wells(1),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['E7', 'G5', 'A1', 'G11', 'C12', 'F6', 'A12', 'F12', 'E6', 'B9', 'E2', 'H10', 'A8', 'H2', 'H7', 'D12', 'H3', 'A11', 'A9', 'E4', 'B7', 'B6', 'G4', 'D11', 'E5', 'G7', 'F5', 'H5', 'D7', 'A6', 'E10', 'F1'])]
p10.distribute(
    ['5.64'],
    plate_source.wells(1),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['B1'])]
p10.distribute(
    ['8'],
    plate_source.wells(1),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['D3', 'A2', 'E3', 'B2', 'E7', 'G5', 'A1', 'G11', 'D6', 'C7', 'D1', 'F8', 'E6', 'B9', 'E2', 'H10', 'C10', 'D2', 'C5', 'D8', 'H3', 'A11', 'A9', 'E4', 'C1', 'E8', 'B3', 'C3', 'E5', 'G7', 'F5', 'H5'])]
p10.distribute(
    ['0.36'],
    plate_source.wells(2),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['C9', 'H12', 'F4', 'H6', 'G8', 'G9', 'C8', 'F7', 'A5', 'C11', 'D4', 'A4', 'H4', 'B1', 'H11', 'F9', 'F11', 'H1', 'H8', 'H9', 'B11', 'C6', 'C4', 'E9'])]
p10.distribute(
    ['4'],
    plate_source.wells(2),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['A7', 'F3', 'B10', 'G12', 'C12', 'F6', 'A12', 'F12', 'B4', 'C2', 'G2', 'B8', 'A8', 'H2', 'H7', 'D12', 'E11', 'A3', 'F2', 'G3', 'B7', 'B6', 'G4', 'D11', 'E12', 'D5', 'B5', 'D9', 'D7', 'A6', 'E10', 'F1'])]
p10.distribute(
    ['5.64'],
    plate_source.wells(2),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['D10'])]
p10.distribute(
    ['8'],
    plate_source.wells(2),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['D3', 'A2', 'E3', 'B2', 'E7', 'G5', 'A1', 'G11', 'A7', 'F3', 'B10', 'G12', 'C12', 'F6', 'A12', 'F12', 'C10', 'D2', 'C5', 'D8', 'H3', 'A11', 'A9', 'E4', 'E11', 'A3', 'F2', 'G3', 'B7', 'B6', 'G4', 'D11'])]
p10.distribute(
    ['1.42'],
    plate_source.wells(3),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['C9', 'H12', 'F4', 'H6', 'G8', 'G9', 'C8', 'F7', 'A5', 'C11', 'D4', 'A4', 'H4', 'B1', 'F10', 'D10', 'F11', 'H1', 'H8', 'H9', 'B11', 'C6', 'C4', 'E9'])]
p10.distribute(
    ['2.4'],
    plate_source.wells(3),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['D6', 'C7', 'D1', 'F8', 'E6', 'B9', 'E2', 'H10', 'B4', 'C2', 'G2', 'B8', 'A8', 'H2', 'H7', 'D12', 'C1', 'E8', 'B3', 'C3', 'E5', 'G7', 'F5', 'H5', 'E12', 'D5', 'B5', 'D9', 'D7', 'A6', 'E10', 'F1'])]
p10.distribute(
    ['3.38'],
    plate_source.wells(3),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['F9'])]
p10.distribute(
    ['4.8'],
    plate_source.wells(3),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['D3', 'A2', 'E3', 'B2', 'E7', 'G5', 'A1', 'G11', 'A7', 'F3', 'B10', 'G12', 'C12', 'F6', 'A12', 'F12', 'D6', 'C7', 'D1', 'F8', 'E6', 'B9', 'E2', 'H10', 'B4', 'C2', 'G2', 'B8', 'A8', 'H2', 'H7', 'D12'])]
p10.distribute(
    ['0.31'],
    plate_source.wells(4),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['C9', 'H12', 'F4', 'H6', 'G8', 'G9', 'C8', 'F7', 'A5', 'C11', 'D4', 'A4', 'H4', 'B1', 'F10', 'D10', 'H11', 'F9', 'H8', 'H9', 'B11', 'C6', 'C4', 'E9'])]
p10.distribute(
    ['3.43'],
    plate_source.wells(4),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['C10', 'D2', 'C5', 'D8', 'H3', 'A11', 'A9', 'E4', 'E11', 'A3', 'F2', 'G3', 'B7', 'B6', 'G4', 'D11', 'C1', 'E8', 'B3', 'C3', 'E5', 'G7', 'F5', 'H5', 'E12', 'D5', 'B5', 'D9', 'D7', 'A6', 'E10', 'F1'])]
p10.distribute(
    ['4.84'],
    plate_source.wells(4),
destination_wells
    )
destination_wells = [well.bottom(2) for well in plate_mapped.wells(['H1'])]
p10.distribute(
    ['6.87'],
    plate_source.wells(4),
destination_wells
    )