#!/usr/bin/python
import re

'''expand_checkbox_variables'''
def add_underscore(match):
    return match.expand("[\\1___\\3]")


def expand_checkbox(logic):
    pattern=re.compile(r'\[(?P<name>\w+)(\()(?P<cat>\d)(\))\]')
    return pattern.sub(add_underscore,logic)

'''add_data['variable']'''
# def add_parenthesis(match):
#     return match.expand("(data\\1)")

def substitute_and(logic):
    return logic.replace(' and ', ' & ')


def substitute_or(logic):
    return logic.replace(' or ', ' | ')

def replace_equals(match):
    return match.expand("\\1\\2\\2")

def substitute_equal_sign(logic):
    y = re.compile(r'([^\<\>\!])(?P<equals>\=)')
    return y.sub(replace_equals,logic)

# def substitute_quote(logic):
#     y = re.compile(r'\\\'')
#     return y.sub("'", logic)
def substitute_quote(logic):
    return logic.replace('\'', "'")

def substitute_not_equal_sign(logic):
    y = re.compile(r'\<\>')
    return y.sub("!=", logic)


def subs1(logic):
    pattern5 = re.compile(r'\[')
    iterator4 = pattern5.finditer(logic)
    for match4 in iterator4:
        n = match4.group()
    return logic.replace(n, "['")

def subs2(logic):
    pattern7 = re.compile(r'\]')
    iterator7 = pattern7.finditer(logic)
    for match7 in iterator7:
        m = match7.group()
    return logic.replace(m, "']")

def add_data(match):
    return match.expand("(data\\1)")

def expand_parenthesis(match):
    p=match.group()
    return match.expand("({})".format(p))

def add_parenthesis(logic):
    # pattern = re.compile(r"\[\w*\]\s?[!<>]*=*\s?\'?\-?\d*\'?\[*\w*\]*")
    pattern = re.compile(r"\(*\[\w*\]\)*\s?[!<>]*=*\s*\\?\'?\"?\-?\w*\\?\'?\"?\[*\w*\]*\)*")
    return pattern.sub(expand_parenthesis,logic)


def add_data_name(logic_,data_name="data"):
    pattern=re.compile(r"(?P<variable>\[\w+\])")
    replacement=r'{}\1'.format(data_name)
    return pattern.sub(replacement, logic_)

def substitute_equal_sign(logic):
    return logic.replace(']=', ']==').replace('] =', ']==').replace(') =',')==')



def convert_branching_logic(logic,data_name="data"):

    logic_ = expand_checkbox(logic)
    logic_ = add_parenthesis(logic_)
    logic_ = substitute_or(logic_)
    logic_ = substitute_and(logic_)
    logic_ = substitute_equal_sign(logic_)
    logic_ = substitute_not_equal_sign(logic_)
    logic_ = add_data_name(logic_)
    logic_ = subs1(logic_)
    logic_ = subs2(logic_)
    logic_ = substitute_quote(logic_)
    return logic_






def branching_check(row,variable,metadata):
    """

    :param row:
    :param variable:
    :param metadata:
    :return:
    """
    logic = metadata.get_branching_logic(variable)
    if logic is None:
        return True
    python_logic = convert_branching_logic(logic)
    try:
        result=eval(python_logic, {"data": row})
    except TypeError as e:
        if 'NoneType' in str(e):
            # print(str(e))
            return False
        else:
            raise e

    return result

def hidden_check(row, variable,metadata):
   if metadata.get_hidden(variable):
       return False
   else:
       return True













































































