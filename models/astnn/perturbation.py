import re
class CodePerturbator:
    def __init__(self, language: str):
        """
        Initialize the perturbator with the target language.

        Args:
            language (str): Programming language ('c' or 'java').
        """
        self.language = language.lower()
        assert self.language in ('c', 'java'), "Unsupported language. Choose 'c' or 'java'."

    def insert_dead_code(self, code: str) -> str:
        """
        Insert dead code into the given source code.

        Args:
            code (str): Original source code.

        Returns:
            str: Source code with dead code inserted.
        """
        if self.language == 'c':
            dead_code = """
            int unused_variable = 42;
            """
        elif self.language == 'java':
            dead_code = """
            int unusedVariable = 42;
            float unusedVariable2 = 4.2;
            char unusedVariable3 = '42';
            int unusedVariable4 = 42;
            int unusedVariable5 = 42;
            """
        else:
            raise ValueError("Unsupported language for dead code insertion")
        return dead_code + "\n" + code

    def rename_variables(self, code: str) -> str:
        """
        Rename variables in the source code.

        Args:
            code (str): Original source code.

        Returns:
            str: Source code with variables renamed.
        """
        if self.language == 'c':
            # Replace 'int ' with 'int new_' as a naive example
            return re.sub(r'\bint (\w+)', r'int new_\1', code)
        elif self.language == 'java':
            # Replace 'int ' with 'int new_' as a naive example
            return re.sub(r'\bint (\w+)', r'int new_\1', code)
        else:
            raise ValueError("Unsupported language for variable renaming")

    def add_comments(self, code: str) -> str:
        """
        Add comments to the source code.

        Args:
            code (str): Original source code.

        Returns:
            str: Source code with comments added.
        """
        comment = "// This is an added comment\n" if self.language == 'java' else "/* This is an added comment */\n"
        return comment + code

    def apply_perturbation(self, code: str, perturbation_type: str) -> str:
        """
        Apply a specific perturbation to the code.

        Args:
            code (str): Original source code.
            perturbation_type (str): Type of perturbation ('dead_code', 'rename_variables', 'add_comments').

        Returns:
            str: Perturbed source code.
        """
        if perturbation_type == 'dead_code':
            return self.insert_dead_code(code)
        elif perturbation_type == 'rename_variables':
            return self.rename_variables(code)
        elif perturbation_type == 'add_comments':
            return self.add_comments(code)
        else:
            raise ValueError(f"Unsupported perturbation type: {perturbation_type}")
        
    
    def insert_dead_code_in_main(self, code: str) -> str:
        """
        Insert dead code specifically inside the `main` function.

        Args:
            code (str): Original source code.

        Returns:
            str: Modified source code with dead code inserted in the `main` function.
        """
        dead_code_c = """
        /* Dead code block */
        int unused_variable = 42;
        if (0) {
            printf("This will never be executed\\n");
        }
        """
        dead_code_java = """
        // Dead code block
        int unusedVariable = 42;
        if (false) {
            System.out.println("This will never be executed");
        }
        """

        # Select dead code based on language
        dead_code = dead_code_c if self.language == 'c' else dead_code_java

        # Regex pattern to find the main method/function
        if self.language == 'c':
            pattern = r"(int\s+main\s*\([^)]*\)\s*\{)"
        else:  # Java
            pattern = r"(public\s+static\s+void\s+main\s*\([^)]*\)\s*\{)"

        # Replace the start of the main function with the dead code inserted
        def insert_dead_code(match):
            main_declaration = match.group(1)
            return f"{main_declaration}\n{dead_code}"

        # Modify the source code
        modified_code = re.sub(pattern, insert_dead_code, code, flags=re.MULTILINE)
        return modified_code
