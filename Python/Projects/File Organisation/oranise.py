import pathlib 
import shutil
import pprint 
dire = pathlib.Path("Organised_Folder")
folders = []
files = []
for file in dire.iterdir():
    if file.is_file():
        files.append(file)
    elif file.is_dir():
        folders.append(file)

#print(folders)         
#print(files)

filefolder = {}
for folder in folders:
    if folder.name.endswith('Pdf'):
        pdflist = []
        for file in files:
            if file.name.endswith('pdf'):
                filefolder[folder] = pdflist
                pdflist.append(file)
    elif folder.name.endswith('images'):
        imagelist = []
        for file in files:
            if file.name.endswith('jpg'):
                filefolder[folder] = imagelist
                imagelist.append(file)
    elif folder.name.endswith('sound'):
        soundlist = []
        for file in files:
            if file.name.endswith('mp3'):
                filefolder[folder] = soundlist
                soundlist.append(file)
    elif folder.name.endswith('Text'):
        textlist = []
        for file in files:
            if file.name.endswith('txt'):
                filefolder[folder] = textlist
                textlist.append(file)

pprint.pprint(filefolder)


for keys, values in filefolder.items():
    for elements in values:
        shutil.move(elements,keys)