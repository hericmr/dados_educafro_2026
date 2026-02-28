import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import pandas as pd

# Core Color Palette (Premium)
COLORS = {
    'primary': '#1D3557',  # Prussian Blue (Institutional Primary)
    'secondary': '#457B9D', # Steel Blue
    'accent': '#A8DADC',    # Powder Blue
    'neutral': '#6C757D',   # Gray
    'neutral_light': '#E9ECEF',
    'dark': '#1D3557',     
    'light': '#F8F9FA',
    'black': '#000000',
    'white': '#FFFFFF',
    'race_preto': '#343A40',
    'race_pardo': '#6C757D',
    'race_branco': '#ADB5BD',
    'race_negro': '#1D3557' # Highlighted color for Negros(as)
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
    """1. Gráfico de Composição Racial (Raça/Povo) - Padrão Institucional"""
    # 1. Normalização e contagem
    counts = df['Race_Group'].value_counts()
    
    # 2. Dados básicos
    pretos_val = counts.get('Pretos(as)', 0)
    pardos_val = counts.get('Pardos(as)', 0)
    brancos_val = counts.get('Brancos(as)', 0)
    negros_val = pretos_val + pardos_val
    total_samples = len(df)
    
    # 3. Criar gráfico empilhado institucional
    fig = go.Figure()

    # --- Barra Brancos (simples) ---
    if 'Brancos(as)' in counts.index:
        brancos_pct = brancos_val / total_samples * 100

        fig.add_trace(go.Bar(
            y=['Brancos(as)'],
            x=[brancos_pct],
            orientation='h',
            marker_color=COLORS['race_branco'],
            text=[f"{brancos_pct:.1f}% ({brancos_val})"],
            textposition='inside',
            name='Brancos(as)',
            showlegend=False
        ))

    # --- Barra Negros (empilhada: Pretos + Pardos) ---
    if negros_val > 0:
        pretos_pct = pretos_val / total_samples * 100
        pardos_pct = pardos_val / total_samples * 100

        # Parte Pretos
        fig.add_trace(go.Bar(
            y=['Negros(as)'],
            x=[pretos_pct],
            orientation='h',
            marker_color=COLORS['race_preto'],
            text=[f"{pretos_pct:.1f}% ({pretos_val})"],
            textposition='inside',
            name='Pretos(as)',
            showlegend=True
        ))

        # Parte Pardos
        fig.add_trace(go.Bar(
            y=['Negros(as)'],
            x=[pardos_pct],
            orientation='h',
            marker_color=COLORS['race_pardo'],
            text=[f"{pardos_pct:.1f}% ({pardos_val})"],
            textposition='inside',
            name='Pardos(as)',
            showlegend=True
        ))

    # 4. Ajustar Layout
    fig.update_layout(
        barmode='stack',
        title={
            'text': (
                "<b>Composição Racial dos Estudantes</b>"
                "<br><span style='font-size:12px; color:gray'>"
                "Autodeclaração racial. "
                f"N = {total_samples}. "
                "Negros(as) corresponde à agregação de Pretos(as) e Pardos(as)."
                "</span>"
            ),
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis=dict(
            title="Percentual (%)",
            range=[0, 100],
            ticksuffix="%"
        ),
        yaxis=dict(
            categoryorder='array',
            categoryarray=['Brancos(as)', 'Negros(as)']
        ),
        margin=dict(l=120, r=20, t=90, b=40),
        height=420,
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def chart_2_gender_distribution(df):
    """2. Gráfico de Distribuição por Gênero"""
    counts = df['Identidade de Gênero'].value_counts().reset_index()
    counts.columns = ['Gênero', 'Total']
    fig = px.pie(counts, values='Total', names='Gênero', hole=0.6,
                 color_discrete_sequence=[COLORS['secondary'], COLORS['primary'], COLORS['accent']],
                 title="Distribuição por Identidade de Gênero")
    return fig

def chart_3_race_by_gender(df):
    """3. Composição Raça/Povo por Gênero (Percentual Empilhado Institucional)"""

    # 1. Tabela de frequências absolutas
    df_counts = pd.crosstab(df['Identidade de Gênero'], df['Race_Group'])
    
    # 2. Tabela de percentuais para os rótulos
    df_pct = (df_counts.div(df_counts.sum(axis=1), axis=0) * 100).round(1)

    # Garantir ordem institucional das colunas
    ordered_cols = ['Brancos(as)', 'Pretos(as)', 'Pardos(as)']
    cols_present = [c for c in ordered_cols if c in df_counts.columns]
    
    df_counts = df_counts.reindex(columns=cols_present).reset_index()
    df_pct = df_pct.reindex(columns=cols_present).reset_index()

    fig = go.Figure()

    # Adicionar cada grupo racial como segmento empilhado
    for col in cols_present:
        # Texto do rótulo: "Count (Pct%)"
        text_labels = []
        for i in range(len(df_counts)):
            cnt = df_counts.iloc[i][col]
            pct = df_pct.iloc[i][col]
            if cnt > 0:
                text_labels.append(f"{int(cnt)} ({pct}%)")
            else:
                text_labels.append("")

        fig.add_trace(go.Bar(
            x=df_counts['Identidade de Gênero'],
            y=df_counts[col],
            name=col,
            text=text_labels,
            textposition='inside',
            marker_color={
                'Brancos(as)': COLORS['race_branco'],
                'Pretos(as)': COLORS['race_preto'],
                'Pardos(as)': COLORS['race_pardo']
            }.get(col, COLORS['neutral'])
        ))

    fig.update_layout(
        barmode='stack',
        title={
            'text': (
                "<b>Composição Raça/Povo por Gênero</b>"
                "<br><span style='font-size:12px; color:gray'>"
                "Exibindo números absolutos e percentual dentro de cada gênero."
                "</span>"
            )
        },
        yaxis=dict(
            title="Número de Pessoas (Frequência Absoluta)",
        ),
        xaxis=dict(title="Identidade de Gênero"),
        legend_title="Raça/Povo",
        plot_bgcolor='rgba(0,0,0,0)',
        height=450
    )

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
    fig = px.bar(counts, x='Cidade', y='Total', title="Distribuição Geográfica dos Estudantes",
                 color_discrete_sequence=[COLORS['dark']])
    return fig

def chart_6_employment_general(df):
    """6. Gráfico de Situação de Trabalho (Geral)"""
    counts = df['Employment_Status'].value_counts().reset_index()
    counts.columns = ['Situação', 'Total']
    fig = px.pie(counts, values='Total', names='Situação', hole=0.6,
                 color_discrete_sequence=[COLORS['primary'], COLORS['dark']],
                 title="Situação Atual no Mercado de Trabalho")
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
                 title="Natureza do Vínculo de Trabalho")
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
                 title="Faixa de Renda Familiar",
                 color_discrete_sequence=[COLORS['secondary']])
    return fig

def chart_10_money_usage(df):
    """10. Destino da Renda (Uso do Dinheiro)"""
    counts = df['Uso do Dinheiro (Trabalho)'].dropna().value_counts().reset_index()
    counts.columns = ['Uso', 'Total']
    fig = px.pie(counts, values='Total', names='Uso', hole=0.6,
                 title="Destinação Principal da Renda Individual",
                 color_discrete_sequence=[COLORS['primary'], COLORS['dark']])
    return fig

def chart_10b_cadunico(df):
    """10b. Inscrição no CadÚnico"""
    counts = df['CadÚnico'].value_counts().reset_index()
    counts.columns = ['Inscrito', 'Total']
    fig = px.pie(counts, values='Total', names='Inscrito', hole=0.6,
                 title="Inscrição no Cadastro Único (CadÚnico)",
                 color_discrete_map={'Sim': COLORS['primary'], 'Não': COLORS['dark']})
    return fig

def chart_11_tech_access(df):
    """11. Gráficos de Acesso à Tecnologia (Internet)"""
    counts = df['Possui Internet?'].value_counts().reset_index()
    counts.columns = ['Internet', 'Total']
    fig = px.pie(counts, values='Total', names='Internet', hole=0.6,
                 title="Acesso à Internet no Domicílio", color_discrete_sequence=[COLORS['secondary'], COLORS['primary']])
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
                 title="Distribuição por Orientação Sexual",
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    return fig

def chart_19_school_type(df):
    """19. Tipo de Escola (Ensino Médio)"""
    counts = df['Tipo de Escola'].value_counts().reset_index()
    counts.columns = ['Tipo', 'Total']
    fig = px.bar(counts, x='Tipo', y='Total', title="Trajetória Escolar (Tipo de Escola de Origem)",
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
                 title="Cobertura de Saúde (SUS e/ou Plano Privado)",
                 color_discrete_map={'Sim': COLORS['secondary'], 'Não': COLORS['primary'], 'Apenas SUS': COLORS['primary']})
    return fig

def chart_22_social_benefits(df):
    """22. Recebimento de Benefícios Sociais"""
    counts = df['Recebe Benefícios'].value_counts().reset_index()
    counts.columns = ['Recebe', 'Total']
    fig = px.pie(counts, values='Total', names='Recebe', hole=0.6,
                 title="Acesso a Benefícios Sociais",
                 color_discrete_sequence=[COLORS['dark'], COLORS['accent']])
    return fig

def chart_23_transport_modes(df):
    """23. Meios de Transporte"""
    counts = df['Meio de Transporte'].value_counts().reset_index()
    counts.columns = ['Meio', 'Total']
    fig = px.bar(counts, x='Meio', y='Total', title="Meios de Transporte Utilizados",
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
                 title="Tipo de Moradia")
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
                     barmode='group', title="Representação de Deficiências (Estudantes e Familiares)",
                     color_discrete_map={'Estudante': COLORS['primary'], 'Familiar': COLORS['secondary']})
        
    fig.update_layout(title="Representação de Deficiências")
    return fig

