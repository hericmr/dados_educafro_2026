
import pandas as pd
from data_loader import load_data
import os

# Caminho do CSV
CSV_PATH = 'entrevistas_educafro_consolidated_final_20260308.csv'
df = load_data(CSV_PATH)

def get_stats(df, column_name):
    if column_name not in df.columns:
        return "  - Sem dados (Coluna não encontrada)"
    counts = df[column_name].value_counts()
    if counts.empty:
        return "  - Sem ocorrências"
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
        ('Estado Civil', 'Estado Civil'),
        ('Faixa Etária', 'Faixa Etária'),
        ('Naturalidade', 'naturalidade'),
        ('Localização (Cidade)', 'Cidade'),
        ('Tipo de Escola', 'Tipo de Escola'),
        ('Escolaridade da Mãe', 'Escolaridade da Mãe'),
        ('Escolaridade do Pai', 'Escolaridade do Pai')
    ],
    "Eixo 2: Trabalho, Renda e Condições Socioeconômicas": [
        ('Situação de Trabalho', 'Employment_Status'),
        ('Vínculo de Trabalho', 'Vínculo de Trabalho'),
        ('Renda Familiar', 'Renda Familiar'),
        ('Benefícios Sociais', 'Recebe Benefícios'),
        ('Tipo de Benefício', 'beneficios_tipo'),
        ('Acesso à Internet', 'Possui Internet?'),
        ('Tipo de Internet', 'Tipo de Internet'),
        ('Sinal de Internet', 'Sinal de Internet'),
        ('Condição de Moradia', 'Condição de Moradia'),
        ('Tipo de Moradia', 'Tipo de Moradia'),
        ('Estudantes com Filhos', 'Tem Filhos?'),
        ('Ajuda no Sustento Familiar', 'Ajuda no Sustento Familiar?'),
        ('Segurança Alimentar (Cesta Básica)', 'cesta_basica'),
        ('Uso do Dinheiro', 'Uso do Dinheiro (Trabalho)'),
        ('Inscritos no CadÚnico', 'CadÚnico'),
        ('Início do Trabalho (Horário)', 'trabalho_horario_inicio')
    ],
    "Eixo 3: Mobilidade e Interesses Formativos": [
        ('Meios de Transporte', 'Meio de Transporte'),
        ('Necessidade de Auxílio Transporte', 'transporte_auxilio'),
        ('Disponibilidade para Estudo', 'objetivo_frequencia'),
        ('Meios de Transporte', 'Meio de Transporte')
    ],
    "Eixo 4: Saúde e Assistência": [
        ('Plano de Saúde', 'Plano de Saúde'),
        ('Tipo Sanguíneo', 'Tipo Sanguíneo'),
        ('Uso de Substâncias', 'Uso de Substâncias'),
        ('Possui Deficiência', 'Possui Deficiência?'),
        ('Detalhe Deficiência', 'Detalhe Deficiência'),
        ('Familiar com Deficiência', 'Familiar com Deficiência?'),
        ('Detalhe Deficiência Familiar', 'Detalhe Deficiência Familiar'),
        ('Configuração Familiar (Mora com)', 'cotidiano_mora_com_quem')
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

print("Arquivo 'dados dos graficos.txt' regerado com todos os novos campos e gráficos.")
