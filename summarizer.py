from openai import OpenAI
from openai import RateLimitError
import os
import time
import utils
import prompts.summarizer_prompt as summarizer_prompt
import summarizer_helper

period_timer = None
start_execution_time = time.time()
# Initialize OpenAI API key
OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)
model = "gpt-4o-mini"
temperature = 0.7
max_tokens = 8000   

completion_usage = {}
def generate_transcript_summary(file_path,summary_format):
    """
    Creates a summary for a given file using the OpenAI GPT 4 API.

    Parameters:
    file_path (str): The path of the file.
    prompt (list): The prompt to use for the OpenAI API.

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
    total_chunks = len(chunks)
    for i,chunk in enumerate(chunks, start=1):
        system_message = summarizer_prompt.get_summarizer_system_message(word_limit=1500)
        prompt_message = summarizer_prompt.get_summarizer_user_prompt(chunk,summary_format,utils.get_major_context)
        retries = 0
        while retries < 5:
            try:
                print(f"Making summarization request {i}/{total_chunks} to OpenAI API for {os.path.basename(file_path)}", end="")
                utils.print_period()
                message = [
                    {"role" : "system", "content": system_message}
                ,   {"role" : "user", "content" : prompt_message}
                ]
                completion_response = client.chat.completions.create(
                    model=model,
                    messages = message,
                    temperature = temperature,
                    max_tokens = max_tokens 
                )
                utils.stop_print_period()
                print("")
                summary = completion_response.choices[0].message.content.replace("```", "")
                print(summary)
                summary_list.append(summary)
                break
            except RateLimitError:
                print("\nReceived rate limit error, waiting for 60 seconds before retrying...")
                utils.stop_print_period()
                time.sleep(60)
                retries += 1
            except Exception as e:
                print("\nQuitting due to unexpected error: {}".format(e))
                utils.stop_print_period()
                return None
        if retries >= 5:
            print("\nExceeded maximum number of retries. Giving up on current chunk.")
    print(summary_list)
    return "".join(summary_list)

def save_summary_file(file_path,summary):
    """
    This function saves a summary file to folder_path based on the provided final_response_content.

    Parameters:
        summary : The text content to be written to the transcript file.
        file_path (optional): The directory path where the transcript file will be saved.
    Returns:
        None
    """
    # Write the content to the transcript file
    with open(file_path, 'w') as file:
        file.write(summary)

def perform_call_transcript_summary_generation():
    # To do: add transcript_folder, input_file_name and summary_format from input or runtime parameter
    transcript_folder = "generated_transcripts"
    input_file_name = "darwinbox_srijan_sales_call_transcript_20241021_020017.txt"
    # either paragraph , bullet_points, concise
    summary_format = "bullet_points"
    transcript_file_path = os.path.join(transcript_folder, input_file_name)
    if not os.path.exists(transcript_file_path):
        print(f"file {os.path.basename(transcript_file_path)} does not exists.")
        return 
    # summary_format paragraph format, bullet points, concise
    summary = generate_transcript_summary(transcript_file_path,summary_format)
    # folder path to save summary 
    folder_path="generated_summaries"
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_name = input_file_name.replace(".txt",f"_{summary_format}_summary.txt")
    file_path = os.path.join(folder_path, file_name)
    if os.path.exists(file_name):
        print(f"Output file {os.path.basename(file_path)} already exists, skipping.")
        return 
    if summary is not None:
        try:
            save_summary_file(file_path,summary)
            print(f"Summary generated successfully and saved to folder: {folder_path}\nFilename: {file_name}")
        except PermissionError:
            print(f"No permission to write file: {file_path}")
        except FileExistsError:
            print(f"File already exists: {file_path}")
        except Exception as e:
            print(f"An error occurred while writing the file: {file_path}. Error: {e}")
    #print(summary)

perform_call_transcript_summary_generation() 
# summary_format - paragraph format ,bullet points or concise
#print(completion_usage)
end_execution_time = time.time()
total_time = float(end_execution_time - start_execution_time)
print(f"Total time taken: {total_time:.4f} seconds")
