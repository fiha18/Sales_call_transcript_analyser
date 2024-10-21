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


def perform_user_query_on_call_transcript_generation():
    # To do: add transcript_folder, input_file_name and summary_format from input or runtime parameter
    transcript_folder = "generated_transcripts"
    summary_folder = "generated_summaries"
    summary_format = "bullet_points"
    command_line_args = sys.argv
    input_file_name = command_line_args[1]
    user_query = command_line_args[2]
    transcript_file_path = os.path.join(transcript_folder, input_file_name)
    if any(keyword in query_helper.extract_keywords(user_query) for keyword in utils.get_summary_related_words()):
        # User query is related to summary, attempt to use the summary file
        print("Reading attempt to Summary file, as query is closly related to summary")
        summary_file = input_file_name.replace(".txt", f"_{summary_format}_summary.txt")
        summary_file_path = os.path.join(summary_folder, summary_file)       
        if os.path.exists(summary_file_path):
            # Summary file exists, use it for querying
            with open(summary_file_path, "r") as f:
                print(f"Reading {os.path.basename(summary_file_path)}")
                querying_file = f.read()
        else:
            # Summary file doesn't exist, fallback to the full transcript
            print(f"Summary file {os.path.basename(summary_file_path)} does not exist, using transcript file instead.")
            if os.path.exists(transcript_file_path):
                with open(transcript_file_path, "r") as f:
                    print(f"Reading {os.path.basename(transcript_file_path)}")
                    querying_file = f.read()
            else:
                print(f"Transcript file {os.path.basename(transcript_file_path)} does not exist.")
                return None # To do : Add Exception cases here 
    else:
        # If no summary-related keywords, use the full transcript file directly
        if os.path.exists(transcript_file_path):
            print(f"Reading transcript file as no summary-related keywords were found.")
            with open(transcript_file_path, "r") as f:
                querying_file = f.read()
        else:
            print(f"Transcript file {os.path.basename(transcript_file_path)} does not exist.")
            return None
    response = query_transcript(querying_file,user_query)
    print(response)
    #To Do : Persist Chat into file 
        
perform_user_query_on_call_transcript_generation() 
# summary_format - paragraph format ,bullet points or concise
print(completion_usage)
end_execution_time = time.time()
total_time = float(end_execution_time - start_execution_time)
print(f"Total time taken: {total_time:.4f} seconds")