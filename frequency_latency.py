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

def get_pipeline_depth(operator_info, frequency):
    # Construct the FloPoCo command based on the operator_config
    command = [
        setup.flopoco_executable_path, 
        operator_info["flopoco_name"],
        f'wE={operator_info["exponent_size"]}', 
        f'wF={operator_info["mantissa_size"]}', 
        f'frequency={frequency}',
        f'name={operator_info["name"]}',
        f'clockEnable=True'
    ]
    
    # Execute the command and capture the output
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = process.stdout
    
    # Also capture any errors: IN THIS CASE errors contains the informative command line output
    errors = process.stderr

    # Determine the pipeline depth and thus the latency of the generated operator
    # Find all occurrences of pipeline depth
    pipeline_depth_matches = re.findall(r'Pipeline depth = (\d+)', errors)
    
    # Select the last occurrence if there are any, otherwise set to None
    pipeline_depth = int(pipeline_depth_matches[-1]) if pipeline_depth_matches else None

    return pipeline_depth


def main():
    pipeline_depth_to_frequency = {}

    # Iterate over the operators_info list
    for operator_info in setup.supported_operators_info:
        frequency_to_pipeline_depth = [None] * (900 - 100) // 10
        for freq in range(100, 900, 10):
            # Get the pipeline depth and target frequency
            target_frequency = freq
            pipeline_depth = get_pipeline_depth(operator_info, target_frequency)
            frequency_to_pipeline_depth[target_frequency // 10] = pipeline_depth
            # Plot the values
            frequencies = list(range(100, 900, 10))
            plt.plot(frequencies, frequency_to_pipeline_depth)
            plt.xlabel('Frequency')
            plt.ylabel('Pipeline Depth')
            # Save the plot as an image
            plt.savefig('/Users/sevketbaturay/Documents/Flop2Dyn/plot.png')

        # Get the pipeline depth and target frequency
        pipeline_depth = operator_info['pipeline_depth']
        target_frequency = operator_info['target_frequency']  # Assuming 'target_frequency' is a key in operator_info

        # Add the pipeline depth and target frequency to the mapping
        pipeline_depth_to_frequency[pipeline_depth] = target_frequency

# Now, pipeline_depth_to_frequency is a dictionary that maps pipeline depth to target frequency
    print(pipeline_depth_to_frequency)

if __name__ == "__main__":
    main()