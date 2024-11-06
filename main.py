import re
import argparse
import sys


COMMENT_START = r"=begin"
COMMENT_END = r"=cut"
DICT_BEGIN = r"begin"
DICT_END = r"end"
SET_CONST = r"set\s+([_a-zA-Z]+)\s+=\s+(.+)"
EXPR_CONST = r"\$\(([^)]+)\)"
STR_PATTERN = r"\[\[([^\]]+)\]\]"
KEY_VALUE = r"([_a-zA-Z]+)\s*:=\s*(.+);"

def parse_file(filepath):
    config = {}
    try:
        with open(filepath, 'r') as file:
            content = file.read()
            content = re.sub(f"{COMMENT_START}.*?{COMMENT_END}", "", content, flags=re.DOTALL)
            for line in content.splitlines():
                print("Processing line:", line)  
                
                if match := re.match(SET_CONST, line):
                    name, value = match.groups()
                    config[name] = int(value) if value.isdigit() else value  
                    print("Set value:", name, "=", config[name])
                
                elif line.startswith("$("):
                    result = evaluate_expression(line, config)  
                    print("Expression result:", line, "=", result)
                    config["city_code_next"] = result  

    except FileNotFoundError:
        print("File not found:", filepath)
    
    return config



def evaluate_expression(expr, config):
    # Убираем символы `$(` и `)` для получения токенов
    tokens = expr.strip("$()").split()
    operation = tokens[0]

    if operation == '+':
        return config.get(tokens[1], 0) + int(tokens[2])
    elif operation == '-':
        return config.get(tokens[1], 0) - int(tokens[2])
    elif operation == '*':
        return config.get(tokens[1], 0) * int(tokens[2])
    elif operation == 'max':

        values = [config.get(token, int(token)) for token in tokens[1:]]
        return max(values)

    return None 

    
def to_toml(config):
    toml_str = ""
    for key, value in config.items():
        toml_str += f"{key} = {value}\n"
    return toml_str

def main():
    parser = argparse.ArgumentParser(description="Config to TOML Converter")
    parser.add_argument("file", help="Path to the input configuration file")
    args = parser.parse_args()
    
    config = parse_file(args.file)
    toml_output = to_toml(config)
    print(toml_output)

if __name__ == "__main__":
    main()
