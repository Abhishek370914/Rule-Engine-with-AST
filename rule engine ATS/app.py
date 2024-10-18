from flask import Flask, render_template, request, jsonify
import json
from rule_engine import create_rule, combine_rules, evaluate_rule
from database import store_rule, load_rule

app = Flask(__name__)

# Serve the HTML file
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_rule', methods=['POST'])
def api_create_rule():
    data = request.get_json()
    rule_string = data['rule_string']
    rule_name = data['rule_name']
    
    rule_ast = create_rule(rule_string)
    store_rule(rule_name, rule_ast, rule_string)
    
    return jsonify({"message": "Rule created successfully", "ast": rule_ast.to_dict()}), 201

@app.route('/evaluate_rule/<rule_name>', methods=['POST'])
def api_evaluate_rule(rule_name):
    data = request.get_json()
    rule_ast = load_rule(rule_name)
    
    if not rule_ast:
        return jsonify({"error": "Rule not found"}), 404
    
    result = evaluate_rule(rule_ast, data)
    return jsonify({"result": result})

@app.route('/combine_rules', methods=['POST'])
def api_combine_rules():
    data = request.get_json()
    rules = data['rules']
    
    combined_ast = combine_rules(rules)
    return jsonify({"combined_ast": combined_ast.to_dict()})

if __name__ == '__main__':
    app.run(debug=True)
