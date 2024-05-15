# Function to create token objects
def create_token(token_type, value):
    return {'type': token_type, 'value': value}

# Function to tokenize the input code
def tokenize(input_string):
    current_position = 0
    tokens = []
    # tokens[-1]={'type': 'EMPTYSPACE', 'value': ''}

    while current_position < len(input_string):
        char = input_string[current_position]

        # Numeric literal DFA
        if char.isdigit():
            token_value = char
            current_position += 1
            while current_position < len(input_string) and \
                    (input_string[current_position].isdigit() or
                     input_string[current_position] == '.'):
                token_value += input_string[current_position]
                current_position += 1
            tokens.append(create_token("NUMERIC_CONSTANT", token_value))

        # Character constant DFA (simplified for demonstration)
        elif char == "'":
            token_value = char
            current_position += 1
            while current_position < len(input_string) and \
                    input_string[current_position] != "'":
                token_value += input_string[current_position]
                current_position += 1
            token_value += "'"
            tokens.append(create_token("CHARACTER_CONSTANT", token_value))
            current_position += 1  # Move past the closing single quote

        # Identifier DFA
        elif char.isalpha():
            token_value = char
            current_position += 1
            while current_position < len(input_string) and \
                    (input_string[current_position].isalnum()):
                token_value += input_string[current_position]
                current_position += 1

            # Check if it's a keyword
            if token_value in ["if", "else", "while", "for", "int", "float", "print"]:
                tokens.append(create_token("KEYWORD", token_value))
            else:
                tokens.append(create_token("IDENTIFIER", token_value))

        # Operators
        elif char in "=+-*/><":
            if char == '=' and current_position + 1 < len(input_string) and input_string[current_position + 1] == '=':
                tokens.append(create_token("OPERATOR", "=="))
                current_position += 2  # Move past both '=' characters for '=='
            else:
                tokens.append(create_token("OPERATOR", char))
                current_position += 1
     
        # special characters       
        elif char in "(){}[].:;,":
            tokens.append(create_token("SPECIAL CHARACTER", char))
            current_position += 1

        elif char == '#':
            tokens.append(create_token("SPECIAL CHARACTER", char))
            comment_value = ""
            current_position += 1
            # Capture the content after '#' till the end of the line as a comment
            while current_position < len(input_string) and input_string[current_position] != '\n':
                comment_value += input_string[current_position]
                current_position += 1
            tokens.append(create_token("COMMENT", comment_value))


        elif char.isspace():
            if char == '\n':
                tokens.append(create_token("NEWLINE", "\\n"))
            current_position += 1

        else:
            # Handle other characters or raise an error
            print(f"Error: Unrecognized character '{char}'")
            current_position += 1
    # tokens.extend([{'type': 'EMPTYSPACE', 'value': ''}])    
    return tokens

# Example usage
input_code =open(r"G:\Python\Learn\Scanner\parser.txt").read()
tokens = tokenize(input_code)#tokens = list [{"key1":"type","key2":"value"},.....]
input_tokens = []
for token in tokens:
    print(f"Token: Type={token['type']}, Value='{token['value']}'")
    # print(token)
    input_tokens.append(token)

print("-------------------------------------------------------------------")
input_tokens.extend([{'type': 'EMPTYSPACE', 'value': ''}])  
# input_tokens = [print(token)] 
# print(input_tokens)  
    


#--------------------------------------------

# Function to check syntax based on the token list
def check_syntax(tokens):
    current_token = 0
    line_number = 1  # Initialize line number counter

    def match(expected_type, expected_value=None):
        nonlocal current_token
        nonlocal line_number
        if current_token < len(tokens):
            if tokens[current_token]['value'] == '\\n':
                line_number += 1
            if tokens[current_token]['type'] == expected_type:
                if expected_value is None or tokens[current_token]['value'] == expected_value:
                    current_token += 1
                    return True
        return False

    def syntax_error(expected):
        nonlocal line_number
        if tokens[current_token]['value'] == '\\n':
            line_number -= 1
        if (expected == 'end of statement' and tokens[current_token]['type']=='EMPTYSPACE') or (expected == 'end of statement' and tokens[current_token]['type']=='NEWLINE'):
            pass
        else:
            print(f"Syntax Error at line {line_number}:Expected: {expected}, Found: {tokens[current_token]['type']}- '{tokens[current_token]['value']}'")

    # Grammar for the if-else statement
    def statement():
        if not match('KEYWORD', 'if'):
            syntax_error("'if'")
            return False
        if not match('IDENTIFIER'):
            if not match('NUMERIC_CONSTANT'):
                syntax_error("an identifier or NUMERIC_CONSTANT")
                return False
        if not match('OPERATOR','>'):
            if not match('OPERATOR','=='):
                if not match('OPERATOR','<'):
                    syntax_error("'=='or '>' or '<'")
                    return False
        if not match('NUMERIC_CONSTANT'):
            if not match('IDENTIFIER'):
                syntax_error("a numeric constant or identifier")
                return False
        if not match('SPECIAL CHARACTER', ':'):
            syntax_error("':'")
            return False
        if not match('NEWLINE'):#line =2
            syntax_error("a new line")
            return False
        if not match('IDENTIFIER'):
            syntax_error("an identifier")
            return False
        if not match('OPERATOR', '='):
            syntax_error("'='")
            return False
        if not match('NUMERIC_CONSTANT'):
            syntax_error("a numeric constant")
            return False
        if not match('OPERATOR', '+'):
            syntax_error("'+'")
            return False
        if not match('IDENTIFIER'):
            if not match('NUMERIC_CONSTANT'):
                syntax_error("an identifier or NUMERIC_CONSTANT")
                return False
        if not match('NEWLINE'):#line =3
            syntax_error("a new line")
            return False
        if  match('KEYWORD','else'):
            if not match('SPECIAL CHARACTER', ':'):
                syntax_error("':'")
                return False
            if not match('NEWLINE'):#line =4
                syntax_error("a new line")
                return False
        if not match('KEYWORD', 'print'):
            syntax_error("'print'")
            return False
        if not match('SPECIAL CHARACTER', '('):
            syntax_error("'('")
            return False
        if not match('IDENTIFIER') :
            if not match('NUMERIC_CONSTANT'):
                syntax_error("an identifier or NUMERIC_CONSTANT")
                return False
        if not match('SPECIAL CHARACTER', ')'):
            syntax_error("')'")
            return False
        if match('EMPTYSPACE'):
            return True
        return True
    
# Start checking syntax
    if not statement():
        return False
    elif current_token == len(tokens):
        print("No Syntax Error Found")
    else:
        while current_token < len(tokens):
            syntax_error("end of statement")
            current_token += 1


check_syntax(input_tokens)