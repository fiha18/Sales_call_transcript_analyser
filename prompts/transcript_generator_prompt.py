import utils as utils
def generate_call_transcript_system_message(call_duration):
    system_message = f"""
    You are an expert dialogue and script generator.
    Your task is to create detailed, realistic, and technical sales call transcripts. The goal is to produce a natural and comprehensive conversation focused on the provided context, split into smaller chunks of {call_duration}-minute intervals to ensure accuracy and token efficiency.
    The conversation should be highly engaging, with deep technical discussions on the products, including product features, security, integration, and scalability. 
    You are expected to add transitions, customer objections, clarifications, and responses, making it as authentic as possible. Each segment should continue smoothly from the previous one to ensure the transcript feels continuous.
    In this setup:
    1. You will generate the conversation in smaller increments (e.g., 5 minutes), avoiding generatin in one go and aiming for a response that uses the maximum token limit.
    2. Each new chunk should pick up where the last one ended. The last few lines from the previous segment will be passed to ensure continuity.
    3. Please do not use any markdown code blocks or formatting, such as triple backticks (```).
    The transcript must maintain a natural flow, focusing on problem-solving and selling the product effectively.
    """
    return system_message



def generate_call_transcript_prompt(sales_representative, client_representative, product_domain, customer_domain, product_detail_list, start_time, call_duration,last_ending_line):
    end_time = utils.add_time(start_time, call_duration)
    product_details = ""
    for product in product_detail_list:
        feature = product['feature']
        description = product['description']
        pricing = product['pricing']
        product_details += f"\n- {feature}: {description}. Pricing: {pricing}"

    prompt = f"""As an AI language model, your role is to create a detailed transcript for a sales call. 
    The conversation is between {sales_representative}, a senior sales representative from a {product_domain} company, and {client_representative}, a representative of an {customer_domain} business.
    The call will be split into smaller chunks to fit within token limits. This request covers the segment from {start_time} and last for {call_duration} minutes, ending at {end_time}, and future requests will continue from the stopping point.
    The conversation should include natural pauses, clarifications, and follow-ups to make the dialogue engaging and stretch it over the specified time.
    The main focus of the call is discussing these products and services:
    {product_details}

    Here are the primary points for the call:
    - {sales_representative} should emphasize ease of integration, security protocols, scalability, and support for multiple {product_domain} methods.
    - Address concerns related to data security, pricing breakdown, and ongoing support/maintenance costs.
    - Provide technical insights into how the integration would work with {client_representative}'s existing systems.

    Instructions for the dialogue:
    - No need for greeting or concluding remarks, as these prompts are part of a loop.
    - Format the transcript with timestamps and speaker names, like this: `{start_time} [Speaker Name]: Dialogue content.`
    - Make the conversation flow naturally with technical depth discussions and high level architecture.
    - Each new chunk conversation will begin by alternative speaker after the last few lines from the previous segment as provided within ``` ``` quotes below.
    - There must be follow up questions from {client_representative}
    - Each response should be detailed and relevant to the client's needs.
    
    Continuation: This transcript chunk starts with the following lines for continuity from the previous segment: provided within  ``` ``` quotes.
    Example format: provided within ``` ``` quotes.
    ```{last_ending_line}```
    """
    return prompt