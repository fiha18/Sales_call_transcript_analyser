import utils as utils
def generate_call_transcript_system_message(call_duration):
    system_message = f"""
    You are an expert dialogue and script generator.
    Your task is to create detailed, realistic, and technical sales call transcripts. The goal is to produce a natural and comprehensive {call_duration}-minute conversation focused on the provided context, with timestamps, technical discussions, and client follow-ups.
    The dialogue should focus on product features, security, integration, and scalability, and should be engaging and authentic with transitions, customer objections, clarifications, and problem-solving.
    For this transcript, there is no need for greeting or conclusion remarks, as these prompts are used in a loop for mid-conversation segments. Focus on keeping the conversation natural, technical, and relevant to the client’s needs.
    """
    return system_message



def generate_call_transcript_prompt(sales_representative, client_representative, product_domain, customer_domain, product_detail_list, start_time, call_duration):
    end_time = utils.add_time(start_time, call_duration)
    product_details = ""
    for product in product_detail_list:
        feature = product['feature']
        description = product['description']
        pricing = product['pricing']
        product_details += f"\n- {feature}: {description}. Pricing: {pricing}"

    prompt = f"""As an AI language model, your role is to create a detailed transcript for a sales call. 
    The conversation is between {sales_representative}, a senior sales representative from a {product_domain} company, and {client_representative}, a representative of an {customer_domain} business.
    
    The call should start at {start_time} and last for {call_duration} minutes, ending at {end_time}. The conversation should include natural pauses, clarifications, and follow-ups to make the dialogue engaging and stretch it over the specified time.

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
    - There must be follow up questions from {client_representative}
    - Each response should be detailed and relevant to the client's needs.

    Example format:
    {start_time} {sales_representative}: Hypercheckout simplifies refunds and reconciliations through its automated workflows.
    {start_time} {client_representative}: That would definitely cut down operational hassles.
    """
    return prompt



