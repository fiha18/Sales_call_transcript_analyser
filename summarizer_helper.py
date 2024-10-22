import threading
from textblob import TextBlob
import time
import re
import utils

lock = threading.Lock()

def split_text(text,line_limit=40):
    """
    Splits a given transcript into chunks on basis of line count.

    Parameters:
    text (str): The text to be split.
    line_limit (int): The maximum lines of each chunk, default 40 lines  ~1200 words in each chunk.

    Returns:
    list: The list of chunks.
    """
    words = text.split("\n\n")
    num_parts = len(words) // line_limit + 1
    return [' '.join(words[i *line_limit : (i + 1) * line_limit]) for i in range(num_parts)]

def preprocess_text(chunks):
    print(f"Chunks to be preprocessed of length {len(chunks)} and content : {chunks}")
    start_execution_time_preprocessing = time.time()
    processed_lines = preprocess_text_multi_thread(chunks)
    end_execution_time_preprocessing = time.time()
    total_time = float(end_execution_time_preprocessing - start_execution_time_preprocessing)
    print(f"Total time taken for preprocessing: {total_time:.4f} seconds")
    return processed_lines

def preprocess_text_multi_thread(chunks):
    """
    Preprocesses a list of text chunks using multi-threading to speed up processing.
    
    Parameters:
    chunks (list): List of text chunks to preprocess.

    Returns:
    list: List of preprocessed text chunks.
    """
    def preprocess_chunk(chunk, index, result_list):
        """
        Processes a single chunk of text and stores the result in the shared list at the correct index. 
        
        Parameters:
        chunk (str): The text chunk to preprocess.
        index (int): The index of the chunk in the original list.
        result_list (list): The list to store preprocessed chunks.
        """
        result_list[index] = preprocess_text_helper(chunk)
        print(f"processed element with index : {index} with content : {result_list[index]}")
        return

    # Prepare a list to store the results, initialized with None
    result_list = [None] * len(chunks)
    threads = []
    try :
        # Start a new thread using Thread class object for each chunk
        for index, chunk in enumerate(chunks):
            print(f"Creating thread for chuck - {index} with chuck content : {chunk} ")
            thread = threading.Thread(target=preprocess_chunk, args=(chunk, index, result_list))
            print(f"Response of preprocessing  for chuck - {index} with chuck content : {thread} ")
            threads.append(thread)
            thread.start()
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
    except Exception as e:
        # Any error in multi-threading and fallback to sequential processing , high latency but availability
        print(f"Error during multi-threaded processing: {str(e)}. Falling back to sequential processing.")
        # Sequential processing as a fallback
        for index, chunk in enumerate(chunks):
            result_list[index] = preprocess_text_helper(chunk)
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
    lines = text.lower().split('\n')
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
        print(processed_lines)
        return processed_lines
    except Exception as e:
        # Catch all preprocessing-related errors and moving forward gracefully with just timestamp and removal participant name
        print(f"Error in preprocessing: {str(e)}, moving forward without preprocessing.")
        return processed_lines

