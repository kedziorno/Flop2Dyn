import os
#List of global variables:

# Name of the configuration file
config_file_name = "float_config.json"

# Path to the FloPoCo executable
flopoco_executable_path = '/home/user/_WORKSPACE_/flopoco/build/bin/flopoco'

# Path to wrapper template
template_path = 'wrapper_template.vhd'

# Use the current working directory as the output directory for VHDL files
vhdl_output_dir = os.getcwd()

#Number of test vectors to be used during simulation
num_test_vectors = 10000

#Name of the output file for operators
out_file_name = 'combined.vhd'

#Name of the output file for wrappers
wrapper_file_name = 'wrapper.vhd'

# Info about all operators, in particular input and output size of flopoco operators
operators_info = {
    "FloatingPointAdder": {
        "input_size": "bitSize",
        "output_size": {
            32: 34,
            64: 66
        },
        "flopoco_name": "FPAdd",
        "wrapper_name": "fadd_op",
        "wrapper_name64": "fadd_op64"
    },
    "FloatingPointComparator": {
        "input_size": "bitSize",
        "output_size": {
            32: 1,
            64: 1
        },          # Output size is 1 bit for a comparator
        "flopoco_name": "FPComp",
        "wrapper_name": ""
    },
    "FloatingPointMultiplier": {
        "input_size": "bitSize",
        "output_size": {
            32: 34,
            64: 66
        },
        "flopoco_name": "FPMult",
        "wrapper_name": "fmul_op",
        "wrapper_name64": "fmul_op64"
    },
    "FloatingPointDivider": {
        "input_size": "bitSize",
        "output_size": {
            32: 34,
            64: 66
        },
        "flopoco_name": "FPDiv",
        "wrapper_name": "fdiv_op",
        "wrapper_name64": "fdiv_op64"
    },
    "FloatingPointSubtractor": {
        "input_size": "bitSize",
        "output_size": {
            32: 34,
            64: 66
        },
        "flopoco_name": "FPAdd",
        "wrapper_name": 'fsub_op',
        "wrapper_name64": "fsub_op64"
    },
    # Add more operators as needed
    "FloatingPointSQRT": {
        "input_size": "bitSize",
        "output_size": {
            32: 34,
            64: 66
        },
        "flopoco_name": "FPSqrt",
        "wrapper_name": 'fsqrt_op',
        "wrapper_name64": "fsqrt_op64"
    },
    "FloatingPoint2Fix": {
        "input_size": "bitSize",
        "output_size": {
            32: 34,
            64: 66
        },
        "flopoco_name": "FP2Fix",
        "wrapper_name": 'fp2fix_op',
        "wrapper_name64": "fp2fix_op64"
    },
    "Fix2FloatingPoint": {
        "input_size": "bitSize",
        "output_size": {
            32: 34,
            64: 66
        },
        "flopoco_name": "Fix2FP",
        "wrapper_name": 'fix2fp_op',
        "wrapper_name64": "fix2fp_op64"
    }
}

# Wrapper templates for components
buffer_template = "buff: entity work.delay_buffer(arch) generic map({buffer_delay})\n        port map(clk,\n                rst,\n                join_valid,\n                oehb_ready,\n                buff_valid);"
join_template = "join: entity work.join(arch) generic map(2)\n        port map( pValidArray,\n                oehb_ready,\n                {join_valid},\n                readyArray);"
oehb_template = "oehb: entity work.OEHB(arch) generic map (1, 1, 1, 1)\n                port map (\n                --inputspValidArray\n                    clk => clk,\n                    rst => rst,\n                    pValidArray(0)  => buff_valid, -- real or speculatef condition (determined by merge1)\n                    nReadyArray(0) => nReadyArray(0),\n                    validArray(0) => validArray(0),\n                --outputs\n                    readyArray(0) => oehb_ready,\n                    dataInArray(0) => oehb_datain,\n                    dataOutArray(0) => oehb_dataOut\n                );"
intermediate_input_template = "signal X_in, Y_in : std_logic_vector({operator_width} downto 0);"
intermediate_output_template = "signal R_out : std_logic_vector({operator_width} downto 0);"
nfloat2ieee_template = "nfloat2ieee : entity work.OutputIEEE_{bit}bit(arch)\n                port map (\n                    --input\n                    X => R_out,\n                    --ouput\n                    R => dataOutArray(0)\n                );"
ieee2nfloat_0_template = "ieee2nfloat_0: entity work.InputIEEE_{bit}bit(arch)\n                port map (\n                    --input\n                    X => dataInArray(0),\n                    --output\n                    R => X_in\n                );"
ieee2nfloat_1_template = "ieee2nfloat_1: entity work.InputIEEE_{bit}bit(arch)\n                port map (\n                    --input\n                    X => {entity_connection},\n                    --output\n                    R => Y_in\n                );"



main_component_template = """component {operator_name} is
        port (
            clk{ce} : in std_logic;
            X : in  std_logic_vector({input_width} downto 0);
            Y : in  std_logic_vector({input_width} downto 0);
            R : out  std_logic_vector({output_width} downto 0)
            );
    end component;"""


