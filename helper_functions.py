import re

from constants import keywords, operators, punctuators
from Token import Token
from SemanticAnalyzer import DataType, FunctionData, MainType, Stack


def is_keyword(string):
    for class_part, values in keywords.items():
        for kw in values:
            if string == kw:
                return class_part
    return False


def is_operator(string):
    for class_part, values in operators.items():
        for kw in values:
            if string == kw:
                return class_part
    return False


def is_punctuator(string):
    for punctuator in punctuators:
        if string == punctuator:
            return punctuator
    return False


def is_identifier(input):
    pattern = re.compile(r'^[A-Za-z_]*[A-Za-z0-9_]+$')
    return bool(pattern.fullmatch(input))


def is_string(input):
    pattern = re.compile(
        r'^\"((\\[\\\'\"\w])*|[A-Za-z0-9 \+\-\*/=@#\$%\^&_()\[\]\{\}:;,.?<>]*)*\"$'
    )
    return bool(pattern.fullmatch(input))


def is_number(input):
    pattern = re.compile(r'(\+|\-)?(\d+|(\d*\.\d+))')
    return bool(pattern.fullmatch(input))


def is_data_type(input):
    return input in keywords.get('data_type')


def numbers_only(input):
    pattern = re.compile(r'(\+|\-)?(\d)*')
    return bool(pattern.fullmatch(input))


def determine_class_part(value):
    class_part = is_operator(value)
    if (class_part):
        return class_part

    class_part = is_punctuator(value)
    if (class_part):
        return value

    class_part = is_number(value)
    if (class_part):
        return 'number'

    class_part = is_string(value)
    if (class_part):
        return 'string'

    class_part = is_identifier(value)
    if (class_part):
        class_part = is_keyword(value)
        if (class_part):
            return class_part
        return 'identifier'

    class_part = is_keyword(value)
    if (class_part):
        return class_part

    if (value == ";"):
        return "EOL"

    if (value == '$'):
        return "end_marker"

    return 'invalid lexeme'


def generate_token(value, line_number):
    class_part = determine_class_part(value)
    return Token(class_part, value, line_number)


def check_end_of_string(string):
    string = string[1:]  # removing first quotation mark
    str_len = len(string)
    iterator = 0
    while iterator < str_len:
        if (string[0] == "\\"):  # if char is backslash remove it and next char as it will have special meaning and can not end string
            string = string[2:]
            iterator += 2
        if (len(string) == 1 and string == "\""):
            return True
        else:
            string = string[1:]
            iterator += 1
    return False

# Semantic Analyzer


def insert_mt(name: str, type: str, type_modifier: str, ext: str, imp: str, main_table: list[MainType]):
    if (not lookup_mt(name, main_table)):
        main_table_row = MainType(name, type, type_modifier, ext, imp)
        main_table.append(main_table_row)
        return main_table_row
    print('Redeclaration Error')


def insert_dt(name: str, type: str, access_modifier: str, static: bool, final: bool, abstract: bool, current_class: MainType):
    if (not lookup_dt(name, current_class) or not lookup_dt_pl(name, type, current_class)):
        current_class.add_data_table_row(
            DataType(name, type, access_modifier, static, final, abstract))

    print('Redeclaration Error')


def insert_ft(name: str, type: str, scope: int, scope_stack: Stack, function_table: list[FunctionData]):
    if (not lookup_ft(name, scope_stack, function_table)):
        function_table.append(FunctionData(name, type, scope))

    print('Redeclaration Error')


def lookup_mt(name: str, main_table: list[MainType]) -> MainType | None:
    for i in range(len(main_table)):
        return main_table[i] if (main_table[i].name == name) else None


def lookup_ft(name: str, scope_stack, function_table: list[FunctionData]) -> str | None:
    for function_data_row in function_table:
        if (function_data_row.scope in scope_stack.stack and function_data_row.name == name):
            return function_data_row.type
    return None


def lookup_dt(name: str, current_class: MainType):
    for data_row in current_class.data_table:
        return data_row if (data_row.name == name) else None


def lookup_dt_pl(name: str, parameter_list: str, current_class: MainType):
    for data_row in current_class.data_table:
        if (data_row.name == name and data_row.type == parameter_list):
            return data_row
    return None
