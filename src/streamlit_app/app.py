import streamlit as st
from src.figma_api.client import FigmaClient
from src.ui_extractor.extractor import UIExtractor
from src.test_generator.playwright_ts_generator import PlaywrightTSGenerator
from src.test_generator.markdown_generator import MarkdownGenerator
from src.ai_integration.ollama_llm import OllamaLLM

def main():
    st.title("Figma to Playwright Test Generator")
    
    st.sidebar.header("Figma API Credentials")
    access_token = st.sidebar.text_input("Access Token")
    file_key = st.sidebar.text_input("File Key")
    node_key = st.sidebar.text_input("Node Key")
    
    if st.sidebar.button("Generate Tests"):
        if access_token and file_key and node_key:
            figma_client = FigmaClient(access_token, file_key, node_key)
            ui_data = figma_client.fetch_ui_elements()
            
            ui_extractor = UIExtractor()
            ui_elements = ui_extractor.extract(ui_data)
            
            playwright_generator = PlaywrightTSGenerator()
            ts_scripts = playwright_generator.generate(ui_elements)
            
            markdown_generator = MarkdownGenerator()
            markdown_cases = markdown_generator.generate(ui_elements)
            
            llm = OllamaLLM()
            ai_generated_scripts = llm.generate_tests(ts_scripts)
            
            st.success("Test scripts generated successfully!")
            st.subheader("Playwright TypeScript Test Scripts")
            st.code(ts_scripts)
            
            st.subheader("Markdown Test Cases")
            st.markdown(markdown_cases)
            
            st.subheader("AI-Enhanced Test Scripts")
            st.code(ai_generated_scripts)
        else:
            st.error("Please fill in all fields.")

if __name__ == "__main__":
    main()