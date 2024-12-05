import ast
import random
import copy
import re
import pandas as pd
import os

class JAdversarialCodeTransformer:
    @staticmethod
    def generate_adversarial_variants(source_df, num_variants=2):
        """
        Generate adversarial variants for code clone detection
        
        :param source_df: DataFrame containing source code
        :param num_variants: Number of adversarial variants to generate per sample
        :return: DataFrame with added adversarial variants
        """
        def generate_variant(code):
            """Generate a single adversarial variant"""
            # 1. Identifier Obfuscation
            def obfuscate_identifiers(code_str):
                try:
                    modified_ast = copy.deepcopy(ast.parse(code_str))
                    
                    class IdentifierObfuscator(ast.NodeTransformer):
                        def __init__(self):
                            self.var_map = {}
                            self.counter = 0
                        
                        def generate_obfuscated_name(self, original_name):
                            if original_name not in self.var_map:
                                self.counter += 1
                                self.var_map[original_name] = f"adv_{self.counter}_{hash(original_name) % 1000}"
                            return self.var_map[original_name]
                        
                        def visit_Name(self, node):
                            if isinstance(node.ctx, (ast.Store, ast.Load)):
                                node.id = self.generate_obfuscated_name(node.id)
                            return node
                        
                        def visit_arg(self, node):
                            node.arg = self.generate_obfuscated_name(node.arg)
                            return node
                    
                    transformer = IdentifierObfuscator()
                    modified_ast = transformer.visit(modified_ast)
                    
                    return ast.unparse(modified_ast)
                except Exception:
                    return code_str
            
            # 2. Equivalent Expression Replacement
            def replace_equivalent_expressions(code_str):
                try:
                    # Simple mathematical expression replacements
                    replacements = [
                        (r'\+', 'sum([{0}])'),
                        (r'-', 'sum([{0}, -{}])'),
                        (r'\*', 'sum([{}]*1)'),
                        (r'/', 'sum([{}])/sum([1])'),
                    ]
                    
                    for pattern, replacement in replacements:
                        code_str = re.sub(pattern, lambda m: replacement.format(m.group(0)), code_str)
                    
                    return code_str
                except Exception:
                    return code_str
            
            # 3. Redundant Code Injection
            def inject_redundant_code(code_str):
                try:
                    modified_ast = copy.deepcopy(ast.parse(code_str))
                    
                    class RedundantCodeInjector(ast.NodeTransformer):
                        def visit_FunctionDef(self, node):
                            # Inject redundant statements
                            redundant_statements = [
                                ast.Assert(test=ast.Constant(value=True), msg=None),
                                ast.Expr(value=ast.Call(
                                    func=ast.Name(id='locals', ctx=ast.Load()),
                                    args=[],
                                    keywords=[]
                                ))
                            ]
                            
                            # Inject at the beginning of the function
                            node.body = redundant_statements + node.body
                            return node
                    
                    transformer = RedundantCodeInjector()
                    modified_ast = transformer.visit(modified_ast)
                    
                    return ast.unparse(modified_ast)
                except Exception:
                    return code_str
            
            # Apply transformations
            variant = code
            variant = obfuscate_identifiers(variant)
            variant = replace_equivalent_expressions(variant)
            variant = inject_redundant_code(variant)
            
            return variant
        
        # Create a copy of the original DataFrame
        augmented_df = source_df.copy()
        
        # Generate adversarial variants
        adversarial_rows = []
        for _, row in source_df.iterrows():
            for _ in range(num_variants):
                new_row = row.copy()
                new_row['code'] = generate_variant(row['code'])
                new_row['is_adversarial'] = True
                adversarial_rows.append(new_row)
        
        # Combine original and adversarial samples
        augmented_df = pd.concat([augmented_df, pd.DataFrame(adversarial_rows)], ignore_index=True)
        
        return augmented_df