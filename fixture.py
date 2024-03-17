#!/usr/bin/env python

import sys
import re

input = sys.argv[1]

def read_swift_code_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def generate_fixture_extension(swift_code):
    # Regex to match struct definitions and capture their contents
    struct_pattern = re.compile(r'struct (\w+)\s*.*?{([^}]*)}', re.DOTALL)
    property_pattern = re.compile(r'let ([\w\[\]]+): ([\w\[\]]+)')
    
    # Find all struct definitions in the given Swift code
    structs = struct_pattern.findall(swift_code)
    
    fixture_extensions = []
    
    for struct_name, struct_body in structs:
        # Find all properties in the current struct
        properties = property_pattern.findall(struct_body)
        
        # Start building the fixture extension
        extension_code = f'extension {struct_name} {{\n'
        extension_code += f'\tstatic func fixture('
        
        # Generate parameters for the fixture function
        extension_code += ','.join(generate_fixture_extension_properties_code(properties))
        
        # Complete the fixture function
        extension_code += f'\n\t) -> {struct_name} {{\n'
        extension_code += f'\t\treturn {struct_name}(\n'
        
        for prop_name, _ in properties:
            extension_code += f'\t\t\t{prop_name}: {prop_name},\n'
        
        # Close the fixture function and extension
        extension_code = extension_code.rstrip(',\n') + '\n'
        extension_code += '\t\t)\n\t}\n}\n'
        
        fixture_extensions.append(extension_code)
    
    # Join all extensions for the output
    return '\n'.join(fixture_extensions)

def generate_fixture_extension_properties_code(properties):
    params = []
    for prop_name, prop_type in properties:
        # Check if the type is a custom struct or a Foundation type
        default_value = ".fixture()"
        if prop_type == "String":
            default_value = "\"fixture\""
        elif prop_type == "Int":
            default_value = "0"
        elif prop_type == "Float":
            default_value = "0.0"
        elif prop_type == "Data":
            default_value = "Data()"
        elif "[" in prop_type:
            default_value = "[]"
            

        params.append(f'\n\t\t{prop_name}: {prop_type} = {default_value}')

    return params

# Generate the fixture extension
swift_code_from_file = read_swift_code_from_file(input)
fixture_extension = generate_fixture_extension(swift_code_from_file)

f = open(input, "a")
f.write("\n")
f.write(fixture_extension)
f.close()
