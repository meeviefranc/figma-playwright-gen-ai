import os
from datetime import datetime

class MarkdownGenerator:
    def __init__(self, ai_integration):
        self.ai_integration = ai_integration

    def generate(self, extracted_elements):
        """Generate human-readable markdown test cases using AI"""
        all_test_cases = {}
        
        for frame_name, frame_data in extracted_elements.items():
            # Use AI to generate test cases by groups/rows
            test_cases = self.ai_integration.generate_test_cases_by_group(frame_name, frame_data)
            all_test_cases.update(test_cases)
        
        return all_test_cases

    def save_test_cases(self, test_cases, output_dir="output", filename_prefix=""):
        """Save all generated test cases to markdown files with UTF-8 encoding"""
        os.makedirs(output_dir, exist_ok=True)
        saved_files = []
        
        for case_name, markdown in test_cases.items():
            sanitized_name = self._sanitize_name(case_name)
            if filename_prefix:
                filename = f"{filename_prefix}_{sanitized_name}_test_cases.md"
            else:
                filename = f"{sanitized_name}_test_cases.md"
            filepath = os.path.join(output_dir, filename)
            
            try:
                # Clean the markdown content
                cleaned_markdown = self._clean_content(markdown)
                
                # Write with explicit UTF-8 encoding
                with open(filepath, 'w', encoding='utf-8', errors='replace') as file:
                    file.write(cleaned_markdown)
                
                saved_files.append(filepath)
                print(f"Successfully saved: {filepath}")
                
            except Exception as e:
                print(f"Error saving {filepath}: {e}")
                # Try saving with error handling
                try:
                    with open(filepath, 'w', encoding='utf-8', errors='ignore') as file:
                        file.write(self._clean_content(markdown))
                    saved_files.append(filepath)
                    print(f"Saved with character cleanup: {filepath}")
                except Exception as e2:
                    print(f"Failed to save {filepath}: {e2}")
        
        return saved_files

    def _clean_content(self, content):
        """Clean content to remove problematic characters"""
        if not content:
            return ""
        
        # Replace common problematic characters
        replacements = {
            '"': '"',  # Smart quotes
            '"': '"',
            ''': "'",
            ''': "'",
            '–': '-',  # En dash
            '—': '--', # Em dash
            '…': '...',  # Ellipsis
            '®': '(R)',
            '©': '(C)',
            '™': '(TM)'
        }
        
        cleaned = content
        for old, new in replacements.items():
            cleaned = cleaned.replace(old, new)
        
        # Keep more characters for markdown (allow Unicode but handle encoding errors)
        try:
            # Test if the content can be encoded
            cleaned.encode('utf-8')
            return cleaned
        except UnicodeEncodeError:
            # If there are still issues, replace problematic characters
            return ''.join(char if ord(char) < 128 or char.isalnum() else '?' for char in cleaned)

    def _sanitize_name(self, name):
        """Sanitize name for use in filenames"""
        return ''.join(c if c.isalnum() else '_' for c in name).lower()