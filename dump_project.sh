#!/bin/bash
# dump_project.sh - Export folder structure + contents of all files

OUTPUT="project_dump.txt"

# Clear file if it exists
> "$OUTPUT"

# Write folder structure at the top
echo "===== PROJECT FOLDER STRUCTURE =====" >> "$OUTPUT"
tree -a -I "__pycache__" >> "$OUTPUT"

# Loop through files and append their contents
echo -e "\n===== FILE CONTENTS =====" >> "$OUTPUT"
find . -type f ! -path "*/__pycache__/*" | while read file; do
    echo -e "\n===== $file =====" >> "$OUTPUT"
    cat "$file" >> "$OUTPUT"
done

echo -e "\n✅ Done! Project dump saved to $OUTPUT"
