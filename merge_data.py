import pandas as pd
import uuid
import os
import re
from datetime import datetime

# File paths
OLD_CSV = 'entrevistas_educafro_2026-02-10.csv'
NEW_CSV = 'entrevistas_educafro_2026-02-28.csv'
CONSOLIDATED_CSV = 'entrevistas_educafro_consolidated_20260228.csv'
BACKUP_CSV = f'entrevistas_educafro_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

def normalize_age(age_val):
    if pd.isna(age_val):
        return pd.NA
    # Extract first number found
    match = re.search(r'\d+', str(age_val))
    if match:
        return int(match.group())
    return pd.NA

def normalize_gender(gender_val):
    if pd.isna(gender_val):
        return gender_val
    g = str(gender_val).strip()
    if 'Mulher Cis' in g or g == 'Feminino':
        return 'Feminina'
    if 'Homem Cis' in g or g == 'Masculino':
        return 'Masculina'
    return g

def merge_data():
    print(f"Loading {OLD_CSV}...")
    df_old = pd.read_csv(OLD_CSV)
    
    print(f"Loading {NEW_CSV}...")
    df_new = pd.read_csv(NEW_CSV)

    # Combine both datasets
    print("Combining datasets...")
    df_combined = pd.concat([df_old, df_new], ignore_index=True)

    # Deduplicate by form_uuid
    # Keeping the record that was updated most recently (if updated_at exists)
    if 'updated_at' in df_combined.columns:
        df_combined['updated_at'] = pd.to_datetime(df_combined['updated_at'], format='ISO8601', utc=True)
        df_combined = df_combined.sort_values('updated_at', ascending=False)
    
    initial_count = len(df_combined)
    df_merged = df_combined.drop_duplicates(subset=['form_uuid'], keep='first')
    final_count = len(df_merged)
    
    # Sort back by ID for consistency
    df_merged = df_merged.sort_values('id')

    # Backup original files (just for safety)
    print(f"Creating backup of {OLD_CSV}...")
    df_old.to_csv(f'backup_old_{OLD_CSV}', index=False)
    print(f"Creating backup of {NEW_CSV}...")
    df_new.to_csv(f'backup_new_{NEW_CSV}', index=False)

    # Save consolidated
    print(f"Saving merged data to {CONSOLIDATED_CSV}...")
    df_merged.to_csv(CONSOLIDATED_CSV, index=False)
    
    print(f"Merge complete!")
    print(f"Initial total records: {initial_count}")
    print(f"Duplicate records removed: {initial_count - final_count}")
    print(f"Total unique records in {CONSOLIDATED_CSV}: {final_count}")

    # Check if records from OLD_CSV that were missing in NEW_CSV are now present
    missing_uuids = set(df_old['form_uuid']) - set(df_new['form_uuid'])
    if missing_uuids:
        print(f"Successfully recovered {len(missing_uuids)} records that were missing in the more recent file.")
    else:
        print("No missing records were found between files, but they are now consolidated.")

if __name__ == "__main__":
    merge_data()
