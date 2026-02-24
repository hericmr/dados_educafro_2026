import pandas as pd
import numpy as np
from datetime import datetime

def load_data(filepath):
    """Loads and preprocesses the version 2 Educafro CSV (snake_case)."""
    df = pd.read_csv(filepath)
    
    # Cleaning column names
    df.columns = [c.strip() for c in df.columns]
    
    # Filter for completed forms only
    if 'status_formulario' in df.columns:
        df = df[df['status_formulario'] == 'completo']
    elif 'Status' in df.columns:
        df = df[df['Status'] == 'completo']

    # 1. Processing Age
    birth_col = 'data_nascimento' if 'data_nascimento' in df.columns else 'Data de Nascimento'
    df[birth_col] = pd.to_datetime(df[birth_col], errors='coerce')
    current_year = datetime.now().year
    df['Idade'] = df[birth_col].apply(lambda x: current_year - x.year if pd.notnull(x) else None)
    
    def get_age_group(age):
        if age is None: return "Não informado"
        if age < 18: return "Menor que 18 anos"
        if age <= 30: return "18 a 30 anos"
        return "30 anos ou mais"
    
    df['Faixa Etária'] = df['Idade'].apply(get_age_group)
    
    # 2. Race Mapping
    race_col = 'raca_cor' if 'raca_cor' in df.columns else 'Raça/Cor'
    df['Race_Group'] = df[race_col].replace({
        'Preto/a/e': 'Pretos/as/es',
        'Pardo/a/e': 'Pardos/as/es',
        'Branco/a/e': 'Brancos/as/es'
    })
    
    # 3. Employment
    emp_col = 'trabalho_renda_semana' if 'trabalho_renda_semana' in df.columns else 'Trabalhou na última semana?'
    df['Employment_Status'] = df[emp_col].replace({'Sim': 'Empregado', 'Não': 'Fora da força de trabalho'})
    
    # 4. Initialize missing fields
    df['Frequência'] = "Sem dados"
    df['Busca_Ativa_Result'] = "Sem dados"
    
    # Map other columns for visualizations.py to stay consistent or update visualizations.py
    # We'll use a mapping dict to ensure compatibility
    mapping = {
        'nome_completo': 'Nome Completo',
        'genero': 'Identidade de Gênero',
        'cidade': 'Cidade',
        'trabalho_vinculo': 'Vínculo de Trabalho',
        'renda_familiar': 'Renda Familiar',
        'internet_tem': 'Possui Internet?',
        'internet_tipo': 'Tipo de Internet',
        'moradia_condicao': 'Condição de Moradia',
        'objetivo_temas': 'Temas de interesse',
        'objetivo_curso': 'Qual curso pretende?',
        'orientacao_sexual': 'Orientação Sexual',
        'estado_civil': 'Estado Civil',
        'escola_publica_privada': 'Tipo de Escola',
        'escolaridade': 'Escolaridade',
        'escolaridade_mae': 'Escolaridade da Mãe',
        'escolaridade_pai': 'Escolaridade do Pai',
        'saude_plano': 'Plano de Saúde',
        'saude_psicoterapia': 'Psicoterapia',
        'beneficios_recebe': 'Recebe Benefícios',
        'transporte_meio': 'Meio de Transporte',
        'trabalho_uso_dinheiro': 'Uso do Dinheiro (Trabalho)',
        'trans_travesti': 'Identidade Trans/Travesti',
        'internet_sinal': 'Sinal de Internet',
        'moradia_tipo': 'Tipo de Moradia',
        'filhos_tem': 'Tem Filhos?',
        'saude_deficiencia': 'Possui Deficiência?',
        'saude_familiar_deficiencia': 'Familiar com Deficiência?',
        'saude_tipo_sanguineo': 'Tipo Sanguíneo',
        'entrevistador': 'Entrevistador',
        'saude_substancias': 'Uso de Substâncias',
        'trabalho_ajuda_familiar': 'Ajuda no Sustento Familiar?'
    }
    
    for old_col, new_name in mapping.items():
        if old_col in df.columns:
            df[new_name] = df[old_col]
            
    # Move 'Nome Completo' to the first column if it exists
    if 'Nome Completo' in df.columns:
        cols = ['Nome Completo'] + [c for c in df.columns if c != 'Nome Completo']
        df = df[cols]
            
    return df

if __name__ == "__main__":
    import os
    path = 'entrevistas_educafro_2026_clean.csv' if os.path.exists('entrevistas_educafro_2026_clean.csv') else 'entrevistas_educafro_2026-02-10.csv'
    data = load_data(path)
    print(f"Loaded {len(data)} real records from {path}.")
    if len(data) > 0:
        # Check if Name exists (it shouldn't in clean version)
        name_col = 'Nome Completo' if 'Nome Completo' in data.columns else None
        cols = [name_col, 'Faixa Etária', 'Race_Group', 'Employment_Status']
        cols = [c for c in cols if c is not None]
        print(data[cols].head())
