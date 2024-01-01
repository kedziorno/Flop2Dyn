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
    parser = argparse.ArgumentParser(description='Process VHDL files.')
    
    # Add optional arguments
    parser.add_argument('--vhdl_output_dir', help='Directory for VHDL output. Default is current working directory.', default=setup.vhdl_output_dir)
    parser.add_argument('--wrapper_file_name', help='Name of the wrapper file. Default is wrapper.vhd in current working directory.', default=setup.wrapper_file_name)
    parser.add_argument('--template_path', help='Path to the wrapper template file. Default is wrapper_template.vhd in current working directory.', default=setup.template_path)
    parser.add_argument('--out_file_name', help='Name of the output file. Default is combined.vhd', default=setup.out_file_name)
    parser.add_argument('--num_test_vectors', type=int, help='Number of test vectors. Default is 10000', default=setup.num_test_vectors)
    parser.add_argument('--config_file_name', help='Path to the configuration JSON file. Default is float_config.json in current working directory.', default=setup.config_file_name)
    parser.add_argument('--flopoco_path', help='Path to the FloPoCo executable.', default=setup.flopoco_executable_path)
    parser.add_argument('--clean_simulation_files', type=bool, help='Set to false to keep simulation files. Default is true.', default=True)

    # Parse the arguments
    args = parser.parse_args()
    # print(args)
    config = read_config(args.config_file_name)
    # print(args.config_file_name)
    operators = config['operators']

    #This list will contain the path(s) to all generated vhdl files, later these files will be merged
    path_list = []

    #This dictionary will contain information about the generated operators that will be used in wrapper generation
    operators_info = []

    for operator in operators:
        vhdl_info = generate_vhdl(
            operator, args.num_test_vectors, 
            args.vhdl_output_dir, 
            args.flopoco_path, 
            args.clean_simulation_files, 
            setup.operators_info)

        # Store information regarding the generation of operators in this list
        operator_info = {
            'name': operator['name'],
            'bitSize': operator['bitSize'],
            'pipeline_depth': vhdl_info['pipeline_depth'],
        }
        operators_info.append(operator_info)

        if vhdl_info['pipeline_depth'] is not None:
            print(f"Pipeline depth: {vhdl_info['pipeline_depth']}")
            pipeline_depth = vhdl_info['pipeline_depth']
        else:
            print("Pipeline-depth regex is not working")

        if 'vhdl_file_path' in vhdl_info:
            path_list.append(vhdl_info['vhdl_file_path'])
            print(f"Generated VHDL file moved to: {vhdl_info['vhdl_file_path']}")

    wrapper_path = os.path.join(args.vhdl_output_dir, args.wrapper_file_name)
    create_wrappers(operators_info, args.template_path, wrapper_path, setup.operators_info, setup.component_templates)

    # combined_vhdl_file_path = args.out_file_name
    combined_vhdl_file_path = os.path.join(args.vhdl_output_dir, args.out_file_name)
    combine_vhdl_files(path_list, combined_vhdl_file_path)

if __name__ == "__main__":
    main()