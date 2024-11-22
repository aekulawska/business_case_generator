import streamlit as st
import pandas as pd
from business_case_generator import BusinessCaseGenerator
from concurrent.futures import ThreadPoolExecutor, TimeoutError

class BusinessCaseApp:
    def __init__(self):
        st.set_page_config(page_title="Business Case Generator", layout="wide")
        # Cache the BusinessCaseGenerator instance
        if 'bcg' not in st.session_state:
            st.session_state.bcg = BusinessCaseGenerator()
        self.bcg = st.session_state.bcg

    @st.cache_data(ttl=3600)  # Cache results for 1 hour
    def generate_cached_business_case(_self, url):
        try:
            with ThreadPoolExecutor() as executor:
                future = executor.submit(st.session_state.bcg.generate_business_case, url)
                # Wait for 5 minutes (300 seconds)
                result = future.result(timeout=300)
                return result
        except TimeoutError:
            st.error("Analysis timed out after 5 minutes. Please try again with a different URL.")
            return None
        except Exception as e:
            st.error(f"Generation error: {str(e)}")
            return None

    def run(self):
        st.title("Business Case Generator")
        url = st.text_input("Enter website URL:")
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        analyze_button = st.button("Analyze")

        if analyze_button and url:
            try:
                with st.spinner("Analyzing website..."):
                    # Step 1: Website Analysis
                    website_data = st.session_state.bcg.analyze_website(url)
                    if not website_data:
                        st.error("Failed to analyze website")
                        return
                        
                    # Step 2: Revenue Streams
                    revenue_streams = st.session_state.bcg.identify_revenue_streams(website_data)
                    
                    # Step 3: Business Model
                    business_model = st.session_state.bcg.analyze_business_model(website_data, revenue_streams)
                    
                    # Step 4: Final Generation
                    business_case = st.session_state.bcg.generate_business_case(url)
                    
                    # Display results
                    if business_case:
                        st.success("Analysis complete!")
                        st.write(business_case)
                    else:
                        st.error("No results generated")
                
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
                st.write("Please check if the URL is correct and accessible")
    def display_business_overview(self, business_case):
        st.subheader("Business Overview")
        col1, col2 = st.columns(2)
        with col1:
            st.write("Revenue Streams")
            for stream in business_case['company_overview']['revenue_streams']:
                st.write(f"- {stream}")
        with col2:
            st.write("Key Processes")
            for process in business_case['company_overview']['business_model']['key_processes']:
                st.write(f"- {process}")
    def display_solution_strategy(self, business_case):
        st.subheader("Digital Transformation Strategy")
        col1, col2 = st.columns(2)
        with col1:
            st.write("iPaaS Solutions")
            for integration in business_case['digital_transformation_strategy']['ipaas_solutions']['core_integrations']:
                st.write(f"- {integration}")
        with col2:
            st.write("AI Solutions")
            for agent in business_case['digital_transformation_strategy']['ai_solutions']['operational_agents']:
                st.write(f"- {agent}")
    def display_implementation(self, business_case):
        st.subheader("Implementation Plan")
        st.write(business_case['implementation_timeline'])
        # Benefits analysis
        st.subheader("Benefits Analysis")
        st.write(business_case['benefits_analysis'])
    def export_options(self, business_case):
        st.sidebar.subheader("Export Options")
        if st.sidebar.button("Export as PDF"):
            self.export_as_pdf(business_case)
        if st.sidebar.button("Export as Excel"):
            self.export_as_excel(business_case)
    def export_as_pdf(self, business_case):
        # PDF export implementation
        pass
    def export_as_excel(self, business_case):
        # Excel export implementation
        pass
if __name__ == "__main__":
    app = BusinessCaseApp()
    app.run()