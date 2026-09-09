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
