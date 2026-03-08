import csv
import os

FILE1 = '/home/hericmr/Documentos/dados_educafro_2026/entrevistas_rows_atualizada_8-3-2026.csv'
FILE2 = '/home/hericmr/Documentos/dados_educafro_2026/entrevistas_educafro_consolidated_20260228.csv'
OUTPUT = '/home/hericmr/Documentos/dados_educafro_2026/entrevistas_educafro_consolidated_final_20260308.csv'

def main():
    records = {}
    columns_set = set()
    columns_list = []

    # Read the first (newer) file
    with open(FILE1, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for col in reader.fieldnames:
            if col not in columns_set:
                columns_list.append(col)
                columns_set.add(col)
                
        for row in reader:
            id_val = row.get('id')
            if not id_val:
                continue
            records[id_val] = row

    # Read the second file
    with open(FILE2, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for col in reader.fieldnames:
            if col not in columns_set:
                columns_list.append(col)
                columns_set.add(col)
                
        for row in reader:
            id_val = row.get('id')
            if not id_val:
                continue
            if id_val not in records:
                records[id_val] = row
            else:
                # Merge existing keys preferring File1's non-empty data
                # but if File1 has an empty value and File2 has data, take File2.
                # Since File1 is 'entrevistas_rows_atualizada', we assume it's more accurate
                for k, v in row.items():
                    if k not in records[id_val] or not records[id_val][k]:
                        records[id_val][k] = v

    # Ensure 'id' is always first
    if 'id' in columns_list:
        columns_list.remove('id')
    columns_list.insert(0, 'id')

    # Sort records by integer ID, if not parseable fallback to string comparison
    def sort_key(item):
        try:
            return int(item[0])
        except (ValueError, TypeError):
            return 0
    
    sorted_records = sorted(records.items(), key=sort_key)

    with open(OUTPUT, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns_list)
        writer.writeheader()
        for _, row in sorted_records:
            writer.writerow(row)
            
    print(f"Merge successful! Total variables (columns): {len(columns_list)}")
    print(f"Total merged records (rows): {len(sorted_records)}")
    print(f"Output saved to: {OUTPUT}")

if __name__ == '__main__':
    main()
