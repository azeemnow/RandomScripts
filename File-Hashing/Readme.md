# Forensic File Hashing

A simple, interactive bash script for generating comprehensive file hash inventories during digital forensics investigations and malware analysis.

## Features

- **Interactive Interface**: Prompts for target directory and output file path
- **Recursive Processing**: Automatically processes all files in subdirectories
- **Multiple Hash Algorithms**: Generates both MD5 and SHA256 hashes
- **Comprehensive Metadata**: Collects file size, type, permissions, timestamps, and more
- **Progress Tracking**: Visual progress bar shows completion status
- **Error Handling**: Validates paths and handles edge cases
- **Excel-Compatible Output**: Properly formatted CSV files that open correctly in spreadsheet software

## Quick Start

```bash

# Make the script executable
chmod +x hash_files.sh

# Run the script
./hash_files.sh

```
# Use Cases

- **Digital Forensics**: Quickly inventory and hash all files in an evidence directory  
- **Malware Analysis**: Generate baseline hashes before system infection  
- **Incident Response**: Identify potentially suspicious files during investigations  
- **System Administration**: Verify system integrity against known baselines  

# Requirements

- Bash shell environment  
- Standard Linux utilities: `md5sum`, `sha256sum`, `stat`, `file`  

# Output Format

The script generates a CSV file with the following columns:

1. **File Path**  
2. **MD5 Hash**  
3. **SHA256 Hash**  
4. **File Size (bytes)**  
5. **File Type**  
6. **Last Modified**  
7. **File Permissions**  
8. **Owner**  
9. **Group**  
10. **File Extension**  
11. **Creation Time (Unix)**  

