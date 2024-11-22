import requests
from bs4 import BeautifulSoup
import openai
import json
from datetime import datetime
import time
class BusinessCaseGenerator:
    def __init__(self):
        self.revenue_patterns = {
            'ecommerce': ['shop', 'store', 'cart', 'checkout', 'products'],
            'subscription': ['pricing', 'plans', 'subscribe', 'membership'],
            'service': ['services', 'solutions', 'consulting', 'book'],
            'advertising': ['advertisers', 'sponsors', 'media kit'],
            'marketplace': ['sellers', 'vendors', 'partners', 'marketplace']
        }
    def analyze_website(self, url):
        """Analyze website content and structure"""
        try:
            # Increase timeout to 30 seconds and add headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, timeout=30, headers=headers)
            response.raise_for_status()
            
            # Add a small delay to prevent overloading
            time.sleep(1)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Return minimal data if full analysis fails
            data = {
                'title': soup.title.string if soup.title else url,
                'text_content': soup.get_text()[:5000],  # Limit text content
                'links': [],
                'meta_description': ''
            }
            
            # Try to enhance data if possible
            try:
                data['links'] = [link.get('href') for link in soup.find_all('a', limit=100)]
                data['meta_description'] = soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else ''
            except Exception:
                pass  # Continue with minimal data if enhancement fails
                
            return data
            
        except requests.Timeout:
            raise Exception(f"Website {url} is taking too long to respond. Please try again later or try a different URL.")
        except requests.RequestException as e:
            raise Exception(f"Cannot access website {url}. Error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error analyzing website {url}: {str(e)}")
    def identify_revenue_streams(self, website_data):
        """Identify potential revenue streams based on website content"""
        revenue_streams = []
        for stream, patterns in self.revenue_patterns.items():
            if any(pattern in website_data['text_content'].lower() for pattern in patterns):
                revenue_streams.append(stream)
        return revenue_streams
    def analyze_business_model(self, website_data, revenue_streams):
        """Analyze business model and operational patterns"""
        business_model = {
            'revenue_streams': revenue_streams,
            'customer_segments': self._identify_customer_segments(website_data),
            'key_processes': self._identify_key_processes(website_data),
            'pain_points': self._identify_pain_points(website_data)
        }
        return business_model
    def generate_ipaas_recommendations(self, business_model):
        """Generate iPaaS implementation recommendations"""
        recommendations = {
            'core_integrations': [],
            'automation_opportunities': [],
            'data_flow_improvements': []
        }
        # Map business processes to iPaaS solutions
        for process in business_model['key_processes']:
            recommendations['core_integrations'].append(
                self._map_process_to_integration(process)
            )
        return recommendations
    def generate_ai_recommendations(self, business_model):
        """Generate AI agent recommendations"""
        ai_recommendations = {
            'operational_agents': [],
            'analytical_agents': [],
            'customer_facing_agents': []
        }
        # Map business needs to AI solutions
        for pain_point in business_model['pain_points']:
            ai_recommendations['operational_agents'].append(
                self._map_pain_point_to_ai_solution(pain_point)
            )
        return ai_recommendations
    def generate_business_case(self, url):
        """Generate complete business case"""
        # Analyze website
        website_data = self.analyze_website(url)
        revenue_streams = self.identify_revenue_streams(website_data)
        business_model = self.analyze_business_model(website_data, revenue_streams)
        # Generate recommendations
        ipaas_recommendations = self.generate_ipaas_recommendations(business_model)
        ai_recommendations = self.generate_ai_recommendations(business_model)
        # Calculate potential benefits
        benefits = self._calculate_benefits(business_model, ipaas_recommendations, ai_recommendations)
        # Generate final business case
        business_case = {
            'company_overview': {
                'url': url,
                'revenue_streams': revenue_streams,
                'business_model': business_model
            },
            'digital_transformation_strategy': {
                'ipaas_solutions': ipaas_recommendations,
                'ai_solutions': ai_recommendations
            },
            'benefits_analysis': benefits,
            'implementation_timeline': self._generate_timeline(),
            'generated_date': datetime.now().strftime("%Y-%m-%d")
        }
        return self._format_business_case(business_case)
    def _identify_customer_segments(self, website_data):
        """Identify customer segments from website content"""
        # Basic implementation
        segments = []
        text = website_data['text_content'].lower()
        
        if 'business' in text or 'enterprise' in text:
            segments.append('Business')
        if 'consumer' in text or 'individual' in text:
            segments.append('Consumer')
        
        return segments or ['General']
    def _identify_key_processes(self, website_data):
        """Identify key business processes"""
        processes = []
        text = website_data['text_content'].lower()
        
        process_keywords = {
            'sales': ['sales', 'purchase', 'buy'],
            'marketing': ['marketing', 'advertis', 'promotion'],
            'support': ['support', 'help', 'service'],
            'operations': ['operations', 'logistics', 'delivery']
        }
        
        for process, keywords in process_keywords.items():
            if any(keyword in text for keyword in keywords):
                processes.append(process)
                
        return processes or ['General Operations']
    def _identify_pain_points(self, website_data):
        """Identify potential pain points"""
        return ['Process Automation Needed', 'Data Integration Required']
    def _map_process_to_integration(self, process):
        """Map business process to iPaaS integration solution"""
        integration_map = {
            'sales': 'CRM Integration',
            'marketing': 'Marketing Automation',
            'support': 'Help Desk Integration',
            'operations': 'ERP Integration'
        }
        return integration_map.get(process, 'General Integration')
    def _map_pain_point_to_ai_solution(self, pain_point):
        """Map pain point to AI solution"""
        return 'Process Automation Agent'
    def _calculate_benefits(self, business_model, ipaas_recs, ai_recs):
        """Calculate potential benefits and ROI"""
        return "Estimated 25% efficiency improvement through automation"
    def _generate_timeline(self):
        """Generate implementation timeline"""
        return "3-6 months implementation timeline"
    def _format_business_case(self, business_case):
        """Format business case for presentation"""
        return f"""
        Digital Transformation Business Case
        Company: {business_case['company_overview']['url']}
        Date: {business_case['generated_date']}
        1. Business Overview
        Revenue Streams: {', '.join(business_case['company_overview']['revenue_streams'])}
        Key Processes: {', '.join(business_case['company_overview']['business_model']['key_processes'])}
        2. Digital Transformation Strategy
        iPaaS Solutions:
        - Core Integrations: {', '.join(business_case['digital_transformation_strategy']['ipaas_solutions']['core_integrations'])}
        - Automation Opportunities: {', '.join(business_case['digital_transformation_strategy']['ipaas_solutions']['automation_opportunities'])}
        AI Solutions:
        - Operational Agents: {', '.join(business_case['digital_transformation_strategy']['ai_solutions']['operational_agents'])}
        - Analytical Agents: {', '.join(business_case['digital_transformation_strategy']['ai_solutions']['analytical_agents'])}
        3. Benefits Analysis
        {business_case['benefits_analysis']}
        4. Implementation Timeline
        {business_case['implementation_timeline']}
        """