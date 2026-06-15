"""AI Quotation Service"""
import os
import json
import time
from datetime import datetime
from database import db
from database.models import Quotation, QuotationItem, AIQuotationLog, Material, Customer
import openai

class AIQuotationService:
    """Service for generating quotations using AI"""
    
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    def generate_quotation(self, customer_id, requirements, use_model='gpt-3.5-turbo'):
        """
        Generate a quotation using AI based on customer requirements
        
        Args:
            customer_id: ID of the customer
            requirements: Dict with 'project_type', 'area', 'finish', 'budget', 'description'
            use_model: AI model to use (gpt-3.5-turbo or gpt-4)
        
        Returns:
            quotation_id: ID of created quotation
        """
        try:
            customer = Customer.query.get(customer_id)
            if not customer:
                raise ValueError(f"Customer {customer_id} not found")
            
            # Build prompt for AI
            prompt = self._build_quotation_prompt(customer, requirements)
            
            # Call OpenAI API
            start_time = time.time()
            response = openai.ChatCompletion.create(
                model=use_model,
                messages=[
                    {"role": "system", "content": "You are an expert marble and porcelain quotation specialist. Generate detailed and accurate quotations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            processing_time = time.time() - start_time
            
            # Parse AI response
            ai_response = response.choices[0].message.content
            quotation_data = self._parse_ai_response(ai_response)
            
            # Create quotation
            quotation = self._create_quotation_from_ai(
                customer_id, 
                quotation_data, 
                requirements
            )
            
            # Log AI interaction
            self._log_ai_quotation(
                quotation.id,
                use_model,
                prompt,
                ai_response,
                processing_time,
                response.usage.total_tokens
            )
            
            return quotation.id
        
        except Exception as e:
            raise Exception(f"Error generating quotation: {str(e)}")
    
    def suggest_materials(self, quotation_id, customer_preferences=None, use_model='gpt-3.5-turbo'):
        """
        Suggest materials for a quotation
        
        Args:
            quotation_id: ID of the quotation
            customer_preferences: Dict with preferences
            use_model: AI model to use
        
        Returns:
            List of suggested materials with reasons
        """
        try:
            quotation = Quotation.query.get(quotation_id)
            if not quotation:
                raise ValueError(f"Quotation {quotation_id} not found")
            
            # Build prompt
            prompt = self._build_material_suggestion_prompt(
                quotation, 
                customer_preferences
            )
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=use_model,
                messages=[
                    {"role": "system", "content": "You are an expert in marble and porcelain selection. Suggest the best materials for the project."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            # Parse suggestions
            suggestions = self._parse_material_suggestions(response.choices[0].message.content)
            
            return suggestions
        
        except Exception as e:
            raise Exception(f"Error generating suggestions: {str(e)}")
    
    def estimate_project_cost(self, area_sqft, material_type, finish, labor_rate=None):
        """
        Estimate project cost using AI
        
        Args:
            area_sqft: Area in square feet
            material_type: 'marble' or 'porcelain'
            finish: 'polished', 'honed', 'brushed', etc.
            labor_rate: Optional labor rate per sqft
        
        Returns:
            Dict with cost breakdown
        """
        try:
            prompt = f"""
            Estimate the cost for a marble/porcelain project:
            - Area: {area_sqft} square feet
            - Material Type: {material_type}
            - Finish: {finish}
            - Labor Rate: {labor_rate} per sqft (if provided)
            
            Provide a detailed cost breakdown including:
            1. Material cost
            2. Labor cost
            3. Installation cost
            4. Finishing cost
            5. Total estimated cost
            
            Format as JSON.
            """
            
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {"role": "system", "content": "You are a cost estimation expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1000
            )
            
            # Parse JSON response
            response_text = response.choices[0].message.content
            # Extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            json_str = response_text[start_idx:end_idx]
            cost_breakdown = json.loads(json_str)
            
            return cost_breakdown
        
        except Exception as e:
            raise Exception(f"Error estimating cost: {str(e)}")
    
    # Private helper methods
    
    def _build_quotation_prompt(self, customer, requirements):
        """Build prompt for quotation generation"""
        return f"""
        Generate a detailed quotation for the following:
        
        Customer: {customer.name}
        Company: {customer.company}
        Location: {customer.city}, {customer.state}
        
        Project Requirements:
        - Type: {requirements.get('project_type')}
        - Area: {requirements.get('area')} square feet
        - Preferred Finish: {requirements.get('finish')}
        - Budget: ${requirements.get('budget')}
        - Description: {requirements.get('description')}
        
        Please suggest suitable marble or porcelain materials from our inventory,
        calculate quantities needed, and provide pricing.
        
        Format the response as:
        1. Project Overview
        2. Recommended Materials (with reasons)
        3. Quantity Calculations
        4. Cost Breakdown
        5. Timeline
        6. Special Notes
        """
    
    def _build_material_suggestion_prompt(self, quotation, preferences):
        """Build prompt for material suggestions"""
        prefs = preferences or {}
        return f"""
        Suggest the best marble or porcelain materials for this project:
        
        Project: {quotation.title}
        Description: {quotation.description}
        Customer: {quotation.customer.name}
        Budget: Variable
        
        Preferences:
        - Color Preference: {prefs.get('color_preference')}
        - Finish Preference: {prefs.get('finish_preference')}
        - Durability Priority: {prefs.get('durability_priority')}
        - Aesthetic Priority: {prefs.get('aesthetic_priority')}
        
        Please suggest 3-5 materials with:
        1. Material name and type
        2. Specific advantages for this project
        3. Estimated cost per sqft
        4. Durability rating
        5. Maintenance requirements
        """
    
    def _parse_ai_response(self, response):
        """Parse AI response and extract quotation data"""
        # This is a simplified parser - in production, use JSON response format
        return {
            'materials': [],
            'total': 0,
            'notes': response
        }
    
    def _parse_material_suggestions(self, response):
        """Parse material suggestions from AI response"""
        return {
            'suggestions': response,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _create_quotation_from_ai(self, customer_id, quotation_data, requirements):
        """Create quotation record from AI data"""
        # Generate quotation number
        last_quotation = Quotation.query.order_by(Quotation.id.desc()).first()
        quotation_number = f"QT-AI-{datetime.now().strftime('%Y%m%d')}-{(last_quotation.id if last_quotation else 0) + 1:04d}"
        
        quotation = Quotation(
            quotation_number=quotation_number,
            customer_id=customer_id,
            title=requirements.get('project_type'),
            description=requirements.get('description'),
            ai_generated=True,
            status='draft'
        )
        
        db.session.add(quotation)
        db.session.commit()
        
        return quotation
    
    def _log_ai_quotation(self, quotation_id, model, prompt, response, processing_time, tokens_used):
        """Log AI quotation generation"""
        log = AIQuotationLog(
            quotation_id=quotation_id,
            ai_model=model,
            prompt=prompt,
            response=response,
            processing_time=processing_time,
            tokens_used=tokens_used
        )
        db.session.add(log)
        db.session.commit()
