from openai import OpenAI
from openai import RateLimitError
import os
import sys
import time
import utils
import query_helper
import prompts.query_prompt as query_prompt

period_timer = None
start_execution_time = time.time()
# Initialize OpenAI API key
OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)
model = "gpt-4o-mini"
temperature = 0.7
max_tokens = 8000 
completion_usage = {}

def query_chunks_with_openai(user_query,chunks):
    total_chunks = len(chunks)
    final_response = []
    for i,chunk in enumerate(chunks,start=1):
        system_message = query_prompt.get_querying_system_message()
        prompt_message = query_prompt.get_querying_user_prompt(chunk,user_query)
        retries = 0
        while retries < 5:
            try:
                print(f"Making query request {i}/{total_chunks} to OpenAI API for call transcript", end="")
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
                response = completion_response.choices[0].message.content.replace("```", "")
                final_response.append(response)
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
    return "".join(final_response)

# Main function that handles the querying of the transcript chunks
def query_transcript(transcript, query):
    chunk_size = 10000  # Each chunk is approximately 10,000 characters (~2,500 tokens)
    
    # dividing transcript into chunks
    transcript_chunks = query_helper.chunk_transcript(transcript, chunk_size)
    # getting relevent chunks out of all chunks
    relevant_chunks = query_helper.find_relevant_chunks(query, transcript_chunks)
    
    # OpenAI API with relevant chunks
    if relevant_chunks:
        responses = query_chunks_with_openai(query, relevant_chunks)
    else:
        return "No relevant information found in the transcript."
    
    return responses


def perform_call_transcript_summary_generation():
    # To do: add transcript_folder, input_file_name and summary_format from input or runtime parameter
    transcript_folder = "generated_transcripts"
    command_line_args = sys.argv
    input_file_name = command_line_args[1]
    user_query = command_line_args[2]
    transcript_file_path = os.path.join(transcript_folder, input_file_name)
    if not os.path.exists(transcript_file_path):
        print(f"file {os.path.basename(transcript_file_path)} does not exists.")
        return 
    with open(transcript_file_path, "r") as f:
        print(f"Reading {os.path.basename(transcript_file_path)}")
        transcript = f.read()
    response = query_transcript(transcript,user_query)
    print(response)
    #To Do : Persist Chat into file 
        
perform_call_transcript_summary_generation() 
# summary_format - paragraph format ,bullet points or concise
print(completion_usage)
end_execution_time = time.time()
total_time = float(end_execution_time - start_execution_time)
print(f"Total time taken: {total_time:.4f} seconds")