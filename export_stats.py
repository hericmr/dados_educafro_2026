
import pandas as pd
from data_loader import load_data
import os

# Caminho do CSV
CSV_PATH = 'entrevistas_educafro_2026-02-10.csv'
df = load_data(CSV_PATH)

def get_stats(df, column_name):
    if column_name not in df.columns:
        return "Sem dados"
    counts = df[column_name].value_counts()
    total = len(df)
    lines = []
    for label, count in counts.items():
        percent = (count / total * 100)
        lines.append(f"  - {label}: {count} ({percent:.1f}%)")
    return "\n".join(lines)

sections = {
    "Eixo 1: Perfil Sociodemográfico": [
        ('Composição Racial', 'Race_Group'),
        ('Identidade de Gênero', 'Identidade de Gênero'),
        ('Orientação Sexual', 'Orientação Sexual'),
        ('Tipo de Escola', 'Tipo de Escola'),
        ('Faixa Etária', 'Faixa Etária'),
        ('Localização (Cidade)', 'Cidade')
    ],
    "Eixo 2: Trabalho, Renda e Infrequência": [
        ('Situação de Trabalho', 'Employment_Status'),
        ('Vínculo de Trabalho', 'Vínculo de Trabalho'),
        ('Renda Familiar', 'Renda Familiar'),
        ('Benefícios Sociais', 'Recebe Benefícios'),
        ('Acesso à Internet', 'Possui Internet?'),
        ('Tipo de Internet', 'Tipo de Internet'),
        ('Condição de Moradia', 'Condição de Moradia'),
        ('Tipo de Moradia', 'Tipo de Moradia'),
        ('Estudantes com Filhos', 'Tem Filhos?'),
        ('Uso do Dinheiro', 'Uso do Dinheiro (Trabalho)'),
        ('Inscritos no CadÚnico', 'CadÚnico')
    ],
    "Eixo 3: Interesses Formativos": [
        ('Meios de Transporte', 'Meio de Transporte')
    ],
    "Eixo 4: Saúde e Assistência": [
        ('Plano de Saúde', 'Plano de Saúde'),
        ('Sinal de Internet', 'Sinal de Internet'),
        ('Tipo Sanguíneo', 'Tipo Sanguíneo'),
        ('Possui Deficiência', 'Possui Deficiência?'),
        ('Familiar com Deficiência', 'Familiar com Deficiência?')
    ],
    "Gestão": [
        ('Volume por Entrevistador', 'Entrevistador')
    ]
}

content = ["RELATÓRIO DE DADOS - EDUCAFRO 2026", "="*35, f"Total de Entrevistados: {len(df)}\n"]

for section, charts in sections.items():
    content.append(f"\n{section}")
    content.append("-" * len(section))
    for title, col in charts:
        content.append(f"\n{title}:")
        content.append(get_stats(df, col))

with open('dados dos graficos.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(content))

print("Arquivo 'dados dos graficos.txt' regerado com sucesso.")
