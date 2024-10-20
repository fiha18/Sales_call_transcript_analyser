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
        system_message = summarizer_prompt.get_summarizer_system_message(word_limit=1300)
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
                completion_usage[i] = completion_response.usage
                utils.stop_print_period()
                print("")
                summary = completion_response.choices[0].message.content.replace("```", "")
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

input_file = "generated_transcripts/darwinbox_srijan_sales_call_transcript_20241019_190826.txt"
summary = generate_transcript_summary(input_file,summary_format="paragraph")
print(f"Summary of call transcript {input_file.split("/")[1]} is provided below :\n")
print(summary)
end_execution_time = time.time()
total_time = float(end_execution_time - start_execution_time)
print(f"Total time taken: {total_time:.4f} seconds")
