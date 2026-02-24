import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import pandas as pd

# Core Color Palette (Premium)
COLORS = {
    'primary': '#E63946',  # Deep Red/Coral
    'secondary': '#457B9D', # Steel Blue
    'accent': '#A8DADC',    # Powder Blue
    'dark': '#1D3557',      # Prussian Blue
    'light': '#F1FAEE',     # Off White
    'black': '#000000',
    'white': '#FFFFFF',
    'race_preto': '#2D2D2D',
    'race_pardo': '#B5651D',
    'race_branco': '#D3D3D3'
}

def chart_1_race_composition(df):
    """1. Gráfico de Composição Racial (Raça/Povo)"""
    counts = df['Race_Group'].value_counts().reset_index()
    counts.columns = ['Raça', 'Total']
    fig = px.pie(counts, values='Total', names='Raça', hole=0.6,
                 color_discrete_sequence=[COLORS['race_preto'], COLORS['race_pardo'], COLORS['race_branco']],
                 title="Composição Racial (Raça/Povo)")
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def chart_2_gender_distribution(df):
    """2. Gráfico de Distribuição por Gênero"""
    counts = df['Identidade de Gênero'].value_counts().reset_index()
    counts.columns = ['Gênero', 'Total']
    fig = px.pie(counts, values='Total', names='Gênero', hole=0.6,
                 color_discrete_sequence=[COLORS['secondary'], COLORS['primary'], COLORS['accent']],
                 title="Distribuição por Gênero")
    return fig

def chart_3_race_by_gender(df):
    """3. Gráfico de Composição Raça/Povo por Gênero"""
    fig = px.bar(df, x="Identidade de Gênero", color="Race_Group",
                 title="Composição Raça/Povo por Gênero",
                 labels={'Race_Group': 'Raça/Povo'},
                 color_discrete_map={'Pretos/as/es': COLORS['race_preto'], 
                                   'Pardos/as/es': COLORS['race_pardo'], 
                                   'Brancos/as/es': COLORS['race_branco']})
    fig.update_layout(barmode='stack')
    return fig

def chart_4_age_groups(df):
    """4. Gráfico de Estudantes por Faixa Etária"""
    counts = df['Faixa Etária'].value_counts().reset_index()
    counts.columns = ['Faixa', 'Total']
    fig = px.pie(counts, values='Total', names='Faixa', hole=0.6,
                 color_discrete_sequence=px.colors.sequential.RdBu,
                 title="Distribuição por Faixa Etária")
    return fig

def chart_5_geography(df):
    """5. Mapa Infográfico de Localização Geográfica (as Bar Chart)"""
    counts = df['Cidade'].value_counts().reset_index()
    counts.columns = ['Cidade', 'Total']
    fig = px.bar(counts, x='Cidade', y='Total', title="Distribuição Geográfica (Baixada Santista)",
                 color_discrete_sequence=[COLORS['dark']])
    return fig

def chart_6_employment_general(df):
    """6. Gráfico de Situação de Trabalho (Geral)"""
    counts = df['Employment_Status'].value_counts().reset_index()
    counts.columns = ['Situação', 'Total']
    fig = px.pie(counts, values='Total', names='Situação', hole=0.6,
                 color_discrete_sequence=[COLORS['primary'], COLORS['dark']],
                 title="Situação de Trabalho (Geral)")
    return fig

def chart_7_employment_by_gender(df):
    """7. Gráfico de Distribuição de Emprego por Gênero"""
    # Calculate percentages within each gender
    df_emp = df.groupby(['Identidade de Gênero', 'Employment_Status']).size().reset_index(name='count')
    total_per_gender = df.groupby('Identidade de Gênero').size().reset_index(name='total')
    df_emp = df_emp.merge(total_per_gender, on='Identidade de Gênero')
    df_emp['percent'] = (df_emp['count'] / df_emp['total'] * 100).round(1)
    
    fig = px.bar(df_emp, x="Identidade de Gênero", y="percent", color="Employment_Status",
                 barmode='group', title="Taxa de Emprego por Gênero (%)",
                 text='percent', color_discrete_map={'Empregado': COLORS['primary'], 'Fora da força de trabalho': COLORS['dark']})
    return fig

def chart_8_job_categories(df):
    """8. Gráfico de Categorias de Trabalho (Grau de Precarização)"""
    counts = df['Vínculo de Trabalho'].value_counts().reset_index()
    counts.columns = ['Vínculo', 'Total']
    fig = px.pie(counts, values='Total', names='Vínculo', hole=0.6,
                 title="Categorias de Trabalho e Vínculo")
    return fig

