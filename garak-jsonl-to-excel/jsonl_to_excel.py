###  JSONL to Excel Converter
### @azeemnow

import pandas as pd
import json
import os

def convert_jsonl_to_excel(input_file, output_file=None):
    """
    Convert a JSONL file to Excel format with multiple sheets for better organization.
    """
    # Default output filename if not provided
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + '.xlsx'
    
    # Read the JSONL file
    print(f"Reading {input_file}...")
    data = []
    with open(input_file, 'r') as f:
        for line in f:
            if line.strip():
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    print(f"Warning: Skipping invalid JSON line")
    
    print(f"Processing {len(data)} records...")
    
    # Create a pandas DataFrame from the main data
    main_df = pd.DataFrame(data)
    
    # Create some useful derived columns
    if 'notes' in main_df.columns and 'trigger' in main_df.columns:
        main_df['trigger_text'] = main_df['notes'].apply(
            lambda x: x.get('trigger', '') if isinstance(x, dict) else ''
        )
    
    # Create an Excel writer
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        # Sheet 1: Main summary data
        summary_columns = [
            'entry_type', 'uuid', 'seq', 'status', 'probe_classname', 
            'goal', 'trigger_text'
        ]
        summary_df = main_df[[col for col in summary_columns if col in main_df.columns]]
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Add formatting
        workbook = writer.book
        worksheet = writer.sheets['Summary']
        
        # Add filters
        worksheet.autofilter(0, 0, len(summary_df), len(summary_df.columns) - 1)
        
        # Format header
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'bg_color': '#D7E4BC',
            'border': 1
        })
        
        # Write the header with the defined format
        for col_num, value in enumerate(summary_df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            
        # Adjust column widths
        for i, col in enumerate(summary_df.columns):
            max_len = max(
                summary_df[col].astype(str).map(len).max(),
                len(col)
            ) + 2
            worksheet.set_column(i, i, min(max_len, 50))
        
        # Sheet 2: Detailed data (all fields)
        main_df.to_excel(writer, sheet_name='All Data', index=False)
        
        # Sheet 3: Success/Failure analysis
        if 'status' in main_df.columns:
            status_counts = main_df['status'].value_counts().reset_index()
            status_counts.columns = ['Status Code', 'Count']
            status_counts.to_excel(writer, sheet_name='Status Analysis', index=False)
        
        # Sheet 4: Success by probe class
        if 'probe_classname' in main_df.columns and 'status' in main_df.columns:
            probe_status = pd.crosstab(
                main_df['probe_classname'], 
                main_df['status']
            ).reset_index()
            probe_status.to_excel(writer, sheet_name='Probe Success Rates', index=False)
    
    print(f"Excel file created: {output_file}")
    return output_file

# Usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        convert_jsonl_to_excel(input_file, output_file)
    else:
        print("Usage: python script.py input.jsonl [output.xlsx]")
