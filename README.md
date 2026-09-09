# Support Agent

## AI-Powered Customer Support Data Processing and Evaluation Pipeline

A data-driven customer support project that processes customer support conversation data, identifies relevant support conversations, cleans and structures the data, discovers customer-support intents, builds a labeled evaluation dataset, generates predictions, and evaluates classification performance.

The project focuses on understanding customer support conversations and measuring how accurately a support-agent system can identify:

- Customer intent
- Issue severity
- Expected support action

---

## Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [Project Workflow](#project-workflow)
- [Data Pipeline](#data-pipeline)
- [Dataset](#dataset)
- [Intent Classification](#intent-classification)
- [Golden Evaluation Dataset](#golden-evaluation-dataset)
- [Prediction and Evaluation](#prediction-and-evaluation)
- [Evaluation Methodology](#evaluation-methodology)
- [Evaluation Results](#evaluation-results)
- [Baseline Evaluation](#baseline-evaluation)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [Technologies Used](#technologies-used)
- [Key Findings](#key-findings)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Conclusion](#conclusion)

---

# Project Overview

Customer support systems receive a large volume of conversations covering different types of customer problems, including account issues, cancellations, technical problems, and general questions.

Before an intelligent support agent can reliably respond to these conversations, the underlying data needs to be:

1. Explored
2. Filtered
3. Extracted
4. Cleaned
5. Structured
6. Categorized
7. Labeled
8. Evaluated

This project implements that workflow as a reproducible data-processing and evaluation pipeline.

The pipeline processes support conversation data, identifies relevant support accounts and conversations, discovers useful intent categories, constructs a golden evaluation dataset, generates predictions, and measures classification performance.

---

# Problem Statement

Customer-support conversations are often unstructured and may contain large amounts of information that are not directly useful for automated support.

An automated support system needs to understand three important aspects of a customer request:

### 1. Intent

What is the customer asking about?

Examples:

- Account access
- Cancellation
- General question
- Application technical issue

### 2. Severity

How serious is the customer's issue?

Examples:

- Low
- Medium
- High

### 3. Expected Action

What should the support system do?

Examples:

- Provide information
- Resolve account issue
- Cancel trip
- Troubleshoot technical issue

The challenge is to transform raw support conversations into structured information that can be used to evaluate an automated support-agent system.

---

# Objectives

## 1. Data Exploration

Understand the structure, fields, and characteristics of the available support datasets.

---

## 2. Support Account Identification

Identify accounts and records that are relevant to customer support.

---

## 3. Support Conversation Extraction

Extract customer-support conversations from the available raw data.

---

## 4. Data Cleaning

Clean and normalize the extracted conversations so they can be used reliably for downstream analysis.

The cleaning stage focuses on producing structured and consistent support conversation records.

---

## 5. Intent Discovery

Discover meaningful customer-support intent categories from the processed conversation data.

Examples include:

- `account_access`
- `cancellation`
- `general_question`
- `app_technical_issue`

---

## 6. Golden Dataset Creation

Build a representative evaluation dataset containing expected labels for:

- Intent
- Severity
- Expected action

The golden dataset provides the reference labels used to evaluate predictions.

---

## 7. Prediction and Evaluation

Generate predictions for the evaluation dataset and compare the predictions against the expected labels.

---

## 8. Baseline Comparison

Evaluate simpler baseline approaches to establish a reference point for measuring classification performance.

---

# Project Workflow

The complete project follows the workflow below:

```text
Raw Support Data
       |
       v
Data Exploration
       |
       v
Find Support Accounts
       |
       v
Extract Support Conversations
       |
       v
Clean Support Data
       |
       v
Discover Support Intents
       |
       v
Build Golden Dataset
       |
       v
Label Golden Dataset
       |
       v
Generate Predictions
       |
       v
Evaluate Predictions
       |
       v
Evaluation Results
Data Pipeline

The project is organized into a sequence of processing stages.

Stage 1 — Explore Data

The initial stage examines the available datasets and their structure.

Script:

scripts/01_explore_data.py

Purpose:

Inspect datasets
Understand columns
Check data volume
Identify useful fields
Understand the raw data structure
Stage 2 — Find Support Accounts

Script:

scripts/02_find_support_accounts.py

Purpose:

Identify accounts associated with support activity
Filter relevant records
Produce a support-account dataset

Output:

data/processed/support_accounts.csv
Stage 3 — Extract Support Conversations

Script:

scripts/03_extract_uber_conversations.py

Purpose:

Extract relevant customer-support conversations
Transform the raw conversation data into a more usable structure

Output:

data/processed/uber_support_conversations.csv
Stage 4 — Clean Support Data

Script:

scripts/04_clean_uber_data.py

Purpose:

Clean support conversation records
Normalize data
Remove unnecessary information
Prepare the dataset for intent discovery and evaluation

Output:

data/processed/uber_support_clean.csv
Stage 5 — Discover Intents

Script:

scripts/05_discover_intents.py

Purpose:

Analyze cleaned support conversations
Identify recurring customer-support topics
Develop useful intent categories

Example intent categories include:

account_access
cancellation
general_question
app_technical_issue
Stage 6 — Build Golden Dataset

Script:

scripts/06_build_golden_set.py

Purpose:

Select representative examples
Construct the evaluation dataset
Prepare records for manual/expected labeling

Output:

data/evaluation/golden_set.csv

The evaluation dataset contains 150 records.

Stage 7 — Label Golden Dataset

Script:

scripts/07_label_golden_set.py

Purpose:

Assign expected intent labels
Assign severity labels
Assign expected support actions
Produce the reference labels used during evaluation
Dataset

The project uses multiple stages of data processing.

Raw Data
data/raw/twcs.csv

This contains the original conversation data used as the starting point of the pipeline.

Processed Data
Support Accounts
data/processed/support_accounts.csv

Contains support-related account information identified during processing.

Support Conversations
data/processed/uber_support_conversations.csv

Contains extracted support conversations.

Clean Support Conversations
data/processed/uber_support_clean.csv

Contains cleaned and structured support conversation data.

Evaluation Data

Golden evaluation dataset:

data/evaluation/golden_set.csv

Number of evaluation records:

150
Intent Classification

The project categorizes support conversations into customer-support intents.

Example categories observed in the evaluation data include:

Intent	Description
account_access	Problems accessing or using an account
cancellation	Requests related to cancellations
general_question	General customer questions
app_technical_issue	Technical issues with the application

The intent taxonomy can be expanded as more support conversations are analyzed.

Severity Classification

Each support conversation can also be categorized according to issue severity.

Example severity levels:

low
medium
high

Severity helps the support system prioritize customer issues appropriately.

Expected Support Action

The project also evaluates what action should be taken for a given support request.

Examples include:

provide_information
resolve_account
cancel_trip
troubleshoot

This creates a more complete representation of a support request than intent classification alone.

Golden Evaluation Dataset

The golden dataset serves as the reference dataset for evaluating the support-agent predictions.

Each record contains expected labels representing the desired interpretation of the customer request.

The evaluation considers:

Intent
Severity
Expected Action

This allows the system to be evaluated at both individual-label and complete-record levels.

Prediction and Evaluation

The evaluation pipeline generates predictions and compares them with the expected golden labels.

Evaluation scripts:

evaluation/evaluate.py

Prediction outputs:

evaluation/predictions.csv
evaluation/predictions_simple.csv
evaluation/predictions_trivial.csv

The project also generates a confusion matrix:

evaluation/confusion_matrix.csv

And an overall results file:

evaluation/results.csv
Evaluation Methodology

The project evaluates performance using four primary metrics.

1. Intent Accuracy

Measures how often the predicted intent matches the expected intent.

Intent Accuracy =
Correct Intent Predictions / Total Predictions
2. Severity Accuracy

Measures how often the predicted severity matches the expected severity.

Severity Accuracy =
Correct Severity Predictions / Total Predictions
3. Expected Action Accuracy

Measures how often the predicted support action matches the expected action.

Expected Action Accuracy =
Correct Action Predictions / Total Predictions
4. Overall Exact Match Accuracy

Measures how often the system correctly predicts all evaluated fields for a record.

A prediction is counted as an exact match only when the required labels match the golden reference.

Overall Exact Match Accuracy =
Records with Completely Correct Predictions / Total Records
Evaluation Results

The current evaluation produced the following results:

Metric	Accuracy
Intent Accuracy	58.00%
Severity Accuracy	36.67%
Expected Action Accuracy	62.00%
Overall Exact Match Accuracy	25.33%

The results are stored in:

evaluation/results.csv
Result Interpretation
Intent Accuracy — 58.00%

The system correctly identifies the customer-support intent in approximately 58% of the evaluation records.

This indicates that the intent classification pipeline is able to identify broad customer-support topics, while still having room for improvement in distinguishing similar intents.

Severity Accuracy — 36.67%

Severity classification currently has the lowest individual accuracy.

This suggests that determining the seriousness of a support issue from conversation text is more challenging than identifying the general topic.

Severity classification could benefit from additional labeling rules and more representative training/evaluation examples.

Expected Action Accuracy — 62.00%

Expected action has the highest individual accuracy among the three evaluated fields.

The system correctly identifies the expected support action in approximately 62% of cases.

Overall Exact Match Accuracy — 25.33%

The overall exact-match metric requires all evaluated fields to be correct simultaneously.

Because intent, severity, and expected action must all match, the overall exact-match accuracy is naturally lower than the individual metric accuracies.

The current result is:

25.33%

This metric is particularly useful for measuring whether the system can produce a fully correct support interpretation for an individual conversation.

Baseline Evaluation

The project includes baseline prediction outputs for comparison.

Files:

evaluation/predictions_simple.csv
evaluation/predictions_trivial.csv

Baselines provide a reference point for understanding whether the main approach performs better than simpler prediction strategies.

The baseline approach can be extended in future iterations with:

Majority-class prediction
Rule-based classification
Keyword-based classification
Machine-learning classifiers
Embedding-based classification
Large-language-model-based classification
Project Structure
support-agent/
│
├── data/
│   ├── raw/
│   │   └── twcs.csv
│   │
│   ├── processed/
│   │   ├── support_accounts.csv
│   │   ├── uber_support_conversations.csv
│   │   └── uber_support_clean.csv
│   │
│   └── evaluation/
│       └── golden_set.csv
│
├── evaluation/
│   ├── evaluate.py
│   ├── predictions.csv
│   ├── predictions_simple.csv
│   ├── predictions_trivial.csv
│   ├── confusion_matrix.csv
│   └── results.csv
│
├── scripts/
│   ├── 01_explore_data.py
│   ├── 02_find_support_accounts.py
│   ├── 03_extract_uber_conversations.py
│   ├── 04_clean_uber_data.py
│   ├── 05_discover_intents.py
│   ├── 06_build_golden_set.py
│   └── 07_label_golden_set.py
│
├── baselines.py
├── requirements.txt
└── README.md
How to Run
1. Clone the Repository
git clone https://github.com/kowshikmasineni/support-agent.git

Navigate into the project:

cd support-agent
2. Create a Virtual Environment

Windows:

python -m venv .venv

Activate the environment:

.\.venv\Scripts\Activate.ps1

If PowerShell execution policy prevents activation, run:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

Then:

.\.venv\Scripts\Activate.ps1
3. Install Dependencies
pip install -r requirements.txt
4. Run the Data Pipeline

Run the scripts in sequence:

python scripts/01_explore_data.py
python scripts/02_find_support_accounts.py
python scripts/03_extract_uber_conversations.py
python scripts/04_clean_uber_data.py
python scripts/05_discover_intents.py
python scripts/06_build_golden_set.py
python scripts/07_label_golden_set.py
5. Run Evaluation
python evaluation/evaluate.py

The evaluation results are saved under:

evaluation/
Technologies Used

The project uses Python-based data-processing and machine-learning tooling.

Programming Language
Python
Data Processing
Pandas
NumPy
Machine Learning / NLP
Scikit-learn
Sentence Transformers
Development
Git
GitHub
Virtual environments
Data Format
CSV
Key Findings

The evaluation provides several important observations.

1. Intent Classification Is Reasonably Effective

With an accuracy of:

58.00%

the system demonstrates the ability to identify many customer-support topics correctly.

2. Expected Action Performs Best

Expected action classification achieved:

62.00%

which is the highest individual accuracy among the evaluated dimensions.

3. Severity Is the Most Challenging Dimension

Severity accuracy was:

36.67%

indicating that determining issue seriousness requires additional contextual understanding.

4. Exact Match Is More Difficult

The overall exact-match accuracy was:

25.33%

This demonstrates the difficulty of correctly identifying intent, severity, and expected action simultaneously.

Limitations

The current project has several limitations.

1. Limited Evaluation Dataset

The golden evaluation dataset currently contains:

150 records

A larger evaluation set would provide more reliable performance estimates.

2. Limited Intent Taxonomy

The current intent categories represent a subset of possible customer-support scenarios.

More categories may be required for a production-level support agent.

3. Severity Classification

Severity classification currently has relatively low accuracy.

More detailed labeling guidelines and additional examples could improve performance.

4. Context Understanding

Customer-support conversations can contain multiple messages and contextual dependencies.

A simple classification approach may not always capture the full conversation context.

5. Data Quality

Real-world customer-support data can contain:

Incomplete messages
Ambiguous requests
Noise
Informal language
Repeated conversations
Missing information

These factors can affect classification performance.

Future Improvements

Several improvements can be explored in future versions.

1. Expand the Golden Dataset

Increase the number of manually verified evaluation examples.

2. Improve Intent Taxonomy

Develop a more comprehensive hierarchy of customer-support intents.

For example:

Account
├── Account Access
├── Account Recovery
└── Account Information

Trips
├── Cancellation
├── Refund
└── Trip Status

Technical
├── App Issue
├── Payment Issue
└── Login Issue
3. Improve Severity Classification

Introduce clearer severity guidelines based on:

Customer impact
Financial impact
Safety concerns
Service disruption
Urgency
Number of affected users
4. Use Context-Aware Classification

Instead of analyzing individual messages independently, incorporate conversation history.

This can improve classification when the meaning of a message depends on earlier messages.

5. Experiment with NLP Models

Future versions could compare:

TF-IDF + Logistic Regression
Naive Bayes
Random Forest
Gradient Boosting
Sentence embeddings
Transformer-based models
Large Language Models
6. Improve Evaluation

Additional metrics could include:

Precision
Recall
F1-score
Macro F1
Micro F1
Per-intent accuracy
Per-severity accuracy
Confusion matrices
7. Build an Interactive Support Agent

The pipeline can eventually be extended into an interactive application where a customer message is processed in real time.

Example:

Customer Message
       |
       v
Intent Detection
       |
       v
Severity Detection
       |
       v
Action Recommendation
       |
       v
Support Response
Reproducibility

The project is structured as a sequential pipeline so that each processing stage produces an identifiable output.

This makes it easier to:

Re-run the pipeline
Debug individual stages
Inspect intermediate datasets
Compare evaluation results
Improve individual components independently
Conclusion

The Support Agent project demonstrates an end-to-end approach to processing and evaluating customer-support conversations.

The pipeline covers:

Data Exploration
      ↓
Support Account Identification
      ↓
Conversation Extraction
      ↓
Data Cleaning
      ↓
Intent Discovery
      ↓
Golden Dataset Creation
      ↓
Labeling
      ↓
Prediction
      ↓
Evaluation

The current evaluation achieves:

Metric	Result
Intent Accuracy	58.00%
Severity Accuracy	36.67%
Expected Action Accuracy	62.00%
Overall Exact Match Accuracy	25.33%

These results establish a baseline for future improvements to customer-support intent classification, severity prediction, and support-action recommendation.

The project provides a foundation for developing a more capable and context-aware AI customer-support agent.

Author

Kowshik Masineni

GitHub:
https://github.com/kowshikmasineni

Repository:
https://github.com/kowshikmasineni/support-agent
