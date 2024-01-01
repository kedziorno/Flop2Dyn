# PyFloGen - VHDL Generation for FloPoCo and Dynamatic Integration

PyFloGen is a toolkit for generating VHDL code for floating-point operations, specifically tailored for integration with Dynamatic, an academic, open-source high-level synthesis compiler. This tool automates the process of creating VHDL modules via FloPoCo, making it easier to incorporate floating-point computations in Dynamatic's dynamically-scheduled circuits generated from C/C++ code.

## Features

- Automated VHDL code generation using FloPoCo.
- Custom wrapper generation for integration with Dynamatic.
- Support for a variety of floating-point operations including addition, subtraction, multiplication, and division.
- Command-line interface for adaptable and dynamic usage.
- Simulation and testbench generation for robust testing and validation.

## Getting Started

### Prerequisites

- Python 3.x
- FloPoCo (Floating Point Core Generator) installed.

### Overview of project

- float_gen.py includes the main function.
- float_config.json is an example configuration file.
- The directory lib contains additional VHDL code. The generated VHDL code will depend on this code.
- setup.py includes default parameters and variables.
- wrapper_template.vhd is the VHDL template with placeholders.

### Installation

1. Clone the PyFloGen repository:
   ```bash
   git clone https://github.com/sevkobat/PyFloGen.git

2. Navigate to the PyFloGen directory:
    ````bash
    cd PyFloGen

3. Run "float_gen.py" with desired parameters.
    ```bash
    python3 float_gen.py -h
    ```
    This will list all possible parameters and their descriptions.