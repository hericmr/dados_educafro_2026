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

    # Remove 'pronomes' column as requested
    if 'pronomes' in df.columns:
        df = df.drop(columns=['pronomes'])

    # Merge 'Outro' columns with their specific descriptions
    outro_pairs = [
        ('internet_tipo', 'internet_tipo_outro'),
        ('trabalho_vinculo', 'trabalho_vinculo_outro'),
        ('moradia_tipo', 'moradia_tipo_outro'),
        ('moradia_condicao', 'moradia_condicao_outro'),
        ('transporte_meio', 'transporte_meio_outro'),
        ('genero', 'genero_outro'),
        ('escolaridade', 'escolaridade_outro'),
        ('escolaridade_mae', 'escolaridade_mae_outro'),
        ('escolaridade_pai', 'escolaridade_pai_outro'),
        ('saude_servicos', 'saude_servicos_outro'),
        ('saude_psicoterapia', 'saude_psicoterapia_outro'),
        ('internet_sinal', 'internet_sinal_outro'),
        ('beneficios', 'beneficios_outro'),
        ('orientacao_sexual', 'orientacao_sexual_outra'),
        ('cidade', 'cidade_outra')
    ]
    
    for main_col, outro_col in outro_pairs:
        if main_col in df.columns and outro_col in df.columns:
            # Replace 'Outro' or 'Outra' (case insensitive) with the value from the outro column
            mask = df[main_col].astype(str).str.contains('Outro|Outra', case=False, na=False)
            df.loc[mask, main_col] = df.loc[mask, outro_col].fillna(df.loc[mask, main_col])
            # Clean up: strip whitespace
            df[main_col] = df[main_col].astype(str).str.strip().replace('nan', np.nan)

    # Normalization of values
    if 'genero' in df.columns:
        df['genero'] = df['genero'].replace({
            'Mulher Cis': 'Feminina',
            'Homem Cis': 'Masculina',
            'Feminino': 'Feminina',
            'Masculino': 'Masculina'
        }).str.strip()

    if 'internet_tipo' in df.columns:
        df['internet_tipo'] = df['internet_tipo'].replace({
            'Wi-fi': 'Wi-Fi (Banda Larga)',
            'Dados móveis e wi-fi': 'Wi-Fi (Banda Larga)' # Or keep separate? User highlighted repetition.
        }).str.strip()

    # 1. Processing Age
    birth_col = 'data_nascimento' if 'data_nascimento' in df.columns else 'Data de Nascimento'
    if birth_col in df.columns:
        df[birth_col] = pd.to_datetime(df[birth_col], errors='coerce')
        current_year = datetime.now().year
        
        # Calculate age only for those with missing or null Idade, or recalculate if possible
        def calculate_age(row):
            if pd.notnull(row[birth_col]):
                return current_year - row[birth_col].year
            if 'Idade' in row and pd.notnull(row['Idade']):
                return row['Idade']
            return None
            
        df['Idade'] = df.apply(calculate_age, axis=1).astype('Int64')
    
    def get_age_group(age):
        if pd.isna(age): return "Não informado"
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
    
    df['Race_Supergroup'] = df['Race_Group'].replace({
        'Pretos/as/es': 'Negros (Pretos + Pardos)',
        'Pardos/as/es': 'Negros (Pretos + Pardos)',
        'Brancos/as/es': 'Brancos/as/es'
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
        'nome_completo': 'nome_completo',
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
        'saude_deficiencia_qual': 'Detalhe Deficiência',
        'saude_familiar_deficiencia': 'Familiar com Deficiência?',
        'saude_familia_deficiencia_qual': 'Detalhe Deficiência Familiar',
        'saude_tipo_sanguineo': 'Tipo Sanguíneo',
        'entrevistador': 'Entrevistador',
        'saude_substancias': 'Uso de Substâncias',
        'trabalho_ajuda_familiar': 'Ajuda no Sustento Familiar?',
        'beneficios_cadunico': 'CadÚnico',
        'trabalho_vinculo_outro': 'Vínculo de Trabalho (Outro)',
        'saude_psicoterapia_atual': 'Psicoterapia (Atual)'
    }
    
    # 4. Rename columns using the mapping
    df = df.rename(columns=mapping)
            
    # Define Column Priority for Display
    priority_cols = [
        'nome_completo', 'Idade', 'Faixa Etária', 'Identidade de Gênero', 'Race_Group', 
        'Employment_Status', 'Vínculo de Trabalho', 'Renda Familiar', 'CadÚnico', 
        'Recebe Benefícios', 'Escolaridade', 'Tipo de Escola', 'Qual curso pretende?', 
        'Temas de interesse', 'Cidade', 'Bairro', 'Telefone', 'Email', 
        'Orientação Sexual', 'Estado Civil', 'Escolaridade da Mãe', 'Escolaridade do Pai', 
        'Plano de Saúde', 'Psicoterapia', 'Psicoterapia (Atual)', 'Meio de Transporte', 'Uso do Dinheiro (Trabalho)', 
        'Sinal de Internet', 'Tipo de Moradia', 'Tem Filhos?', 'Possui Deficiência?', 
        'Familiar com Deficiência?', 'Tipo Sanguíneo', 'Entrevistador', 
        'Uso de Substâncias', 'Ajuda no Sustento Familiar?'
    ]
    
    # Metadata and other technical columns to move to the end
    metadata_cols = ['id', 'created_at', 'updated_at', 'status_formulario', 'form_uuid']
    
    # Reorder columns: Priority first, then everything else not in metadata, then metadata last
    existing_priority = [c for c in priority_cols if c in df.columns]
    existing_metadata = [c for c in metadata_cols if c in df.columns]
    remaining = [c for c in df.columns if c not in existing_priority and c not in existing_metadata]
    
    new_order = existing_priority + remaining + existing_metadata
    df = df[new_order]
            
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
