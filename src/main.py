import streamlit as st
import os
from figma_api.client import FigmaClient
from ui_extractor.extractor import UIExtractor
from test_generator.playwright_ts_generator import PlaywrightTSGenerator
from test_generator.markdown_generator import MarkdownGenerator
from ai_integration.ollama_llm import OllamaLLM

def main():
    st.subheader("Figma Wireframe Test Case & Test Script Generator")
    
    # Add expandable help section
    with st.expander("ℹ️ How to Use This Tool - Click to Expand"):
        st.markdown("""
        ### 📋 Description
        This tool automatically generates **AI-enhanced Playwright TypeScript test scripts** and **human-readable test cases** from your Figma wireframes using local Ollama AI.
        
        ### 🚀 What You'll Get
        - **TypeScript Test Scripts**: AI-generated Playwright automation tests
        - **Markdown Test Cases**: AI-generated human-readable test documentation
        - **Frame Grouping**: Tests organized by Figma frames and table rows
                
        ### 📝 Required Information
        1. **Figma Access Token**: Go to Figma → Settings → Account → Personal Access Tokens
        2. **Figma File Key**: Found in your Figma file URL
        3. **Figma Node Key**: Format as `1376:2`
        
        ### 🤖 AI Models Available
        - **TinyLlama**: Fastest, basic quality (recommended for quick testing)
        - **Mistral**: Balanced speed and quality (recommended for most use cases)
        - **CodeLlama**: Best for code generation, slower (recommended for production tests)
        
        ### 🛠️ Setup Commands (Required)
        ```bash
        ollama serve
        ollama pull tinyllama
        ollama pull mistral
        ollama pull codellama
        ```
        
        ### ⚠️ Important
        - Ollama must be running locally for this tool to work
        - Make sure you have pulled the AI model you want to use
        - Generation time varies by model: TinyLlama (fastest) → Mistral (balanced) → CodeLlama (slowest but best quality)
        """)
    
    # User input
    st.subheader("🔑 Figma API Configuration")
    access_token = st.text_input("Figma Access Token", type="password")
    file_key = st.text_input("Figma File Key")
    node_key = st.text_input("Figma Node Key (format: `1376:2`)")
    
    # AI Model Selection (Required)
    st.subheader("🤖 AI Model Selection")
    model_options = {
        "tinyllama": "TinyLlama (Fastest, Basic Quality)",
        "mistral": "Mistral (Balanced Speed & Quality)",
        "codellama": "CodeLlama (Best Quality, Slower)"
    }
    
    selected_model = st.selectbox(
        "Select Ollama Model:",
        options=list(model_options.keys()),
        format_func=lambda x: model_options[x],
        index=1  # Default to mistral
    )
    
    # Show model info
    model_info = {
        "tinyllama": "⚡ **TinyLlama**: ~1-2 seconds per frame, basic test generation",
        "mistral": "⚖️ **Mistral**: ~3-5 seconds per frame, good balance of speed and quality",
        "codellama": "🎯 **CodeLlama**: ~5-10 seconds per frame, best code quality and detailed tests"
    }
    st.info(model_info[selected_model])
    
    if st.button("🚀 Generate AI-Enhanced Tests", type="primary"):
        if access_token and file_key and node_key:
            try:
                # Initialize AI integration (Required)
                with st.spinner(f"🔌 Connecting to Ollama with {selected_model}..."):
                    ai_integration = OllamaLLM(model=selected_model)
                    
                    # Show detailed connection status
                    st.write("**🔍 Connection Test Details:**")
                    
                    # Capture print output to show in Streamlit
                    import io
                    import sys
                    from contextlib import redirect_stdout
                    
                    # Capture the test output
                    output_buffer = io.StringIO()
                    with redirect_stdout(output_buffer):
                        connection_result = ai_integration.test_connection()
                    
                    # Show the captured output
                    test_output = output_buffer.getvalue()
                    if test_output.strip():
                        st.code(test_output, language="text")
                    
                    if not connection_result:
                        st.error(f"❌ Connection test failed for {selected_model} model")
                        st.error("**Debug information is shown above. Please check:**")
                        st.code("ollama serve", language="bash")
                        st.code(f"ollama pull {selected_model}", language="bash")
                        st.info("💡 Try running the commands above and restart the app")
                        st.stop()
                    
                    st.success(f"✅ Successfully connected to Ollama with {selected_model}!")
                
                with st.spinner("📡 Fetching data from Figma..."):
                    figma_client = FigmaClient(access_token, file_key, node_key)
                    ui_elements = figma_client.fetch_ui_elements()
                    st.success(f"✅ Fetched {len(ui_elements)} UI elements")
                
                with st.spinner("🔍 Extracting UI elements..."):
                    ui_extractor = UIExtractor(ui_elements)
                    extracted_elements = ui_extractor.extract_ui_elements()
                    st.success(f"✅ Analyzed {len(extracted_elements)} frames")
                    
                    # Show frame summary
                    for frame_name, frame_data in extracted_elements.items():
                        element_count = len(frame_data.get('elements', []))
                        is_table = frame_data.get('is_table', False)
                        table_info = f" (Table with {len(frame_data.get('table_rows', []))} rows)" if is_table else ""
                        st.info(f"📋 {frame_name}: {element_count} elements{table_info}")
                
                # Create a list of frame items to avoid dictionary change during iteration
                frame_items = list(extracted_elements.items())
                total_frames = len(frame_items)
                progress_bar = st.progress(0)
                
                with st.spinner(f"🧪 Generating TypeScript tests with {selected_model}..."):
                    playwright_generator = PlaywrightTSGenerator(ui_elements, ai_integration)
                    
                    st.write(f"**🤖 AI Processing with {selected_model.upper()}:**")
                    
                    ts_scripts = {}
                    for i, (frame_name, frame_data) in enumerate(frame_items):
                        st.write(f"🔄 Processing frame: **{frame_name}** ({i+1}/{total_frames}) with {selected_model}")
                        
                        try:
                            frame_scripts = ai_integration.generate_playwright_tests_by_group(frame_name, frame_data)
                            ts_scripts.update(frame_scripts)
                            st.write(f"✅ {selected_model} generated {len(frame_scripts)} test(s)")
                        except Exception as e:
                            st.warning(f"⚠️ Failed to generate tests for {frame_name}: {str(e)}")
                            continue
                        
                        progress_bar.progress((i + 1) / (total_frames * 2))
                    
                    st.success(f"✅ Generated {len(ts_scripts)} TypeScript test files")
                
                with st.spinner(f"📝 Generating test case documentation with {selected_model}..."):
                    markdown_generator = MarkdownGenerator(ai_integration)
                    
                    markdown_cases = {}
                    for i, (frame_name, frame_data) in enumerate(frame_items):
                        try:
                            frame_cases = ai_integration.generate_test_cases_by_group(frame_name, frame_data)
                            markdown_cases.update(frame_cases)
                        except Exception as e:
                            st.warning(f"⚠️ Failed to generate test cases for {frame_name}: {str(e)}")
                            continue
                        
                        progress_bar.progress((total_frames + i + 1) / (total_frames * 2))
                    
                    progress_bar.progress(1.0)
                    st.success(f"✅ Generated {len(markdown_cases)} test case files")
                
                # Only proceed if we have generated content
                if not ts_scripts and not markdown_cases:
                    st.error("❌ No test files were generated. Please check the error messages above.")
                    st.stop()
                
                # Save files
                output_dir = "output"
                os.makedirs(output_dir, exist_ok=True)
                
                sanitized_file_key = ''.join(c if c.isalnum() else '_' for c in file_key)[:20]
                sanitized_node_key = ''.join(c if c.isalnum() else '_' for c in node_key)[:10]
                filename_prefix = f"{sanitized_file_key}_{sanitized_node_key}"
                
                with st.spinner("💾 Saving files..."):
                    ts_files = []
                    md_files = []
                    
                    if ts_scripts:
                        ts_files = playwright_generator.save_scripts(ts_scripts, output_dir, filename_prefix)
                    
                    if markdown_cases:
                        md_files = markdown_generator.save_test_cases(markdown_cases, output_dir, filename_prefix)
                
                # Display results
                st.subheader(f"🎉 Test Cases and Scripts Generation Complete with {selected_model.upper()}!")
                
                # Show saved files
                st.subheader("📁 Saved Files")
                if ts_files or md_files:
                    st.success(f"✅ Generated {len(ts_files)} TypeScript files and {len(md_files)} Markdown files")
                    
                    with st.expander("📋 View File Paths"):
                        if ts_files:
                            st.write("**TypeScript Files:**")
                            for file_path in ts_files:
                                st.code(os.path.abspath(file_path))
                        
                        if md_files:
                            st.write("**Markdown Files:**")
                            for file_path in md_files:
                                st.code(os.path.abspath(file_path))
                else:
                    st.warning("⚠️ No files were saved. Check the error messages above.")
                
            except Exception as e:
                st.error(f"❌ Error during AI generation: {str(e)}")
                if "Cannot connect to Ollama" in str(e) or "Ollama" in str(e):
                    st.error("🚨 Ollama Connection Issue:")
                    st.info("Please ensure Ollama is running:")
                    st.code("ollama serve", language="bash")
                    st.info(f"And make sure the {selected_model} model is available:")
                    st.code(f"ollama pull {selected_model}", language="bash")
                st.exception(e)
        else:
            st.error("⚠️ Please provide all required Figma credentials.")

if __name__ == "__main__":
    main()