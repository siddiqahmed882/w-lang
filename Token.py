class Token:
    def __init__(self, class_part, value_part, line_number):
        self.cp = class_part
        self.vp = value_part if (class_part != value_part) else "_"
        self.line_number = line_number

    def __str__(self):
        return f"(class: {self.cp}, value: {self.vp}, line: {self.line_number})"
