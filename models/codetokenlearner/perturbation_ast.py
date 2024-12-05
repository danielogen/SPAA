import ast
import astor
import random


def rename_variables(node, prefix="var"):
    """
    Rename all variable identifiers in the AST.
    """
    class RenameTransformer(ast.NodeTransformer):
        def __init__(self):
            self.counter = 0
            self.mapping = {}

        def visit_Name(self, name_node):
            if isinstance(name_node.ctx, ast.Store):
                if name_node.id not in self.mapping:
                    self.mapping[name_node.id] = f"{prefix}_{self.counter}"
                    self.counter += 1
                name_node.id = self.mapping[name_node.id]
            elif isinstance(name_node.ctx, ast.Load):
                if name_node.id in self.mapping:
                    name_node.id = self.mapping[name_node.id]
            return name_node

    return RenameTransformer().visit(node)


def reorder_independent_statements(node):
    """
    Reorder independent statements in a block.
    """
    class ReorderTransformer(ast.NodeTransformer):
        def visit_Module(self, module_node):
            module_node.body = self.shuffle_statements(module_node.body)
            return module_node

        def visit_FunctionDef(self, func_node):
            func_node.body = self.shuffle_statements(func_node.body)
            return func_node

        def shuffle_statements(self, statements):
            # Shuffle non-control flow statements
            independent_statements = [
                stmt for stmt in statements if isinstance(stmt, (ast.Assign, ast.Expr))
            ]
            other_statements = [
                stmt for stmt in statements if not isinstance(stmt, (ast.Assign, ast.Expr))
            ]
            random.shuffle(independent_statements)
            return independent_statements + other_statements

    return ReorderTransformer().visit(node)


def add_dead_code(node):
    """
    Add dead (non-functional) code into the AST.
    """
    class DeadCodeTransformer(ast.NodeTransformer):
        def visit_FunctionDef(self, func_node):
            # Add a no-op statement at the beginning of the function body
            dead_code = ast.Expr(value=ast.Constant(value="dead code", kind=None))
            func_node.body.insert(0, dead_code)
            return func_node

    return DeadCodeTransformer().visit(node)


def perturb_ast(code):
  
    tree = ast.parse(code)

    tree = rename_variables(tree)
    tree = reorder_independent_statements(tree)
    tree = add_dead_code(tree)
    return tree

    # Convert the modified AST back to source code
    # return astor.to_source(tree)
