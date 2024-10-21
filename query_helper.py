import summarizer_helper 
import re
from collections import defaultdict

# all synonym words into one words for optimised query keywords
def get_synonyms_dict():
    synonyms = {
        'price': ['pricing', 'cost', 'fee', 'charge', 'model'],
        'security': ['safety', 'protection', 'protocol', 'encryption', 'access controls'],
        'integration': ['connecting', 'linking', 'combining', 'unifying', 'incorporating'],
        'features': ['functionality', 'capabilities', 'options', 'characteristics'],
        'capability': ['ability', 'capacity', 'functionality'],
        'support': ['assistance', 'help', 'service'],
        'data security': ['data protection', 'information security'],
        'service level agreement': ['SLA', 'support agreement', 'service commitment'],
        'customization': ['tailoring', 'personalization', 'adaptation'],
        'reporting': ['analytics', 'data reporting', 'insight generation'],
        'real-time': ['immediate', 'live', 'instant'],
    }
    return synonyms

def map_synonyms_to_original_keyword(query_word, synonyms_dict):
    """Map a synonym to its keyword."""
    for key, synonym_list in synonyms_dict.items():
        if query_word in synonym_list:
            return key
    return query_word 

def extract_keywords(query):
    """AI-Generated Code for using re.sub to remove punctuation"""
    # Lowercase, remove punctuation, and split into words
    normalized_query = re.sub(r'[^\w\s]', '', query.lower())
    query_keywords = normalized_query.split()
    
    generic_synonyms = get_synonyms_dict()

    # Replace synonyms with their corresponding keyword
    combined_keywords = set()
    for keyword in query_keywords:
        # Map the synonym to its main keyword if applicable
        main_keyword = map_synonyms_to_original_keyword(keyword, generic_synonyms)
        combined_keywords.add(main_keyword)
    return combined_keywords

# Function to search for relevant chunks based on keyword matching
def find_relevant_chunks(query, transcript_chunks):
    """
    Finds relevant chunks within a transcript based on keyword matching.
    
    Parameters:
        query (str): The search query to match against the transcript chunks.
        transcript_chunks (list): A list of transcript chunks, each containing a 'chunk' key with the text content.
    
    Returns:
        list: A list of relevant chunks that contain at least one of the query keywords.
    """
    relevant_chunks = []
    query_keywords = extract_keywords(query)  # Splitting the query into keywords
    
    for chunk in transcript_chunks:
        chunk_text = chunk['chunk'].lower()
        if any(keyword in chunk_text for keyword in query_keywords):  # Check if any keyword is present
            relevant_chunks.append(chunk)
    
    return relevant_chunks

def chunk_transcript(transcript, max_chunk_size=10000):
    """
    Splits a large transcript into smaller, logical chunks based on a character limit.

    Parameters:
    transcript (str): The full transcript as a string.
    max_chunk_size (int): The maximum size of each chunk in characters.

    Returns:
    List[Dict]: A list of chunks where each chunk is stored along with its start and end position.
    """

    # Split transcript into sentences for logical chunking.
    sentences = summarizer_helper.preprocess_text_helper(transcript)
    chunks = []
    current_chunk = ""
    start_idx = 0

    for sentence in sentences:
        # If adding the sentence exceeds the chunk size, store the current chunk
        if len(current_chunk) + len(sentence) + 2 > max_chunk_size:
            end_idx = start_idx + len(current_chunk)
            # Each chunk is stored in a dictionary along with its start and end positions, allowing easy reference back to the original transcript.
            chunks.append({
                'chunk': current_chunk.strip(),
                'start_idx': start_idx,
                'end_idx': end_idx
            })
            # Reset for the next chunk
            start_idx = end_idx + 1
            current_chunk = ""

        # Add sentence to the current chunk
        current_chunk += sentence + ". "

    # Add the last chunk if it's not empty
    if current_chunk:
        end_idx = start_idx + len(current_chunk)
        chunks.append({
            'chunk': current_chunk.strip(),
            'start_idx': start_idx,
            'end_idx': end_idx
        })

    return chunks
