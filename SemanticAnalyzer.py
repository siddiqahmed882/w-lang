class DataType:
    def __init__(self, name: str, type: str, access_modifier: str, static: bool, final: bool, abstract: bool):
        self.name = name
        self.type = type
        self.access_modifier = access_modifier
        self.static = static
        self.final = final
        self.abstract = abstract


class MainType:
    def __init__(self, name: str, type: str, type_modifier: str, ext: str, imp: str):
        self.name = name
        self.type = type
        self.type_modifier = type_modifier
        self.ext = ext
        self.imp = imp
        self.data_table: list[DataType] = []

    def add_data_table_row(self, data_table_row: DataType):
        self.data_table.append(data_table_row)


class FunctionData:
    def __init__(self, name: str, type: str, scope: int):
        self.name = name
        self.type = type
        self.scope = scope


class Counter:
    count: int = 0

    @staticmethod
    def get_next_count():
        Counter.count += 1
        return Counter.count


class Stack:
    stack: list[int]

    def __init__(self):
        self.stack = []

    def push(self):
        next_scope = Counter.get_next_count()
        self.stack.append(next_scope)
        return self.stack

    def pop(self):
        self.stack.pop()

    def peek(self):
        return self.stack[len(self.stack) - 1]
