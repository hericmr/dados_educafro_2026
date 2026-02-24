import pandas as pd
import uuid
import os
import re
from datetime import datetime

# File paths
MAIN_CSV = 'entrevistas_educafro_2026-02-10.csv'
NEW_CSV = 'Entrevista Social 2026- N.A.E (1° Semestre ).csv'
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
    print(f"Loading {MAIN_CSV}...")
    df_main = pd.read_csv(MAIN_CSV)
    
    print(f"Loading {NEW_CSV}...")
    df_new = pd.read_csv(NEW_CSV)

    # Column mapping from New CSV -> Main CSV
    mapping = {
        'NOME DA(O) ASSISTENTE SOCIAL ENTREVISTADOR(A)': 'entrevistador',
        'Data  Entrevista Social *': 'data_entrevista',
        'Nome da aluna Completo(o)': 'nome_completo',
        'Telefone para contato (WhatsApp, se possível)': 'telefone',
        'E-mail*': 'email',
        'Data Nascimento': 'data_nascimento',
        'R.G': 'rg',
        'C.P.F': 'cpf',
        'Cidade*': 'cidade',
        'Naturalidade - Cidade/Estado*': 'naturalidade',
        'Endereço (Rua, Número)*': 'endereco',
        'Bairro*': 'bairro',
        'Estado Civil*': 'estado_civil',
        'Sua cor ou raça é': 'raca_cor',
        'Qual pronome você quer ser tratado?*': 'pronomes',
        'Identidade de Gênero*': 'genero',
        'Qual é a sua orientação sexual? (Você pode selecionar mais de uma opção, se desejar.)': 'orientacao_sexual',
        'Escolaridade*': 'escolaridade',
        'Nome da mãe': 'nome_mae',
        'Profissão da Mãe': 'profissao_mae',
        'Escolaridade da Mãe': 'escolaridade_mae',
        'Nome do Pai': 'nome_pai',
        'Profissão do Pai': 'profissao_pai',
        'Escolaridade do Pai': 'escolaridade_pai',
        'Possui algum familiar estudando atualmente no núcleo?': 'familiar_nucleo',
        'Se sim, para resposta anterior. Qual o vínculo familiar? ': 'vinculo_familiar',
        'Nome completo do familiar que está matriculado no núcleo?': 'nome_familiar',
        'Condição*': 'moradia_condicao',
        'Tipo*': 'moradia_tipo',
        'Possui internet?*': 'internet_tem',
        'Qual tipo?*': 'internet_tipo',
        'A Internet possui um sinal estável?*': 'internet_sinal',
        'Tem alguma atividade remunerada?*\nSim': 'trabalho_renda_semana',
        'Se sim, qual tipo de vínculo?*': 'trabalho_vinculo',
        'Onde trabalha e qual a função?': 'trabalho_vinculo_outro', # Fixed per user request
        'Qual a renda familiar?\nObs:  Valor aproximado da soma de todos os rendimentos mensais das pessoas que moram na mesma casa.': 'renda_familiar',
        'Recebe algum Benefício Social?\n': 'beneficios_recebe', # Fixed: Main CSV uses beneficios_recebe
        'Qual/Quais tipo de benefício?': 'beneficios_tipo',
        'Se sim, você tem CadÚnico*': 'beneficios_cadunico',
        'Precisa de Cesta Básica?*\n': 'cesta_basica',
        'Filhos*': 'filhos_tem',
        'Você paga pensão alimentícia a filhos ou para ex-cônjuge?': 'pensao_paga',
        'Você recebe pensão alimentícia para seus filhos?': 'pensao_recebe',
        'Vc e sua família possui veículo próprio? Se sim. Qual tipo?': 'transporte_veiculo',
        'Qual tipo de transporte você utilizará para se deslocar até a Educafro?*': 'transporte_meio',
        'Precisa de auxílio transporte?  *\n': 'transporte_auxilio',
        'Você utiliza os serviços do SUS, ou possui plano de saúde?*': 'saude_plano',
        'Utiliza alguns desses serviços do SUS?': 'saude_servicos',
        'Sabe qual o seu tipo sanguíneo? Se sim, qual?': 'saude_tipo_sanguineo',
        'Já fez algum tipo de psicoterapia?*': 'saude_psicoterapia',
        'Faz algum tipo de psicoterapia?*': 'saude_psicoterapia_atual',
        'Se sim, por quanto tempo? Há quanto tempo terminou?\n': 'saude_psicoterapia_tempo',
        'Tem algum problema de saúde? Se sim, qual?\n': 'saude_problemas_qual',
        'Possui alguma alergia?\n': 'saude_alergias_qual',
        'Faz uso de medicamento contínuo? ': 'saude_medicamentos',
        'Já fez algum uso de alguma substância psicoativa? Obs: álcool e cigarro são também ': 'saude_substancias',
        'Se sim, qual?': 'saude_substancias_qual',
        'Mora sozinho?': 'cotidiano_mora_com',
        'Com quem mora?': 'cotidiano_mora_com_quem',
        'Como é a relação com a sua família?': 'cotidiano_relacao',
        'Histórico pessoal e/ou familiar (Informações relevantes da história de vida da pessoa)': 'cotidiano_historico',
        'Já sabe que curso(s) quer fazer na graduação?': 'objetivo_curso',
        'Qual o seu objetivo em estudar na Educafro?': 'objetivo_educafro',
        'Que temas você gostaria que fossem trabalhados coletivamente aqui na Educafro?': 'objetivo_temas',
        'Como será a frequência na Educafro, em quais dias pretende/poderá comparecer?': 'objetivo_frequencia',
        'Possui alguma deficiência com ou sem laudo médico ?*': 'saude_deficiencia',
        'Possui algum familiar com deficiência? Se sim, Qual?': 'saude_familiar_deficiencia',
        'Idade': 'Idade' # Raw age to extract later
    }

    # Transform new data
    new_data_dict = {}
    for new_col, main_col in mapping.items():
        if new_col in df_new.columns:
            new_data_dict[main_col] = df_new[new_col]
            
    df_transformed = pd.DataFrame(new_data_dict)

    # Normalization
    if 'genero' in df_transformed.columns:
        df_transformed['genero'] = df_transformed['genero'].apply(normalize_gender)
    
    if 'Idade' in df_transformed.columns:
        df_transformed['Idade'] = df_transformed['Idade'].apply(normalize_age)

    # Fill technical columns
    df_transformed['status_formulario'] = 'completo'
    df_transformed['form_uuid'] = [str(uuid.uuid4()) for _ in range(len(df_transformed))]
    
    # Calculate starting ID
    max_id = df_main['id'].max() if not df_main.empty else 1000
    df_transformed['id'] = range(int(max_id) + 1, int(max_id) + len(df_transformed) + 1)
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_transformed['created_at'] = now
    df_transformed['updated_at'] = now

    # Ensure all columns from main are present (filled with NA if missing)
    for col in df_main.columns:
        if col not in df_transformed.columns:
            df_transformed[col] = pd.NA

    # Append data
    df_merged = pd.concat([df_main, df_transformed], ignore_index=True)

    # Backup original
    print(f"Creating backup: {BACKUP_CSV}...")
    df_main.to_csv(BACKUP_CSV, index=False)

    # Save merged
    print(f"Saving merged data to {MAIN_CSV}...")
    df_merged.to_csv(MAIN_CSV, index=False)
    
    print(f"Merge complete! Added {len(df_transformed)} new records.")
    print(f"Total records now: {len(df_merged)}")

if __name__ == "__main__":
    merge_data()