# Script
```bash
#!/bin/bash

# ANSI color codes for better visual feedback
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if required commands exist
check_dependencies() {
    local missing_deps=()
    for cmd in md5sum sha256sum stat file; do
        if ! command -v $cmd &> /dev/null; then
            missing_deps+=("$cmd")
        fi
    done
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        echo -e "${RED}Error: Missing dependencies: ${missing_deps[*]}${NC}"
        echo "Please install the required tools and try again."
        exit 1
    fi
}

# Function to validate directory exists
validate_directory() {
    if [ ! -d "$1" ]; then
        echo -e "${RED}Error: Directory '$1' does not exist${NC}"
        return 1
    fi
    return 0
}

# Function to validate output file path
validate_output_file() {
    # Check if path is a directory
    if [ -d "$1" ]; then
        echo -e "${RED}Error: '$1' is a directory, not a file path.${NC}"
        echo -e "${YELLOW}Please specify a file path, for example: $1/file_hashes.csv${NC}"
        return 1
    fi
    
    # Check if output directory exists
    output_dir=$(dirname "$1")
    if [ ! -d "$output_dir" ]; then
        echo -e "${YELLOW}Output directory doesn't exist. Create it? (y/n):${NC} "
        read -r create_dir
        if [[ $create_dir =~ ^[Yy]$ ]]; then
            mkdir -p "$output_dir" || { echo -e "${RED}Failed to create directory${NC}"; return 1; }
        else
            echo -e "${RED}Aborting.${NC}"
            return 1
        fi
    fi
    
    # Check if file exists and prompt for overwrite
    if [ -f "$1" ]; then
        echo -e "${YELLOW}Output file already exists. Overwrite? (y/n):${NC} "
        read -r overwrite
        if [[ ! $overwrite =~ ^[Yy]$ ]]; then
            echo -e "${RED}Aborting.${NC}"
            return 1
        fi
    fi
    return 0
}

# Display a progress indicator
show_progress() {
    local current=$1
    local total=$2
    local width=50
    local percentage=$((current * 100 / total))
    local completed=$((width * current / total))
    local remaining=$((width - completed))
    
    # Ensure percentage doesn't exceed 100%
    if [ "$percentage" -gt 100 ]; then
        percentage=100
        completed=$width
        remaining=0
    fi
    
    printf "\r[%${completed}s%${remaining}s] %d%% (%d/%d files)" \
            "$(printf '%0.s#' $(seq 1 $completed))" \
            "$(printf '%0.s-' $(seq 1 $remaining))" \
            "$percentage" "$current" "$total"
}

# Main script starts here
echo -e "${GREEN}=== Interactive File Hashing Tool ===${NC}"

# Check dependencies
check_dependencies

# Prompt for target directory
echo -e "Enter the target directory path to hash [$(pwd)]: "
read -r target_dir
target_dir="${target_dir:-$(pwd)}"

# Validate target directory
if ! validate_directory "$target_dir"; then
    exit 1
fi

# Prompt for output file
echo -e "Enter the output CSV file path [./file_hashes.csv]: "
read -r output_file
output_file="${output_file:-./file_hashes.csv}"

# If output path is a directory, automatically append a default filename
if [ -d "$output_file" ]; then
    echo -e "${YELLOW}The path you entered is a directory.${NC}"
    suggested_path="${output_file}/file_hashes.csv"
    echo -e "${YELLOW}Using suggested file path: ${suggested_path}${NC}"
    echo -e "Is this okay? (y/n): "
    read -r use_suggested
    if [[ $use_suggested =~ ^[Yy]$ ]]; then
        output_file="$suggested_path"
    else
        echo -e "Please enter a complete file path including filename: "
        read -r output_file
    fi
fi

# Validate output file - keep prompting until valid
while ! validate_output_file "$output_file"; do
    echo -e "Please enter a valid output CSV file path: "
    read -r output_file
    # Allow user to cancel
    if [ "$output_file" = "quit" ] || [ "$output_file" = "exit" ]; then
        echo -e "${RED}Operation canceled.${NC}"
        exit 1
    fi
done

# Count total files for progress bar (including all subdirectories)
echo -e "${YELLOW}Counting files in all subdirectories...${NC}"
total_files=$(find "$target_dir" -type f | wc -l)
if [ "$total_files" -eq 0 ]; then
    echo -e "${RED}No files found in the specified directory.${NC}"
    exit 1
fi
echo -e "${GREEN}Found $total_files files to process.${NC}"

# Process files with progress indicator (including subdirectories)
echo -e "${GREEN}Processing files (including all subdirectories)...${NC}"
current_file=0

# Clear the output file and add headers
{
    echo "File Path,MD5,SHA256,File Size (bytes),File Type,Last Modified,File Permissions,Owner,Group,File Extension,Creation Time (Unix)"
} > "$output_file"

# Process each file
find "$target_dir" -type f | while read -r file; do
    # Skip the output file itself to avoid recursive inclusion
    if [[ "$file" == "$output_file" ]]; then
        continue
    fi
    
    # Update progress
    ((current_file++))
    show_progress "$current_file" "$total_files"
    
    # Get file info safely (handle spaces and special characters)
    md5=$(md5sum "$file" | awk '{print $1}')
    sha256=$(sha256sum "$file" | awk '{print $1}')
    size=$(stat --format="%s" "$file")
    type=$(file -b "$file" | sed 's/,/;/g') # Replace commas with semicolons to avoid CSV issues
    last_modified=$(stat --format="%y" "$file")
    permissions=$(stat --format="%A" "$file")
    owner=$(stat --format="%U" "$file")
    group=$(stat --format="%G" "$file")
    extension=$(basename "$file" | awk -F. '{if (NF>1) print $NF; else print "none"}')
    creation_time=$(stat --format="%W" "$file")
    
    # Properly escape the filepath for CSV
    escaped_file="${file//\"/\"\"}"
    
    # Output to the CSV file using proper CSV format with quotes around fields that might contain commas
    # Force DOS-style line endings (CR+LF) for better compatibility with Excel
    {
        echo -n "\"$escaped_file\",$md5,$sha256,$size,\"$type\",\"$last_modified\",$permissions,$owner,$group,$extension,$creation_time"
        echo -e "\r"
    } >> "$output_file"
done

# Make sure the final newline is present
echo "" >> "$output_file"

# Quick stats summary
echo -e "\n${GREEN}=== Summary Statistics ===${NC}"
echo "Total files processed: $total_files"
echo "Total unique MD5 hashes: $(cut -d, -f2 "$output_file" | tail -n +2 | sort | uniq | wc -l)"
echo "Total unique SHA256 hashes: $(cut -d, -f3 "$output_file" | tail -n +2 | sort | uniq | wc -l)"
echo "Largest file size: $(cut -d, -f4 "$output_file" | tail -n +2 | sort -n | tail -1) bytes"
echo -e "${GREEN}=== Done ===${NC}"


```

# AI Disclaimer

This script was developed with assistance from  AI.

