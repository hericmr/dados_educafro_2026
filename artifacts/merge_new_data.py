import pandas as pd
import os

# Paths
CONSOLIDATED_OLD = 'entrevistas_educafro_consolidated_final_20260308.csv'
NEW_DATA = 'entrevistas atualizada.csv'
DATA_DIR = 'data'
CONSOLIDATED_NEW = os.path.join(DATA_DIR, 'entrevistas_consolidated.csv')

def merge():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    print(f"Lendo {CONSOLIDATED_OLD}...")
    df_old = pd.read_csv(CONSOLIDATED_OLD)
    
    print(f"Lendo {NEW_DATA}...")
    df_new = pd.read_csv(NEW_DATA)
    
    # Combinar ambos
    # Priorizar o 'form_uuid' para identificar registros únicos
    # Se houver duplicatas, manter a versão mais recente com base no 'updated_at'
    
    df_combined = pd.concat([df_old, df_new], ignore_index=True)
    
    if 'updated_at' in df_combined.columns:
        df_combined['updated_at'] = pd.to_datetime(df_combined['updated_at'], errors='coerce', utc=True)
        df_combined = df_combined.sort_values('updated_at', ascending=False)
    
    # Se 'form_uuid' for missing, use 'cpf' (limpo)
    if 'form_uuid' in df_combined.columns:
        initial_count = len(df_combined)
        df_merged = df_combined.drop_duplicates(subset=['form_uuid'], keep='first')
        print(f"Removidas {initial_count - len(df_merged)} duplicatas por form_uuid.")
    else:
        # Fallback para ID se form_uuid não estiver lá
        initial_count = len(df_combined)
        df_merged = df_combined.drop_duplicates(subset=['id'], keep='first')
        print(f"Removidas {initial_count - len(df_merged)} duplicatas por id (form_uuid ausente).")

    # Salvar o novo consolidado
    df_merged.to_csv(CONSOLIDATED_NEW, index=False)
    print(f"Sucesso! Total de registros únicos: {len(df_merged)}")
    print(f"Arquivo salvo em: {CONSOLIDATED_NEW}")

if __name__ == "__main__":
    merge()
