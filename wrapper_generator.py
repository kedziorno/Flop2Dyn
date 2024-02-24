

#TODO: take the edge cases into account, where pipeline-depth is 1 or 0
#TODO: implement wrappers for 64bit operators
def create_wrappers(operators, template, combined_file_path, operators_info, component_templates):
    # Create/overwrite wrapper VHDL file
    with open(combined_file_path, 'w') as combined_file:
        for operator in operators:
            # Format the operator with appropriate parameters
            ce_signal_1 = ""
            for i in range(operator['pipeline_depth']):
                ce_signal_1 = ce_signal_1 + f", ce_{i+1}"
            main_component = component_templates['main_component_template'].format(
                operator_name=operator['name'],
                ce=ce_signal_1,
                input_width=operator['bitSize'] + 2 - 1, # +2 because 2 extra bits in nFloat
                output_width=operators_info[operator['name']]["output_size"][operator['bitSize']] - 1
            )
            # Handle intermediate signals between conversion (between IEEE and nFloat) and operator
            intermediate_input = component_templates['intermediate_input_template'].format(operator_width=operator['bitSize'] + 2 - 1)
            intermediate_output = component_templates['intermediate_output_template'].format(
                operator_width=operators_info[operator['name']]["output_size"][operator['bitSize']] - 1)
            
            # Handle first IEEE to nFloat converter
            ieee2nfloat_0 = component_templates['ieee2nfloat_0_template'].format(bit=operator["bitSize"])

            # Handle second IEEE to nFloat converter and additional components depending on the operator
            if operator['name'] == "FloatingPointSubtractor":
                additional_signals = component_templates['sub_intermediate_signal']
                bit_flip_instance = component_templates['bit_flipper'].format(bit_width=operator['bitSize'])
                ieee2nfloat_1 = component_templates['ieee2nfloat_1_template'].format(bit=operator["bitSize"], entity_connection="Y_flipped")
            else:
                additional_signals = ""
                bit_flip_instance = ""
                ieee2nfloat_1 = component_templates['ieee2nfloat_1_template'].format(bit=operator["bitSize"], entity_connection="dataInArray(1)")

            # If the output is not a float (e.g FP comparator), do not instantiate converter from nFloat to IEEE
            if operators_info[operator['name']]["output_size"][operator['bitSize']] == 1:
                nfloat2ieee = ""
            else:
                nfloat2ieee = component_templates['nfloat2ieee_template'].format(bit=operator['bitSize'])

            # TODO: Prepare VHDL code based on pipeline_depth
            if operator['pipeline_depth'] == 0 or operator['pipeline_depth'] == 1:
                buffer = ""
                signal_join_valid = ""
                join = component_templates['join_template'].format(join_valid="buff_valid")
                print("Warning: Pipeline depth of " + str(operator['name']) + " is " + str(operator['pipeline_depth']))
            elif operator['pipeline_depth'] > 1:
                buffer = component_templates['buffer_template'].format(buffer_delay=operator['pipeline_depth'] - 1)
                signal_join_valid = component_templates['signal_join_valid']
                join = component_templates['join_template'].format(join_valid="join_valid")
            #elif operator['pipeline_depth'] == 1:
            #    buffer = ""
            else:
                print("Warning: Something went wrong. Pipeline depth: " + str(operator['pipeline_depth']) + " for operator " + str(operator['name']))

            ce_signal_2 = ""
            for i in range(operator['pipeline_depth']):
                ce_signal_2 = ce_signal_2 + f"\n            ce_{i+1} => oehb_ready,"

            # Replace placeholders in the template
            wrapper_vhdl = template.format(
                dynamatic_name=operators_info[operator['name']]['wrapper_name'],
                operator_name=operator['name'],
                #buffer_delay=operator['pipeline_depth'] - 1,
                operator_width=operator['bitSize'] + 2 - 1, # +2 because 2 extra bits in FloPoCo
                additional_signals=additional_signals,
                bit_flip_instance=bit_flip_instance,
                #entity_connection=entity_connection,
                join=join,
                buffer=buffer,
                main_component=main_component,
                intermediate_input=intermediate_input,
                intermediate_output=intermediate_output,
                ieee2nfloat_0 = ieee2nfloat_0,
                ieee2nfloat_1 = ieee2nfloat_1,
                nfloat2ieee = nfloat2ieee,
                signal_join_valid = signal_join_valid,
                clock_enable = ce_signal_2
            )

            # Write the formatted VHDL to the combined file
            combined_file.write(wrapper_vhdl)
            combined_file.write('\n\n')  # Add newlines for separation
