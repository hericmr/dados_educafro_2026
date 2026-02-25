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
    'race_negro': '#2D2D2D',
    'race_branco': '#D3D3D3'
}

def get_summary_stats(df, column_name):
    """Retorna uma string formatada com os valores reais e percentuais de uma coluna."""
    if column_name not in df.columns:
        return ""
    
    counts = df[column_name].value_counts()
    total = len(df)
    
    stats_list = []
    for label, count in counts.items():
        percent = (count / total * 100)
        stats_list.append(f"{label}: {count} ({percent:.1f}%)")
    
    return " | ".join(stats_list)

def chart_1_race_composition(df):
    """1. Gráfico de Composição Racial (Raça/Povo)"""
    counts = df['Race_Group'].value_counts().reset_index()
    counts.columns = ['Raça', 'Total']
    fig = px.pie(counts, values='Total', names='Raça', hole=0.6,
                 color_discrete_sequence=[COLORS['race_negro'], COLORS['race_branco']],
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
                 color_discrete_map={'Negros (Pretos e Pardos)': COLORS['race_negro'], 
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

def chart_8b_job_wordcloud(df):
    """8b. Nuvem de Palavras: Vínculos de Trabalho (Outros)"""
    return generate_wordcloud(df['Vínculo de Trabalho (Outro)'], "Descrição de Vínculos de Trabalho (Outros)")

def chart_9_household_income(df):
    """9. Gráfico de Renda Familiar (Valores Brutos) - Sincronizado com CSV"""
    counts = df['Renda Familiar'].value_counts().reset_index()
    counts.columns = ['Faixa', 'Total']
    
    # Actual categories found in CSV
    order = ["Sem renda", "Até R$ 1.045,00", "De R$ 1.046,00 R$ 2080,00", 
             "De R$ 2081,00 a R$ 3.120,00", "De R$ 3.120,00 a R$ 4.160,00", 
             "Acima de R$ 4.161,00"]
    
    # Filter to only keep categories present in order
    counts['Faixa'] = pd.Categorical(counts['Faixa'], categories=order, ordered=True)
    counts = counts.dropna(subset=['Faixa']).sort_values('Faixa')
    
    fig = px.bar(counts, y='Faixa', x='Total', orientation='h',
                 title="Renda Familiar Mensal (Categorias do Formulário)",
                 color_discrete_sequence=[COLORS['secondary']])
    return fig

def chart_10_money_usage(df):
    """10. Destino da Renda (Uso do Dinheiro)"""
    counts = df['Uso do Dinheiro (Trabalho)'].dropna().value_counts().reset_index()
    counts.columns = ['Uso', 'Total']
    fig = px.pie(counts, values='Total', names='Uso', hole=0.6,
                 title="Destino da Renda (Estudantes que Trabalham)",
                 color_discrete_sequence=[COLORS['primary'], COLORS['dark']])
    return fig

def chart_10b_cadunico(df):
    """10b. Inscrição no CadÚnico"""
    counts = df['CadÚnico'].value_counts().reset_index()
    counts.columns = ['Inscrito', 'Total']
    fig = px.pie(counts, values='Total', names='Inscrito', hole=0.6,
                 title="Inscritos no CadÚnico",
                 color_discrete_map={'Sim': COLORS['primary'], 'Não': COLORS['dark']})
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

def chart_18_orientation(df):
    """18. Distribuição de Orientação Sexual"""
    counts = df['Orientação Sexual'].value_counts().reset_index()
    counts.columns = ['Orientação', 'Total']
    fig = px.pie(counts, values='Total', names='Orientação', hole=0.6,
                 title="Diversidade: Orientação Sexual",
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    return fig

def chart_19_school_type(df):
    """19. Tipo de Escola (Ensino Médio)"""
    counts = df['Tipo de Escola'].value_counts().reset_index()
    counts.columns = ['Tipo', 'Total']
    fig = px.bar(counts, x='Tipo', y='Total', title="Trajetória: Tipo de Escola (EM)",
                 color_discrete_sequence=[COLORS['secondary']])
    return fig

def chart_20_parental_education(df):
    """20. Escolaridade Parental Comparada"""
    mae = df['Escolaridade da Mãe'].value_counts().reset_index()
    mae.columns = ['Escolaridade', 'Mãe']
    pai = df['Escolaridade do Pai'].value_counts().reset_index()
    pai.columns = ['Escolaridade', 'Pai']
    
    comp = pd.merge(mae, pai, on='Escolaridade', how='outer').fillna(0)
    fig = px.bar(comp, x='Escolaridade', y=['Mãe', 'Pai'], barmode='group',
                 title="Escolaridade dos Pais",
                 color_discrete_map={'Mãe': COLORS['primary'], 'Pai': COLORS['dark']})
    return fig

def chart_21_health_access(df):
    """21. Acesso à Saúde (Plano vs SUS)"""
    counts = df['Plano de Saúde'].value_counts().reset_index()
    counts.columns = ['Acesso', 'Total']
    fig = px.pie(counts, values='Total', names='Acesso', hole=0.6,
                 title="Acesso a Plano de Saúde",
                 color_discrete_map={'Sim': COLORS['secondary'], 'Não': COLORS['primary'], 'Apenas SUS': COLORS['primary']})
    return fig

def chart_22_social_benefits(df):
    """22. Recebimento de Benefícios Sociais"""
    counts = df['Recebe Benefícios'].value_counts().reset_index()
    counts.columns = ['Recebe', 'Total']
    fig = px.pie(counts, values='Total', names='Recebe', hole=0.6,
                 title="Estudantes que recebem Benefícios Sociais",
                 color_discrete_sequence=[COLORS['dark'], COLORS['accent']])
    return fig

def chart_23_transport_modes(df):
    """23. Meios de Transporte"""
    counts = df['Meio de Transporte'].value_counts().reset_index()
    counts.columns = ['Meio', 'Total']
    fig = px.bar(counts, x='Meio', y='Total', title="Logística: Meio de Transporte",
                 color_discrete_sequence=[COLORS['secondary']])
    return fig

def chart_25_internet_signal(df):
    """25. Qualidade do Sinal de Internet"""
    counts = df['Sinal de Internet'].value_counts().reset_index()
    counts.columns = ['Sinal', 'Total']
    fig = px.bar(counts, x='Sinal', y='Total', title="Qualidade do Sinal de Internet",
                 color_discrete_sequence=[COLORS['accent']])
    return fig

def chart_26_housing_type(df):
    """26. Tipo de Moradia (Construção)"""
    counts = df['Tipo de Moradia'].value_counts().reset_index()
    counts.columns = ['Tipo', 'Total']
    fig = px.pie(counts, values='Total', names='Tipo', hole=0.6,
                 title="Tipo de Construção da Moradia")
    return fig

def chart_27_parenthood(df):
    """27. Estudantes com Filhos"""
    counts = df['Tem Filhos?'].value_counts().reset_index()
    counts.columns = ['Possui', 'Total']
    fig = px.pie(counts, values='Total', names='Possui', hole=0.6,
                 title="Estudantes com Filhos",
                 color_discrete_sequence=[COLORS['dark'], COLORS['primary']])
    return fig

def chart_28_disability(df):
    """28. Representação de Deficiências (Estudantes e Familiares) com Nomes"""
    # Use qualitative details if present, otherwise fall back to Sim/Não
    def get_display_val(row, main_col, detail_col):
        if pd.notnull(row.get(detail_col)) and str(row.get(detail_col)).strip() != '':
            return str(row.get(detail_col))
        return "Nenhuma/Não" if row.get(main_col) == 'Não' else row.get(main_col, 'Não informado')

    df_estudante = df[df['Possui Deficiência?'] == 'Sim']
    df_familiar = df[df['Familiar com Deficiência?'] == 'Sim']
    
    # Count specific disabilities
    est_counts = df_estudante['Detalhe Deficiência'].value_counts().reset_index()
    est_counts.columns = ['Deficiência', 'Total']
    est_counts['Tipo'] = 'Estudante'
    
    fam_counts = df_familiar['Detalhe Deficiência Familiar'].value_counts().reset_index()
    fam_counts.columns = ['Deficiência', 'Total']
    fam_counts['Tipo'] = 'Familiar'
    
    combined = pd.concat([est_counts, fam_counts])
    
    if combined.empty:
        # Fallback if no specific details but still some 'Sim' counts
        est_total = len(df_estudante)
        fam_total = len(df_familiar)
        fig = go.Figure(data=[
            go.Bar(name='Estudante', x=['Sim (Geral)'], y=[est_total], marker_color=COLORS['primary']),
            go.Bar(name='Familiar', x=['Sim (Geral)'], y=[fam_total], marker_color=COLORS['secondary'])
        ])
    else:
        fig = px.bar(combined, x='Deficiência', y='Total', color='Tipo',
                     barmode='group', title="Representação de Deficiências (Nomes Específicos)",
                     color_discrete_map={'Estudante': COLORS['primary'], 'Familiar': COLORS['secondary']})
        
    fig.update_layout(title="Representação de Deficiências")
    return fig

def chart_29_blood_type(df):
    """29. Distribuição de Tipo Sanguíneo"""
    counts = df['Tipo Sanguíneo'].value_counts().reset_index()
    counts.columns = ['Tipo', 'Total']
    fig = px.bar(counts, x='Tipo', y='Total', title="Distribuição de Tipo Sanguíneo",
                 color_discrete_sequence=[COLORS['primary']])
    return fig

def chart_30_interviewer_balance(df):
    """30. Volume de Entrevistas por Entrevistador"""
    counts = df['Entrevistador'].value_counts().reset_index()
    counts.columns = ['Entrevistador', 'Total']
    fig = px.bar(counts, y='Entrevistador', x='Total', orientation='h',
                 title="Volume de Entrevistas por Voluntário",
                 color_discrete_sequence=[COLORS['dark']])
    return fig