def chart_29_blood_type(df):
    """29. Distribuição de Tipo Sanguíneo"""
    counts = df['Tipo Sanguíneo'].value_counts().reset_index()
    counts.columns = ['Tipo', 'Total']
    fig = px.bar(counts, x='Tipo', y='Total', title="Conhecimento do Tipo Sanguíneo",
                 color_discrete_sequence=[COLORS['primary']])
    return fig

def chart_30_interviewer_balance(df):
    """30. Volume de Entrevistas por Entrevistador"""
    counts = df['Entrevistador'].value_counts().reset_index()
    counts.columns = ['Entrevistador', 'Total']
    fig = px.bar(counts, y='Entrevistador', x='Total', orientation='h',
                 title="Distribuição de Entrevistas por Entrevistador(a)",
                 color_discrete_sequence=[COLORS['dark']])
    return fig

def chart_31_marital_status(df):
    """31. Distribuição de Estado Civil"""
    counts = df['Estado Civil'].value_counts().reset_index()
    counts.columns = ['Estado Civil', 'Total']
    fig = px.pie(counts, values='Total', names='Estado Civil', 
                 title="Perfil por Estado Civil",
                 color_discrete_sequence=px.colors.qualitative.Prism)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def chart_32_naturalidade(df):
    """32. Naturalidade dos Estudantes (Top 10)"""
    counts = df['naturalidade'].value_counts().head(10).reset_index()
    counts.columns = ['Naturalidade', 'Total']
    fig = px.bar(counts, x='Total', y='Naturalidade', orientation='h',
                 title="Top 10 Cidades de Origem (Naturalidade)",
                 color_discrete_sequence=[COLORS['secondary']])
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

