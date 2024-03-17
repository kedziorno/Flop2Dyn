import json
import subprocess
import os
import re
import shutil
import argparse

import setup # This file contains variables
from file_manager import read_config
from file_manager import remove_simulation_files
from file_manager import combine_vhdl_files
from vhdl_generator import generate_vhdl
from wrapper_generator import create_wrappers

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Generate floating point arithmetic units using FloPoCo.')
    
    # Add optional arguments
    parser.add_argument('--vhdl_output_dir', help='Directory for VHDL output. Default is current working directory.', default=setup.vhdl_output_dir)
    parser.add_argument('--wrapper_file_name', help='Name of the wrapper file. Default is wrapper.vhd in current working directory.', default=setup.wrapper_file_name)
    parser.add_argument('--template_path', help='Path to the wrapper template file. Default is wrapper_template.vhd in current working directory.', default=setup.template_path)
    parser.add_argument('--out_file_name', help='Name of the output file. Default is combined.vhd', default=setup.out_file_name)
    parser.add_argument('--num_test_vectors', type=int, help='Number of test vectors. Default is 10000', default=setup.num_test_vectors)
    parser.add_argument('--config_file_name', help='Path to the configuration JSON file. Default is float_config.json in current working directory.', default=setup.config_file_name)
    parser.add_argument('--flopoco_path', help='Path to the FloPoCo executable.', default=setup.flopoco_executable_path)
    parser.add_argument('--keep_simulation_files', action='store_false', help='Prevents deletion of files created during simulation. No value required')
    parser.add_argument('--skip_simulation', action='store_false', help='Prevents simulation. No value required')

    # Parse the arguments
    args = parser.parse_args()

    pipeline_depth_to_frequency = {}

    # Iterate over the operators_info list
    for operator_info in setup.operators_info:
        # Get the pipeline depth and target frequency
        pipeline_depth = operator_info['pipeline_depth']
        target_frequency = operator_info['target_frequency']  # Assuming 'target_frequency' is a key in operator_info

        # Add the pipeline depth and target frequency to the mapping
        pipeline_depth_to_frequency[pipeline_depth] = target_frequency

# Now, pipeline_depth_to_frequency is a dictionary that maps pipeline depth to target frequency
    print(pipeline_depth_to_frequency)

if __name__ == "__main__":
    main()