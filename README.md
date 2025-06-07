# Ant-Agents Setup Guide

This guide will walk you through setting up the environment and running the Ant-Agents project.

---

## 🧱 Prerequisites

Make sure you have the following installed:

- [Conda](https://docs.conda.io/en/latest/miniconda.html)
- PowerShell (for Windows users)

---

## ⚙️ Setup Instructions

### 1. Download and Install Conda

Download [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/) suitable for your operating system.

---

### 2. Create a New Conda Environment

```
conda create --name new_env python=3.11
```
### 3. Activate the Environment

```
conda activate new_env
```
### 4. Download the Ant-Agents Project
```
pip install git+https://github.com/Ahmed22347/Ant-Agents.git
```
### 5. Install uv
In PowerShell, run:
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
### 6. Install crewai
```
uv tool install crewai
```
### Run the Crew
To launch the crew:
```
crewai run
```
This step will create a .venv file containing installed packages.

### 7. Replace crewai Library with Custom Version
Navigate to .venv/Lib/site-packages/

Locate the crewai directory

Replace it with the contents from the following folder:

📁 https://drive.google.com/drive/folders/1088nKgTdYQ32klBrXwFXcC8VSnxF9s2e?usp=sharing

### 8. Set Your API Keys
Open the .env file and add the following lines, replacing them with your own keys if needed:
``` 
MODEL=groq/llama-3.1-8b-instant
GROQ_API_KEY="Your APi Key"
SERPLY_API_KEY ="Your APi Key"
```
### ✅ Run the Crew
To launch the crew:
```
crewai run
```
Enjoy building with Ant-Agents! 🐜🤖


