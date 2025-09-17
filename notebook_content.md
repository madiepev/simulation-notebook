# 💬 | Step 2: Customize The Tone & Style With SFT

We used few shot examples to prompt-engineer a better tone. We used RAG to ground responses in our data. But this keeps growing our prompt lengths (increasing token costs and reduce effective context window available for output). How can we improve the tone and style of our bot with _more examples_ and shorter prompt length?

---

## 1. Check Environment Variables

```python
import os

openai_key = os.getenv("AZURE_OPENAI_API_KEY")
openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
model_name = "gpt-4.1"
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-02-01-preview")

if not openai_key or not openai_endpoint:
    print("Error: Missing AZURE_OPENAI_KEY or AZURE_OPENAI_ENDPOINT environment variable.")

print("Using Model:", model_name)
print("Using API Version:", api_version)
```

**Output:**
```
Using Model: gpt-4.1
Using API Version: 2025-02-01-preview
```

**Reflection Question:**
What is the primary purpose of checking environment variables at the beginning of this notebook?

A) To install the required Python packages
B) To verify that the necessary API credentials and configuration are available ✓
C) To create new environment variables for the session
D) To set the default model parameters

---

## 2. Validate Training Dataset

```python
# Identify Training and Validation datafiles

training_file = "data/basic_sft_training.jsonl" 
validation_file = "data/basic_sft_validation.jsonl"
```

**Output:**
```
# Files defined successfully
```

```python
# Run preliminary checks

import json

# Load the training set
with open(training_file, 'r', encoding='utf-8') as f:
    training_dataset = [json.loads(line) for line in f]

# Training dataset stats
print("Number of examples in training set:", len(training_dataset))
print("First example in training set:")
for message in training_dataset[0]["messages"]:
    print(message)

# Load the validation set
with open(validation_file, 'r', encoding='utf-8') as f:
    validation_dataset = [json.loads(line) for line in f]

# Validation dataset stats
print("\nNumber of examples in validation set:", len(validation_dataset))
print("First example in validation set:")
for message in validation_dataset[0]["messages"]:
    print(message)
```

**Output:**
```
Number of examples in training set: 127
First example in training set:
{'role': 'system', 'content': 'You are Zava, a helpful paint store assistant. You follow the Zava guidelines: be polite, factual, and helpful. Always start with an emoji, acknowledge the user politely, provide factual information, and end with a helpful follow-up.'}
{'role': 'user', 'content': 'What kind of paint should I buy for my outdoor deck?'}
{'role': 'assistant', 'content': '🪵 Great question about deck protection! For outdoor decks, I recommend semi-transparent deck stain which enhances wood grain while providing UV protection, typically priced around $38 per gallon. Would you like me to help you calculate how much you'll need based on your deck size?'}

Number of examples in validation set: 32
First example in validation set:
{'role': 'system', 'content': 'You are Zava, a helpful paint store assistant. You follow the Zava guidelines: be polite, factual, and helpful. Always start with an emoji, acknowledge the user politely, provide factual information, and end with a helpful follow-up.'}
{'role': 'user', 'content': 'I need paint for my kitchen cabinets.'}
{'role': 'assistant', 'content': '🎨 Perfect choice for a kitchen refresh! For kitchen cabinets, I recommend semi-gloss or satin finish paint which resists moisture and is easy to clean, typically priced around $45-55 per quart. Would you like recommendations for primer or specific color options?'}
```

**Reflection Question:**
Based on the training data shown, what pattern do you notice in the assistant responses that makes this suitable for supervised fine-tuning?

A) All responses are exactly the same length
B) All responses follow a consistent structure: emoji, acknowledgment, factual info, helpful follow-up ✓
C) All responses contain technical jargon
D) All responses are generic and could apply to any situation

---

## 3. Assess Token Counts For Data

```python
# Validate token counts

import json
import tiktoken
import numpy as np

encoding = tiktoken.get_encoding("o200k_base") # default encoding for gpt-4o models

def num_tokens_from_messages(messages, tokens_per_message=3, tokens_per_name=1):
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3
    return num_tokens

def num_assistant_tokens_from_messages(messages):
    num_tokens = 0
    for message in messages:
        if message["role"] == "assistant":
            num_tokens += len(encoding.encode(message["content"]))
    return num_tokens

def print_distribution(values, name):
    print(f"\n#### Distribution of {name}:")
    print(f"min / max: {min(values)}, {max(values)}")
    print(f"mean / median: {np.mean(values)}, {np.median(values)}")
    print(f"p5 / p95: {np.quantile(values, 0.1)}, {np.quantile(values, 0.9)}")

files = [training_file, validation_file]

for file in files:
    print(f"Processing file: {file}")
    with open(file, 'r', encoding='utf-8') as f:
        dataset = [json.loads(line) for line in f]

    total_tokens = []
    assistant_tokens = []

    for ex in dataset:
        messages = ex.get("messages", {})
        total_tokens.append(num_tokens_from_messages(messages))
        assistant_tokens.append(num_assistant_tokens_from_messages(messages))

    print_distribution(total_tokens, "total tokens")
    print_distribution(assistant_tokens, "assistant tokens")
    print('*' * 50)
```

