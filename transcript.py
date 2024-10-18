import os
from datetime import datetime
from openai import OpenAI
import PyPDF2
import prompt
import product_details.juspay_product as jp

# Set your OpenAI API key
OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)
# book = ""

# product_file_path = "products/hypercheckout_juspay.pdf"
# product_name = "hypercheckout-juspay"
# with open(product_file_path,"rb") as file:
#     reader = PyPDF2.PdfReader(file)
#     total_pages = len(reader.pages)
#     start_page = 1
#     for page_number in range(start_page-1,total_pages):
#         page = reader.pages[page_number]
#         book += page.extract_text().replace('\n', ' ') + " "

# print(book)

sales_representative = "Rahul Kothari"
client_representative = "Kailash Nath"
product_company = "juspay"
product_domain = "payment"
customer_domain = "e-commerce"
call_duration = 5

# To do : add greeting with first name only
final_response_content = f"""
00:00:00 {sales_representative}: Hi {client_representative}, thanks for taking the time today. Let's discuss how we can improve your {product_domain} solutions.
00:00:05 {client_representative}: Sure, I’m excited to learn more about your offerings.
"""
# To do : change range end point to generic based on split part
for i in range(0,5):
    product_detail_list = jp.product_detail[2*i:2*i + 2]
    start_time = "00:"+str(i*call_duration)+":10"
    system_message = prompt.generate_system_message(call_duration)
    prompt_message = prompt.generate_call_transcript_prompt(sales_representative, client_representative,product_domain, customer_domain, product_detail_list, start_time, call_duration)
    if i==4:
        prompt_message = prompt_message + "Last Instruction - Conclude the transcript with next steps for a product demo and potential follow-up meetings."
    model = "gpt-4o-mini"
    max_tokens = 8000
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
    final_response_content += "\n" + response_content

print(final_response_content)


folder_path = "transcript"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

file_name = f"{product_company}_sales_call_transcript_{current_time}.txt"

file_path = os.path.join(folder_path, file_name)

with open(file_path, 'w') as file:
    file.write(final_response_content)

