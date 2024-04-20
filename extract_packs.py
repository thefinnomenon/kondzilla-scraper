import json
import wget
import sys
import glob
import os
import shutil
from zipfile import ZipFile

######
## Kondzilla Pack Extractor
##
## Json list => http://api.kondzilla.opalastudios.com/api/fetch
##
## Pack url example (name = Compromisso)
## http://storage.kondzilla.opalastudios.com/kondzilla/Compromisso/Sounds.zip
##
## Sounds.zip contains wav files for the different pad sounds and a 
## few files for app information that can be ignored.
##
## Output
## ./kondzilla/{Name1}/wav files
##            /{Name2}/wav files
##            ...
######

url = 'http://storage.kondzilla.opalastudios.com/kondzilla/{}/Sounds.zip' 
outputDir = './kondzilla/{}/'

if os.path.isdir(outputDir.format('')):
  print ("Root directory exists")
else:
  try:
    os.mkdir(outputDir.format(''))
  except OSError:
    print ("Creation of the root directory failed")
    sys.exit(1)

with open('kondzilla_list.json') as data_file:
  data = json.load(data_file)
  for kit in data['kits']:
    print(kit['name'])
    name = kit['name']
    packOutputDir = outputDir.format(name)
    if os.path.isdir(packOutputDir):
      print ("Pack directory already exists, skipping...")
    else:
      try:
        os.mkdir(packOutputDir)
      except OSError:
        print ("Creation of the pack directory failed")
        continue
      else:
        wget.download(url.format(name), packOutputDir+'Pack.zip')
        with ZipFile(packOutputDir+'Pack.zip', 'r') as zip_ref:
          zip_ref.extractall(packOutputDir)
          for file in glob.glob(packOutputDir+'Sounds/*.wav'):
            shutil.move(file, packOutputDir)
          os.remove(packOutputDir+'Pack.zip')
          shutil.rmtree(packOutputDir+'Sounds', ignore_errors=True)