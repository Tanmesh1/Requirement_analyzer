from app.services.ai_agent import LLMRequirementRefiner

raw_text = """
Client wants a residential building.
- 3 bedrooms
- 2 bedrooms
- open kitchen 
Modern design.
Fast delivery required.
"""

refiner = LLMRequirementRefiner()

result = refiner.refine(raw_text)

print("=====clean output======")
print(result)