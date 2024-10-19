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
pip install PyPDF2
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

## Task 2: Call Summarization {WIP}
## Task 3: Querying Transcripts{WIP}