import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from app.services.memory import memory_agent

class LeadEmailGenerator:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7 
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["name", "company", "job_title", "context"],
            template="""
            You are an expert AI sales outreach agent. Write a highly personalized, short, and engaging cold email for the following prospect.
            
            Prospect Details:
            - Name: {name}
            - Job Title: {job_title}
            - Company: {company}
            
            Background Context (Use this to personalize the email):
            {context}
            
            Requirements:
            - Keep it under 150 words.
            - Focus on how our AI services can help their specific company/role.
            - Do not sound like a generic AI. Sound like a friendly human professional.
            - End with a simple call to action (CTA).
            
            Subject Line: [Generate a catchy subject line]
            
            Email Body:
            """
        )

    def generate_email(self, lead_data: dict, lead_id: int):
        context = memory_agent.get_relevant_context(
            query=f"Find background info or pain points about {lead_data['company']} or {lead_data['name']}",
            lead_id=lead_id
        )
    
        formatted_prompt = self.prompt_template.format(
            name=lead_data.get("name", "there"),
            company=lead_data.get("company", "your company"),
            job_title=lead_data.get("job_title", "your role"),
            context=context
        )
        
        response = self.llm.invoke(formatted_prompt)
        return response.content

email_generator = LeadEmailGenerator()