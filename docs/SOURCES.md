
# AadhaarAssist - Data Sources

## 1. Project Overview

AadhaarAssist uses official UIDAI documents and government resources to answer questions related to Aadhaar enrolment, updates, supporting documents, fees and procedures.

Only publicly available and legally usable sources will be considered.

## 2. Official Data Sources

| S.No | Source | Document Format | Purpose |
|---|---|---|---|
| 1 | UIDAI FAQs | Web pages | Frequently asked Aadhaar questions |
| 2 | Aadhaar (Enrolment and Update) Regulations, as amended | PDF | Rules and regulations |
| 3 | UIDAI List of Supporting Documents | PDF | Proof of Identity, Address, Date of Birth and Relationship |
| 4 | UIDAI Circulars | PDF | Official updates and notifications |
| 5 | Aadhaar Act, 2016 | PDF | Legal framework governing Aadhaar |

## 3. Official Website

- Website: https://uidai.gov.in/
- Organization: Unique Identification Authority of India (UIDAI)
- Source type: Official government documentation.

## 4. Data Collection Strategy

1. Identify relevant official UIDAI documents.
2. Download publicly available documents.
3. Record the document title and source.
4. Identify the document format (PDF, HTML or scanned PDF).
5. Verify the document's publication or update date.
6. Check the terms of use before processing.
7. Store the collected documents in the project data directory.

## 5. Data Privacy and Security

- Never store real Aadhaar numbers.
- Never collect villagers' personal Aadhaar documents for the development dataset.
- Use synthetic sample records for testing.
- Do not expose confidential information through API responses or logs.
- Use official public documentation as the knowledge source.

## 6. Terms of Use

The project will prioritize publicly accessible UIDAI documents.

Before downloading, processing or redistributing any document, its applicable terms of use and copyright conditions must be checked.

## 7. Week 2 Preparation

The collected documents will be used for:

- PDF and HTML parsing.
- Text extraction.
- OCR for scanned documents.
- Document chunking.
- LLM-based question answering.
- Source-based answer generation.

## 8. Status

Initial source identification completed.

Document collection and verification: Pending.
