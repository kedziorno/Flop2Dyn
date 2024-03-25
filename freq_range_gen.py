import json
import subprocess
import os
import re
import shutil
import argparse
import matplotlib.pyplot as plt

import setup # This file contains variables
from file_manager import read_config
from file_manager import remove_simulation_files
from file_manager import combine_vhdl_files
from vhdl_generator import generate_vhdl
from wrapper_generator import create_wrappers

# This python script generates the operators for a range of frequencies

def generate_operator(operator_info, frequency):
    # Construct the FloPoCo command based on the operator_config
    command = [
        setup.flopoco_executable_path, 
        operator_info["flopoco_name"],
        f'wE={operator_info["exponent_size"]}', 
        f'wF={operator_info["mantissa_size"]}', 
        f'frequency={frequency}',
        f'name={operator_info["name"]}',
        f'clockEnable=True',
        f'outputFile={operator_info["name"]}_{frequency}_MHz.vhd'
    ]

    # Execute the command and capture the output
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(f"Generated: {operator_info['name']}_{frequency}_MHz.vhd")

def main():
    step_size = 50
    max_frequency = 900
    min_frequency = 100

    # Iterate over the operators_info list
    for operator_info in setup.supported_operators_info:
        
        #frequencies = [None] * ((max_frequency - min_frequency) // step_size)

        for freq in range(min_frequency, max_frequency, step_size):
            # Get the pipeline depth and target frequency
            target_frequency = freq
            generate_operator(operator_info, target_frequency)
            #frequencies[(freq - min_frequency) // step_size] = freq


if __name__ == "__main__":
    main()