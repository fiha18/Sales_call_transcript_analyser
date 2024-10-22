# Sales Call Transcript Analysis

## Project Overview

This project aims to develop a command-line application using OpenAI's GPT API to generate, analyze, and query sales call transcripts. The application will generate realistic call transcripts, summarize them, and answer questions related to the content. The functionality will run entirely via the command line, and all outputs will be displayed in the console. No frontend or additional API is required.

The project is divided into three main tasks:
1. **Transcript Generation**: Creating a script to generate realistic sales call transcripts using dynamic inputs and saving the output in a text file.
2. **Call Summarization**: Summarizing the call transcript with key points.
3. **Querying Transcripts**: Answering user queries based on the generated transcript content.

---

## Task 1: Generic Transcript Generator

### Objective

The goal of Task 1 is to develop a script that generates a realistic sales call transcript based on dynamic inputs and saves the generated transcript to a text file. This transcript mimics an actual sales call, detailing the interactions between a sales representative and a client.
### Assumption 
1. **Call Duration**: Sales call are initial discussion between product owner and potential client , so in realistic enviornment the call duration is assumed to be 30 minutes. 
2. **Product**: 4 products juspay(payment solutions), darwinbox(hr management tool), sap-erp(enterprise resource planning) and shopify(e-commerce), to add new product create a python file <product_name>_product indside product_details folder and follow below below format for each file.
  ```python
    {
    product_company = "str type"
    potential_customer = "str type"
    sales_representative = f"str type"
    client_representative = f"str type"
    product_domain = "str type"
    customer_domain = "str type"
    major_issue = "str type"
    product_details = [{{
     "feature": "str type",
     "description": "str type",
     "pricing": "str type"
      }}]
    }
  ```
3. **Product Details**: Product feature list are assumed to follow a format and have 10 features 
 ```json
   {
     "feature": "HyperCheckout",
     "description": "HyperCheckout is a pre-built, customizable payment page UI that allows businesses to effortlessly collect payments on their app or website. It supports multiple payment methods, including UPI, cards, net banking, and wallets. This product is designed for fast integration, offering a seamless payment experience with minimal development effort.",
     "pricing": "0.35% per transaction."
   }
```

### Approach

To create a realistic and accurate transcript, I leveraged OpenAI’s GPT models, ranging from `gpt-3.5-turbo` to `gpt-4`. The objective was to generate a high-quality sales transcript by feeding in key product details, call start times, and other dynamic inputs. Below is an outline of the approach taken:

1. **API Integration**: 
    - The OpenAI Completion API was used for generating the transcripts. 
    - Using **call_openai_api** function with system_message and prompt_message at **llm_strategy/openai** folder.

2. **Limitations**:
    - I aimed to generate realistic transcripts by analyzing product_detail_list format and trying out various combinations of models, prompts, temperature settings, and `max_tokens`.
    - I faced token limitations that resulted in transcripts lacking essential product details.
    - Due to these token limitations, the transcripts were constrained to cover a duration of approximately 4–5 minutes.

3. **Optimization Strategy**:
    - To generate more realistic and detailed transcripts, a **product detail list** was introduced.
    - This list includes features, descriptions, and pricing of the product being discussed in the call, ensuring key details are incorporated into the generated transcript.
    - A dynamic prompt generation function, `generate_call_transcript_prompt`, was developed to take dynamic inputs such as the sales representative’s name, client representative’s name, product details, and conversation timings.
    - previous transcript context is provided to user prompt for more realistic response (below is a screenshot of response time without previous  )
    - sequential open ai completion api call based on **product detail list** elements

### Function: `generate_call_transcript_prompt`

The function `generate_call_transcript_prompt` is at the core of this task. It generates a well-structured prompt to be sent to the GPT model, ensuring that the conversation is both realistic and informative.

**Function Arguments:**

1. **`sales_representative`**: Name of the sales representative (e.g., "Rahul Kothari").
2. **`client_representative`**: Name of the client representative (e.g., "Kailash Nath").
3. **`product_detail_list`**: A list of product details to be discussed in the call following product_detail format. 
  
4. **start_time**: The start time of the transcript, formatted as `HH:MM:SS` (e.g., "00:05:00").
5. **call_duration**: The duration of the call in minutes (e.g., 5 minutes). If the `start_time` is "00:15:00" and the `call_duration` is 5, the transcript will cover the conversation until "00:20:00".

### Additional Features
- **Dynamic Timing**: The script calculates timestamps for each part of the transcript, ensuring that the call flows smoothly with realistic intervals between dialogue.
- **Greeting and Conclusion**: A greeting is added at the start of the conversation, and a conclusion is appended based on the calculated time at the end of the call.

### How to Run the Script

Below are the steps to set up your environment and run the transcript generator script:

### Set Up Virtual Environment

