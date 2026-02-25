import streamlit as st
import pandas as pd
from data_loader import load_data
import visualizations as viz
import os

# v1.1 - Added data captions

# Page config
st.set_page_config(page_title="Perfil Educafro 2026", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
<style>
    .main {
        background-color: #F8F9FA;
    }
    .stMetric {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #1D3557;
        font-family: 'Inter', sans-serif;
    }
    .stPlotlyChart {
        background-color: #FFFFFF;
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# App Title and Description
st.title("Educafro | Base Parcial de Entrevistas - 2026")
st.markdown("---")

# Sidebar
st.sidebar.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_R0f8iI9RjV-mC09x8q8K_mX9y8j_H6D_9w&s", width=200) # Placeholder for Educafro Logo
st.sidebar.title("Navegação")
section = st.sidebar.radio("Ir para:", [
    "Resumo Geral",
    "Eixo 1: Perfil Sociodemográfico", 
    "Eixo 2: Trabalho, Renda e Condições Socioeconômicas", 
    "Eixo 3: Mobilidade e Interesses Formativos",
    "Eixo 4: Saúde e Assistência",
    "Gestão e Operacionalização da Pesquisa"
])

# Load Data
CSV_PATH = 'entrevistas_educafro_2026-02-10.csv'
try:
    df = load_data(CSV_PATH)
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.stop()

def render_chart_with_stats(chart_func, df, column_name=None, custom_stats=None, **kwargs):
    """Renderiza um gráfico e adiciona uma legenda com estatísticas em baixo."""
    fig = chart_func(df)
    st.plotly_chart(fig, use_container_width=True, **kwargs)
    
    if custom_stats:
        stats_text = custom_stats
    elif column_name:
        stats_text = viz.get_summary_stats(df, column_name)
    else:
        stats_text = None
        
    if stats_text:
        st.caption(f"**Dados:** {stats_text}")

if section == "Resumo Geral":

    st.markdown("""
    Esta síntese apresenta os principais indicadores sociodemográficos dos estudantes do cursinho Educafro 2026, com base nas entrevistas realizadas até o momento.
   """)
    
    st.info("""
    **Base de dados atualizada em: 24 de fevereiro de 2026**

    """)

    st.divider()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Estudantes", len(df))
    
    # Race percentage calculation
    negros_count = len(df[df['Race_Group'].isin(['Pretos(as)', 'Pardos(as)'])])
    negros_pct = (negros_count / len(df) * 100) if len(df) > 0 else 0
    col2.metric("Negros (Pretos/Pardos)", f"{negros_pct:.1f}%")
    
    # Gender percentage calculation
    mulheres_count = len(df[df['Identidade de Gênero'] == 'Feminina'])
    mulheres_pct = (mulheres_count / len(df) * 100) if len(df) > 0 else 0
    col3.metric("Mulheres", f"{mulheres_pct:.1f}%")
    
    col4.metric("Frequência Média", "N/A") 

    st.subheader("Tabela de Dados Consolidados")
    
    # Function to highlight workers (anyone with a work tie/link)
    def highlight_workers(row):
        is_worker = pd.notnull(row['Vínculo de Trabalho']) and row['Vínculo de Trabalho'] != 'Não'
        return ['background-color: #ffe6e6'] * len(row) if is_worker else [''] * len(row)

    # Apply styling and set index for sticky column
    if 'nome_completo' in df.columns:
        # Bold and Black index (nome_completo) using set_table_styles
        styled_df = df.set_index('nome_completo').style.apply(highlight_workers, axis=1)\
            .set_table_styles([{'selector': 'th.row_heading', 'props': [('font-weight', 'bold'), ('color', 'black')]}])
        st.dataframe(styled_df, use_container_width=True)
    else:
        styled_df = df.style.apply(highlight_workers, axis=1)
        st.dataframe(styled_df, use_container_width=True)
        
    st.markdown("<small>* alunos marcados em vermelho são os estudantes trabalhadores que sabemos que podem apresentar maior taxa de infrequência</small>", unsafe_allow_html=True)

elif section == "Eixo 1: Perfil Sociodemográfico":
    st.header("Eixo 1: Perfil Sociodemográfico")
    
    if len(df) == 0:
        st.warning("Nenhum dado completo encontrado no CSV.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            render_chart_with_stats(viz.chart_1_race_composition, df, 'Race_Group')
        with col2:
            render_chart_with_stats(viz.chart_2_gender_distribution, df, 'Identidade de Gênero')
        
        render_chart_with_stats(viz.chart_3_race_by_gender, df) # Custom logic needed later or simple chart
        
        col_new1, col_new2 = st.columns(2)
        with col_new1:
            render_chart_with_stats(viz.chart_18_orientation, df, 'Orientação Sexual')
        with col_new2:
            render_chart_with_stats(viz.chart_19_school_type, df, 'Tipo de Escola')
        
        col3, col4 = st.columns(2)
        with col3:
            render_chart_with_stats(viz.chart_4_age_groups, df, 'Faixa Etária')
        with col4:
            render_chart_with_stats(viz.chart_5_geography, df, 'Cidade')

elif section == "Eixo 2: Trabalho, Renda e Condições Socioeconômicas":
    st.header("🔹 EIXO 2 — Trabalho, Renda e Condições Socioeconômicas")
    
    if len(df) == 0:
        st.warning("Nenhum dado completo encontrado no CSV.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            render_chart_with_stats(viz.chart_6_employment_general, df, 'Employment_Status')
        with col2:
            render_chart_with_stats(viz.chart_7_employment_by_gender, df)
        
        col_job1, col_job2 = st.columns(2)
        with col_job1:
            render_chart_with_stats(viz.chart_8_job_categories, df, 'Vínculo de Trabalho')
        with col_job2:
            st.subheader("Vínculos Diversos")
            wc_jobs = viz.chart_8b_job_wordcloud(df)
            if wc_jobs:
                st.image(wc_jobs)
            else:
                st.write("Sem detalhes adicionais de vínculos.")
        
        col3, col4 = st.columns(2)
        with col3:
            render_chart_with_stats(viz.chart_9_household_income, df, 'Renda Familiar')
        with col4:
            st.write("Dados baseados nas respostas de renda familiar.")
            render_chart_with_stats(viz.chart_22_social_benefits, df, 'Recebe Benefícios')
        
        render_chart_with_stats(viz.chart_20_parental_education, df)

        col5, col6 = st.columns(2)
        with col5:
            render_chart_with_stats(viz.chart_11_tech_access, df, 'Possui Internet?')
        with col6:
            render_chart_with_stats(viz.chart_11b_device_quality, df, 'Tipo de Internet')
            
        render_chart_with_stats(viz.chart_12_housing, df, 'Condição de Moradia')
        
        col_new3, col_new4 = st.columns(2)
        with col_new3:
            render_chart_with_stats(viz.chart_26_housing_type, df, 'Tipo de Moradia')
        with col_new4:
            render_chart_with_stats(viz.chart_27_parenthood, df, 'Tem Filhos?')
            
        render_chart_with_stats(viz.chart_10_money_usage, df, 'Uso do Dinheiro (Trabalho)')
        render_chart_with_stats(viz.chart_10b_cadunico, df, 'CadÚnico')
        
        st.divider()
        st.subheader("Evasão e Infrequência")
        st.info("Os dados de infrequência não constam no formulário atual.")

elif section == "Eixo 3: Mobilidade e Interesses Formativos":
    st.header("🔹 EIXO 3 — Mobilidade e Interesses Formativos")
    
    if len(df) == 0:
        st.warning("Nenhum dado completo encontrado no CSV.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Temas de Interesse")
            wc_interests = viz.chart_16_interests(df)
            if wc_interests:
                st.image(wc_interests)
            else:
                st.write("Sem dados suficientes para gerar a nuvem.")
                
        with col2:
            st.subheader("Cursos Desejados")
            wc_courses = viz.chart_17_courses(df)
            if wc_courses:
                st.image(wc_courses)
            else:
                st.write("Sem dados suficientes para gerar a nuvem.")
        
        render_chart_with_stats(viz.chart_23_transport_modes, df, 'Meio de Transporte')

elif section == "Eixo 4: Saúde e Assistência":
    st.header("🔹 EIXO 4 — Saúde e Assistência")
    
    if len(df) == 0:
        st.warning("Nenhum dado completo encontrado no CSV.")
    else:
        col7, col8 = st.columns(2)
        with col7:
            render_chart_with_stats(viz.chart_21_health_access, df, 'Plano de Saúde')
        with col8:
            render_chart_with_stats(viz.chart_25_internet_signal, df, 'Sinal de Internet')
            
        col9, col10 = st.columns(2)
        with col9:
            render_chart_with_stats(viz.chart_28_disability, df) # Special chart
        with col10:
            render_chart_with_stats(viz.chart_29_blood_type, df, 'Tipo Sanguíneo')
            
        st.info("A maioria das informações de saúde são qualitativas e podem ser consultadas na tabela de dados no Resumo Geral.")

elif section == "Gestão e Operacionalização da Pesquisa":
    st.header("🔹 Gestão e Operacionalização da Pesquisa")
    
    if len(df) == 0:
        st.warning("Nenhum dado completo encontrado no CSV.")
    else:
        render_chart_with_stats(viz.chart_30_interviewer_balance, df, 'Entrevistador')

st.sidebar.markdown("---")
st.sidebar.caption("Desenvolvido por Heric Moura para Educafro Valongo © 2026")
