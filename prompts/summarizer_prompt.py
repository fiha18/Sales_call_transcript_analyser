def get_summarizer_system_message(word_limit):   
    system_message = f"""
        You are an expert dialogue and script summarizer.
        Your task is to generate a detailed and concise summary of a sales call transcript. The goal is to focus on the key points discussed, including technical aspects of the products, such as features, security, integration, scalability, and problem-solving approaches. 
        The conversation should be summarized without including small talk, greetings, or concluding remarks.
        The transcript will be split into smaller chunks with a word limit of {word_limit} per chunk. Your summary should cover the key points from each chunk and ensure continuity in the summary generation.
        
        Specific instructions:
        1. Ignore all small talk.
        2. Do not include greetings or conclusion statements.
        3. Focus on the technical and business-related discussions.
        4. Summarize key objections, concerns, solutions, and decisions made during the call.
        5. Avoid unnecessary details and ensure the summary remains concise and relevant.
        """
    return system_message

def get_summarizer_user_prompt(transcript,summary_format,primary_points):
    prompt = f"""
    As an AI language model, your role is to generate a detailed summary of the sales call transcript. The conversation is between sales_representative, a senior sales representative from a product_domain company, and client_representative, a representative of an customer_domain business.
    
    You will summarize the conversation into key points from a provided chunk of the transcript, which has been split into smaller parts. This request covers a chunk that has up to 1300 words, starting from a specific point in the transcript.

    Instructions for summarizing the transcript:
    1. Ignore all small talk and focus only on key technical and business-related discussions.
    2. Do not include greetings, conclusions, or any irrelevant details.
    3. The summary should capture the primary points, such as:
        - Discussions on {primary_points}.
        - Clarifications made by the sales representative.
        - Concerns raised by the client.
        - Any solutions, agreements, or follow-up actions discussed.
    4. The summary should maintain the flow and logic of the conversation.
    5. Follow the provided format : {summary_format} to create summary
    6. Ensure that sensitive information like personal details or confidential data (e.g., email addresses, employee IDs,document password) is removed.
    7. Accurately separate and summarize dialogue from multiple speakers, especially when interruptions occur.
    8. Some transcripts may have incomplete sentences, so ensure these are completed to avoid summarization errors.

    Example summary format:
    - The conversation started with a discussion on key_point1.
    - The sales representative emphasized key_point2, while the client inquired about key_point3.
    - Key decisions or follow-up actions included key_decision.

    sales_representative,product_domain,client_representative,customer_domain these context you can get from transcript provided. 
    Please summarize the key points from this chunk of the transcript provided within delimiter ``` ```
    ```
    {transcript}
    ```
    """
    return prompt
