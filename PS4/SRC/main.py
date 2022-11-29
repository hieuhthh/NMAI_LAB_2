import os
from KB import *

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'
DEBUG = True

make_dir(OUTPUT_DIR)

for file in sorted(os.listdir(INPUT_DIR)):
    print(f'Solving {file}')
    input_path = os.path.join(INPUT_DIR, file)
    output_path = os.path.join(OUTPUT_DIR, file)
    solve_end2end(input_path, output_path, DEBUG)
    print(f'Finished {file}\n')