def chart_33_benefits_breakdown(df):
    """33. Detalhamento dos Benefícios Sociais"""
    # beneficios_tipo is often a string representation of a list like '["PBF", "Outro"]'
    # We need to flatten it
    all_benefits = []
    for val in df['beneficios_tipo'].dropna():
        if isinstance(val, str) and val.startswith('['):
            try:
                # Basic parsing for JSON-like strings
                items = val.strip('[]').replace('"', '').split(',')
                all_benefits.extend([i.strip() for i in items if i.strip()])
            except:
                all_benefits.append(val)
        else:
            all_benefits.append(str(val))
    
    if not all_benefits:
        return None
        
    counts = pd.Series(all_benefits).value_counts().reset_index()
    counts.columns = ['Benefício', 'Total']
    fig = px.bar(counts, x='Benefício', y='Total', 
                 title="Tipos de Benefícios Recebidos",
                 color_discrete_sequence=[COLORS['accent']])
    return fig

def chart_34_substance_use(df):
    """34. Uso de Substâncias (Álcool, Cigarro, etc.)"""
    counts = df['Uso de Substâncias'].value_counts().reset_index()
    counts.columns = ['Uso', 'Total']
    fig = px.bar(counts, x='Uso', y='Total', title="Relato de Uso de Substâncias",
                 color_discrete_sequence=[COLORS['danger']])
    return fig

