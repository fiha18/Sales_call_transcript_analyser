from openai import OpenAI
from openai import RateLimitError
import time
import utils

period_timer = None
OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)
# Helper function to make OpenAI API calls
def call_openai_api(system_message, prompt_message, model = "gpt-4o-mini", max_tokens = 8000, temperature = 0.7):
    """
    This function interacts with the OpenAI API to generate text based on user prompts and system information.
    
    Parameters:
    system_message (str): The initial message or context provided by the system.
    prompt_message (str): The user's prompt or query that the AI will respond to.
    model (str, optional): The OpenAI model to use for generation. Defaults to "gpt-4o-mini".
    max_tokens (int, optional): The maximum number of tokens for the generated response. Defaults to 8000.
    temperature (float, optional): Controls the randomness of the generated text. Lower values are more deterministic, higher values are more creative. Defaults to 0.7.
    
    Return type:
    str: The generated response from the OpenAI model, or None if an error occurs.
        """
    retries = 0
    while retries < 5:
        try:
            print(f"Sending request to OpenAI API...", end="")
            utils.print_period()
            message = [
                    {"role" : "system", "content": [{"type":"text","text":system_message}]}
                ,   {"role" : "user", "content" : [{"type":"text","text":prompt_message}]}
                ]
            completion_response = client.chat.completions.create(
                    model=model,
                    messages = message,
                    temperature = temperature,
                    max_tokens = max_tokens 
                )
            utils.stop_print_period()
            print("")
            response_content = completion_response.choices[0].message.content.replace("```", "")
            return response_content
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