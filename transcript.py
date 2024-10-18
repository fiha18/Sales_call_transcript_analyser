import os
from datetime import datetime
from openai import OpenAI
import PyPDF2
import prompt

# Set your OpenAI API key
OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)
book = ""

filePath = "products/hypercheckout-juspay.pdf"
product_name = "hypercheckout-juspay"
with open(filePath,"rb") as file:
    reader = PyPDF2.PdfReader(file)
    total_pages = len(reader.pages)
    start_page = 1
    for page_number in range(start_page-1,total_pages):
        page = reader.pages[page_number]
        book += page.extract_text() + " "

#print(book)

sales_representive = "Rahul Kothari"
client_representive = "Kailash Nath"
system_message = prompt.system_message
prompt_message = prompt.generate_prompt(sales_representive,client_representive,book)

model = "gpt-4o"
temperature = 0.3
max_tokens = 500
messages=[
        {"role": "system", "content": system_message},
        {
            "role": "user",
            "content": prompt_message
        }
    ]


completion = client.chat.completions.create(
    model=model,
    messages = messages
)
response = completion
response_content = response.choices[0].message.content

print(response)
print(response.usage)

folder_path = "transcript"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

file_name = f"{product_name}_sales_call_transcript_{current_time}.txt"

file_path = os.path.join(folder_path, file_name)

with open(file_path, 'w') as file:
    file.write(response_content)

