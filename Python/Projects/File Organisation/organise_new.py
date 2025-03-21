import pathlib 
import shutil
from pprint import pprint
dire = pathlib.Path("Organised_Folder")
folders = {folder.name: folder for folder in dire.iterdir() if folder.is_dir()}
files = {file.name: file for file in dire.iterdir() if file.is_file()}
# pprint(folders)
# pprint(files)

filefolders = {folder: [] for folder in folders.values()}

foldermapping = {
    "Pdf" : "pdf",
    "images" : "jpg",
    "sound" : "mp3",
    "Text" : "txt",
}

# for foldername, file in zip(folders.values(), files.values()):
#     for folder, extenstion in zip( filefolders.keys(), foldermapping.values()):
#         if file.suffix == f".{extenstion}": #and foldername.name == folder:
#             filefolders[folder].append(file)

for file in files.values():
    # for folder in folders.values():
        for folder_name, extention in foldermapping.items():
            if file.suffix == f".{extention}": #and folder.name == folder_name:
                folder = folders.get(folder_name)
                if folder:
                    filefolders[folder].append(file)

pprint(filefolders)
for folder, files in filefolders.items():
    for file in files:
        shutil.move(str(file),str(folder))