def chart_35_family_context(df):
    """35. Configuração Familiar (Com quem mora)"""
    counts = df['cotidiano_mora_com_quem'].value_counts().head(8).reset_index()
    counts.columns = ['Com quem mora', 'Total']
    fig = px.bar(counts, x='Total', y='Com quem mora', orientation='h',
                 title="Configuração Familiar (Principais Arranjos)",
                 color_discrete_sequence=[COLORS['primary']])
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

def chart_36_household_sustenance(df):
    """36. Estudantes que ajudam no sustento familiar"""
    counts = df['Ajuda no Sustento Familiar?'].value_counts().reset_index()
    counts.columns = ['Ajuda?', 'Total']
    fig = px.pie(counts, values='Total', names='Ajuda?', 
                 title="Estudantes que Ajudam no Sustento da Casa",
                 color_discrete_map={'Sim': COLORS['accent'], 'Não': COLORS['light']})
    return fig

def chart_37_transport_subsidy(df):
    """37. Necessidade de Auxílio Transporte"""
    counts = df['transporte_auxilio'].value_counts().reset_index()
    counts.columns = ['Necessita Auxílio?', 'Total']
    fig = px.bar(counts, x='Necessita Auxílio?', y='Total', 
                 title="Necessidade de Auxílio Transporte",
                 color_discrete_sequence=[COLORS['secondary']])
    return fig

def chart_38_parental_professions_cloud(df):
    """38. Nuvem de Palavras: Profissões dos Pais"""
    professions = []
    for col in ['profissao_mae', 'profissao_pai']:
        if col in df.columns:
            professions.extend(df[col].dropna().astype(str).tolist())
    
    if not professions:
        return None
        
    return generate_wordcloud(professions, "Origem Profissional Familiar")

def chart_39_food_security(df):
    """39. Segurança Alimentar (Recebimento de Cesta Básica)"""
    counts = df['cesta_basica'].value_counts().reset_index()
    counts.columns = ['Recebe Cesta Básica?', 'Total']
    fig = px.bar(counts, x='Recebe Cesta Básica?', y='Total', 
                 title="Segurança Alimentar: Recebimento de Cesta Básica",
                 color_discrete_sequence=[COLORS['accent']])
    return fig

def chart_40_study_availability(df):
    """40. Disponibilidade para Estudo (Frequência)"""
    counts = df['objetivo_frequencia'].value_counts().reset_index()
    counts.columns = ['Frequência Preferida', 'Total']
    fig = px.bar(counts, x='Frequência Preferida', y='Total', 
                 title="Disponibilidade para Estudo (Frequência)",
                 color_discrete_sequence=[COLORS['primary']])
    return fig

def chart_41_health_needs_cloud(df):
    """41. Nuvem de Palavras: Necessidades de Saúde (Medicamentos/Alergias)"""
    health_notes = []
    for col in ['saude_medicamentos_qual', 'saude_alergias_qual', 'saude_problemas_qual']:
        if col in df.columns:
            health_notes.extend(df[col].dropna().astype(str).tolist())
            
    if not health_notes:
        return None
        
    return generate_wordcloud(health_notes, "Perfil de Medicamentos e Alergias")

def chart_42_work_start_hours(df):
    """42. Histograma de Horário de Início do Trabalho"""
    if 'trabalho_horario_inicio' not in df.columns:
        return None
        
    times = df['trabalho_horario_inicio'].dropna().astype(str)
    # Clean up common patterns like "09:00", "08:00" etc.
    # We'll just take the hour for simplicity if it looks like a time
    hours = []
    for t in times:
        if ':' in t:
            try:
                hours.append(int(t.split(':')[0]))
            except:
                pass
                
    if not hours:
        return None
        
    fig = px.histogram(hours, nbins=24, title="Horário de Início da Jornada de Trabalho",
                       labels={'value': 'Hora do Dia (0-24)'},
                       color_discrete_sequence=[COLORS['dark']])
    fig.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=1))
    return fig
