system_message = """
You are an expert dialogue and script generator.
Your primary role today is to create detailed, realistic conversations based on the context provided.
Over the past few years, I have been working on projects requiring high-quality, scenario-based transcripts. It’s important that the conversations you generate are natural, engaging, and aligned with the specified objectives.
As the requester, I authorize you to analyze the prompt and generate an accurate, context-driven dialogue
"""

def generate_prompt(book):
    prompt = f""" As the author of this manuscript, I am seeking your expertise in generating a detailed sales call transcript.
The manuscript is a comprehensive work detailing the product descriptions and pricing of fintech solutions. Your role is to create a 30-minute sales call transcript between a senior sales representative from a fintech company and the CTO of an e-commerce business, with a focus on the following key products: {book}.

Here is a segment from the manuscript for review: {book}

Instructions for Task Completion:

Your output should be formatted with timestamps and speaker names, like: 00:00:00 [Speaker Name]: Dialogue content
The sales representative should explain product features like ease of integration, security, and scalability.
The customer should express concerns about integration costs and data security.
Include a pricing discussion based on the manuscript segment provided.
Conclude the transcript with next steps for a product demo.
The conversation should be natural, realistic, and cover a full 30-minute call.
Example of format: 00:00:00 Sam (openai.com): Hey there Satya. 00:00:02 Satya (microsoft.com): Hi Sam, how are you? 00:00:05 Sam (openai.com): I'm doing good. Do you think you can give us 10000 more GPUs? 00:00:06 Satya (microsoft.com): I'm sorry Sam, we can't do 10000, how about 5000?

With the provided manuscript and instructions, proceed with generating the transcript. """
    return prompt
