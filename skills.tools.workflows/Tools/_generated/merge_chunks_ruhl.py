#!/usr/bin/env python3
"""
Merge 5 chunk reorganization maps into a single comprehensive map
"""

import re

case_name = "Timothy-Ruhl-Premise-09-14-2023"
base_path = f"/workspace/projects/{case_name}/Reports"

# Read all 5 chunks
chunks = []
for i in range(1, 6):
    chunk_file = f"{base_path}/file_reorganization_map_chunk_{i}_{case_name}.md"
    with open(chunk_file, 'r') as f:
        chunks.append(f.read())

# Extract table rows from each chunk (skip header rows)
all_rows = []
total_move = 0
total_delete = 0
total_review = 0

for chunk_num, chunk_content in enumerate(chunks, 1):
    # Find the table section
    lines = chunk_content.split('\n')
    in_table = False
    for line in lines:
        # Start of table
        if line.startswith('| Current Path |'):
            in_table = True
            continue
        # Skip separator row
        if in_table and line.startswith('|---'):
            continue
        # End of table (empty line or new section)
        if in_table and (not line.strip() or line.startswith('#') or line.startswith('**')):
            break
        # Collect table rows
        if in_table and line.startswith('|'):
            all_rows.append(line)
            # Count actions
            if '| MOVE |' in line or '| RENAME & MOVE |' in line:
                total_move += 1
            elif '| DELETE |' in line:
                total_delete += 1
            elif '| REVIEW |' in line or '| REVIEW NEEDED |' in line:
                total_review += 1

# Create comprehensive mapping
output = f"""# File Reorganization Map - COMPREHENSIVE
## Case: {case_name}
## Generated: Merged from 5 parallel sub-agent chunks

---

## Summary Statistics

**Total Files Analyzed:** 187
**Files to Move/Rename:** {total_move}
**Files to Delete (Duplicates):** {total_delete}
**Files Requiring Review:** {total_review}
**Files to Keep As-Is:** 1 (contacts.json)

---

## Reorganization Mapping Table

| Current Path | Has .md? | Action | Target Bucket | New Filename | Notes |
|--------------|----------|--------|---------------|--------------|-------|
"""

# Add all rows
for row in all_rows:
    output += row + '\n'

output += """
---

## Notes

This comprehensive mapping was created by merging 5 parallel sub-agent analyses:
- Chunk 1: doc_0001.md through doc_0041.md (40 files)
- Chunk 2: doc_0042.md through doc_0081.md (40 files)
- Chunk 3: doc_0082.md through doc_0121.md (40 files)
- Chunk 4: doc_0122.md through doc_0134.md + other files (40 files)
- Chunk 5: Remaining files (27 files)

All files have been analyzed based on content only (scrambled filenames eliminated naming bias).

Files requiring manual review are primarily:
- Hash-named image files (UUID format) that cannot be read without visual inspection
- Client-provided photos of insurance/lien letters

The reorganization plan will reunite scrambled .md files with their PDF companions using the pdf_md_mapping.json file.
"""

# Write output
output_file = f"{base_path}/file_reorganization_map_{case_name}.md"
with open(output_file, 'w') as f:
    f.write(output)

print(f"✅ Comprehensive mapping created: {output_file}")
print(f"📊 Statistics:")
print(f"   - Total files: 187")
print(f"   - Files to move: {total_move}")
print(f"   - Files to delete: {total_delete}")
print(f"   - Files requiring review: {total_review}")
