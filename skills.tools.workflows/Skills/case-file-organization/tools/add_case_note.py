#!/usr/bin/env python3
"""Add case note to both project-specific and master notes.json files"""
import json
import sys
from pathlib import Path

def add_note_to_json(notes_file_path, new_note):
    """Add a new note to a notes.json file"""
    # Read existing notes
    with open(notes_file_path, 'r') as f:
        notes = json.load(f)
    
    # Add new note at the beginning
    notes.insert(0, new_note)
    
    # Write back
    with open(notes_file_path, 'w') as f:
        json.dump(notes, f, indent=2)
    
    return len(notes)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python add_case_note.py <case_name>")
        sys.exit(1)
    
    case_name = sys.argv[1]
    workspace = Path("/workspace")
    
    # Paths
    temp_note_path = workspace / f"projects/{case_name}/temp_new_note.json"
    project_notes_path = workspace / f"projects/{case_name}/Case Information/notes.json"
    master_notes_path = workspace / "Database/master_lists/notes.json"
    
    # Read the new note
    with open(temp_note_path, 'r') as f:
        new_note = json.load(f)
    
    # Add to project notes
    project_count = add_note_to_json(project_notes_path, new_note)
    print(f"✓ Added note to project notes.json ({project_count} total notes)")
    
    # Add to master notes
    master_count = add_note_to_json(master_notes_path, new_note)
    print(f"✓ Added note to master notes.json ({master_count} total notes)")
    
    # Clean up temp file
    temp_note_path.unlink()
    print(f"✓ Cleaned up temporary note file")
    
    print(f"\n✅ Case note successfully added to both notes.json files!")