```bash
python3 -m venv $PATH/to/venv
source $PATH/to/venv/bin/activate
```
### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Transcript Generator:

- Right now sales_representative, client_representative,product_company,product_domain,  customer_domain,call_duration are hardcoded .
```bash
python3 transcript.py
```
- The transcript will be saved to a .txt file inside transcipt folder for further analysis.

## Task 2: Summarization of Sales Call Transcripts

For Task 2, the objective is to create a script that generates a summary of a sales call transcript, either in paragraph form, bullet points, or a concise format, based on the user's preference. The resulting summary is saved into a `.txt` file for further analysis. 

### Approach

1. **Pre-processing the Transcript:**
   - The transcript text file is cleaned and pre-processed to remove unnecessary elements that could interfere with summarization accuracy (~ reduction in size of text from 32,000 to 20,000 length):q
     1. **Remove timestamps and participant names** from the transcript (e.g., `00:00:03 Sam(open.ai)`).
     2. **Remove filler and stop words** such as "um," "so," "a," "an," "the," etc., from the text.
     3. **Expand contractions** such as "won't" to "will not" for better clarity.

2. **Splitting the Text into Chunks:**
   - The cleaned text is split into smaller chunks, typically using a default word limit of **1500 words** per chunk to ensure the summarization process is manageable and fits within API token limits.

3. **Summarizer System Message:**
   - The system is set up using the `get_summarizer_system_message` function, with a word limit set to **default** to guide the OpenAI API in generating a precise summary.

4. **Prompt for Summarization:(LLM Strategy = OpenAI)**
   - The user prompt is generated using the function `get_summarizer_user_prompt`, which takes the chunk of text and user-defined `summary_format` (paragraph, bullet points, or concise). It also uses a hardcoded list of key context points such as:
     - **Product feature**
     - **Product pricing**
     - **Maintainability**
     - **Scalability**
     - **Security protocols**
     - **Data security**
     - **Support/maintenance costs**
     - **Ease of integration**


5. **Merging Chuck Summary System Message(LLM Strategy = OpenAI):**
  - The system is set up using the `get_merge_response_system_message` function for merging chunk responses in a cohesive, well-structured final summary.

6. **Saving the Summary List:**
   - The final step involves saving the generated summary to a `.txt` file using the `save_summary_file(file_path, summary)` function. This allows further analytics, such as querying the summary content for insights or answering user queries based on the call context.
### Run the Summary Generator:

```bash
python3 summarizer.py <input_file_name> [summary_format] [word_limit]
```
  - <input_file_name>: Replace this with the actual name of the input file (located in the generated_transcripts folder).
  - [summary_format]: (Optional) Specify the desired summary format: paragraph,bullet_points, or concise. If not provided, the paragraph format will be used.
  - [word_limit]: (Optional) word limit for the summary.If not provided, 1000 word limit will be used for paragraph,bullet_points and 200 words for concise. ***word limit does not guarentee exact word count***

### Future work 
  - Use of language detection to ensure the correct language model is applied for multilingual scenarios.
  - Tone Filtering: tone analysis as part of the processing, identify emotive language or sarcasm for better insight.
  - Keyword Segmentation: From a list of important keywords that signify different sections of the conversation. When a keyword is detected, segment the transcript at that point.


## Task 3: Querying the Transcript Efficiently

In this task, the focus is on efficiently querying large transcripts while handling token limitations in GPT models, and using summaries for faster responses when applicable.

#### Approach

**Step 1: Chunking the Transcript for Querying**

Due to token limitations in models like GPT-3.5 and GPT-4 (approximately 4,000 tokens for GPT-3.5 and up to 8,000 tokens for GPT-4), the transcript must be split into smaller, manageable chunks to fit within these constraints.

**Steps:**
1. **Define Chunk Size**:  
   Chunk the transcript into segments of around 2,500 tokens (approximately 10,000 characters) to ensure each chunk can be processed effectively.
   
2. **Create a Chunking Function**:  
   The function splits the transcript into logical segments, ensuring the breaks occur at natural points such as the end of a sentence or topic.

3. **Store and Index Chunks**:  
  Storing each chunk in a list of dict, indexing them by their start and end positions allowing easy reference back to the original transcript.

4. **Synonym Replacement for Efficient Querying**:  
  a function to replace synonyms with their corresponding keyword, ensuring that multiple related terms are combined into a single word. This optimization helps match relevant chunks more effectively.

   - **Example**:  
     Query: "Explain in brief about Employee onboarding, its security protocols, encryption, their pricing, fee or charge, and how integration or linking can be done?"  
     After processing, the query will be converted into a set of keywords:  
     `{'protocols', 'or', 'how', 'done', 'brief', 'their', 'and', 'price', 'onboarding', 'be', 'explain', 'in', 'employee', 'its', 'integration', 'security', 'can', 'about'}`

   This approach simplifies the query by collapsing related terms (e.g., "pricing", "fee", "charge" are all combined into "price"), ensuring a more efficient search through transcript chunks.

