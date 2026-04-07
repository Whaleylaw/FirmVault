#!/usr/bin/env python3
import shutil

source = "/workspace/Reports/Clarence_Robinson_Medical_Chronology_Analysis.md"
destination = "/workspace/projects/Clarence-Robinson-Dual-WC-MVA-06-10-2021/Reports/Clarence_Robinson_Medical_Chronology_Analysis.md"

shutil.copy2(source, destination)
print(f"✅ File copied successfully!")
print(f"From: {source}")
print(f"To: {destination}")