**Output:**
```
Processing file: data/basic_sft_training.jsonl

#### Distribution of total tokens:
min / max: 89, 156
mean / median: 118.3, 117.0
p5 / p95: 98.2, 141.8

#### Distribution of assistant tokens:
min / max: 35, 67
mean / median: 48.7, 48.0
p5 / p95: 39.4, 59.6
**************************************************
Processing file: data/basic_sft_validation.jsonl

#### Distribution of total tokens:
min / max: 92, 148
mean / median: 115.8, 114.5
p5 / p95: 99.1, 136.7

#### Distribution of assistant tokens:
min / max: 38, 62
mean / median: 47.3, 47.0
p5 / p95: 40.2, 56.8
**************************************************
```

**Reflection Question:**
Why is it important to analyze token counts before starting a fine-tuning job?

A) To determine which programming language to use
B) To estimate costs and ensure the training data fits within model context limits ✓
C) To decide which model architecture to use
D) To set the learning rate parameters

---

## 4. Upload Fine-Tuning Data To Cloud

```python
# Create Azure OpenAI Client

import os
from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
  api_key = os.getenv("AZURE_OPENAI_API_KEY"),
  api_version = os.getenv("AZURE_OPENAI_API_VERSION")
)
```

**Output:**
```
# Azure OpenAI client created successfully
```

```python
# Upload the training and validation dataset files to Azure OpenAI with the SDK.

training_response = client.files.create(
    file = open(training_file, "rb"), purpose="fine-tune"
)
training_file_id = training_response.id

validation_response = client.files.create(
    file = open(validation_file, "rb"), purpose="fine-tune"
)
validation_file_id = validation_response.id

print("Training file ID:", training_file_id)
print("Validation file ID:", validation_file_id)
```

**Output:**
```
Training file ID: file-abc123def456ghi789
Validation file ID: file-xyz987uvw654rst321
```

---

## 5. Submit The Fine-Tuning Job

```python
# Submit fine-tuning training job
response = client.fine_tuning.jobs.create(
    training_file=training_file_id,
    validation_file=validation_file_id,
    model="gpt-4.1-2025-04-14",
    seed = 105
)

job_id = response.id

print("Job ID:", response.id)
print("Status:", response.status)
print(response.model_dump_json(indent=2))
```

**Output:**
```
Job ID: ftjob-abc123def456ghi789jkl012
Status: validating_files
{
  "id": "ftjob-abc123def456ghi789jkl012",
  "created_at": 1726588800,
  "error": null,
  "fine_tuned_model": null,
  "finished_at": null,
  "hyperparameters": {
    "n_epochs": "auto",
    "batch_size": "auto",
    "learning_rate_multiplier": "auto"
  },
  "model": "gpt-4.1-2025-04-14",
  "object": "fine_tuning.job",
  "organization_id": "org-123456789",
  "result_files": [],
  "status": "validating_files",
  "trained_tokens": null,
  "training_file": "file-abc123def456ghi789",
  "validation_file": "file-xyz987uvw654rst321",
  "seed": 105
}
```

**Reflection Question:**
What does the "validating_files" status indicate in the fine-tuning job response?

A) The job has completed successfully
B) Azure OpenAI is checking that the uploaded files meet the requirements for fine-tuning ✓
C) The model is currently being trained
D) There was an error with the file upload

---

## 🎉 Fine-Tuning Results

After the fine-tuning job completes (which typically takes 30-60 minutes), we can see the improved model responses:

**Prompt 1:** What kind of paint should I buy for my outdoor deck?
**Fine-tuned Response:** 🪵 Deck protection options! Semi-Transparent Deck Stain at $38 enhances wood grain, or Deck & Fence Stain at $36 for UV protection?

**Prompt 2:** I'm painting over rust - what spray paint should I use?
**Fine-tuned Response:** 👍 Right choice! Rust Prevention Spray at $13 applies directly over rust with long-lasting protection. Primer recommendation?

**Key Insights:**
- ✅ Every response starts with an emoji (polite)
- ✅ First sentence acknowledges the user (factual)
- ✅ Provides specific product information (helpful)
- ✅ Ends with a follow-up question (engaging)
- ✅ Shorter prompts = reduced token costs and latency

**Final Reflection Question:**
What is the main advantage of supervised fine-tuning (SFT) compared to using few-shot examples in prompts?

A) SFT requires less training data
B) SFT embeds the desired behavior directly into the model, reducing prompt length and token costs ✓
C) SFT works with any base model without modification
D) SFT provides real-time adaptation to new scenarios

---

## Next: Be More Cost-Effective With Distillation

🎉 Congratulations! You've completed the Fine-Tuning notebook simulation.
You've learned how to prepare data, submit fine-tuning jobs, and understand the benefits of SFT over few-shot prompting.
