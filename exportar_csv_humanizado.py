import pandas as pd
from data_loader import load_data
import os

def export_humanized_csv():
    # 1. Carrega os dados exatos processados pelo Streamlit no app.py
    CSV_PATH = 'entrevistas_educafro_consolidated_final_20260308.csv'
    df = load_data(CSV_PATH)
    
    # 2. As colunas já foram renomeadas e reordenadas pelo `data_loader.py` na Priority List
    # Retiramos apenas colunas técnicas criadas pelo sistema que o humano não precisa ler
    colunas_remover = ['id', 'created_at', 'updated_at', 'status_formulario', 'form_uuid', 'Busca_Ativa_Result', 'Frequência']
    colunas_limpas = [c for c in df.columns if c not in colunas_remover]
    
    df_clean = df[colunas_limpas].copy()
    
    # Substituir os campos faltantes vazios por "Não informado" para melhor legibilidade
    # Converte tipos numéricos estritos (Int64) para object antes para aceitar string
    for col in df_clean.columns:
        if str(df_clean[col].dtype) == 'Int64':
            df_clean[col] = df_clean[col].astype(object)
            
    df_clean = df_clean.fillna("Não informado")
    
    # 3. Exporta para CSV
    output_filename = 'entrevistas_educafro_humanizado_2026.csv'
    df_clean.to_csv(output_filename, index=False, encoding='utf-8-sig')
    print(f"Sucesso! Gerado arquivo '{output_filename}' com {len(df_clean)} registros e {len(df_clean.columns)} colunas formatadas.")

if __name__ == "__main__":
    export_humanized_csv()
