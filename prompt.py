from datetime import timedelta

def generate_system_message(call_duration):
    system_message = f"""
    You are an expert dialogue and script generator.
    Your task is to create detailed, realistic, and technical sales call transcripts. The goal is to produce a natural and comprehensive {call_duration}-minute conversation focused on the provided context.
    The conversation should be highly engaging, with deep technical discussions on the products, including product features, security, integration, and scalability. 
    You are expected to add transitions, customer objections, clarifications, and responses, making it as authentic as possible.
    Ensure that the dialogue maintains a natural flow with a focus on problem-solving and selling the product effectively.
    """
    return system_message

def generate_prompt(sales_representative,client_representative,context,call_duration):
    prompt = f"""As the author of this manuscript, I am seeking your expertise in generating a detailed sales call transcript.
    Your role is to create a {call_duration}-minute sales call transcript between a senior sales representative {sales_representative} from a fintech company and the CTO {client_representative} of an e-commerce business. The conversation should be natural, technically detailed, and focused in depth, including {context}.
    Here are the main points for the call:
    - The customer’s primary challenge is improving their checkout experience and reducing transaction failures.
    - The sales rep should focus on technical features: ease of integration, security protocols, API usage, and scalability of the solution.
    - Address the customer's concerns regarding integration costs, data security, and ongoing maintenance.
    - Discuss product pricing: breakdown of pricing tiers, transaction costs, and additional fees.
    - Include technical details such as how the integration would fit into the client’s existing system, security layers, and performance optimizations.
   
    Instructions for the dialogue:
    - Format with timestamps and speaker names, like: `00:00:00 [Speaker Name]: Dialogue content`.
    - Add natural pauses, clarifications, and small talk to make the dialogue more engaging.
    - generate longer and more detailed responses. This can be done by asking for more elaboration, more in-depth explanations, or adding follow-up questions and clarifications in the conversation to encourage a more extended dialogue.
    - Add Pauses and Clarifications: Request that the conversation includes natural pauses, clarifications, and in-depth follow-ups to stretch the dialogue.
    - Include an in-depth discussion of how to solve the customer's problem.
    - Provide detailed responses to pricing objections and security concerns.
    - Conclude the transcript with next steps for a product demo and potential follow-up meetings.

    More focus on this -  Make sure the conversation flows for a full {call_duration} minutes.

    Example of format:
    00:00:00 Sam (fintech.com): Hi Satya, how’s it going today?
    00:00:02 Satya (ecommerce.com): Doing well, Sam.
    """
    return prompt



def generate_call_transcript_prompt(sales_representative, client_representative,product_domain, customer_domain, product_detail_list, start_time, call_duration):
    def add_time(start_time_str, minutes_to_add):
        start_time_obj = timedelta(hours=int(start_time_str.split(":")[0]), 
                                   minutes=int(start_time_str.split(":")[1]), 
                                   seconds=int(start_time_str.split(":")[2]))
        end_time_obj = start_time_obj + timedelta(minutes=minutes_to_add)
        return str(end_time_obj)

    end_time = add_time(start_time, call_duration)

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
    - {client_representative}'s company is looking to improve their checkout experience and reduce transaction failures.
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



