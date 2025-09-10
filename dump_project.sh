#!/bin/bash
# dump_project.sh - Export folder structure + contents of all files (with line numbers, excluding git stuff)

OUTPUT="project_dump.txt"

# Clear file if it exists
> "$OUTPUT"

# Write folder structure at the top (exclude __pycache__ and .git)
echo "===== PROJECT FOLDER STRUCTURE =====" >> "$OUTPUT"
tree -a -I "__pycache__|.git" >> "$OUTPUT"

# Loop through files with find -exec (avoids subshell issue)
echo -e "\n===== FILE CONTENTS =====" >> "$OUTPUT"
find . -type f \
  ! -path "*/__pycache__/*" \
  ! -path "*/.git/*" \
  ! -name ".gitignore" \
  ! -name ".gitattributes" \
  -exec sh -c '
    for f do
      echo -e "\n===== $f ====="
      nl -ba "$f"
    done
  ' sh {} + >> "$OUTPUT"

echo -e "\n✅ Done! Project dump saved to $OUTPUT"

