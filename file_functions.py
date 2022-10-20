def read_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
        return content


def write_to_file(filepath, values):
    with open(filepath, 'w') as f:
        f.write('(class_part, value_part, line_number)\n')
        for value in values:
            f.write(f'{value}\n')
    return 'file write completed'
