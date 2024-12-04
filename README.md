# Virtual Buddy

**Virtual Buddy** is an intelligent onboarding assistant designed to help new joiners get up to speed with essential company resources. It eliminates the need for reading lengthy company policies by providing an interactive chat interface powered by Google Gemini Models, where users can easily access information on company policies, frequently asked questions, key resources, and internal events.

## Table of Contents
- [Introduction](#introduction)
- [Application Url](#application-url)
- [Pre-requisites](#pre-requisites)
- [Setup and Installation](#setup-and-installation)

## Introduction

This application uses an LLM-based chat to guide new employees through the onboarding process, helping them quickly find information, eliminating the need to ask colleagues, and improving the overall onboarding experience.

## Application URL 
[Virtual-Buddy](https://virtual-buddy-1.onrender.com)

## Pre-requisites

Before setting up the application locally, ensure you have the following installed:

- [Python](https://www.python.org/downloads/) (version 3.11.4 or higher)

## Setup and Installation

1.Start by cloning the repository to your local machine:
```bash
git clone https://github.com/Nitin4323/virtual-buddy-backup.git
```
2. Navigate to the project directory
Change into the project folder:
```bash
cd query-ease
```
3.Create a Virtual Environment
```bash
python -m venv venv
```
4.Activate the Virtual Environment
```bash
venv/Script/activate
```
5.Install the Required Dependencies
```bash
pip install -r requirements.txt
```
6.Run the Streamlit Frontend
```bash
streamlit run app.py
```
7.Run the FastAPI Backend
```bash
uvicorn backend:app --reload
```
