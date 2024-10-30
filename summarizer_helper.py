import threading
import queue
from textblob import TextBlob
import time
import re
import utils

lock = threading.Lock()
start_execution_time_preprocessing_global = time.time()
# def split_text(text,line_limit=40):
#     """
#     Splits a given transcript into chunks on basis of line count.

#     Parameters:
#     text (str): The text to be split.
#     line_limit (int): The maximum lines of each chunk, default 40 lines  ~1200 words in each chunk.

#     Returns:
#     list: The list of chunks.
#     """
#     words = text.split("\n\n")
#     num_parts = len(words) // line_limit + 1
#     return [' '.join(words[i *line_limit : (i + 1) * line_limit]) for i in range(num_parts)]

def split_text(text, line_limit=20):
    """
    Splits a given transcript into chunks based on the specified number of lines per chunk.

    Parameters:
    text (str): The text to be split.
    line_limit (int): The maximum lines of each chunk; default is 40 lines.

    Returns:
    list: A list of lists, where each inner list contains lines of text as individual elements.
    """
    # Split text by individual lines
    lines = text.split("\n\n")
    chunks = []
    # Split lines into chunks of specified line limit
    for i in range(0, len(lines), line_limit):
        line_chunk = "\n".join(lines[i:i + line_limit])
        chunks.append(line_chunk)        
    #chunks = [lines[i:i + line_limit] for i in range(0, len(lines), line_limit)]
    # Join each chunk's lines back into a single text block with "\n" at line ends
    return chunks

def preprocess_text(chunks):
    #print(f"Chunks to be preprocessed of length {len(chunks)} and content : {chunks}")
    start_execution_time_preprocessing = time.time()
    result_list = preprocess_text_multi_thread(chunks)
    # result_list = [None] * len(chunks)
    # for index, chunk in enumerate(chunks):
    #     result_list[index] = preprocess_text_helper(chunk)
    end_execution_time_preprocessing = time.time()
    total_time = float(end_execution_time_preprocessing - start_execution_time_preprocessing)
    print(f"Total time taken for preprocessing: {total_time:.4f} seconds")
    return result_list

# def preprocess_text_multi_thread(chunks):
#     """
#     Preprocesses a list of text chunks using multi-threading to speed up processing.
    
#     Parameters:
#     chunks (list): List of text chunks to preprocess.

#     Returns:
#     list: List of preprocessed text chunks.
#     """
#     def preprocess_chunk(chunk, index, result_list):
#         """
#         Processes a single chunk of text and stores the result in the shared list at the correct index. 
        
#         Parameters:
#         chunk (str): The text chunk to preprocess.
#         index (int): The index of the chunk in the original list.
#         result_list (list): The list to store preprocessed chunks.
#         """
#         result_list[index] = preprocess_text_helper(chunk)
#         print(f"processed element with index : {index} with content : {result_list[index]}")
#         return

#     # Prepare a list to store the results, initialized with None
#     result_list = [None] * len(chunks)
#     threads = []
#     try :
#         # Start a new thread using Thread class object for each chunk
#         for index, chunk in enumerate(chunks):
#             print(f"Creating thread for chuck - {index} with chuck content : {chunk} ")
#             thread = threading.Thread(target=preprocess_chunk, args=(chunk, index, result_list))
#             print(f"Response of preprocessing  for chuck - {index} with chuck content : {thread} ")
#             threads.append(thread)
#             thread.start()
#         # Wait for all threads to complete
#         for thread in threads:
#             thread.join()
#     except Exception as e:
#         # Any error in multi-threading and fallback to sequential processing , high latency but availability
#         print(f"Error during multi-threaded processing: {str(e)}. Falling back to sequential processing.")
#         # Sequential processing as a fallback
#         for index, chunk in enumerate(chunks):
#             result_list[index] = preprocess_text_helper(chunk)
#     return result_list

