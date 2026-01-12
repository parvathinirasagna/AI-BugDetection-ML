import re
import ast
import numpy as np
from typing import List, Dict, Tuple
import tokenize
import io

class FeatureExtractor:
    """Extract features from source code for bug detection"""
    
    def __init__(self):
        self.features_dict = {}
    
    def extract_all_features(self, code_snippet: str) -> np.ndarray:
        """Extract all features from code snippet"""
        features = []
        features.extend(self.extract_syntax_features(code_snippet))
        features.extend(self.extract_semantic_features(code_snippet))
        features.extend(self.extract_complexity_features(code_snippet))
        return np.array(features)
    
    def extract_syntax_features(self, code: str) -> List[float]:
        """Extract syntactic features from code"""
        features = []
        
        # Feature 1: Count of loops
        loop_count = len(re.findall(r'\b(for|while)\b', code))
        features.append(loop_count)
        
        # Feature 2: Count of conditionals
        conditional_count = len(re.findall(r'\b(if|elif|else)\b', code))
        features.append(conditional_count)
        
        # Feature 3: Count of function calls
        func_call_count = len(re.findall(r'\w+\s*\(', code))
        features.append(func_call_count)
        
        # Feature 4: Count of try-except blocks
        try_except_count = len(re.findall(r'\b(try|except|finally)\b', code))
        features.append(try_except_count)
        
        # Feature 5: Count of variable assignments
        assignment_count = len(re.findall(r'\w+\s*=', code))
        features.append(assignment_count)
        
        return features
    
    def extract_semantic_features(self, code: str) -> List[float]:
        """Extract semantic features from code"""
        features = []
        
        try:
            tree = ast.parse(code)
        except:
            return [0] * 5  # Return zeros if parsing fails
        
        # Feature 6: Count of function definitions
        func_defs = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        features.append(len(func_defs))
        
        # Feature 7: Count of class definitions
        class_defs = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        features.append(len(class_defs))
        
        # Feature 8: Average function length
        if func_defs:
            avg_length = np.mean([len(ast.get_source_segment(code, f).split('\n')) if ast.get_source_segment(code, f) else 0 for f in func_defs])
        else:
            avg_length = 0
        features.append(avg_length)
        
        # Feature 9: Count of imports
        imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
        features.append(len(imports))
        
        # Feature 10: Count of return statements
        returns = [node for node in ast.walk(tree) if isinstance(node, ast.Return)]
        features.append(len(returns))
        
        return features
    
    def extract_complexity_features(self, code: str) -> List[float]:
        """Extract code complexity features"""
        features = []
        
        # Feature 11: Cyclomatic complexity
        cc = self._calculate_cyclomatic_complexity(code)
        features.append(cc)
        
        # Feature 12: Lines of code
        loc = len([line for line in code.split('\n') if line.strip() and not line.strip().startswith('#')])
        features.append(loc)
        
        # Feature 13: Nesting depth
        nesting = self._calculate_nesting_depth(code)
        features.append(nesting)
        
        # Feature 14: Comment to code ratio
        comments = len([line for line in code.split('\n') if line.strip().startswith('#')])
        comment_ratio = comments / max(loc, 1)
        features.append(comment_ratio)
        
        # Feature 15: Number of empty lines
        empty_lines = len([line for line in code.split('\n') if not line.strip()])
        features.append(empty_lines)
        
        return features
    
    def _calculate_cyclomatic_complexity(self, code: str) -> int:
        """Calculate cyclomatic complexity of code"""
        complexity = 1
        complexity += len(re.findall(r'\b(if|elif|for|while|and|or)\b', code))
        complexity += len(re.findall(r'\bexcept\b', code))
        return complexity
    
    def _calculate_nesting_depth(self, code: str) -> int:
        """Calculate maximum nesting depth"""
        lines = code.split('\n')
        max_depth = 0
        current_depth = 0
        
        for line in lines:
            stripped = line.lstrip()
            if not stripped or stripped.startswith('#'):
                continue
            
            depth = (len(line) - len(stripped)) // 4
            max_depth = max(max_depth, depth)
        
        return max_depth

class CodeBERTFeatureExtractor:
    """Extract features using CodeBERT embeddings (improved model)"""
    
    def __init__(self):
        # TODO: Initialize CodeBERT model
        self.model = None
        self.tokenizer = None
    
    def extract_embeddings(self, code: str) -> np.ndarray:
        """Extract CodeBERT embeddings from code"""
        # TODO: Implement CodeBERT embedding extraction
        # For now, return random embeddings
        return np.random.rand(768)  # CodeBERT produces 768-dimensional embeddings
    
    def extract_features(self, code: str) -> np.ndarray:
        """Extract features using CodeBERT"""
        embeddings = self.extract_embeddings(code)
        # Reduce dimensionality to 15 features
        return embeddings[:15] if len(embeddings) > 15 else embeddings


class LanguageSpecificExtractor:
    """Extract language-specific features for Python, Java, and C++"""
    
    def extract_python_features(self, code: str) -> List[int]:
        """Extract Python-specific features"""
        features = []
        
        # Count of function definitions
        features.append(len(re.findall(r'\bdef\s+\w+\s*\(', code)))
        
        # Count of class definitions
        features.append(len(re.findall(r'\bclass\s+\w+', code)))
        
        # Count of imports
        features.append(len(re.findall(r'\b(import|from)\s+', code)))
        
        # Count of decorators
        features.append(len(re.findall(r'@\w+', code)))
        
        # Count of try-except blocks
        features.append(len(re.findall(r'\btry\s*:', code)))
        
        return features
    
    def extract_java_features(self, code: str) -> List[int]:
        """Extract Java-specific features"""
        features = []
        
        # Count of class definitions
        features.append(len(re.findall(r'\bclass\s+\w+', code)))
        
        # Count of method definitions
        features.append(len(re.findall(r'\bpublic\s+\w+\s+\w+\s*\(', code)))
        
        # Count of interface definitions
        features.append(len(re.findall(r'\binterface\s+\w+', code)))
        
        # Count of try-catch blocks
        features.append(len(re.findall(r'\btry\s*\{', code)))
        
        # Count of synchronized blocks
        features.append(len(re.findall(r'\bsynchronized\s*\(', code)))
        
        return features
    
    def extract_cpp_features(self, code: str) -> List[int]:
        """Extract C++-specific features"""
        features = []
        
        # Count of class definitions
        features.append(len(re.findall(r'\bclass\s+\w+', code)))
        
        # Count of function definitions
        features.append(len(re.findall(r'\w+\s+\w+\s*\([^)]*\)\s*\{', code)))
        
        # Count of templates
        features.append(len(re.findall(r'\btemplate\s*<', code)))
        
        # Count of pointers
        features.append(len(re.findall(r'\*', code)))
        
        # Count of memory operations (new/delete)
        features.append(len(re.findall(r'\b(new|delete)\s+', code)))
        
        return features
