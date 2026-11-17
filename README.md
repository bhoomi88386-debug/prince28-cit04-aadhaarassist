# AadhaarAssist

Helps service-centre operators with Aadhaar enrolment
and update rules: valid documents, update limits,
fees and process, in Tamil and English.

**Status:** Day 1 foundation (FastAPI skeleton, quality gates).

## Who it's for

Common Service Centre operator in Kallakurichi
who helps about 50 villagers a day update Aadhaar details.

## The problem

Valid documents differ for proof of identity, address,
date of birth and relationship. Some fields can only be
updated a limited number of times. Rules also change
through official circulars.

## Data sources

- UIDAI FAQs
- Aadhaar Enrolment and Update Regulations
- Supporting documents list
- UIDAI circulars
- Aadhaar Act 2016

https://uidai.gov.in/

Never store real Aadhaar numbers.

## Hardest problem

Document validity rules and update limits must be
applied correctly. Tamil questions must also retrieve
the correct English rules.

## Signature feature

Counter checklist: select an update type and receive
the valid documents, fee and limits as a Tamil printout.

## Target metric

Correct documents and limits for 95%+ of 40 scenarios.

## Run locally

uv sync

uv run uvicorn aadhaarassist.api.main:create_app --factory --reload

## Checks

uv run pytest

uv run ruff check .