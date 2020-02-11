#!/usr/bin/env python3

from ply import yacc
import parser


if __name__ == '__main__':
    code = input('> ')
    try:
        ast = yacc.parse(code)
    except SyntaxError as syntaxE:
        print('SyntaxError: {}'.format(syntaxE))
        exit()

    try:
        ast.a_interp({})
    except Exception as e:
        print('Error: {}'.format(e))
        exit()

    try:
        ast.interp({})
    except Exception as e:
        print('Error: {}'.format(e))
        exit()
