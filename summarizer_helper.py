
from textblob import TextBlob
import time
import re
import utils

def split_text(text, word_limit=1500):
    """
    Splits a given text into chunks of a specific size.

    Parameters:
    text (str): The text to be split.
    word_limit (int): The maximum size of each chunk.

    Returns:
    list: The list of chunks.
    """
    words = text.split()
    num_parts = len(words) // word_limit + 1
    return [' '.join(words[i * word_limit: (i + 1) * word_limit]) for i in range(num_parts)]



def preprocess_text(text):
    """
    Preprocess the chunk of call transcript text
        1. removing timestamp and participant name from lines like ( 00:00:03 Sam(open.ai) )
        2. remove filler and stop words from each line like um, so, a, an, the
        3. replace contraction words to its original for in each line like won't to will not

    Parameters:
    text (str): The text to be split.

    Returns:
    list: The list of lines.
    """
    start_execution_time_preprocessing = time.time()
    lines = text.lower().split('\n')
    # removing timestamp and participant name from lines
    processed_lines = [line.split("): ")[-1]for line in lines]
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
        blob = TextBlob(line)
        return str(blob.correct())  
    
    processed_lines = [spell_check_and_correct(replace_contractions(remove_fillers_and_stop_words(line))) for line in processed_lines]
    end_execution_time_preprocessing = time.time()
    total_time = float(end_execution_time_preprocessing - start_execution_time_preprocessing)
    print(f"Total time taken for preprocessing: {total_time:.4f} seconds")
    return '\n'.join(processed_lines)