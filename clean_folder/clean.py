import re
import sys
import shutil
from pathlib import Path

UKRAINIAN = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

images_files = []
docx_files = []
folders = []
audio_files = []
video_files = []
archives = []
other = []
unknown_extensions = set()
extensions = set()

known_extensions = {
    ('JPEG', 'PNG', 'JPG', 'SVG') : images_files,
    ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'RTF'): docx_files,
    ('ZIP', 'GZ', 'TAR', 'WIN'): archives,
    ('MP3', 'OGG', 'WAV', 'AMR') : audio_files,
    ('AVI', 'MP4', 'MOV', 'MKV', 'WEBM') : video_files
}

TRANS = {}

for key, value in zip(UKRAINIAN, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()

def normalize(name: str) -> str:
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', '_', new_name)
    return f"{new_name}.{'.'.join(extension)}"


def all_extentions() -> tuple: #returns tuple all known extentions
    keys = ()
    for key in known_extensions:
        keys+=key

    return keys

def get_extensions(file_name) -> str:
    return Path(file_name).suffix[1:].upper()

def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'other_files'):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name

        if not extension:
            other.append(new_name)
        if extension not in all_extentions():
            unknown_extensions.add(extension)
            other.append(new_name)
        else:
            for key in known_extensions:
                try: #not sure if try-except actualy needed here 
                    if extension in key:
                        container = known_extensions[key]
                        extensions.add(extension)
                        container.append(new_name)
                except KeyError:
                    unknown_extensions.add(extension)
                    other.append(new_name)

#scans all folders, needed to create a result.txt after sorting
def simple_scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            folders.append(item)
            simple_scan(item)

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name

        if extension not in all_extentions() and not item.is_dir():
            if extension:
                unknown_extensions.add(extension)
                other.append(new_name)
            if not extension:
                unknown_extensions.add('unknown')
        else:
            for key in known_extensions:
                if extension in key:
                    container = known_extensions[key]
                    extensions.add(extension)
                    container.append(new_name)

#creates reault.txt after simple_scan
def write_results_to_file(path): 
    file = open(f"{path}/result.txt", "w")

    file.writelines([f'Images: \n{images_files}\n', 
    f'\nDocx: \n{docx_files}\n', 
    f'\nArchives: \n{archives}\n', 
    f'\nAudio: \n{audio_files}\n', 
    f'\nVideo: \n{video_files}\n', 
    f'\nOthers: \n{other}\n', 
    f'\nAll extensions: {extensions}\n', 
    f'\nUnknown extensions: {unknown_extensions}\n',])

    file.close()

def handle_file(path, root_folder, dist):
    target_folder = root_folder/dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize(path.name))

def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    suffix = Path(path.name).suffix
    new_name = normalize(path.name).replace(suffix, '')

    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()

def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass

def main():
    folder_path = Path(sys.argv[1])

    print(folder_path)

    scan(folder_path)

    for file in other:
        handle_file(file, folder_path, "others")

    for file in images_files:
        handle_file(file, folder_path, "images")

    for file in docx_files:
        handle_file(file, folder_path, "documents")

    for file in audio_files:
        handle_file(file, folder_path, "audio")

    for file in video_files:
        handle_file(file, folder_path, "video")

    for file in archives:
        handle_archive(file, folder_path, "archives")

    remove_empty_folders(folder_path)

#aftersorting scan
    simple_scan(folder_path) 
#creates txt file with all files and extentions
    write_results_to_file(folder_path)

#no need in this because of created result.txt. Can be commented
    print(f"Images: {len(images_files)}")
    print(f"Docx: {len(docx_files)}")
    print(f"Audio: {len(audio_files)}")
    print(f"Video: {len(video_files)}")
    print(f"Others: {len(other)}")
    print(f"All known extensions: {extensions}")
    print(f"Unknown extensions: {unknown_extensions}")
    print(f'For a more detailed report, look at this file {folder_path}/result.txt') 

if __name__ == '__main__':
    main()
