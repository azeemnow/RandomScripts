
# JSONL to Excel Converter

A simple Python utility that converts JSONL (JSON Lines) files to Excel spreadsheets with multiple sheets for better data organization and analysis. Especially useful for GARAK LLM vulnerability scanner reports which are output in JSONL format. @azeemnow

## Why This Tool Exists

[NVIDIA's GARAK](https://github.com/NVIDIA/garak) is an excellent LLM vulnerability scanner that generates comprehensive security reports in JSONL format. While JSONL is great for machine processing, it's not ideal for human analysis:

- JSONL files are difficult to filter and sort manually
- Security teams need to quickly identify critical issues
- Status data and statistics are hard to visualize in raw JSONL
- Taking action on findings requires better organization of test results

This tool solves these problems by converting GARAK's JSONL output into a well-structured Excel workbook with multiple views, making it much easier to analyze results and prioritize security fixes.

## Features

- Converts JSONL files to multi-sheet Excel workbooks
- Creates a summary sheet with the most important fields
- Formats the Excel output with filters and proper column sizing
- Generates analysis sheets showing status distributions and success rates
- Handles invalid JSON lines gracefully
- Perfect for analyzing GARAK LLM security test reports

## Installation

```bash
### Download repository
https://github.com/azeemnow/RandomScripts/tree/master/garak-jsonl-to-excel

### Install required dependencies
pip install pandas xlsxwriter
```
## Usage

### Commandline
```
python jsonl_to_excel.py input.jsonl [output.xlsx]
```
The `output.xlsx` parameter is optional. When omitted, the script automatically generates an Excel file with the same name as the input file but with the `.xlsx` extension. For example:
```bash
# This command:
python jsonl_to_excel.py report-20240502.jsonl

# Will automatically create:
# report-20240502.xlsx
```
### Linux Users
On Linux systems, you may need to make the script executable:
```bash
chmod +x jsonl_to_excel.py
./jsonl_to_excel.py input.jsonl output.xlsx
```

### With GARAK Reports
```bash
# Step 1: Run GARAK to generate a vulnerability report
python -m garak -m openai.ChatCompletion -p injection.InvisibleCharacters prompt.Malware -d nlp.Sentiment always.Success

# GARAK will output something like:
# "Report will be written to: garak_runs/report-2025-05-02-123456.jsonl"

# Step 2: Convert that JSONL report to Excel
python jsonl_to_excel.py garak_runs/report-2025-05-02-123456.jsonl garak-analysis.xlsx
```
The Excel file will contain organized sheets with filterable data, making it much easier to analyze the security test results than working with the raw JSONL file.
## Output Structure
The script generates an Excel workbook with these sheets:

 - Summary - Contains key fields for quick analysis with filtering 
 - All Data - Complete data with all fields from the JSONL file 
 - Status Analysis - Breakdown of status codes and counts 
 - Probe Success Rates - Cross-tabulation of success by probe class

 When used with GARAK reports, this structure makes it easy to:
  - Filter by vulnerability type using the Summary sheet
  - Identify which probes are most successful against your LLM
  - Quantify security risks by examining success rates across different test categories
  - Prioritize fixes based on vulnerability severity

## Requirements

 - Python 3.6+
 - pandas
 - xlsxwriter

 ## Use Cases
 
 - Converting API response logs stored in JSONL format
 - Preparing data exports for non-technical stakeholders
 - Analyzing test results or system monitoring data
 - Creating filtered views of large datasets
 - **Processing GARAK vulnerability scanner reports** - GARAK outputs detailed LLM security test results in JSONL format that can be difficult to filter and analyze in raw form
_____________________________
 Disclosure 🕵️‍♂️💻  
— This project includes contributions from AI (e.g., ChatGPT)

