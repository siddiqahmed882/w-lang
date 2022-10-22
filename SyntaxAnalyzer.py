from locale import currency


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
        if (SA.S() and SA.token_set[SA.current_index].cp == "$"):
            return True
        return False

    @staticmethod
    def S():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {DT, ID, while, for, if, return, break, continue, pass}
        if (cp in ['data_type', 'idenitifier', 'while', 'for', 'if', 'return', 'jump_statements']):
            if (SA.sst() and SA.S()):
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
        elif (cp in ['data_type', 'idenitifier', 'while', 'for', 'if', 'return', 'jump_statements', 'final', 'static', 'abstract', 'class', 'func', 'end_marker']):
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
        elif (cp in ['data_type', 'identifier', 'while', 'for', 'if', 'return', 'jump_statements']):
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
        elif (cp in [')', ']']):
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

        # ? selection_set => { ), ] }
        elif (cp == ')' or cp == ']'):
            return True

        return False

    @staticmethod
    def func_def():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {func}
        if (cp == 'func'):
            SA.current_index += 1
            if (SA.FDT1()):
                if (SA.token_set[SA.current_index].cp == 'identifier'):
                    SA.current_index += 1
                    if (SA.token_set[SA.current_index].cp == '('):
                        SA.current_index += 1
                        if (SA.para()):
                            if (SA.token_set[SA.current_index].cp == ')'):
                                SA.current_index += 1
                                if (SA.token_set[SA.current_index].cp == "{"):
                                    SA.current_index += 1
                                    if (SA.mst()):
                                        if (SA.token_set[SA.current_index].cp == '}'):
                                            SA.current_index += 1
                                            return True

        return False

    @staticmethod
    def FDT():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {DT}
        if (cp == 'data_type'):
            SA.current_index += 1
            if (SA.A()):
                return True
        # ? selection_set => {ID}
        elif (cp == 'identifier'):
            SA.current_index += 1
            if (SA.A()):
                return True

        return False

    @staticmethod
    def FDT1():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {DT, ID}
        if (cp in ['data_type', 'identifier']):
            if (SA.FDT()):
                return True
        # ? selection_set => { void }
        elif (cp == 'void'):
            SA.current_index += 1
            return True

        return False

    @staticmethod
    def para():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {DT, ID}
        if (cp in ['data_type', 'identifier']):
            if (SA.FDT()):
                if (SA.token_set[SA.current_index].cp == 'identifier'):
                    SA.current_index += 1
                    if (SA.s_para()):
                        return True
        # ? selection_set => { ) }
        elif (cp == ')'):
            return True

        return False

    @staticmethod
    def s_para():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {  ,  }
        if (cp == ','):
            SA.current_index += 1
            if (SA.FDT()):
                if (SA.token_set[SA.current_index].cp == 'identifier'):
                    SA.current_index += 1
                    if (SA.s_para):
                        return True
        # ? selection_set => { ) }
        elif (cp == ')'):
            return True

        return False

    @staticmethod
    def while_st():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {while}
        if (cp == 'while'):
            SA.current_index += 1
            if (SA.token_set[SA.current_index].cp == '('):
                SA.current_index += 1
                if (SA.OE()):
                    if (SA.token_set[SA.current_index].cp == ')'):
                        SA.current_index += 1
                        if (SA.token_set[SA.current_index].cp == '{'):
                            SA.current_index += 1
                            if (SA.mst()):
                                if (SA.token_set[SA.current_index].cp == '}'):
                                    return True

        return False

    @staticmethod
    def for_st():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {for}
        if (cp == 'for'):
            SA.current_index += 1
            if (SA.token_set[SA.current_index].cp == '('):
                SA.current_index += 1
                if (SA.assign_st()):
                    if (SA.OE()):
                        if (SA.token_set[SA.current_index].cp == ';'):
                            SA.current_index += 1
                            if (SA.inc_dec_st()):
                                if (SA.token_set[SA.current_index].cp == ')'):
                                    SA.current_index += 1
                                    if (SA.token_set[SA.current_index].cp == '{'):
                                        SA.current_index += 1
                                        if (SA.mst()):
                                            if (SA.token_set[SA.current_index].cp == '}'):
                                                SA.current_index += 1
                                                return True

        return False

    @staticmethod
    def inc_dec_st():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {ID}
        if (cp == 'identifier'):
            SA.current_index += 1
            if (SA.inc_dec_st1()):
                if (SA.inc_dec_opr()):
                    if (SA.token_set[SA.current_index].cp == ';'):
                        SA.current_index += 1
                        return True
        # ? selection_set => { ++ , -- }
        elif (cp == 'inc_dec'):
            if (SA.inc_dec_opr()):
                if (SA.token_set[SA.current_index].cp == 'identifier'):
                    SA.current_index += 1
                    if (SA.inc_dec_st1()):
                        if (SA.token_set[SA.current_index].cp == ';'):
                            SA.current_index += 1
                            return True
        return False

    @staticmethod
    def inc_dec_st1():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => { . }
        if (cp == '.'):
            SA.current_index += 1
            if (SA.token_set[SA.current_index] == 'identifier'):
                SA.current_index += 1
                if (SA.inc_dec_st1()):
                    return True
        # ? selection_set => { ( }
        elif (cp == '('):
            SA.current_index += 1
            if (SA.p()):
                if (SA.token_set[SA.current_index].cp == ')'):
                    SA.current_index += 1
                    if (SA.token_set[SA.current_index].cp == '.'):
                        SA.current_index += 1
                        if (SA.token_set[SA.current_index] == 'identifier'):
                            SA.current_index += 1
                            if (SA.inc_dec_st1()):
                                return True
        # ? selection_set => { [ }
        elif (cp == '['):
            SA.current_index += 1
            if (SA.OE()):
                if (SA.token_set[SA.current_index].cp == ']'):
                    SA.current_index += 1
                    if (SA.inc_dec_st2()):
                        return True
        # ? selection_set => {++, --, DT, ID, while, for, if, return, break, continue, pass,  ; }
        elif (cp in ['inc_dec', 'data_type', 'identifier', 'while', 'for', 'if', 'return', 'jump_statements', ';']):
            return True

        return False

    @staticmethod
    def inc_dec_st2():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {  .  }
        if (cp == '.'):
            SA.current_index += 1
            if (SA.token_set[SA.current_index].cp == 'identifier'):
                SA.current_index += 1
                if (SA.inc_dec_st1()):
                    return True
        # ? selection_set => { ++, --, DT, ID, while, for, if, return, break, continue, pass, ; }
        elif (cp in ['inc_dec', 'data_type', 'identifier', 'while', 'for', 'if', 'return', 'jump_statements', ';']):
            return True

        return False

    @staticmethod
    def p():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {this, super, ID, constant, (, ! }
        if (cp in ['this', 'super', 'identifier', 'num', '(', 'not_operator']):
            if (SA.OE()):
                if (SA.p1()):
                    return True
        # ? selection_set => { ) , ] }
        if (cp in [')', ']']):
            return True

        return False

    @staticmethod
    def inc_dec_opr():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {++, --}
        if (cp == 'inc_dec'):
            SA.current_index += 1
            return True

        return False

    @staticmethod
    def sst():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {DT, ID, while, for, if, return, break, continue, pass}
        # TODO: error handle is not included
        if (SA.decl() or SA.while_st() or SA.for_st() or SA.if_st() or SA.func_call() or SA.AFCI() or cp in ['return', 'jump_statements']):
            return True

        return False

    @staticmethod
    def AFCI():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {ID}
        if (cp == 'identifier'):
            SA.current_index += 1
            if (SA.AFCI1()):
                return True

        return False

    @staticmethod
    def AFCI1():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => { . , ( , [ }
        if (cp in ['.', '(', '[']):
            if (SA.inc_dec_st1()):
                if (SA.inc_dec_opr()):
                    return True
        # ? selection_set => { ++ , --}
        elif (cp == 'inc_dec'):
            if (SA.inc_dec_opr()):
                if (SA.token_set[SA.current_index].cp == 'identifier'):
                    SA.current_index += 1
                    if (SA.inc_dec_st1()):
                        return True
        # ? selection_set => { ( }
        elif (cp == '('):
            SA.current_index += 1
            if (SA.p()):
                if (SA.token_set[SA.current_index].cp == ')'):
                    SA.current_index += 1
                    if (SA.end()):
                        return True
        # ? selection_set =>  { . , ( , [ , = , CO as compound_assignment }
        elif (cp in ['.', '(', '[', 'assignment', 'compound_assignment']):
            if (SA.assign_st()):
                if (SA.assign_op()):
                    if (SA.OE()):
                        return True
        # ? selection_set => { ID }
        elif (cp == 'identifier'):
            SA.current_index += 1
            if (SA.token_set[SA.current_index].cp == 'assignment'):
                SA.current_index += 1
                if (SA.token_set[SA.current_index].cp == 'new'):
                    SA.current_index += 1
                    if (SA.token_set[SA.current_index].cp == 'identifier'):
                        SA.current_index += 1
                        if (SA.token_set[SA.current_index].cp == '('):
                            SA.current_index += 1
                            if (SA.token_set[SA.current_index].cp == ')'):
                                SA.current_index += 1
                                if (SA.token_set[SA.current_index].cp == ';'):
                                    SA.current_index += 1
                                    return True

        return False

    @staticmethod
    def mst():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {DT, ID, while, for, if, return, break, continue, pass}
        if (cp in ['data_type', 'identifier', 'while', 'for', 'if', 'return', 'jump_statements']):
            if (SA.sst()):
                if (SA.mst()):
                    return True
        # ? selection_set => {  } , public, sealed, static, func, construct, DT, ID, while, for, if, return, break, continue, pass}
        elif (cp in ['}', 'access_modifier', 'static', 'func', 'constructor', 'data_type', 'identifier', 'for', 'if', 'return', 'jump_statements']):
            return True

        return False

    @staticmethod
    def interface_def():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {interface}
        if (cp == 'interface'):
            SA.current_index += 1
            if (SA.token_set[SA.current_index].cp == 'identifier'):
                SA.current_index += 1
                if (SA.impl()):
                    if (SA.token_set[SA.current_index].cp == '{'):
                        SA.current_index += 1
                        if (SA.interface_body()):
                            if (SA.token_set[SA.current_index].cp == '}'):
                                SA.current_index += 1
                                return True

        return False

    @staticmethod
    def impl():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {implements}
        if (cp == 'implements'):
            SA.current_index += 1
            if (SA.token_set[SA.current_index].cp == 'identifier'):
                SA.current_index += 1
                if (SA.nt()):
                    return True

        return False

    @staticmethod
    def interface_body():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {DT, ID, void}
        if (cp in ['data_type', 'identifier', 'void']):
            if (SA.FDT1()):
                if (SA.token_set[SA.current_index].cp == 'identifier'):
                    SA.current_index += 1
                    if (SA.token_set[SA.current_index].cp == '('):
                        SA.current_index += 1
                        if (SA.para()):
                            if (SA.token_set[SA.current_index].cp == ')'):
                                SA.current_index += 1
                                return True
        # ? selection_set => {DT}
        if (cp == 'data_type'):
            if (SA.decl()):
                return True

        return False

    @staticmethod
    def nt():
        cp = SA.token_set[SA.current_index].cp

        # ? selection_set => {  , }
        if (cp == ','):
            SA.current_index += 1
            if (SA.token_set[SA.current_index].cp == 'identifier'):
                SA.current_index += 1
                if (SA.nt()):
                    return True
        # ? selection_set => { { }
        elif (cp == '{'):
            return True

        return False

# ! Continue from if-else-elif on page 6
    @staticmethod
    def if_st():
        Cp = SA.token_set[SA.current_index].cp

        # ? Selection Set => { if }
        if (Cp == 'if'):
            SA.current_index += 1
            if (SA.token_set[SA.current_index].cp == '('):
                SA.current_index += 1
                if (SA.OE()):
                    if (SA.token_set[SA.current_index].cp == ')'):
                        SA.current_index += 1
                        if (SA.token_set[SA.current_index].cp == '{'):
                            SA.current_index += 1
                            if (SA.mst()):
                                if (SA.token_set[SA.current_index].cp == '}'):
                                    SA.current_index += 1
                                    if (SA.elif_st()):
                                        if (SA.else_st()):
                                            return True
        return False

    @staticmethod
    def elif_st():
        Cp = SA.token_set[SA.current_index].cp

        # ? Selection Set => {elif}
        if (Cp == 'elif'):
            SA.current_index += 1
            if (SA.token_set[SA.current_index].cp == '('):
                SA.current_index += 1
                if (SA.OE()):
                    if (SA.token_set[SA.current_index].cp == ')'):
                        SA.current_index += 1
                        if (SA.token_set[SA.current_index].cp == '{'):
                            SA.current_index += 1
                            if (SA.mst()):
                                if (SA.token_set[SA.current_index].cp == '}'):
                                    SA.current_index += 1
                                    if (SA.elif_st()):
                                        return True
        # ? Selection Set {else, DT, ID, while, for, if, return, break, continue, pass}
            elif (Cp in ['else', 'data_type', 'identifier', 'while', 'for', 'if', 'return', 'break', 'continue', 'pass']):
                return True
            return False

    @staticmethod
    def else_st():
        Cp = SA.token_set[SA.current_index].cp

        # ? Selection Set => {else}
        if (Cp == 'else'):
            SA.current_index += 1
            if (SA.token_set[SA.current_index].cp == '{'):
                SA.current_index += 1
                if (SA.mst()):
                    if (SA.token_set[SA.current_index].cp == '}'):
                        SA.current_index += 1
                        return True
        # ? Selection Set (DT, ID, while, for, if, return, break, continue, pass)

        elif (Cp in ['data_type', 'identifier', 'while', 'for', 'if', 'return', 'break', 'continue', 'pass']):
            return True
        return False

    @staticmethod
    def Ass_st():
        Cp = SA.token_set[SA.current_index].cp

        # ? Selection Set {ID}
        if (Cp == 'identifier'):
            SA.current_index += 1
            if (SA.Ass_st1()):
                if (SA.Ass_op()):
                    if (SA.OE()):
                        if (SA.token_set[SA.current_index].cp == ' ; '):
                            SA.current_index += 1
                            return True
        return False

    @staticmethod
    def Ass_st2():
        Cp = SA.token_set[SA.current_index].cp

        # ? Selection Set { . , ( , [ , ] }
        if (Cp == '.'):
            SA.current_index += 1
            if (SA.token_set[SA.current_index].cp == '('):
                SA.current_index += 1
                if (SA.token_set[SA.current_index].cp == '['):
                    SA.current_index += 1
                    if (SA.token_set[SA.current_index].cp == ']'):

                        # TODO define assign_st(), assign_op(), class_def(), OE(),
