class SA:
    token_set = []
    current_index = 0
    end_index = 0

    @staticmethod
    def main(token_set):
        SA.end_index = len(token_set) - 1
        SA.token_set = token_set
        if (SA.validate()):
            return "Syntax Valid"
        return f'Invalid Syntax @ line # {token_set[SA.current_index].line_number}'

    @staticmethod
    def validate():
        if (SA.S() and SA.token_list[SA.current_index].cp == "$"):
            return True
        return False

    @staticmethod
    def S():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {DT, ID, while, for, if, return, break, continue, pass}
        if (cp in ['data_type', 'idenitifier', 'while', 'for', 'if', 'return', 'break', 'continue', 'pass']):
            if (SA.SST() and SA.S()):
                return True

        # ? selection set => {final, static, abstract,  class, func, interface}
        elif (cp in ['final', 'static', 'abstract', 'class', 'func', 'interface']):
            if (SA.defs() and SA.S()):
                return True

        # ? selection set => {end_marker}
        elif (cp == 'end_marker'):
            return True

        return False

    @staticmethod
    def defs():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {final, static, abstract,  class}
        if (cp in ['final', 'static', 'abstract', 'class', 'func']):
            if (SA.class_def() and SA.def1()):
                return True

        # ? selction_set => {func}
        elif (cp == 'func'):
            if (SA.func_def() and SA.def1()):
                return True

        # ? selection_set => {inteface}
        elif (cp == 'interface'):
            if (SA.interface_def() and SA.def1()):
                return True

        return False

    @staticmethod
    def def1():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {final, static, abstract,  class, func, interface}
        if (SA.defs()):
            return True

        # ? {DT, ID, while, for, if, return, break, continue, pass, final, static, abstract,  class, func, $}
        elif (cp in ['data_type', 'idenitifier', 'while', 'for', 'if', 'return', 'break', 'continue', 'pass', 'final', 'static', 'abstract', 'class', 'func', 'end_marker']):
            return True

        return False

    @staticmethod
    def decl():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {DT}
        if (cp == 'data_type'):
            SA.current_index += 1
            if (SA.A()):
                if (cp == 'identifier'):
                    SA.current_index += 1
                    if (SA.list()):
                        return True

        return False

    @staticmethod
    def A():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => { [][]  }
        if (cp == 'arr_decl--1D'):
            SA.current_index += 1
            return True

        # ? selection_set => { [][]  }
        elif (cp == 'arr_decl--2D'):
            SA.current_index += 1
            return True

        # ? selection_set => {ID}
        elif (cp == 'idenitifier'):
            return True

        return False

    @staticmethod
    def list():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {  , }
        if (cp == ','):
            SA.current_index += 1
            if (SA.decl()):
                return True

        # ? selection_set => { ; }
        elif (cp == ';'):
            SA.current_index += 1
            return True

        # ? selection_set => {=}
        elif (cp == 'assignment'):
            if (SA.init()):
                return True

        return False

    @staticmethod
    def init():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {=}
        if (cp == 'assignment'):
            SA.current_index += 1
            if (SA.token_set[SA.current_index].cp == 'new'):
                SA.current_index += 1
                if (SA.token_set[SA.current_index].cp == 'data_type'):
                    SA.current_index += 1
                    if (SA.token_set[SA.current_index] == '['):
                        SA.current_index += 1
                        if (SA.p()):
                            if (SA.token_set[SA.current_index] == ']'):
                                SA.current_index += 1
                                return True
        # ? selection_set => { ; }
        elif (cp == ';'):
            return True

        return False

    @staticmethod
    def func_call():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set =>  {ID}
        if (cp == 'identifier'):
            SA.current_index += 1
            if (SA.token_set[SA.current_index].cp == '('):
                SA.current_index += 1
                if (SA.p() and SA.end()):
                    return True

        return False

    @staticmethod
    def end():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => { ; }
        if (cp == ';'):
            SA.current_index += 1
            return True

        # ? selection_set => {DT, ID, while, for, if, return,  break, continue, pass}
        elif (cp in ['data_type', 'identifier', 'while', 'for', 'if', 'return', 'break', 'continue', 'pass']):
            return True

        return False

    @staticmethod
    def p():
        cp = SA.token_set[SA.current_index].cp

        # ? selection set => {this, super, ID, constant as number, ( , ! }
        if (cp in ['this', 'super', 'identifier', 'number', '(', 'not_operator']):
            if (SA.OE() and SA.p1()):
                return True

        # ? selection_set => { ) , ] }
        if (cp in [')', ']']):
            return True

        return False

    @staticmethod
    def p1():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => { , }
        if (cp == ','):
            SA.current_index += 1
            if (SA.OE() and SA.p1()):
                return True

        # ? selection_set => { ) }
        elif (cp == ')'):
            return True

        return False

    @staticmethod
    def func_def():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {func}
        if (cp == 'func'):
            SA.current_index += 1
            if (SA.fdt1()):
                if (SA.token_set[SA.current_index].cp == 'identifier'):
                    SA.current_index += 1
