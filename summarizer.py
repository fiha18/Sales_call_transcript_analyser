# from openai import OpenAI
# from openai import RateLimitError
import os
import sys
import time
import utils
import prompts.summarizer_prompt as summarizer_prompt
import summarizer_helper
import llm_strategy.openai as openai

period_timer = None
start_execution_time = time.time()

def merge_chunk_summaries(chunk_response_list,summary_format="paragraph",word_limit = 1000):
    system_message = summarizer_prompt.get_merge_response_system_message(chunk_response_list,summary_format,word_limit)
    prompt_message = "Generate a cohesive, well-structured summary of call transcript"
    final_response = openai.call_openai_api(system_message,prompt_message)
    return final_response

def generate_transcript_summary_list(file_path,summary_format="paragraph"):
    """
    Creates a summary for a given file using the OpenAI GPT 4 API.

    Parameters:
    file_path (str): The path of the file.
    summary_format (str) : summary format should be paragraph, bullet_point or concise.

    Returns:
    str: The summary.
    """
    with open(file_path, "r") as f:
        print(f"Reading {os.path.basename(file_path)}")
        transcript = f.read()

    # Preprocess the transcript
    transcript = summarizer_helper.preprocess_text(transcript)
    chunks = summarizer_helper.split_text(transcript)
    summary_list = []
    for chunk in enumerate(chunks, start=1):
        system_message = summarizer_prompt.get_summarizer_system_message()
        prompt_message = summarizer_prompt.get_summarizer_user_prompt(chunk,utils.get_major_context,summary_list)
        # Generic openai api function which accepts system message and user prompt
        summary = openai.call_openai_api(system_message,prompt_message)
        summary_list.append(summary)
    return summary_list

def save_summary_file(file_path,summary):
    """
    This function saves a summary file to folder_path based on the provided final_response_content.

    Parameters:
        summary (str) : The text content to be written to the transcript file.
        file_path (str): The directory path where the transcript file will be saved.
    Returns:
        None
    """
    # Write the content to the transcript file
    with open(file_path, 'w') as file:
        file.write(summary)

def perform_call_transcript_summary_generation():
    # To do: add transcript_folder, input_file_name and summary_format from input or runtime parameter
    transcript_folder = "generated_transcripts"
    command_line_args = sys.argv
    input_file_name = command_line_args[1]
    if not input_file_name:
        print(f"Input file {input_file_name} does not exists, skipping.")
        return 
    # either paragraph , bullet_points, concise
    summary_format = command_line_args[2] if len(command_line_args) > 2  else None
    word_limit = command_line_args[3] if len(command_line_args) > 3 else None
    transcript_file_path = os.path.join(transcript_folder, input_file_name)
    if not os.path.exists(transcript_file_path):
        print(f"file {os.path.basename(transcript_file_path)} does not exists.")
        return 
    # summary_format paragraph, bullet points, concise
    summary_list = generate_transcript_summary_list(transcript_file_path,summary_format)
    # folder path to save summary 
    folder_path="generated_summaries"
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_name = input_file_name.replace(".txt",f"_{summary_format}_summary_list.txt")
    file_path = os.path.join(folder_path, file_name)
    if os.path.exists(file_name):
        print(f"Output file {os.path.basename(file_path)} already exists, skipping.")
        return
    # Creating final response 
    summary = merge_chunk_summaries(summary_list,summary_format,word_limit)  
    if summary_list is not None:
        try:
            # Saving only summary list as str , this can optimise query_handler
            save_summary_file(file_path,"".join(summary_list))
            print(f"Summary generated successfully and saved to folder: {folder_path}\nFilename: {file_name}")
        except PermissionError:
            print(f"No permission to write file: {file_path}")
        except FileExistsError:
            print(f"File already exists: {file_path}")
        except Exception as e:
            print(f"An error occurred while writing the file: {file_path}. Error: {e}")
    print(summary)

perform_call_transcript_summary_generation() 
# summary_format - paragraph format ,bullet points or concise
#print(completion_usage)
end_execution_time = time.time()
total_time = float(end_execution_time - start_execution_time)
print(f"Total time taken: {total_time:.4f} seconds")
