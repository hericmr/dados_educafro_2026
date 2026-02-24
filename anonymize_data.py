import pandas as pd

def anonymize(input_file, output_file):
    df = pd.read_csv(input_file)
    
    # Columns with Personally Identifiable Information (PII) to remove
    pii_columns = [
        'telefone', 'email', 'cpf', 'rg', 'endereco', 'bairro',
        'nome_mae', 'nome_pai', 'nome_familiar', 'nome_completo',
        'nome_civil_documento', 'form_uuid', 'entrevistador_outro'
    ]
    
    # Drop columns that exist in the dataframe
    to_drop = [col for col in pii_columns if col in df.columns]
    df_clean = df.drop(columns=to_drop)
    
    # Optionally, we could also mask 'data_nascimento' but keep the derived 'Idade' in data_loader
    # For now, let's keep the birth year or just remove the column if data_loader can handle it
    
    df_clean.to_csv(output_file, index=False)
    print(f"Anonymized data saved to {output_file}")

if __name__ == "__main__":
    anonymize('entrevistas_educafro_2026-02-10.csv', 'entrevistas_educafro_2026_clean.csv')
