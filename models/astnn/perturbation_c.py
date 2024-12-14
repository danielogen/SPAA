import re
import copy
import random
import pandas as pd
import os
from pycparser import c_parser

class CAdversarialCodeTransformer:
    @staticmethod
    def generate_adversarial_variants(source_df, num_variants=1):
        """
        Generate adversarial variants for C code
        
        :param source_df: DataFrame containing source code
        :param num_variants: Number of adversarial variants to generate per sample
        :return: DataFrame with added adversarial variants
        """
        def generate_variant(code):
            """Generate a single adversarial variant for C code"""
            # 1. Identifier Renaming
            def obfuscate_identifiers(code_str):
                # Simple identifier replacement using regex
                def replace_identifier(match):
                    original = match.group(0)
                    keywords = ['int', 'char', 'void', 'return', 'if', 'else', 'for', 'while']
                    if original in keywords:
                        return original
                    # Ensure valid identifier
                    return f"adv_{abs(hash(original)) % 10000}"
                
                # Replace variable and function names
                obfuscated = re.sub(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', replace_identifier, code_str)
                return obfuscated
            def rename_variables_in_main(code):
                """
                Rename variables in the main function of the given C code using regex.
                """
                # Regex to find the main function
                main_function_pattern = r"(int\s+main\s*\([^)]*\)\s*{)(.*?)(\n})"
                
                # Regex to find variable declarations (int, float, etc.) inside main
                variable_declaration_pattern = r"\b(int|float|double|char)\s+([a-zA-Z_][a-zA-Z0-9_]*)\b"
                
                def rename_variables(match):
                    """
                    Renames variables in the matched main function body.
                    """
                    main_header, body, closing_brace = match.groups()
                    
                    # Find all variable declarations
                    variables = re.findall(variable_declaration_pattern, body)
                    renamed_body = body
                    
                    for _, var_name in variables:
                        renamed_var = f"{var_name}_renamed"
                        # print(f"Renaming variable: {var_name} -> {renamed_var}")
                        # Replace all occurrences of the variable name in the body
                        renamed_body = re.sub(rf"\b{var_name}\b", renamed_var, renamed_body)
                    
                    return f"{main_header}{renamed_body}{closing_brace}"
                
                # Replace the main function body with renamed variables
                modified_code = re.sub(main_function_pattern, rename_variables, code, flags=re.S)
                return modified_code
            
            # 2. Equivalent Expression Transformations
            def transform_expressions(code_str):
                # Replace simple arithmetic expressions
                transformations = [
                    (r'(\w+)\s*\+\s*(\w+)', r'(\1 + \2)'),
                    (r'(\w+)\s*-\s*(\w+)', r'(\1 - \2)'),
                    (r'(\w+)\s*\*\s*(\w+)', r'(\1 * \2)'),
                ]

                
                for pattern, replacement in transformations:
                    code_str = re.sub(pattern, 
                        lambda m: replacement.format(m.group(1), m.group(2)), 
                        code_str)
                
                return code_str
            
            # 3. Redundant Code Injection
            def inject_redundant_code(code_str):
                # Add simple no-op statements or assertions
                redundant_snippets = [
                    """int adv_9428(int adv_1234, int adv_5678) {
                        int __dummy = 0;
                        return (adv_1234 + adv_5678);
                    }
                    """,
                    """
                    void static_variable_function() {
                        static int counter = 0;
                        counter++;
                    }
                    """,
                    """
                    void empty_loop() {
                        for (int i = 0; i < 10; i++) {
                        }
                    }
                    """
                ]
            
                for i in redundant_snippets:
                    code_str = '\n' + code_str + '\n' + i + '\n' 
                return code_str
            
                lines = code_str.split('\n')
                modified_lines = []
                for line in lines:
                    if re.match(r'^\s*(int|void|char)\s+\w+\s*\(', line):  # Function start
                        modified_lines.append(random.choice(redundant_snippets))
                    elif 'return' in line:  # Return statement
                        modified_lines.append(random.choice(redundant_snippets))
                    modified_lines.append(line)
                return '\n'.join(modified_lines)

            
            # Apply transformations
            variant = code
            # variant = obfuscate_identifiers(variant)
            # variant  = rename_variables_in_main(variant)
            # variant = transform_expressions(variant)
            variant = inject_redundant_code(variant)

            # Parse to AST
            # parser = c_parser.CParser()
            # try:
            #     ast = parser.parse(variant)
            #     return ast
            # except Exception as e:
            #     raise ValueError(f"Error parsing transformed code into AST: {e}")
                    
            return variant
        
        # Create a copy of the original DataFrame
        augmented_df = source_df.copy()
        
        # Generate adversarial variants
        adversarial_rows = []
        for _, row in source_df.iterrows():
            for _ in range(num_variants):
                new_row = row.copy()
                try:
                    new_row['code'] = generate_variant(row['code'])
                    new_row['is_adversarial'] = True
                    adversarial_rows.append(new_row)
                except Exception as e:
                    # Skip variant generation if it fails
                    print(f"Variant generation failed: {e}")
        
        # Combine original and adversarial samples
        augmented_df = pd.concat([augmented_df, pd.DataFrame(adversarial_rows)], ignore_index=True)
        
        return augmented_df
