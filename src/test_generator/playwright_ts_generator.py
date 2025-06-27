import os
from datetime import datetime

class PlaywrightTSGenerator:
    def __init__(self, ui_elements, ai_integration):
        self.ui_elements = ui_elements
        self.ai_integration = ai_integration

    def generate(self, extracted_elements):
        """Generate Playwright TypeScript test scripts using AI"""
        all_scripts = {}
        
        for frame_name, frame_data in extracted_elements.items():
            # Use AI to generate tests by groups/rows
            scripts = self.ai_integration.generate_playwright_tests_by_group(frame_name, frame_data)
            all_scripts.update(scripts)
        
        return all_scripts

    def save_scripts(self, scripts, output_dir="output", filename_prefix=""):
        """Save all generated scripts to files with UTF-8 encoding"""
        os.makedirs(output_dir, exist_ok=True)
        saved_files = []
        
        for script_name, script in scripts.items():
            sanitized_name = self._sanitize_name(script_name)
            if filename_prefix:
                filename = f"{filename_prefix}_{sanitized_name}_test.ts"
            else:
                filename = f"{sanitized_name}_test.ts"
            filepath = os.path.join(output_dir, filename)
            
            try:
                # Clean the script content to remove problematic characters
                cleaned_script = self._clean_content(script)
                
                # Write with explicit UTF-8 encoding
                with open(filepath, 'w', encoding='utf-8', errors='replace') as file:
                    file.write(cleaned_script)
                
                saved_files.append(filepath)
                print(f"Successfully saved: {filepath}")
                
            except Exception as e:
                print(f"Error saving {filepath}: {e}")
                # Try saving with error handling
                try:
                    with open(filepath, 'w', encoding='utf-8', errors='ignore') as file:
                        file.write(self._clean_content(script))
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
        
        # Remove any remaining non-ASCII characters that might cause issues
        cleaned = ''.join(char if ord(char) < 128 else '?' for char in cleaned)
        
        return cleaned

    def _sanitize_name(self, name):
        """Sanitize element name for use in code"""
        return ''.join(c if c.isalnum() else '_' for c in name).lower()