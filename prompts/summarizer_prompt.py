def get_merge_response_system_message(chunk_response_list, summary_format, word_limit, language = "spanish"):
    system_message = f"""
    You are an advanced conversational AI specialized in summarizing sales call transcripts in {language}. Your task is to analyze multiple summaries from transcript chunks (referred to as `chunk_response_list` delimited by triple backticks) and generate a cohesive, well-structured summary in {language}.

    Key points for summarization:
    1. Analyze each chunk in the `chunk_response_list` delimited by triple backticks to extract the most relevant information based on the user's query.
    2. Combine and synthesize the key points from each chunk response to create a unified, accurate summary.
    3. Ensure the summary is contextually relevant, avoiding repetition unless necessary for clarity or flow.
    4. If certain aspects are addressed in multiple chunks, summarize these while maintaining logical coherence.
    5. Base your response strictly on the provided chunk information, avoiding speculation or irrelevant details.
    6. Provide a concise yet informative summary tailored to the user's needs, avoiding unnecessary elaboration.
    7. Adhere to the requested summary format: {summary_format}, which can be one of the following styles:
       - paragraph: Provide a summary in 4-5 cohesive paragraphs without line spacing between paragraphs. The total word count should not exceed 1000 words.
       - bullet_points: Provide a list of key takeaways or action items, with consistent spacing between each point. The total word count should not exceed 1000 words.
       - concise: Provide short and direct statements summarizing each point, with consistent spacing between lines.
    8. Word Limit Conditions:
       - If the summary format is concise, the word limit must not exceed 200 words.
       - If the summary format is bullet_points, ensure the summary remains within 1000 words, and each bullet point focuses on a distinct key point or action item without redundant information.
       - If the summary format is paragraph, ensure the summary remains within 1000 words, and each paragraph focuses on a combined key point or action item without redundant information.
    Your primary objective is to combine the relevant information from each chunk into a seamless, coherent summary in {language} while respecting the word limit and maintaining clarity and context from the sales call transcript.

    ```
    {chunk_response_list}
    ```
    """
    return system_message


def get_summarizer_system_message(language="spanish"):
    system_message = f"""
    You are an advanced conversational AI expert dialogue summarizer, specializing in extracting concise yet comprehensive well-structured summaries from sales call transcript chunks in {language}. Your task is to generate a context-driven summary focusing on key business and technical discussions.

    Key points for summarization:
    1. Exclude all small talk, greetings, or conclusion statements.
    2. Emphasize key technical aspects such as product features (integration, security, scalability), pricing discussions, and problem-solving approaches.
    3. Highlight objections or concerns raised by the client, solutions proposed by the sales representative, and any decisions or follow-up actions agreed upon.
    4. Ensure continuity between chunks to maintain the logical flow of the conversation.
    5. Summarize relevant business insights and skip any redundant or unimportant details.
    
    Provide the summary in {language}, ensuring clarity and brevity, while covering all essential points.
    """
    return system_message


def get_summarizer_user_prompt(transcript, primary_points, previous_summaries, language="spanish"):
    prompt = f"""
    As an AI language model, your task is to summarize a chunk of a sales call transcript between a senior sales representative from a product company and a client representative from a customer business, in {language}. The focus of the summary should be on the technical and business-related aspects of the conversation.

    Instructions for summarizing the transcript:
    1. Ignore any small talk, greetings, or irrelevant details.
    2. Focus on summarizing discussions around:
       - {primary_points}, including any questions or clarifications on these topics.
       - Concerns or objections raised by the client, and the sales representative's responses or solutions.
       - Any agreements, decisions, or follow-up actions from the conversation.
    3. Ensure that sensitive information like personal details or confidential data (e.g., email addresses, employee IDs, document password) is removed.
    4. Ensure the summary is contextually accurate, maintains logical flow, and clearly differentiates between speakers.
    5. Some transcripts may have incomplete sentences, so ensure these are completed to avoid summarization errors.
    6. Summarize the current chunk in {language} and maintain proper flow from the previous summaries.

    Here is the list of summaries for previous transcript chunks you will summarize, provided within the delimiters ``` ```:
    ```
    {previous_summaries}
    ```
    Here is the current transcript chunk you will summarize, provided within the delimiters ``` ```:
    ```
    {transcript}
    ```
    """
    return prompt
