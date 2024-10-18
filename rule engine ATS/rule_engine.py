from pyparsing import infixNotation, opAssoc, Word, alphas, nums, oneOf, Group
from models import Node
import json

def create_rule(rule_string):
    # Define grammar
    variable = Word(alphas)
    number = Word(nums)
    operand = variable | number
    operator = oneOf("> < = >= <=")
    
    # Binary operators (AND/OR)
    expr = infixNotation(
        Group(operand + operator + operand),
        [
            ('AND', 2, opAssoc.LEFT),
            ('OR', 2, opAssoc.LEFT),
        ]
    )
    
    parsed_rule = expr.parseString(rule_string)
    return build_ast(parsed_rule[0])

def build_ast(parsed_rule):
    # If it's a simple operand, return a node
    if len(parsed_rule) == 3:
        return Node(node_type="operand", value=f"{parsed_rule[0]} {parsed_rule[1]} {parsed_rule[2]}")
    
    # If it's a complex rule (AND/OR), recursively build the AST
    left = build_ast(parsed_rule[0])
    operator = parsed_rule[1]
    right = build_ast(parsed_rule[2])
    
    return Node(node_type="operator", left=left, right=right, value=operator)

def combine_rules(rules):
    combined_root = None
    for rule_string in rules:
        rule_ast = create_rule(rule_string)
        if combined_root is None:
            combined_root = rule_ast
        else:
            combined_root = Node(node_type="operator", left=combined_root, right=rule_ast, value="AND")
    return combined_root

def evaluate_rule(ast, data):
    if ast.type == "operand":
        left, operator, right = ast.value.split()
        left_val = data.get(left)
        right_val = int(right) if right.isdigit() else data.get(right)
        
        if operator == ">":
            return left_val > right_val
        elif operator == "<":
            return left_val < right_val
        elif operator == "=":
            return left_val == right_val
        elif operator == ">=":
            return left_val >= right_val
        elif operator == "<=":
            return left_val <= right_val
        else:
            raise ValueError(f"Unknown operator {operator}")
    
    elif ast.type == "operator":
        if ast.value == "AND":
            return evaluate_rule(ast.left, data) and evaluate_rule(ast.right, data)
        elif ast.value == "OR":
            return evaluate_rule(ast.left, data) or evaluate_rule(ast.right, data)
        else:
            raise ValueError(f"Unknown operator {ast.value}")
