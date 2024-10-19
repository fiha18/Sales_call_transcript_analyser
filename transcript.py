import os
from datetime import datetime
from openai import OpenAI
import time
import prompt
import utils as utils
import product_details.juspay_product as juspay
import product_details.darwinbox_product as darwin

start_execution_time = time.time()
OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)

#TO DO : Time boudation , add it in script

product_owner = juspay
call_duration = 30
# 5 minute call transcript most realistic
part_duration = 5
total_iteration = int(call_duration / part_duration)
# product list is assumed to be of length so to distribute 1 - 10 in 6 pair such that call transcripts do not have repeating discussion
distribution = [[0,2],[2,3],[3,5],[5,7],[7,8],[8,10]]

final_response_content = f"""
00:00:00 {product_owner.sales_representative}: Hi {product_owner.client_representative.split(" ")[0]}, thanks for taking the time today. Let's discuss how we can improve your {product_owner.product_domain} solutions.

00:00:05 {product_owner.client_representative}: Hi {product_owner.sales_representative.split(" ")[0]}, sure I’m excited to learn more about your offerings.
"""
previous_end_time = "00:00:05"
for i in range(0,total_iteration):
    product_detail_list = product_owner.product_details[distribution[i][0]:distribution[i][1]]
    start_time = utils.add_time(previous_end_time,0.1)
    print(" Start Time of "+str(i+1)+ " part of transcript"+ start_time)
    # To Do: start time of ith transcript should be  >= end time of (i-1)th transcript
    system_message = prompt.generate_call_transcript_system_message(part_duration)
    prompt_message = prompt.generate_call_transcript_prompt(product_owner.sales_representative, product_owner.client_representative,product_owner.product_domain, product_owner.customer_domain, product_detail_list, start_time, part_duration)
    if i==(total_iteration-1):
        prompt_message = prompt_message + "Last Instruction - Conclude the transcript with next steps for a product demo and potential follow-up meetings."

    model = "gpt-4o-mini"
    messages=[
            {"role": "system", "content": system_message},
            {
                "role": "user",
                "content": prompt_message
            }
        ]
    completion = client.chat.completions.create(
        model=model,
        messages = messages,
        temperature = 0.7,
        max_tokens = 6000       
    )
    response = completion
    response_content = response.choices[0].message.content
    previous_end_time = response_content.splitlines()[-1].split(" ")[0]
    final_response_content += "\n" + response_content.strip()

print(final_response_content)


# Transcript File creation 
folder_path = "transcript"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

file_name = f"{product_owner.product_company}_sales_call_transcript_{current_time}.txt"

file_path = os.path.join(folder_path, file_name)

with open(file_path, 'w') as file:
    file.write(final_response_content)



end_execution_time = time.time()
total_time = float(end_execution_time - start_execution_time)
print(f"Total time taken: {total_time:.4f} seconds")
