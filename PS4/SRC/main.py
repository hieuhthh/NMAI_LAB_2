import os
from KB import *

INPUT_DIR = 'INPUT'
OUTPUT_DIR = 'OUTPUT'
DEBUG = False # print detail for debug

make_dir(OUTPUT_DIR)

for file in sorted(os.listdir(INPUT_DIR)):
    print(f'Solving {file}')
    input_path = os.path.join(INPUT_DIR, file)
    name_outfile = 'output' + file[5:]
    output_path = os.path.join(OUTPUT_DIR, name_outfile)
    solve_end2end(input_path, output_path, DEBUG)
    print(f'Finished {file}\n')