def chart_9_household_income(df):
    """9. Gráfico de Renda Familiar (Valores Brutos)"""
    counts = df['Renda Familiar'].value_counts().reset_index()
    counts.columns = ['Faixa', 'Total']
    # Sorting order for income
    order = ["Sem renda", "Até 300,00", "De 301,00 a 600,00", "De 601,00 a 1.200,00", 
             "De 1.201,00 a 2.400,00", "De 2.401,00 a 5.200,00", "Acima de 5.201,00"]
    counts['Faixa'] = pd.Categorical(counts['Faixa'], categories=order, ordered=True)
    counts = counts.sort_values('Faixa')
    
    fig = px.bar(counts, y='Faixa', x='Total', orientation='h',
                 title="Renda Familiar Mensal (Valores Brutos)",
                 color_discrete_sequence=[COLORS['secondary']])
    return fig

def chart_11_tech_access(df):
    """11. Gráficos de Acesso à Tecnologia (Internet)"""
    counts = df['Possui Internet?'].value_counts().reset_index()
    counts.columns = ['Internet', 'Total']
    fig = px.pie(counts, values='Total', names='Internet', hole=0.6,
                 title="Acesso à Internet", color_discrete_sequence=[COLORS['secondary'], COLORS['primary']])
    return fig

def chart_11b_device_quality(df):
    """11b. Qualidade do Equipamento"""
    counts = df['Tipo de Internet'].value_counts().reset_index()
    counts.columns = ['Tipo', 'Total']
    fig = px.pie(counts, values='Total', names='Tipo', hole=0.6,
                 title="Qualidade do Equipamento/Conexão")
    return fig

def chart_12_housing(df):
    """12. Gráfico de Condição de Moradia"""
    counts = df['Condição de Moradia'].value_counts().reset_index()
    counts.columns = ['Condição', 'Total']
    fig = px.pie(counts, values='Total', names='Condição', hole=0.6,
                 title="Condição de Moradia")
    return fig

def chart_13_attendance_general(df):
    """13. Gráfico de Infrequência Geral (Based on Mock)"""
    counts = df['Frequência'].value_counts().reset_index()
    counts.columns = ['Status', 'Total']
    fig = px.pie(counts, values='Total', names='Status', hole=0.6,
                 color_discrete_map={'Frequente': '#2A9D8F', 'Infrequente': '#E76F51'},
                 title="Frequência vs Infrequência")
    return fig

def chart_14_busca_ativa(df):
    """14. Gráfico de Resultado da Busca Ativa (Based on Mock)"""
    counts = df['Busca_Ativa_Result'].value_counts().reset_index()
    counts.columns = ['Resultado', 'Total']
    fig = px.pie(counts, values='Total', names='Resultado', hole=0.6,
                 title="Resultado da Busca Ativa")
    return fig

def chart_15_attendance_by_job(df):
    """15. Gráfico de Infrequência por Situação de Trabalho"""
    df_cross = pd.crosstab(df['Employment_Status'], df['Frequência'], normalize='index') * 100
    df_cross = df_cross.reset_index()
    df_melt = df_cross.melt(id_vars='Employment_Status', var_name='Frequência', value_name='Percentual')
    
    fig = px.bar(df_melt, x='Percentual', y='Employment_Status', color='Frequência',
                 orientation='h', title="Infrequência vs Situação de Trabalho (%)",
                 color_discrete_map={'Frequente': '#2A9D8F', 'Infrequente': '#E76F51'})
    return fig

def generate_wordcloud(text_list, title):
    """Generates a word cloud from a list of strings."""
    text = " ".join([str(t) for t in text_list if pd.notnull(t)])
    if not text.strip():
        return None
    
    wc = WordCloud(width=800, height=400, background_color='white', 
                   colormap='RdBu', max_words=50).generate(text)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

def chart_16_interests(df):
    """16. Nuvem de Palavras: Temas de Interesse Coletivo"""
    return generate_wordcloud(df['Temas de interesse'], "Temas de Interesse Coletivo")

def chart_17_courses(df):
    """17. Nuvem de Palavras: Cursos Desejados"""
    return generate_wordcloud(df['Qual curso pretende?'], "Cursos de Interesse (Graduação)")
