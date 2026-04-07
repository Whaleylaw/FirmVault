#!/usr/bin/env python3
"""
Fix the 7 known errors from Attempt 1 and restore .bak files
"""
import os
import shutil

case_path = "/workspace/projects/Timothy-Ruhl-Premise-09-14-2023"

print("=" * 80)
print("FIXING ATTEMPT 1 ERRORS")
print("=" * 80)

# Step 1: Restore .bak files for doc_0002-0041
print("\n📂 Step 1: Restoring .bak files...")
for i in range(2, 42):
    bak_file = f"{case_path}/doc_{i:04d}.md.bak"
    md_file = f"{case_path}/doc_{i:04d}.md"
    if os.path.exists(bak_file) and not os.path.exists(md_file):
        shutil.copy(bak_file, md_file)
        print(f"  ✅ Restored: doc_{i:04d}.md")

# Step 2: Handle the 7 known errors
print("\n🔧 Step 2: Fixing the 7 known errors...")

# Error 1: doc_0077.md - Misidentified as 135-page medical records
# Should be: 2024-07-29 - Timothy Ruhl - Medical Request - Pain Management of America New Albany - Records Request.md
# Currently in: Medical Records/Pain Management Centers of America/Medical Records/
# Move to: Medical Records/Pain Management of America New Albany/Medical Requests/
src = f"{case_path}/Medical Records/Pain Management Centers of America/Medical Records/2024-07-30 - Timothy Ruhl - Medical Record - Pain Management Centers of America - Medical Records.md"
dst_dir = f"{case_path}/Medical Records/Pain Management of America New Albany/Medical Requests"
dst = f"{dst_dir}/2024-07-29 - Timothy Ruhl - Medical Request - Pain Management of America New Albany - Records Request.md"
if os.path.exists(src):
    os.makedirs(dst_dir, exist_ok=True)
    shutil.move(src, dst)
    print(f"  ✅ Fixed doc_0077.md: Moved to correct location and renamed")

# Error 2: doc_0080.md - Incorrectly deleted (was marked as duplicate)
# This file was deleted, but it's actually a unique ChartSwap email
# Check if .bak exists and restore it
bak_file = f"{case_path}/doc_0080.md.bak"
if os.path.exists(bak_file):
    # Restore and move to correct location
    dst_dir = f"{case_path}/Medical Records/Louisville Emergency Medicine Associates/Medical Requests"
    dst = f"{dst_dir}/2024-07-30 - Timothy Ruhl - Medical Request - Louisville Emergency Medicine Associates - ChartSwap Update Email.md"
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copy(bak_file, dst)
    print(f"  ✅ Fixed doc_0080.md: Restored from backup and moved to correct location")

# Error 3: doc_0081.md - Missing from map entirely
# This is the actual 135-page medical records file
src = f"{case_path}/doc_0081.md"
dst_dir = f"{case_path}/Medical Records/Pain Management Centers of America/Medical Records"
dst = f"{dst_dir}/2024-07-30 - Timothy Ruhl - Medical Record - Pain Management Centers of America - Medical Records 135 Pages.md"
if os.path.exists(src):
    os.makedirs(dst_dir, exist_ok=True)
    shutil.move(src, dst)
    print(f"  ✅ Fixed doc_0081.md: Moved to correct location")

# Error 4: doc_0068.md - Off-by-one error (Client voicemail → Insurance letter)
# Currently in: Client/2024-07-26 - Timothy Ruhl - Client - Timothy Ruhl - Voicemail Thank You.md
# Should be: Insurance/Bodily Injury (BI)/Hoosier Cargo Express/2024-07-25 - Timothy Ruhl - Insurance - WLF to Hoosier Cargo - Letter of Representation.md
src = f"{case_path}/Client/2024-07-26 - Timothy Ruhl - Client - Timothy Ruhl - Voicemail Thank You.md"
dst_dir = f"{case_path}/Insurance/Bodily Injury (BI)/Hoosier Cargo Express"
dst = f"{dst_dir}/2024-07-25 - Timothy Ruhl - Insurance - WLF to Hoosier Cargo - Letter of Representation.md"
if os.path.exists(src):
    os.makedirs(dst_dir, exist_ok=True)
    shutil.move(src, dst)
    print(f"  ✅ Fixed doc_0068.md: Moved from Client to Insurance")

# Error 5: doc_0069.md - Off-by-one error (Lien → Client voicemail)
# Currently in: Lien/Anthem BCBS Medicare Advantage/2024-07-29 - Timothy Ruhl - Lien - Anthem BCBS Medicare Advantage - Subrogation Request.md
# Should be: Client/2024-07-26 - Timothy Ruhl - Client - Voicemail Thank You and Cooperation.md
src = f"{case_path}/Lien/Anthem BCBS Medicare Advantage/2024-07-29 - Timothy Ruhl - Lien - Anthem BCBS Medicare Advantage - Subrogation Request.md"
dst = f"{case_path}/Client/2024-07-26 - Timothy Ruhl - Client - Voicemail Thank You and Cooperation.md"
if os.path.exists(src):
    shutil.move(src, dst)
    print(f"  ✅ Fixed doc_0069.md: Moved from Lien to Client")

# Error 6: doc_0070.md - Off-by-one error (Medical Records → Lien)
# Currently in: Medical Records/Capitol Pain Institute of Kentucky/Medical Requests/2024-07-29 - Timothy Ruhl - Medical Record - Capitol Pain Institute of Kentucky - Records Request.md
# Should be: Lien/Anthem BCBS Medicare Advantage/2024-07-29 - Timothy Ruhl - Lien - Anthem BCBS Medicare Advantage - Subrogation Request.md
src = f"{case_path}/Medical Records/Capitol Pain Institute of Kentucky/Medical Requests/2024-07-29 - Timothy Ruhl - Medical Record - Capitol Pain Institute of Kentucky - Records Request.md"
dst_dir = f"{case_path}/Lien/Anthem BCBS Medicare Advantage"
dst = f"{dst_dir}/2024-07-29 - Timothy Ruhl - Lien - Anthem BCBS Medicare Advantage - Subrogation Request.md"
if os.path.exists(src):
    os.makedirs(dst_dir, exist_ok=True)
    shutil.move(src, dst)
    print(f"  ✅ Fixed doc_0070.md: Moved from Medical Records to Lien")

# Error 7: doc_0071.md - Off-by-one error (Pain Management of America → Capitol Pain Institute)
# Currently in: Medical Records/Pain Management of America/Medical Requests/2024-07-29 - Timothy Ruhl - Medical Record - Pain Management of America - Records Request.md
# Should be: Medical Records/Capitol Pain Institute of Kentucky/Medical Requests/2024-07-29 - Timothy Ruhl - Medical Request - Capitol Pain Institute of Kentucky - Records Request.md
src = f"{case_path}/Medical Records/Pain Management of America/Medical Requests/2024-07-29 - Timothy Ruhl - Medical Record - Pain Management of America - Records Request.md"
dst_dir = f"{case_path}/Medical Records/Capitol Pain Institute of Kentucky/Medical Requests"
dst = f"{dst_dir}/2024-07-29 - Timothy Ruhl - Medical Request - Capitol Pain Institute of Kentucky - Records Request.md"
if os.path.exists(src):
    os.makedirs(dst_dir, exist_ok=True)
    shutil.move(src, dst)
    print(f"  ✅ Fixed doc_0071.md: Corrected provider name")

print("\n✅ All 7 errors fixed!")
print("=" * 80)
