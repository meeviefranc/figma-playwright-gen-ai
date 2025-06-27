import requests
import time
import json

class OllamaLLM:
    def __init__(self, model: str = "mistral"):
        self.model = model
        self.base_url = "http://localhost:11434/api/generate"
        
        # Model-specific configurations
        self.model_configs = {
            "tinyllama": {
                "timeout": 1200,
                "temperature": 0.3,
                "num_predict": 400,
                "top_p": 0.8
            },
            "mistral": {
                "timeout": 1200,
                "temperature": 0.1,
                "num_predict": 600,
                "top_p": 0.9
            },
            "codellama": {
                "timeout": 1200,
                "temperature": 0.05,
                "num_predict": 600,
                "top_p": 0.95
            }
        }
        
    def get_model_config(self):
        """Get configuration for the current model"""
        return self.model_configs.get(self.model, self.model_configs["mistral"])
        
    def test_connection(self):
        """Test if Ollama is running and responsive with the selected model"""
        try:
            # Step 1: Check if Ollama server is running
            health_check_url = "http://localhost:11434/api/tags"
            
            print(f"Testing Ollama server connection...")
            response = requests.get(health_check_url, timeout=10)
            if response.status_code != 200:
                print(f"Ollama server not responding: {response.status_code}")
                return False
            
            print(f"Ollama server is running ✓")
            
            # Step 2: Check if the specific model is available
            models_data = response.json()
            available_models = [model['name'].split(':')[0] for model in models_data.get('models', [])]
            
            print(f"Available models: {available_models}")
            
            if self.model not in available_models:
                print(f"Model {self.model} not found in available models")
                return False
            
            print(f"Model {self.model} is available ✓")
            
            # Step 3: Test actual generation with the model (simplified)
            test_data = {
                "model": self.model,
                "prompt": "Hello",
                "stream": False,
                "options": {
                    "num_predict": 5  # Very small response
                }
            }
            
            print(f"Testing generation with {self.model}...")
            print(f"Request data: {json.dumps(test_data, indent=2)}")
            
            response = requests.post(self.base_url, json=test_data, timeout=1200)
            
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Response data: {json.dumps(result, indent=2)}")
                
                # Check if we got a valid response
                if 'response' in result:
                    response_text = result['response'].strip()
                    print(f"Generated text: '{response_text}'")
                    
                    # Accept any non-empty response
                    if len(response_text) > 0:
                        print("Generation test successful ✓")
                        return True
                    else:
                        print("Empty response received")
                        return False
                else:
                    print("No 'response' field in result")
                    return False
            else:
                print(f"Generation failed: {response.status_code}")
                print(f"Error response: {response.text}")
                return False
                
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {e}")
            return False
        except requests.exceptions.Timeout as e:
            print(f"Timeout error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            return False

    def generate_test_script(self, prompt: str) -> str:
        config = self.get_model_config()
        
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": config["temperature"],
                "top_p": config["top_p"],
                "num_predict": config["num_predict"]
            }
        }

        try:
            print(f"Generating with prompt length: {len(prompt)} characters")
            response = requests.post(self.base_url, json=data, timeout=config["timeout"])
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get("response", "").strip()
                print(f"Generated text length: {len(generated_text)} characters")
                return generated_text
            else:
                print(f"Generation error: {response.status_code} - {response.text}")
                raise Exception(f"Ollama error {response.status_code}: {response.text}")
        except requests.exceptions.Timeout:
            raise Exception(f"Ollama request timed out after {config['timeout']} seconds with {self.model}")
        except requests.exceptions.ConnectionError:
            raise Exception(f"Cannot connect to Ollama. Make sure 'ollama serve' and 'ollama pull {self.model}' are running.")

    def generate_playwright_tests_by_group(self, frame_name, frame_data):
        """Generate Playwright tests with model-specific prompts"""
        scripts = {}
        is_table = frame_data.get('is_table', False)
        
        # Adjust element limits based on model capability
        max_elements = 3 if self.model == "tinyllama" else 5 if self.model == "mistral" else 8
        max_rows = 3 if self.model == "tinyllama" else 5 if self.model == "mistral" else 7
        
        if is_table and frame_data.get('table_rows'):
            for row in frame_data['table_rows'][:max_rows]:
                row_index = row['row_index']
                row_elements = row['elements'][:max_elements]
                group_name = f"{frame_name}_Row_{row_index}"
                
                script = self._generate_model_specific_test(group_name, row_elements)
                scripts[group_name] = script
        else:
            elements = frame_data.get('elements', [])[:max_elements]
            script = self._generate_model_specific_test(frame_name, elements)
            scripts[frame_name] = script
        
        return scripts

    def generate_test_cases_by_group(self, frame_name, frame_data):
        """Generate test cases with model-specific prompts"""
        test_cases = {}
        is_table = frame_data.get('is_table', False)
        
        max_elements = 3 if self.model == "tinyllama" else 5 if self.model == "mistral" else 8
        max_rows = 3 if self.model == "tinyllama" else 5 if self.model == "mistral" else 7
        
        if is_table and frame_data.get('table_rows'):
            for row in frame_data['table_rows'][:max_rows]:
                row_index = row['row_index']
                row_elements = row['elements'][:max_elements]
                group_name = f"{frame_name}_Row_{row_index}"
                
                test_case = self._generate_model_specific_test_case(group_name, row_elements)
                test_cases[group_name] = test_case
        else:
            elements = frame_data.get('elements', [])[:max_elements]
            test_case = self._generate_model_specific_test_case(frame_name, elements)
            test_cases[frame_name] = test_case
        
        return test_cases

    def _generate_model_specific_test(self, group_name, elements):
        """Generate test with model-specific prompt complexity"""
        element_names = [e.get('name', 'Element')[:15] for e in elements]
        
        if self.model == "tinyllama":
            prompt = f"""Test for {group_name}:
Elements: {', '.join(element_names)}
Generate Playwright TypeScript test. Check visibility.
Code only:"""
            
        elif self.model == "mistral":
            prompt = f"""Generate Playwright test for "{group_name}":
Elements: {', '.join(element_names)}
- Check visibility and existence
- Use data-testid selectors
- Include text verification
Return TypeScript code only:"""
            
        else:  # codellama
            prompt = f"""Generate comprehensive Playwright TypeScript test for "{group_name}":
Elements: {', '.join(element_names)}
Requirements:
- Check element existence and visibility
- Verify text content where applicable
- Use proper data-testid selectors
- Include error handling
- Add descriptive comments
Return complete TypeScript test code:"""
        
        return self.generate_test_script(prompt)

    def _generate_model_specific_test_case(self, group_name, elements):
        """Generate test case with model-specific prompt complexity"""
        element_names = [e.get('name', 'Element')[:15] for e in elements]
        
        if self.model == "tinyllama":
            prompt = f"""Test case for {group_name}:
Elements: {', '.join(element_names)}
Write test steps in Markdown.
Check visibility.
Markdown only:"""
            
        elif self.model == "mistral":
            prompt = f"""Generate test case for "{group_name}":
Elements: {', '.join(element_names)}
- Title, description, steps, expected results
- Test visibility and text content
Return Markdown only:"""
            
        else:  # codellama
            prompt = f"""Generate comprehensive test case for "{group_name}":
Elements: {', '.join(element_names)}
Include:
- Clear title and description
- Detailed step-by-step instructions
- Expected results for each step
- Verification of element visibility and content
- Edge cases and error scenarios
Return well-formatted Markdown:"""
        
        return self.generate_test_script(prompt)
