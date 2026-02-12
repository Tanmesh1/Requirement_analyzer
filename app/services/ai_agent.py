from app.services.requirement_extractor import extract_requirements
import requests
from typing import Dict

LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL_NAME = "mistralai/mistral-small-3.2"


class LLMRequirementRefiner:
    def __init__(self):
        self.url = LM_STUDIO_URL
        self.model = MODEL_NAME


    def refine(self, raw_text: str) -> str:
        """
        Send messy requirements to local LLMs and return clean professional text.
        """

        system_prompt = (
             "You are a senior architectural consultant.\n\n"
            "You will receive messy client requirements.\n"
            "Your task:\n"
            "1. Rewrite them professionally\n"
            "2. Organize into sections:\n"
            "   - Project Overview\n"
            "   - Functional Requirements\n"
            "   - Design Preferences\n"
            "   - Timeline Expectations\n"
            "   - Missing Clarifications\n"
            "3. Do NOT hallucinate information\n"
            "4. Be concise, clear, and professional\n"
        )

        payload = {
             "model": self.model,
            "messages" : [
                {"role": "system", "content": system_prompt},
                {"role": "user" , "content": raw_text},
            ],
            "temperature": 0.2,
        }

        response = requests.post(self.url, json=payload, timeout = 120)
        # response.raise_for_status()
        print("STATUS:", response.status_code)
        print("RAW RESPONSE:", response.text)

        data = response.json()

        return data["choices"][0]["message"]["content"].strip()

class DocumentAI:
    def __init__(self):
        pass

    def analyze_document(self,full_text: str) -> dict:
        """
        Main intelligence entry point.
        Can later call LLM, embedding, hybrid pipelines etc.
        """

        if not full_text or not full_text.strip():
            raise ValueError("Empty document text")
        
        structured = extract_requirements(full_text)

        return structured



def analyze_requirements_with_ai(text: str) -> dict:
    """
        Mock AI reasoning function.
        This simulates what an LLM would do.
    """

    missing_info = []
    conflicts = []

    text_lower = text.lower()

    if "budget" not in text_lower:
        missing_info.append("Budget not clearly specified")
    
    if "floor" not in text_lower:
        missing_info.append("Number of floors not specified")
    
    if "regulation" not in text_lower and "bylaw" not in text_lower:
        missing_info.append("Local regulation not mentioned")
    if "budget" in text_lower and "luxury" in text_lower:
        conflicts.append("Luxury expectations may conflict with stated budget")

    return {
        "ai_summery" : "This is a preliminary requirement analysis.",
        "missing_information": missing_info,
        "potential_conflicts": conflicts,
        "design_readiness_score" : 70 - (len(missing_info) * 10)
    }