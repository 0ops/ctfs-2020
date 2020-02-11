import ast
from lexer import tokens
from ply import yacc


precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES'),
    ('right', 'SEMICOL'),
)


def p_goal(p):
    """goal : comm"""
    p[0] = p[1]


def p_comm_1(p):
    """comm : COMMA"""
    p[0] = ast.Skip()


def p_comm_2(p):
    """comm : VAR ASSIGN expr"""
    p[0] = ast.Assign(ast.Var(p[1]), p[3])


def p_comm_3(p):
    """comm : comm SEMICOL comm"""
    p[0] = ast.Seq(p[1], p[3])


def p_comm_4(p):
    """comm : cond IFELSE LBRACE comm RBRACE COLON LBRACE comm RBRACE"""
    p[0] = ast.IfElse(p[1], p[4], p[8])


def p_comm_5(p):
    """comm : LBRACK cond LBRACE comm RBRACE RBRACK"""
    p[0] = ast.While(p[2], p[4])


def p_comm_6(p):
    """comm : PRINT expr"""
    p[0] = ast.Print(p[2])


comparison_dict = {
        '<': ast.Lt,
        '<=': ast.Le,
        '==': ast.Eq,
        '!=': ast.Ne,
        '>': ast.Gt,
        '>=': ast.Ge
}


def p_cond(p):
    """cond : VAR LT NUM
            | VAR LE NUM
            | VAR EQ NUM
            | VAR NE NUM
            | VAR GT NUM
            | VAR GE NUM"""
    p[0] = comparison_dict[p[2]](ast.Var(p[1]), ast.Num(p[3]))


def p_expr_1(p):
    """expr : LPAREN expr RPAREN"""
    p[0] = p[2]


def p_expr_2(p):
    """expr : NUM"""
    p[0] = ast.Num(p[1])


def p_expr_3(p):
    """expr : NUM RANDOM NUM"""
    p[0] = ast.Random(p[1], p[3])


def p_expr_4(p):
    """expr : VAR"""
    p[0] = ast.Var(p[1])


binaryop_dict = {
        '+': ast.Add,
        '-': ast.Sub,
        '*': ast.Mul,
}


def p_expr_5(p):
    """expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr"""
    p[0] = binaryop_dict[p[2]](p[1], p[3])


def p_error(p):
    if p is None:
        raise SyntaxError("invalid syntax")
    raise SyntaxError("invalid syntax at '{}'".format(p.value))


c_parser = yacc.yacc()
