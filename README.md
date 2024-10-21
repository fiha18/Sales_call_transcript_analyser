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
2. **Product Details**: Product feature list are assumed to follow a format and have 10 features 
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
    - Model selection involved `gpt-3.5-turbo` and `gpt-4` to experiment with different combinations of settings such as temperature, max tokens, and messages.

2. **Limitations**:
    - I aimed to generate realistic transcripts by analyzing product documentation in PDF format and trying out various combinations of models, prompts, temperature settings, and `max_tokens`.
    - I faced token limitations that resulted in transcripts lacking essential product details.
    - Due to these token limitations, the transcripts were constrained to cover a duration of approximately 4–5 minutes.

3. **Optimization Strategy**:
    - To generate more realistic and detailed transcripts, a **product detail list** was introduced.
    - This list includes features, descriptions, and pricing of the product being discussed in the call, ensuring key details are incorporated into the generated transcript.
    - A custom prompt generation function, `generate_call_transcript_prompt`, was developed to take dynamic inputs such as the sales representative’s name, client representative’s name, product details, and conversation timings.
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
python3 -m venv path/to/venv
source path/to/venv/bin/activate
```
### Install Dependencies
```bash
pip install openai
pip install textblob
```

### Run the Transcript Generator:

- Right now sales_representative, client_representative,product_company,product_domain,  customer_domain,call_duration are hardcoded .
```bash
python3 transcript.py
```
- The transcript will be saved to a .txt file inside transcipt folder for further analysis.

### Inital Folder Structure
```
CALL-TRANSCRIPT-ANALYSIS
│   README.md
│   transcript.py
│   utils.py
│
├───myenv
│   └───...
│   
├───generated_transcripts
│       darwinbox_srijan_sales_call_transcript_20241019_190826.txt
│       juspay_rohit_sales_call_transcript_20241019_191339.txt
├───product_details
│       juspay_product.py
│       darwinbox_product.py     
└───prompts
        transcript_generator_prompt.py
```

## Task 2: Summarization of Sales Call Transcripts

For Task 2, the objective is to create a script that generates a summary of a sales call transcript, either in paragraph form, bullet points, or a concise format, based on the user's preference. The resulting summary is saved into a `.txt` file for further analysis. 

### Approach

1. **Pre-processing the Transcript:**
   - The transcript text file is cleaned and pre-processed to remove unnecessary elements that could interfere with summarization accuracy:
     1. **Remove timestamps and participant names** from the transcript (e.g., `00:00:03 Sam(open.ai)`).
     2. **Remove filler and stop words** such as "um," "so," "a," "an," "the," etc., from the text.
     3. **Expand contractions** such as "won't" to "will not" for better clarity.

2. **Splitting the Text into Chunks:**
   - The cleaned text is split into smaller chunks, typically using a default word limit of **1500 words** per chunk to ensure the summarization process is manageable and fits within API token limits.

3. **Summarizer System Message:**
   - The system is set up using the `get_summarizer_system_message` function, with a word limit set to **default** to guide the OpenAI API in generating a precise summary.

4. **Prompt for Summarization:**
   - The user prompt is generated using the function `get_summarizer_user_prompt`, which takes the chunk of text and user-defined `summary_format` (paragraph, bullet points, or concise). It also uses a hardcoded list of key context points such as:
     - **Product feature**
     - **Product pricing**
     - **Maintainability**
     - **Scalability**
     - **Security protocols**
     - **Data security**
     - **Support/maintenance costs**
     - **Ease of integration**

5. **Summarization Process with API Call and Error Handling:(To do - seperate open ai api logic as all 3 task are using it)** 
   - The core of the summarization process is handled by making API requests to OpenAI’s GPT model.
   
   **Code Block Summary:**
   - The code initiates a retry mechanism with a maximum of 5 attempts. It calls OpenAI's API for summarization, processes each chunk, and handles specific exceptions like `RateLimitError` by implementing a wait time before retrying. If other exceptions occur, the process will stop, and an error message will be displayed.

6. **Saving the Summary:**
   - The final step involves saving the generated summary to a `.txt` file using the `save_summary_file(file_path, summary)` function. This allows further analytics, such as querying the summary content for insights or answering user queries based on the call context.

### Error Handling and Retry Logic:

The script includes robust error handling to ensure smooth operation during the API call phase. If a rate limit error occurs, the script waits for 60 seconds before retrying. After five failed attempts, the script gives up on that particular chunk of text. Other unexpected errors are also caught, and the summarization process for that chunk is halted to avoid crashes.

### Future work 
  - Use of language detection to ensure the correct language model is applied for multilingual scenarios.
  - Tone Filtering: tone analysis as part of the processing, identify emotive language or sarcasm for better insight.
  - Keyword Segmentation: From a list of important keywords that signify different sections of the conversation. When a keyword is detected, segment the transcript at that point.


## Task 3: Querying Transcripts{WIP}