def preprocess_text_multi_thread(chunks):
    """
    Preprocesses a list of text chunks using multi-threading and stores results in order using a queue.
    
    Parameters:
    chunks (list): List of text chunks to preprocess.

    Returns:
    list: List of preprocessed text chunks, ordered by the original chunk sequence.
    """
    
    # Queue to hold the (index, processed chunk) tuples
    processed_queue = queue.Queue()
    
    def preprocess_chunk(chunk, index, output_queue):
        """
        Processes a single chunk of text and stores the result as a tuple (index, processed_chunk)
        in a queue for ordered collection.
        
        Parameters:
        chunk (str): The text chunk to preprocess.
        index (int): The index of the chunk in the original list.
        output_queue (queue.Queue): The queue to store processed chunks as (index, processed_chunk) tuples.
        """
        try:
            # Process the chunk and add it to the queue
            processed_chunk = preprocess_text_helper(chunk)
            output_queue.put((index, processed_chunk))
            end_execution_time_preprocessing = time.time()
            total_time_internal = float(end_execution_time_preprocessing - start_execution_time_preprocessing_global)
            print(f"Processed chunk with index: {index} - content added to queue. TimeTaken global - {total_time_internal} with end time  - {end_execution_time_preprocessing} ")
        except Exception as e:
            # Handle exceptions during chunk processing
            output_queue.put((index, f"Error processing chunk {index}: {str(e)}"))
            print(f"Error processing chunk {index}: {str(e)}")

    threads = []
    
    # Start a new thread for each chunk
    for index, chunk in enumerate(chunks):
        thread = threading.Thread(target=preprocess_chunk, args=(chunk, index, processed_queue))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Collect results from the queue and order them in result_list
    result_list = [None] * len(chunks)
    while not processed_queue.empty():
        (index, processed_chunk) = processed_queue.get()
        print(f"Preprocessed queue tuple item 2 : {processed_chunk}")
        result_list[index] = processed_chunk
    
    return result_list

def preprocess_text_helper(text):
    """
    Preprocess the chunk of call transcript text
        1. removing timestamp and participant name from lines like ( 00:00:03 Sam(open.ai) )
        2. remove filler and stop words from each line like um, so, a, an, the
        3. replace contraction words to its original for in each line like won't to will not

    Parameters:
    text (str): The text to be split.

    Returns:
    lines (str): proccessed lines .
    """
    start_execution_time_preprocessing = time.time()
    lines = text.lower().split('\n')
    print(f"Log Provided chunk size after line split- {len(lines)}")
    # removing timestamp and participant name from lines
    processed_lines = [line.split("): ")[-1]for line in lines]
    try:
        #list of common stop words
        stop_words = utils.get_common_stop_words()
        # list of common filler words to be removed
        filler_words = utils.get_common_fillers()
        # list of common contration words to be replaced with original words
        contraction_words = utils.get_contration_words()
        
        """AI-Generated Code for creating regex for contraction_pattern"""
        contraction_pattern = re.compile(r'\b(' + '|'.join(re.escape(key) for key in contraction_words.keys()) + r')\b')
        filler_pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in filler_words) + r')\b', re.IGNORECASE)
        stop_word_pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in stop_words) + r')\b', re.IGNORECASE)

        # Function to remove filler and stop words from each line
        def remove_fillers_and_stop_words(line):
            line = stop_word_pattern.sub('', line).strip()
            line =filler_pattern.sub('', line).strip()
            return line
    
        # Function to replace contraction words to its original for in each line
        def replace_contractions(line):
            return contraction_pattern.sub(lambda match: contraction_words[match.group(0)], line)
        
        def spell_check_and_correct(line):
            try:
                blob = TextBlob(line)
                return str(blob.correct())
            except Exception as e:
                # Handle any exception in spell checking and return the original line if correction fails
                print(f"Spell-check error: {str(e)}, moving forward without spell checks")
                return line     
                    
        processed_lines = [spell_check_and_correct(replace_contractions(remove_fillers_and_stop_words(line))) for line in processed_lines]
        end_execution_time_preprocessing = time.time()
        total_time_internal = float(end_execution_time_preprocessing - start_execution_time_preprocessing)
        total_time_global = float(end_execution_time_preprocessing - start_execution_time_preprocessing_global)
        print(f"time taken internal function : {total_time_internal} seconds and total time taken within multithreading {total_time_global} seconds")
        return processed_lines
    except Exception as e:
        # Catch all preprocessing-related errors and moving forward gracefully with just timestamp and removal participant name
        print(f"Error in preprocessing: {str(e)}, moving forward without preprocessing.")
        return processed_lines

