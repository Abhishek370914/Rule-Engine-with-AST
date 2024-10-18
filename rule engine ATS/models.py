from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Rule(Base):
    __tablename__ = 'rules'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    rule_string = Column(Text)
    ast_json = Column(Text)  # Store AST in JSON format

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type
        self.left = left
        self.right = right
        self.value = value
    
    def to_dict(self):
        return {
            'type': self.type,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None,
            'value': self.value
        }

    @staticmethod
    def from_dict(node_dict):
        if node_dict is None:
            return None
        return Node(
            node_type=node_dict['type'],
            left=Node.from_dict(node_dict['left']),
            right=Node.from_dict(node_dict['right']),
            value=node_dict['value']
        )
