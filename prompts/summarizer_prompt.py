def get_summarizer_system_message(word_limit):
    system_message = f"""
    You are an expert dialogue and script summarizer, specializing in extracting concise yet comprehensive summaries from sales call transcripts. Your task is to generate a context-driven summary focusing on key business and technical discussions while adhering to a word limit of {word_limit} per chunk.

    Key points for summarization:
    1. Exclude all small talk, greetings, or conclusion statements.
    2. Emphasize key technical aspects such as product features (integration, security, scalability), pricing discussions, and problem-solving approaches.
    3. Highlight objections or concerns raised by the client, solutions proposed by the sales representative, and any decisions or follow-up actions agreed upon.
    4. Ensure continuity between chunks to maintain the logical flow of the conversation.
    5. Summarize relevant business insights and skip any redundant or unimportant details.

    Summary should be concise, but cover all essential points, making sure to balance brevity with clarity.
    """
    return system_message


def get_summarizer_user_prompt(transcript,summary_format,primary_points):
    prompt = f"""
    As an AI language model,Your task is to summarize a portion of a sales call transcript between a senior sales representative from a product company and a client representative from a customer_domain business. The focus of the summary should be on the technical and business-related aspects of the conversation.

    Instructions for summarizing the transcript:
    1. Ignore any small talk, greetings, or irrelevant details.
    2. Focus on summarizing discussions around:
       - {primary_points}, including any questions or clarifications on these topics.
       - Concerns or objections raised by the client, and the sales representative's responses or solutions.
       - Any agreements, decisions, or follow-up actions from the conversation.
    3. Adhere to the provided format: {summary_format}, which can be in one of the following styles:
       - paragraph: A summary in 4-5 cohesive paragraphs, for each paragraph avoid line spacing.
       - bullet_points: A list of key takeaways or action items, maintain same line spacing between each point.
       - concise: Short and direct statements summarizing each point, maintain same line spacing between each line.
    4. Follow the provided format : {summary_format} to create summary
    5. Ensure that sensitive information like personal details or confidential data (e.g., email addresses, employee IDs,document password) is removed.
    6. Ensure the summary is *contextually accurate, maintains logical flow, and clearly differentiates between speakers.
    7. Some transcripts may have incomplete sentences, so ensure these are completed to avoid summarization errors.
    Example summary format:
    - The conversation started with a discussion on key_point1.
    - The sales representative emphasized key_point2, while the client inquired about key_point3.
    - Key decisions or follow-up actions included key_decision.

    Here is the chunk of the transcript you will summarize, provided within the delimiters ``` ```:
    ```
    {transcript}
    ```
    """
    return prompt
