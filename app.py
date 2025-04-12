import streamlit as st
import os
from pathlib import Path
from crewai import Crew, Process
from agents import document_info_agent, market_analysis, news_scraper, risk_assessment_agent, final_integration_agent
from tasks import document_query_task, market_analysis_task, analyze_scraped_content_task, project_risk_assessment_task, final_integration_task
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(page_title="Document Analysis Crew", layout="wide")

# Setup directories
KNOWLEDGE_DIR = Path("knowledge")
OUTPUT_DIR = Path("output")
KNOWLEDGE_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

def update_agent_knowledge(pdf_name):
    """Update knowledge source for all agents"""
    knowledge = PDFKnowledgeSource(file_paths=pdf_name)
    
    # Update knowledge sources for agents that use them
    document_info_agent.knowledge_sources = [knowledge]
    risk_assessment_agent.knowledge_sources = [knowledge]
    
    return knowledge

def setup_crew(pdf_name):
    """Setup crew with dynamic knowledge source"""
    # Update knowledge sources in agents
    knowledge = update_agent_knowledge(pdf_name)
    
    crew = Crew(
        agents=[
            document_info_agent,
            market_analysis,
            news_scraper,
            risk_assessment_agent,
            final_integration_agent
        ],
        tasks=[
            document_query_task,
            market_analysis_task,
            analyze_scraped_content_task,
            project_risk_assessment_task,
            final_integration_task
        ],
        process=Process.sequential,
        knowledge_sources=[knowledge],
        verbose=True,
        embedder={
            "provider": "google",
            "config": {
                "model": "models/text-embedding-004",
                "api_key": os.getenv("GEMINI_API_KEY"),
            }
        }
    )
    return crew

def run_crew(pdf_name):
    """Execute crew analysis"""
    try:
        crew = setup_crew(pdf_name)
        crew.kickoff()
        return True
    except Exception as e:
        st.error(f"Error during crew execution: {e}")
        return False
    
def clear_output_files():
    """Clear existing output files"""
    output_files = [
        'output/project_overview.json',
        'output/market_analysis.json',
        "output/analysis_report.md",
        "output/risk_register.md",
        "output/final_report.md"
    ]
    
    for file in output_files:
        if os.path.exists(file):
            os.remove(file)
            
def display_markdown_report(file_path, title):
    """Display markdown report with scrollable container"""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            content = f.read()
            st.markdown(f"### {title}")
            st.markdown(
                f'<div style="height: 500px; overflow-y: scroll; padding: 20px; border: 1px solid #ccc; border-radius: 5px;">{content}</div>',
                unsafe_allow_html=True
            )
    else:
        st.warning(f"{title} not found.")
        
def main():
    st.title("📄 Upload PDF and Run Crew")
    # Clear existing files in the knowledge directory
    for file in KNOWLEDGE_DIR.iterdir():
        if file.is_file():
            file.unlink()
    st.info("✅ Knowledge directory has been cleared.")
    
    # Upload PDF
    uploaded_file = st.file_uploader("Upload a PDF file:", type="pdf")
    
    if uploaded_file:
        # Save file to knowledge directory
        pdf_name = uploaded_file.name
        file_path = KNOWLEDGE_DIR / pdf_name

        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success(f"✅ Uploaded {pdf_name} to the knowledge directory.")

        # Show run button only after upload
        if st.button("🚀 Run Crew"):
            # Clear previous output files
            clear_output_files()
            
            with st.spinner("🔄 Running Crew Analysis... This may take several minutes..."):
                success = run_crew(pdf_name)  # Pass only the PDF name
            
            if success:
                st.success("🎉 Crew has finished running!")

                # Display output reports in tabs
                tab1, tab2, tab3 = st.tabs(["📋 Analysis Report", "⚠ Risk Register", "📌 Final Report"])
                
                with tab1:
                    display_markdown_report(
                        "output/analysis_report.md",
                        "Analysis Report"
                    )
                
                with tab2:
                    display_markdown_report(
                        "output/risk_register.md",
                        "Risk Register"
                    )
                
                with tab3:
                    display_markdown_report(
                        "output/final_report.md",
                        "Final Report"
                    )

if __name__ == "__main__":
    main()