**2: Handling Summary for Quick Responses**

For call of around 30 minutes the summary is smaller (~12,000 characters) and call transcript (~28,000 character), it is better suited for general queries that do not require deep contextual information. This saves processing time and fits within the token limit for querying.
Attaching Screenshots of querying to call transcript and summary for same query. 
**Steps:**
1. **Direct Query on Summary(LLM Strategy = OpenAI)**:  
   If the query appears general or focused on broad information, the summary file is used for querying directly, avoiding the need to process the full transcript.

2. **Fallback to Full Transcript Query(LLM Strategy = OpenAI)**:  
   If the summary is not present or query type is not closely related to summary, then the system falls back to the full transcript by searching through the chunks generated in Step 1.
  - Querying without summary
    ![Screenshot of querying without summary : Time 29 seconds ]( /screenshots/query_without_summary.png)
  - Querying with summary
    ![Screenshot of querying with summary : Time 9 seconds ]( /screenshots/query_with_summary.png)
    
#### Optimizations
- **Efficient Use of Token Limits**: Avoided exceeding token limits in the GPT models and ensure that responses are accurate without truncation.
- **Priority of Summary**: Using a pre-generated summary for general or simple queries thus speeding up query resolution.
- **Fallback Mechanism**: If the summary does not contain enough information to answer the user query, the system efficiently falls back on querying the transcript chunks.

- **Merging Chunk Responses**: chat completion api response for each chunk are merged in a cohesive, well-structured response that directly addresses the user’s prompt.

### Additional Feature
- **Persist Chat**: The multiple responses for a single transacript are saved in same query response text file like
```
2024:10:22-17:38:16 User Query: Did they have any future questions?

2024:10:22-17:38:19 App Response: 
Yes, during the conversation, the client indicated that they had future questions. They expressed interest in understanding how Shopify supports business growth and had inquiries about next steps. This led to an agreement to schedule a product demonstration, which would provide an opportunity to explore features in more detail and address any further questions they might have. Additionally, a follow-up meeting was organized to discuss specific requirements after the demonstration.

```
### Run the Query Handler:

```bash
python3 query_handler.py <input_file_name> <user_input_query>
```
  - <input_file_name>: Replace this with the actual name of the input file (located in the generated_transcripts folder).
  - <user_query> : Replace with user query


## LLM Strategy(OpenAI) with API Interaction:
   - The core of the open ai in llm_strategy folder is handled by making API requests to OpenAI’s GPT model.
   - This strategy follows code reusability , extensibility and modular approach.
   ### Generic call_open_api function ###
   ```python
   def call_openai_api(system_message, prompt_message, model = "gpt-4o-mini", max_tokens = 8000, temperature = 0.7):
    """
      This function interacts with the OpenAI API to generate text based on user prompts and system information.
      
      Parameters:
      - system_message (str): The initial message or context provided by the system.
      - prompt_message (str): The user's prompt or query that the AI will respond to.
      - model (str, optional): The OpenAI model to use for generation. Defaults to "gpt-4o-mini".
      - max_tokens (int, optional): The maximum number of tokens for the generated response. Defaults to 8000.
      - temperature (float, optional): Controls the randomness of the generated text. Lower values are more deterministic, higher values are more creative. Defaults to 0.7.
      
      Returns:
      - str: The generated response from the OpenAI model, or None if an error occurs.
    """
   ```
  ### Error Handling
  Error Handling
  - Rate Limit Handling: If a rate limit is encountered, the function waits 60 seconds and retries the request.
  - General Errors: For any unexpected error, the function gracefully exits and prints the error message.
  - Retry Logic: The function retries up to 5 times in case of failure before giving up.


## Project Structure
```
CALL-TRANSCRIPT-ANALYSIS
│   README.md
│   query_handler.py
│   query_helper.py
│   summarizer_helper.py
│   summarizer.py
│   transcript.py
│   transcript.py
│   utils.py
│
├───myenv
│   └───...
├───llm_strategy
│       openai.py
├───generated_summaries
│       darwinbox_srijan_sales_call_transcript_20241019_190826_bullet_points_summary_list.txt
│       juspay_rohit_sales_call_transcript_20241019_191339_bullet_points_summary_list.txt
├───generated_transcripts
│       darwinbox_srijan_sales_call_transcript_20241019_190826.txt
│       juspay_rohit_sales_call_transcript_20241019_191339.txt
├───product_details
│       juspay_product.py
│       darwinbox_product.py
├───product_details
│       juspay_product.py
│       darwinbox_product.py 
├───prompts
│       query_prompt.py
│       summarizer_prompt.py
│       transcript_generator_prompt.py     
└───screen_shots
       query_with_summary.png
       query_without_summary.png

```