# Following strings will be used in modifying the wrapper to construct the wrapper for the subtractor
sub_intermediate_signal = "--intermediate signal for bit flipping for subtraction \n    signal Y_flipped : std_logic_vector(31 downto 0); \n"
bit_flipper = "bitflipper: entity work.FlipMSB generic map (BIT_WIDTH => {bit_width}) \n                port map ( \n                    input_signal => dataInArray(1), \n                    output_signal => Y_flipped \n                );"

#
signal_join_valid = "signal join_valid : STD_LOGIC;"

# Defining a dictionary to make access to templates easier and more consistent
component_templates = {
    "buffer_template": buffer_template,
    "join_template": join_template,
    "oehb_template": oehb_template,
    "main_component_template": main_component_template,
    "intermediate_input_template": intermediate_input_template,
    "intermediate_output_template": intermediate_output_template,
    "nfloat2ieee_template": nfloat2ieee_template,
    "ieee2nfloat_0_template": ieee2nfloat_0_template,
    "ieee2nfloat_1_template": ieee2nfloat_1_template,
    "sub_intermediate_signal": sub_intermediate_signal,
    'bit_flipper': bit_flipper,
    "signal_join_valid": signal_join_valid
}

# TODO: Flags of corresponding floating point comparators in FloPoCo
# note: it might make more sense to include this information in operators_info
comparison_flags = {

}

wrapper_template = """-----------------------------------------------------------------------
-- {operator_name}, version 0.0
-----------------------------------------------------------------------

Library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.customTypes.all;

entity {dynamatic_name} is
Generic (
 INPUTS: integer := 2; 
 OUTPUTS: integer := 1; 
 DATA_SIZE_IN: integer := 32; 
 DATA_SIZE_OUT: integer := 32
);
port (
  clk : IN STD_LOGIC;
  rst : IN STD_LOGIC;
  pValidArray : IN std_logic_vector(1 downto 0);
  nReadyArray : in std_logic_vector(0 downto 0);
  validArray : out std_logic_vector(0 downto 0);
  readyArray : OUT std_logic_vector(1 downto 0);
  dataInArray : in data_array (1 downto 0)(DATA_SIZE_IN-1 downto 0);
  dataOutArray : out data_array (0 downto 0)(DATA_SIZE_OUT-1 downto 0));
end entity;

architecture arch of {dynamatic_name} is
    {main_component}

    {signal_join_valid}

    signal buff_valid, oehb_valid, oehb_ready : STD_LOGIC;
    signal oehb_dataOut, oehb_datain : std_logic_vector(0 downto 0);

    --intermediate input signals for float conversion
    {intermediate_input}

    --intermidiate output signal(s) for float conversion
    {intermediate_output}

    {additional_signals}

    begin


        {join}

        {buffer}

        oehb: entity work.OEHB(arch) generic map (1, 1, 1, 1)
                port map (
                --inputspValidArray
                    clk => clk,
                    rst => rst,
                    pValidArray(0)  => buff_valid, -- real or speculatef condition (determined by merge1)
                    nReadyArray(0) => nReadyArray(0),
                    validArray(0) => validArray(0),
                --outputs
                    readyArray(0) => oehb_ready,
                    dataInArray(0) => oehb_datain,
                    dataOutArray(0) => oehb_dataOut
                );

        {ieee2nfloat_0}

        {ieee2nfloat_1}

        {bit_flip_instance}

        {nfloat2ieee}

        operator :  component {operator_name}
        port map (
            clk   => clk,{clock_enable}
            X  => X_in,
            Y  => Y_in,
            R  => R_out
        );
end architecture;

"""

supported_operators_info =[
    {   
        "name": "FloatingPointAdder",
        "flopoco_name": "FPAdd",
        "exponent_size": 8,
        "mantissa_size": 23,
    },
    {
        "name": "FloatingPointMultiplier",
        "flopoco_name": "FPMult",
        "exponent_size": 8,
        "mantissa_size": 23,
    },
    {
        "name": "FloatingPointDivider",
        "flopoco_name": "FPDiv",
        "exponent_size": 8,
        "mantissa_size": 23,
    },
    {
        "name": "FloatingPointComparator",
        "flopoco_name": "FPComparator",
        "exponent_size": 8,
        "mantissa_size": 23,
    },
    {
        "name": "FloatingPointPower",
        "flopoco_name": "FPPow",
        "exponent_size": 8,
        "mantissa_size": 23,
    },
    {
        "name": "FloatingPointSquareRoot",
        "flopoco_name": "FPSqrt",
        "exponent_size": 8,
        "mantissa_size": 23,
    },
    {
        "name": "FloatingPointExponential",
        "flopoco_name": "FPExp",
        "exponent_size": 8,
        "mantissa_size": 23,
    },
    {
        "name": "FloatingPointLogarithm",
        "flopoco_name": "FPLog",
        "exponent_size": 8,
        "mantissa_size": 23,
    }
]
