from app.services.requirement_extractor import extract_requirements

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