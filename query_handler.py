import os
import sys
import time
import utils
import query_helper
from datetime import datetime
import prompts.query_prompt as query_prompt
import llm_strategy.openai as openai
period_timer = None
start_execution_time = time.time()

def query_chunks_with_openai(user_query,chunks):
    #total_chunks = len(chunks)
    chunk_response_list = []
    for i,chunk in enumerate(chunks,start=1):
        system_message = query_prompt.get_querying_system_message()
        prompt_message = query_prompt.get_querying_user_prompt(chunk,user_query)
        # Generic openai api function which accepts system message and user prompt
        chunk_response = openai.call_openai_api(system_message,prompt_message)
        chunk_response_list.append(chunk_response)
    return chunk_response_list

def merge_chunk_responses(user_query,chunk_response_list):
    system_message = query_prompt.get_merge_response_system_message(chunk_response_list)
    prompt_message = user_query
    final_response = openai.call_openai_api(system_message,prompt_message)
    return final_response

# Main function that handles the querying of the transcript chunks
def query_transcript(transcript, query):
    chunk_size = 10000  # Each chunk is approximately 10,000 characters (~2,500 tokens)
    
    # dividing transcript into chunks
    transcript_chunks = query_helper.chunk_transcript(transcript, chunk_size)
   
    # getting relevent chunks out of all chunks
    relevant_chunks = query_helper.find_relevant_chunks(query, transcript_chunks)
    
    # OpenAI API with relevant chunks
    if relevant_chunks:
        chunk_response_list = query_chunks_with_openai(query, relevant_chunks)
        response = merge_chunk_responses(query,chunk_response_list)
    else:
        return "No relevant information found in the transcript."
    
    return response

def save_chat_file(file_path,chat):
    """
    This function appends a chat to file_path based on the provided final_response_content.

    Parameters:
        chat (str) : The text content to be appended to the chat file.
        file_path (str): The directory path where the transcript file will be saved.
    Returns:
        None
    """
    # Write the content to the transcript file
    with open(file_path, 'a') as file:
        file.write(chat)


def perform_user_query_on_call_transcript_generation():
    # To do: add transcript_folder, input_file_name and summary_format from input or runtime parameter
    transcript_folder = "generated_transcripts"
    summary_folder = "generated_summaries"
    summary_format = "bullet_points"
    # to be used in persisting chat
    user_query_time = datetime.now().strftime("%Y:%m:%d-%H:%M:%S")
    command_line_args = sys.argv
    input_file_name = command_line_args[1]
    user_query = command_line_args[2]
    transcript_file_path = os.path.join(transcript_folder, input_file_name)
    if any(keyword in query_helper.extract_keywords(user_query) for keyword in utils.get_summary_related_words()):
        # User query is related to summary, attempt to use the summary file
        print("Reading attempt to Summary file, as query is closly related to summary")
        summary_file = input_file_name.replace(".txt", f"_{summary_format}_summary_list.txt")
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
    response = response.replace("**","")
    # Response takes sometime
    chat_response_time = datetime.now().strftime("%Y:%m:%d-%H:%M:%S")
    print(response)
    folder_path="query_responses"
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_name = input_file_name.replace(".txt",f"_query_responses.txt")
    file_path = os.path.join(folder_path, file_name)
    if os.path.exists(file_name):
        print(f"Output file {os.path.basename(file_path)} already exists, skipping.")
        return
    if response is not None:
        try:
            save_chat_file(file_path,f"\n\n{user_query_time} User Query: {user_query}\n\n{chat_response_time} App Response: \n{response}")
            print(f"Query Response generated successfully and saved to folder: {folder_path}\nFilename: {file_name}")
        except PermissionError:
            print(f"No permission to write file: {file_path}, moving forward.")
        except FileExistsError:
            print(f"File already exists: {file_path}, moving forward.")
        except Exception as e:
            print(f"An error occurred while writing the file: {file_path}. Error: {e}, moving forward.")
        
perform_user_query_on_call_transcript_generation() 
end_execution_time = time.time()
total_time = float(end_execution_time - start_execution_time)
print(f"Total time taken: {total_time:.4f} seconds")