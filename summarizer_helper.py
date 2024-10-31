
import time
import re
import utils

# Initialize the spell checker once
def split_text(text, word_limit=2000):
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
    processed_lines = preprocess_text_helper(text)
    return '\n'.join(processed_lines)

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
    if (not lines[0].split(" ")[0] == "00:00:00"): # If text is summary just splitting based on new line
        end_execution_time_preprocessing = time.time()
        total_time = float(end_execution_time_preprocessing - start_execution_time_preprocessing)
        print(f"Skipping deep preprocessing for summary...")
        print(f"Total time taken for preprocessing: {total_time:.4f} seconds")
        return lines
    # removing timestamp and participant name from lines
    print(f"Total number of words before preprocessing : {len(text)}")
    processed_lines = [line.split("): ")[-1]for line in lines]
    try:
        # Load stop words, filler words, and contraction mappings from utility functions
        stop_words = set(utils.get_common_stop_words())
        filler_words = set(utils.get_common_fillers())
        contraction_words = utils.get_contration_words()

        # Compile regex patterns outside loops for better performance
        contraction_pattern = re.compile(r'\b(' + '|'.join(re.escape(key) for key in contraction_words.keys()) + r')\b')
        filler_stop_pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in filler_words.union(stop_words)) + r')\b', re.IGNORECASE)

        def replace_contractions(line):
            """Replace contractions with their expanded form"""
            return contraction_pattern.sub(lambda match: contraction_words[match.group(0)], line)

        def remove_fillers_and_stop_words(line):
            """Remove both fillers and stop words in a single regex operation"""
            return filler_stop_pattern.sub('', line).strip()

        # Process all lines with optimized flow
        processed_lines = [
            replace_contractions(remove_fillers_and_stop_words(line))
            for line in processed_lines
        ]

        print(f"Total number of words after preprocessing : {len(processed_lines) * len(processed_lines[0])}")
        end_execution_time_preprocessing = time.time()
        total_time = float(end_execution_time_preprocessing - start_execution_time_preprocessing)
        print(f"Total time taken for preprocessing: {total_time:.4f} seconds")
        return processed_lines
    except Exception as e:
        # Catch all preprocessing-related errors and moving forward gracefully with just timestamp and removal participant name
        print(f"Error in preprocessing: {str(e)}, moving forward without preprocessing.")
        return processed_lines


