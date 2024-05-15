def generate_assembly_code(atoms):
    assembly_code = []

    # Assuming variables, constants, and labels
    condition_variable = atoms[1] 
    condition_operator = atoms[2] 
    condition_value = atoms[3]  
    expression_variable = atoms[4]  
    assign_variable = atoms[5]       
    assign_variable2 = atoms[7]       
    constant_value6 = atoms[6]
    constant_value8 = atoms[8]  
    state_else = atoms[9]  
    print_value = atoms[-2]
    

    
    if condition_variable.isdigit() and condition_value.isdigit():
        assembly_code.append(f"LOD R1, {condition_variable}")
        assembly_code.append(f"LOD R2, {condition_value}")
        assembly_code.append(f"CMP R1, R2")       
    if condition_variable.isidentifier() and condition_value.isdigit():
        assembly_code.append(f"LOD R1, {condition_variable}")
        assembly_code.append(f"LOD R2, {condition_value}")
        assembly_code.append(f"CMP R1, R2") 
    if condition_variable.isidentifier() and condition_value.isidentifier():
        assembly_code.append(f"LOD R1, {condition_variable}")
        assembly_code.append(f"LOD R2, {condition_value}")
        assembly_code.append(f"CMP R1, R2")        
        
    if condition_operator=='>':
        assembly_code.append(f"BH L1")
    if condition_operator=='<':
        assembly_code.append(f"BL L1")
    if condition_operator=='==':
        assembly_code.append(f"BE L1")    
    assembly_code.append(f"B  L2")        

    
    if assign_variable=='=':
        if expression_variable.isidentifier():
            if ((constant_value6.isdigit() or constant_value6.isidentifier() ) and (constant_value8.isidentifier() or constant_value8.isdigit())) and assign_variable2=="+":
                assembly_code.append(f"L1: LOD R3, {constant_value6}")
                # assembly_code.append(f"    LOD R4, {constant_value8}")
                assembly_code.append(f"    ADD R3,{constant_value8}")
                assembly_code.append(f"    STO {expression_variable}, R3")
            if ((constant_value6.isdigit() or constant_value6.isidentifier() ) and (constant_value8.isidentifier() or constant_value8.isdigit())) and assign_variable2=="-":
                assembly_code.append(f"L1: LOD R3, {constant_value6}")
                # assembly_code.append(f"    LOD R4, {constant_value8}")
                assembly_code.append(f"    SUB R3,{constant_value8}")
                assembly_code.append(f"    STO {expression_variable}, R3")
            if ((constant_value6.isdigit() or constant_value6.isidentifier() ) and (constant_value8.isidentifier() or constant_value8.isdigit())) and assign_variable2=="*":
                assembly_code.append(f"L1: LOD R3, {constant_value6}")
                # assembly_code.append(f"    LOD R4, {constant_value8}")
                assembly_code.append(f"    MUL R3,{constant_value8}")
                assembly_code.append(f"    STO {expression_variable}, R3")
            if ((constant_value6.isdigit() or constant_value6.isidentifier() ) and (constant_value8.isidentifier() or constant_value8.isdigit())) and assign_variable2=="/":
                assembly_code.append(f"L1: LOD R3, {constant_value6}")
                # assembly_code.append(f"    LOD R4, {constant_value8}")
                assembly_code.append(f"    DIV R3,{constant_value8}")
                assembly_code.append(f"    STO {expression_variable}, R3")
            
    if state_else=='else':
        if print_value.isidentifier() or print_value.isdigit(): 
            assembly_code.append(f"L2: LOD R4, {print_value}")
            assembly_code.append(f"    call write,R4")           
              
                
                

    return assembly_code

# Example input list of atoms
atoms_list = ['if', 'x', '>', '0', 'y', '=', '15', '*', '10', 'else', 'print', '(', '10', ')']

# Generate assembly code based on the provided list of atoms
assembly_code = generate_assembly_code(atoms_list)
for instruction in assembly_code:
    print(instruction)
