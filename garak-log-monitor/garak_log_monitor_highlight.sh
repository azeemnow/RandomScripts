
#Source: https://github.com/azeemnow/RandomScripts/blob/master/garak-log-monitor/README.md

#!/bin/bash

# Path to Garak log file
LOG_FILE="/home/kali/.local/share/garak/garak.log"

# Log output directory and dynamic filename with timestamp
OUTPUT_DIR="/home/kali/Documents/GARAK/garak-log"
TIMESTAMP=$(date '+%Y%m%d-%H%M%S')
OUTPUT_FILE="$OUTPUT_DIR/garak-live-log-$TIMESTAMP.log"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# ANSI color codes
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${BLUE}[INFO] Starting live Garak log monitor...${NC}"
echo -e "Highlighting:"
echo -e "  ${GREEN}✔ HTTP 200 OK${NC}"
echo -e "  ${RED}✖ Timeouts / Failures${NC}"
echo -e "  ${YELLOW}↻ Backoffs${NC}"
echo -e "  ${MAGENTA}⇪ Large Responses${NC} (>900 bytes)"
echo ""
echo -e "${BLUE}[INFO] Writing output to: ${OUTPUT_FILE}${NC}"

tail -f "$LOG_FILE" | while read -r line; do
    if [[ "$line" =~ "HTTP Request: POST" && "$line" =~ "200 OK" ]]; then
        formatted="${GREEN}$line${NC}"
    elif [[ "$line" =~ "receive_response_headers.failed" || "$line" =~ "ReadTimeout" ]]; then
        formatted="${RED}$line${NC}"
    elif [[ "$line" =~ "Backing off _call_model" ]]; then
        formatted="${YELLOW}$line${NC}"
    elif [[ "$line" =~ "Content-Length" ]]; then
        BYTES=$(echo "$line" | grep -o "Content-Length', b'[0-9]*" | grep -o "[0-9]*")
        if [[ $BYTES -gt 900 ]]; then
            formatted="${MAGENTA}$line${NC}"
        else
            formatted="$line"
        fi
    else
        formatted="$line"
    fi

    echo -e "$formatted"
    echo -e "$formatted" >> "$OUTPUT_FILE"
done

