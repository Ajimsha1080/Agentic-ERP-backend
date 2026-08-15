"""
Base Agent Logic
Contains the core ReAct loop for the AI agents.
"""
import time

class BaseAgent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def execute_task(self, prompt: str) -> str:
        """
        Executes a task.
        In a production environment with an API key, this would invoke LangChain.
        For now, it's a robust Mock Engine.
        """
        print(f"[{self.name}] Agent booting up...")
        time.sleep(1) # Simulate LLM thinking
        
        print(f"[{self.name}] Analyzing prompt: '{prompt}'")
        time.sleep(1)
        
        if "invoice" in prompt.lower():
            print(f"[{self.name}] Calling tool: fetch_pending_invoices()")
            time.sleep(1)
            return "I have reviewed the pending invoices. 3 out of 4 meet the criteria and have been approved."
        
        elif "lead" in prompt.lower() or "marketing" in prompt.lower():
            print(f"[{self.name}] Calling tool: scrape_leads()")
            time.sleep(1)
            return "I've scraped 45 new leads and enriched them in the CRM."
            
        else:
            return f"As the {self.name}, I have successfully processed your request regarding '{prompt}'."
