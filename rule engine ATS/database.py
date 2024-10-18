import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Node, Rule

engine = create_engine('sqlite:///rules.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def store_rule(rule_name, rule_ast, rule_string):
    rule = Rule(name=rule_name, ast_json=json.dumps(rule_ast.to_dict()), rule_string=rule_string)
    session.add(rule)
    session.commit()

def load_rule(rule_name):
    rule = session.query(Rule).filter_by(name=rule_name).first()
    if rule:
        return Node.from_dict(json.loads(rule.ast_json))
    return None
