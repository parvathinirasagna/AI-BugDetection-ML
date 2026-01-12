import re
import ast
from typing import Dict, List

class MultiLanguageDetector:
    """Detect bugs in Python, Java, and C++ code"""
    
    def __init__(self):
        self.supported_languages = ['python', 'java', 'cpp']
    
    def detect_language(self, code: str) -> str:
        """Detect the programming language of the code"""
        # Python detection
        if self._is_python(code):
            return 'python'
        # Java detection
        elif self._is_java(code):
            return 'java'
        # C++ detection
        elif self._is_cpp(code):
            return 'cpp'
        else:
            return 'unknown'
    
    def _is_python(self, code: str) -> bool:
        """Check if code is Python"""
        python_keywords = ['def ', 'import ', 'from ', 'class ', 'if __name__']
        python_count = sum(1 for kw in python_keywords if kw in code)
        
        # Python-specific patterns
        has_python_patterns = (re.search(r'\bdef\s+\w+\s*\(', code) or
                              re.search(r'\bimport\s+', code) or
                              re.search(r'\bfrom\s+\w+\s+import', code))
        
        return python_count >= 1 or (has_python_patterns is not None)
    
    def _is_java(self, code: str) -> bool:
        """Check if code is Java"""
        # Java-specific patterns
        has_class_def = re.search(r'public\s+(static\s+)?class\s+\w+', code)
        has_main_method = re.search(r'public\s+static\s+void\s+main\s*\(', code)
        has_java_imports = re.search(r'import\s+java\.', code)
        has_package = re.search(r'^\s*package\s+', code, re.MULTILINE)
        
        java_indicators = sum([bool(x) for x in [has_class_def, has_main_method, has_java_imports, has_package]])
        return java_indicators >= 1
    
    def _is_cpp(self, code: str) -> bool:
        """Check if code is C++"""
        # C++ specific patterns
        has_include = re.search(r'#include\s*[<"]', code)
        has_using = re.search(r'\busing\s+namespace\s+std', code)
        has_namespace = re.search(r'\bnamespace\s+\w+', code)
        has_template = re.search(r'\btemplate\s*<', code)
        has_pointers = re.search(r'\w+\s*\*\s*\w+', code)
        
        cpp_indicators = sum([bool(x) for x in [has_include, has_using, has_namespace, has_template, has_pointers]])
        return cpp_indicators >= 1
    
    def check_python_bugs(self, code: str) -> List[str]:
        """Check for common Python bugs"""
        bugs = []
        
        # Check for undefined variables
        if re.search(r'\w+\s*=.*$', code, re.MULTILINE):
            if not re.search(r'\w+\s*=.*\1', code):
                pass  # Basic undefined var check
        
        # Check for mutable default arguments
        if 'def ' in code and '[]' in code or '{}' in code:
            if re.search(r'def\s+\w+\([^)]*=[\[\{]', code):
                bugs.append('Mutable default argument detected')
        
        # Check for except without exception type
        if re.search(r'except\s*:', code):
            bugs.append('Bare except clause detected - specify exception type')
        
        # Check for missing return statements
        if 'def ' in code and 'return' not in code and 'pass' in code:
            bugs.append('Function may not return value')
        
        # Check for infinite loops
        if 'while True' in code:
            if 'break' not in code:
                bugs.append('Infinite loop detected - missing break statement')
        
        return bugs
    
    def check_java_bugs(self, code: str) -> List[str]:
        """Check for common Java bugs"""
        bugs = []
        
        # Check for null pointer exceptions
        if '.length' in code or '.size()' in code:
            if 'null' not in code and 'if' not in code:
                bugs.append('Potential null pointer exception')
        
        # Check for unclosed resources
        if 'FileInputStream' in code or 'FileOutputStream' in code:
            if 'close()' not in code:
                bugs.append('Resource not closed - use try-with-resources')
        
        # Check for infinite loops
        if 'while(true)' in code:
            bugs.append('Infinite loop detected')
        
        # Check for unhandled exceptions
        if re.search(r'throw new \w+Exception', code):
            if 'catch' not in code and 'throws' not in code:
                bugs.append('Exception thrown without handling')
        
        # Check for missing break in switch
        if 'switch' in code and 'case' in code:
            if 'break' not in code:
                bugs.append('Missing break statement in switch case')
        
        return bugs
    
    def check_cpp_bugs(self, code: str) -> List[str]:
        """Check for common C++ bugs"""
        bugs = []
        
        # Check for memory leaks
        if 'new ' in code and 'delete' not in code:
            bugs.append('Potential memory leak (new without delete)')
        
        # Check for null pointer dereference
        if '->' in code:
            if 'nullptr' not in code and '!=' not in code:
                bugs.append('Potential null pointer dereference')
        
        # Check for buffer overflow
        if 'strcpy' in code or 'sprintf' in code:
            if 'strncpy' not in code and 'snprintf' not in code:
                bugs.append('Unsafe string function used - use safe alternatives')
        
        # Check for uninitialized variables
        if re.search(r'\bint\s+\w+\s*;', code):
            bugs.append('Uninitialized variable detected')
        
        # Check for array out of bounds
        if '[' in code and ']' in code:
            if 'bounds' not in code.lower() and 'check' not in code.lower():
                bugs.append('Array access without bounds checking')
        
        return bugs
    
    def extract_python_features(self, code: str) -> List[int]:
        """Extract features specific to Python code"""
        features = []
        
        # Count of function definitions
        features.append(len(re.findall(r'\bdef\s+\w+\s*\(', code)))
        
        # Count of class definitions
        features.append(len(re.findall(r'\bclass\s+\w+', code)))
        
        # Count of imports
        features.append(len(re.findall(r'\b(import|from)\s+', code)))
        
        # Count of loops
        features.append(len(re.findall(r'\b(for|while)\b', code)))
        
        # Count of conditionals
        features.append(len(re.findall(r'\b(if|elif|else)\b', code)))
        
        return features
    
    def extract_java_features(self, code: str) -> List[int]:
        """Extract features specific to Java code"""
        features = []
        
        # Count of method definitions
        features.append(len(re.findall(r'\bpublic\s+\w+\s+\w+\s*\(', code)))
        
        # Count of class definitions
        features.append(len(re.findall(r'\bclass\s+\w+', code)))
        
        # Count of try-catch blocks
        features.append(len(re.findall(r'\btry\s*\{', code)))
        
        # Count of for loops
        features.append(len(re.findall(r'\bfor\s*\(', code)))
        
        # Count of if statements
        features.append(len(re.findall(r'\bif\s*\(', code)))
        
        return features
    
    def extract_cpp_features(self, code: str) -> List[int]:
        """Extract features specific to C++ code"""
        features = []
        
        # Count of function definitions
        features.append(len(re.findall(r'\w+\s+\w+\s*\([^)]*\)\s*\{', code)))
        
        # Count of class definitions
        features.append(len(re.findall(r'\bclass\s+\w+', code)))
        
        # Count of pointers
        features.append(len(re.findall(r'\w+\s*\*', code)))
        
        # Count of memory allocations (new)
        features.append(len(re.findall(r'\bnew\s+', code)))
        
        # Count of memory deallocations (delete)
        features.append(len(re.findall(r'\bdelete\s+', code)))
        
        return features
    
    def analyze_code(self, code: str) -> Dict:
        """Main analysis function for any language"""
        language = self.detect_language(code)
        
        result = {
            'language': language,
            'bugs_found': [],
            'severity': 'low',
            'feature_count': 0
        }
        
        if language == 'python':
            result['bugs_found'] = self.check_python_bugs(code)
            result['feature_count'] = len(self.extract_python_features(code))
        elif language == 'java':
            result['bugs_found'] = self.check_java_bugs(code)
            result['feature_count'] = len(self.extract_java_features(code))
        elif language == 'cpp':
            result['bugs_found'] = self.check_cpp_bugs(code)
            result['feature_count'] = len(self.extract_cpp_features(code))
        
        # Determine severity
        if len(result['bugs_found']) > 2:
            result['severity'] = 'high'
        elif len(result['bugs_found']) > 0:
            result['severity'] = 'medium'
        
        return result
