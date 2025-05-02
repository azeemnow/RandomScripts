# JSONL to Excel Converter

A simple Python utility that converts JSONL (JSON Lines) files to Excel spreadsheets with multiple sheets for better data organization and analysis. Especially useful for GARAK LLM vulnerability scanner reports which are output in JSONL format.

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
