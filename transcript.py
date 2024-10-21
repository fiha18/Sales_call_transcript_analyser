import os
from datetime import datetime
# from openai import OpenAI
# from openai import RateLimitError
import time
import prompts.transcript_generator_prompt as transcript_generator_prompt
import utils as utils
import importlib
import llm_strategy.openai as openai

start_execution_time = time.time()
# OPENAI_API_KEY = "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"
# client = OpenAI(api_key=OPENAI_API_KEY)

completion_usage = {}
def generate_fake_call_transcript(product_owner,model = "gpt-4o-mini",max_tokens=6000,temperature=0.7,call_duration = 30,chunk_duration=5):
    """
    Function to generate a fake call transcript between a product owner and a client.

    Parameters:
    1. product_owner (str): product owner participating in the call.
    2. model (str, optional): AI language model to be used for generating the transcript.
    3. max_tokens (int, optional): Maximum number of tokens allowed for the transcript generation. Default is 6000.
    4. temperature (float, optional): Sampling temperature to control randomness in the generated output. Ranges between 0 and 1. Default is 0.7.
    5. call_duration (int, optional): Total duration of the simulated call in minutes. Default is 30 minutes.
    6. chunk_duration (int, optional): Duration of each segment or chunk within the call in minutes. Default is 5 minutes.

    Returns:
    - transcript (str): A string representing the generated fake call transcript, broken down into smaller chunks based on the chunk_duration.
    
    """
    #dynamically import a module
    module = f"product_details.{product_owner}_product"
    product_owner = importlib.import_module(module)
    part_duration = chunk_duration
    total_iteration = int(call_duration / part_duration)
    # product list is assumed to be of length so to distribute 1 - 10 in 6 pair such that call transcripts do not have repeating discussion
    distribution = [[0,2],[2,3],[3,5],[5,7],[7,8],[8,10]]
    # storing previous chunk context
    previous_end_lines = f"""00:00:00 {product_owner.sales_representative}: Hi {product_owner.client_representative.split(" ")[0]}, thanks for taking the time today. Let's discuss how we can improve your {product_owner.product_domain} solutions."""
    previous_end_lines += f"""\n\n00:00:05 {product_owner.client_representative}: Hi {product_owner.sales_representative.split(" ")[0]}, sure I’m excited to learn more about your offerings."""
    previous_end_time = "00:00:05"
    final_response_content = previous_end_lines.strip()
    # start time of ith transcript chunk should be  >= end time of (i-1)th transcript chunk
    contraction_word_list = list(utils.get_contration_words().keys())
    for i in range(0,total_iteration):
        product_detail_list = product_owner.product_details[distribution[i][0]:distribution[i][1]]
        print(f"Starting time of {i+1}/{total_iteration} transacript chunk : {previous_end_time}")
        start_time = utils.add_time(previous_end_time,0.1)
        system_message = transcript_generator_prompt.generate_call_transcript_system_message(part_duration)
        prompt_message = transcript_generator_prompt.generate_call_transcript_prompt(product_owner.sales_representative, product_owner.client_representative,product_owner.product_domain, product_owner.customer_domain, product_detail_list, start_time,part_duration,previous_end_lines,utils.get_common_fillers,contraction_word_list,utils.get_major_context)
        # In the last chunk conclusion will be added
        if i==(total_iteration-1):
            prompt_message = prompt_message + "Last Instruction - Conclude the transcript with next steps for a product demo and potential follow-up meetings."
        # Generic openai api function which accepts system message and user prompt
        response_content = openai.call_openai_api(system_message,prompt_message)
        response_lines = response_content.splitlines()
        previous_end_lines = response_lines[-3:]
        previous_end_time = response_lines[-1].split(" ")[0]
        previous_end_time = previous_end_time.replace("[", "").replace("]", "")
        if response_lines[-1]:  
            # Check if the last line is not empty
            previous_end_time = response_lines[-1].split(" ")[0]
            # Strip out any unwanted characters
            previous_end_time = previous_end_time.replace("[", "").replace("]", "")
        else:
            previous_end_time = None  # Handle empty line case
        final_response_content += "\n\n" + response_content.strip()
    return final_response_content

def save_transcript_file(file_path,final_response_content):
    """
    This function saves a transcript file to folder_path based on the provided final_response_content.

    Parameters:
        final_response_content: The text content to be written to the transcript file.
        file_path (optional): The directory path where the transcript file will be saved.
    Returns:
        None
    """
    # Write the content to the transcript file
    with open(file_path, 'w') as file:
        file.write(final_response_content)


def perform_call_transcript_generation():
    predefined_product_list = ["juspay","darwinbox","shopify","sap-erp"]
    print(f"Enter the product owner in this list {predefined_product_list} else add product details in product_details folder following same format as others")
    product_owner = input("Enter product owner : ")
    if product_owner not in predefined_product_list:
        print("Product details not added as of now , add it in product_details folder following same format as others")
        return
    #dynamically import a module
    module = f"product_details.{product_owner}_product"
    product = importlib.import_module(module)
    fake_transcript = generate_fake_call_transcript(product_owner)
    # folder path to save transcripts 
    folder_path="generated_transcripts"
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # Generate the current timestamp
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Construct the filename
    file_name = f"{product.product_company.split('.')[0]}_{product.sales_representative.split(' ')[0].lower()}_sales_call_transcript_{current_time}.txt"
    # Combine folder path and filename
    file_path = os.path.join(folder_path, file_name)
    if os.path.exists(file_name):
        print(f"Output file {os.path.basename(file_path)} already exists, skipping.")
        return 
    if fake_transcript is not None:
        try:
            save_transcript_file(file_path,fake_transcript)
            print(f"Transcript generated successfully and saved to folder: {folder_path}\nFilename: {file_name}")
        except PermissionError:
            print(f"No permission to write file: {file_path}")
        except FileExistsError:
            print(f"File already exists: {file_path}")
        except Exception as e:
            print(f"An error occurred while writing the file: {file_path}. Error: {e}")
    #print(completion_usage)

perform_call_transcript_generation()
## Total execution time
end_execution_time = time.time()
total_time = float(end_execution_time - start_execution_time)
print(f"Total time taken: {total_time:.4f} seconds")
