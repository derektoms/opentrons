## Converting a central composite design (CCD) to Opentrons
## 05-02-2018

# import rpy2 to run R inside python environment
import rpy2
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

base = importr('base')
utils = importr('utils')

# read csv into a R dataframe
m = utils.read_csv('2018-02-01_INS-1_CCD_coded.csv')

# collect factor destinations
factorList = []
for v in range(3,9):
    factorList.append([])
    for u in range(0,5):
        factorList[v-3].append([])
        factorTest = m.rx(m.rx2(v+1).ro==(u+1),'well')
        for w in range(0,len(factorTest)):
            factorList[v-3][u].append(factorTest.levels[factorTest[w]-1])

import csv
# collect base media volumes
with open('Desktop/CCDmedia-vols.csv', 'r') as f:
  reader = csv.reader(f)
  mvolW = []
  mvolV = []
  for row in reader:
      well = row[0]
      volume = row[1]
      
      mvolW.append(well)
      mvolV.append(volume)    

  
# use a calculated value from the spreadsheet for the volume to add
with open('Desktop/CCDvols.csv', 'r') as f:
  reader = csv.reader(f)
  pvol = list(reader)
          
# print 'er out for 'CCD_plate_setup_2018.v1.py'
# base media based on calculated volumes
for x in range(0,8):     print('p1000.distribute(',mvolV[(x*12+1):(x*12+13)],',\ntube_source.wells(\'A3\'),\nplate_mapped.wells(',mvolW[(x*12+1):(x*12+13)],'),\ntouch_tip=True\n)\np1000.home()\n',sep='')

# then drugs
for y in range(1,6): # FACTORS start at 1 to avoid the size variable
    for x in range(1,5): # LEVELS start at 1 because we don't add anything for zeros
        print('destination_wells = [well.bottom(2) for well in plate_mapped.wells(',factorList[y][x],')]\np10.distribute(\n    ',pvol[(x-1)+4*(y-1)],',\n    plate_source.wells(',(y-1),'),\ndestination_wells\n    )',sep='')
        
        
## this is for the first row (aggregate size)
for y in range(0,3):
    for x in range(0,1): # just the first set
        print('p',250*(1+y),factorList[x][y],sep='')