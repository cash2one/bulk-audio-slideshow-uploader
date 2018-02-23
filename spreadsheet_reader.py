import sys
import csv
import os.path


GUIDE_PATH = 'frontera_files/guide20180222.csv'

def make_movie(name, main_image, img_dir, mp3_path, description):
    return

if len(sys.argv) != 3:
    raise Exception("Script requires exactly two arguments for database row start and end")

row_start = int(sys.argv[1]) - 1
row_end = int(sys.argv[2]) - 1

with open(GUIDE_PATH) as f:
    file_reader = list(csv.reader(f))
    for row in file_reader[row_start: row_end]:
        name = row[0]
        main_image = os.path.join(*row[2].split('\\'))
        img_dir = os.path.abspath(os.path.join(row[3], os.pardir))
        mp3_path = os.path.join(*row[10].split('\\'))
        description = "placeholder for description\nwith\n\nmultiple lines" 
        
        make_movie(name, main_image, img_dir, mp3_path, description)