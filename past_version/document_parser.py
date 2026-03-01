import json  ## importing json library 


with open("sample_file.txt", "r", encoding = "utf-8") as file:  # opening file and storing in text variable
    text = file.read()


text_lower = text.lower()   # converts into lower
text_length = len(text)     # finds out the length of the imported text file

project_type = "unknown"            # stores the type of the project
if "residential" in text_lower:
    project_type  = "residential"
elif "commercial" in text_lower:
    project_type = "commercial"

area_mention = []                   # Defining an array
words = text_lower.split()          # creating an full array every word in text file


for i,word in enumerate(words):
    if "sqft" in word  or "sqm" in word:
        area_mention.append(words[i - 1] + " " + word )

budget_mentions = []
for i,word in enumerate(words):
    if "usd" in word or "million" in word:
        budget_mentions.append(words[i-1] + " " + word)


output_data = {
    "project_type" : project_type,
    "budget_mentions" : budget_mentions,
    "area+_mentions" : area_mention,
    "raw_text_length" : text_length
}

with open("output.json","w",encoding = "utf-8") as json_file:
    json.dump(output_data , json_file,indent = 4)


print("Analysis complete, Output written to output.json")