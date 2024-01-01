

#TODO: take the edge cases into account, where pipeline-depth is 1 or 0
#TODO: implement wrappers for 64bit operators
def create_wrappers(operators, template_path, combined_file_path, operators_info, component_templates):
    #print(operators)
    # Open the combined file in write mode to overwrite existing content
    with open(combined_file_path, 'w') as combined_file:
        for operator in operators:
            # Read the template for each operator
            with open(template_path, 'r') as file:
                template = file.read()
            #print(operator)
                
            main_component = component_templates['main_component_template'].format(
                operator_name=operator['name'],
                input_width=operator['bitSize'] + 2 - 1, # +2 because 2 extra bits in nFloat
                output_width=operators_info[operator['name']]["output_size"][operator['bitSize']] - 1
            )
            intermediate_input = component_templates['intermediate_input_template'].format(operator_width=operator['bitSize'] + 2 - 1)
            intermediate_output = component_templates['intermediate_output_template'].format(
                operator_width=operators_info[operator['name']]["output_size"][operator['bitSize']] - 1)
            
            ieee2nfloat_0 = component_templates['ieee2nfloat_0_template'].format(bit=operator["bitSize"])

            # Prepare additional VHDL code based on operator type
            if operator['name'] == "FloatingPointSubtractor":
                additional_signals = component_templates['sub_intermediate_signal']
                bit_flip_instance = component_templates['bit_flipper'].format(bit_width=operator['bitSize'])
                #entity_connection = "Y_flipped"
                ieee2nfloat_1 = component_templates['ieee2nfloat_1_template'].format(bit=operator["bitSize"], entity_connection="Y_flipped")
            else:
                additional_signals = ""
                bit_flip_instance = ""
                #entity_connection = "dataInArray(1)"
                ieee2nfloat_1 = component_templates['ieee2nfloat_1_template'].format(bit=operator["bitSize"], entity_connection="dataInArray(1)")

            # If the output is not a float (e.g FP comparator), do not instantiate converter
            if operators_info[operator['name']]["output_size"][operator['bitSize']] == 1:
                nfloat2ieee = ""
            else:
                nfloat2ieee = component_templates['nfloat2ieee_template'].format(bit=operator['bitSize'])

            # TODO: Prepare VHDL code based on pipeline_depth
            if not operator['pipeline_depth']:
                buffer = ""
                print("Warning: No pipeline depth found")
            elif operator['pipeline_depth'] > 1:
                buffer = component_templates['buffer_template'].format(buffer_delay=operator['pipeline_depth'] - 1)
            elif operator['pipeline_depth'] == 1:
                buffer = ""
            else:
                print("Warning: Pipeline depth: " + str(operator['pipeline_depth']))

            # Replace placeholders in the template
            wrapper_vhdl = template.format(
                dynamatic_name=operators_info[operator['name']]['wrapper_name'],
                operator_name=operator['name'],
                #buffer_delay=operator['pipeline_depth'] - 1,
                operator_width=operator['bitSize'] + 2 - 1, # +2 because 2 extra bits in FloPoCo
                additional_signals=additional_signals,
                bit_flip_instance=bit_flip_instance,
                #entity_connection=entity_connection,
                buffer=buffer,
                main_component=main_component,
                intermediate_input=intermediate_input,
                intermediate_output=intermediate_output,
                ieee2nfloat_0 = ieee2nfloat_0,
                ieee2nfloat_1 = ieee2nfloat_1,
                nfloat2ieee = nfloat2ieee
            )

            # Write the formatted VHDL to the combined file
            combined_file.write(wrapper_vhdl)
            combined_file.write('\n\n')  # Add newlines for separation
