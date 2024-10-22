from datetime import timedelta
import re
import threading


def add_time(start_time_str, minutes_to_add):
        try:
                # Clean the time string using regex to remove invalid characters
                start_time_str = re.sub(r"[^0-9:]", "", start_time_str)
                # Split time string into hours, minutes, seconds
                time_parts = start_time_str.split(":")
                
                # Ensure that there are exactly 3 parts (HH:MM:SS)
                if len(time_parts) != 3:
                        raise ValueError(f"Invalid time format: {start_time_str}")
                
                # Convert the time parts to integers
                start_time_obj = timedelta(hours=int(time_parts[0]), 
                                        minutes=int(time_parts[1]), 
                                        seconds=int(time_parts[2]))
                
                # Add the required minutes
                end_time_obj = start_time_obj + timedelta(seconds=minutes_to_add*60)
                
                return str(end_time_obj)
    
        except ValueError as e:
                print(f"Error parsing time string '{start_time_str}': {e}")
                return None

def print_period():
    """
    Prints a period character to the console every second. 
    Uses a global timer object to schedule itself to run every second.
    """
    global period_timer
    print(".", end="", flush=True)
    period_timer = threading.Timer(1.0, print_period)
    period_timer.start()

def stop_print_period():
    """
    Stops the printing of periods by canceling the timer.
    """
    global period_timer
    if period_timer is not None:
        period_timer.cancel()
        period_timer = None

def get_common_stop_words():
       stop_words = [
                "a",
                "an",
                "the",
                "and",
                "but",
                "or",
                "if",
                "because",
                "while",
                "I",
                "you",
                "he",
                "she",
                "it",
                "we",
                "they",
                "me",
                "him",
                "her",
                "us",
                "them",
                "my",
                "your",
                "his",
                "its",
                "our",
                "their",
                "is",
                "are",
                "was",
                "were",
                "be",
                "been",
                "do",
                "does",
                "did",
                "have",
                "has",
                "had",
                "can",
                "could",
                "would",
                "should",
                "will",
                "shall",
                "for",
                "in",
                "on",
                "at",
                "with"
                ]
       return stop_words

def get_contration_words():
        contraction_words = {
                                "don't": "do not",
                                "won't": "will not",
                                "I'll": "I will",
                                "you're": "you are",
                                "we're": "we are",
                                "they're": "they are",
                                "I've": "I have",
                                "you'll": "you will",
                                "it's": "it is",
                                "there's": "there is",
                                "can't": "cannot",
                                "that's": "that is",
                                "he'll": "he will",
                                "we'll": "we will",
                                "isn't": "is not",
                                "aren't": "are not",
                                "wasn't": "was not",
                                "weren't": "were not",
                                "didn't": "did not",
                                "hasn't": "has not",
                                "hadn't": "had not",
                                "let's": "let us",
                                "wouldn't": "would not",
                                "shouldn't": "should not",
                                "couldn't": "could not",
                                "might've": "might have",
                                "must've": "must have",
                                "you've": "you have"
                                }
        return contraction_words

def get_common_fillers():
        filler = ["uh", "um", "like", "you know", "I mean", "actually", "basically", "so", "right", "well"]
        return filler

def get_major_context():
        major_context = ["product feature","product pricing","maintainability","scalability","security protocols","data security","support/maintenance costs","ease of integration"]
        return major_context

def get_summary_related_words():
        """
        This function returns most commonly sumary related word to make query to summary file if exist.
        More number of related keywords can be added for more precise result.
        """
        summary_related_words = [ "questions","briefly","name","context","summary","overview","abstract", "recap", "synopsis", "digest", "outline", "highlights", "key points", "summary statement", "brief", "condensed version", "summary report", "compendium", "review","conclusion"]
        summary_related_keywords_top_100 = [
        "summary", "overview", "briefly", "context", "abstract", "recap", "synopsis", 
        "digest", "outline", "highlights", "key points", "essence", "gist", 
        "core points", "main ideas", "takeaways", "snapshot", "short version", 
        "quick review", "bullet points", "concise explanation", "primary details", 
        "quick facts", "summary statement", "core message", "main points", "condensed version", 
        "summary report", "compendium", "review", "conclusion", "essence", "critical points", 
        "condensed", "essential points", "summation", "summarized", "core details", 
        "key takeaways", "main highlights", "high-level summary", "summarized statement", 
        "compact version", "concise account", "condensed outline", "important highlights", 
        "summary essentials", "quick facts", "top points", "executive summary", 
        "concise report", "brief summary", "summary memo", "key insights", "highlights report", 
        "summary insight", "summary brief", "important points", "summary findings", 
        "core summary", "brief overview", "summary key points", "final overview", 
        "summary conclusions", "summary recap", "focused summary", "primary summary", 
        "quick key points", "concise insights", "main conclusions", "highlighted points", 
        "final summary", "important ideas", "core takeaways", "concise key points", 
        "critical takeaways", "summary observations", "key facts", "relevant points", 
        "quick highlights", "summary outline", "main ideas summary", "concise synopsis", 
        "bullet summary", "brief analysis", "top-level summary", "summary checklist", 
        "concise review", "quick overview", "summary directive", "brief facts", 
        "main points summary", "final key points", "short recap", "key summary", 
        "concise findings", "summary final points", "condensed version", "summary description", 
        "main summary", "concise points"
        ]
        return summary_related_keywords_top_100
