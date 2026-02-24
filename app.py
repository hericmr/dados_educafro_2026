import streamlit as st
import pandas as pd
from data_loader import load_data
import visualizations as viz
import os

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
st.title("Perfil Educafro 2026")
st.markdown("---")

# Sidebar
st.sidebar.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_R0f8iI9RjV-mC09x8q8K_mX9y8j_H6D_9w&s", width=200) # Placeholder for Educafro Logo
st.sidebar.title("Navegação")
section = st.sidebar.radio("Ir para:", [
    "Resumo Geral",
    "Eixo 1: Perfil Sociodemográfico", 
    "Eixo 2: Trabalho, Renda e Infrequência", 
    "Eixo 3: Interesses Formativos",
    "Eixo 4: Saúde e Assistência",
    "Gestão e Equipe"
])

# Load Data
CSV_PATH = 'entrevistas_educafro_2026_clean.csv' if os.path.exists('entrevistas_educafro_2026_clean.csv') else 'entrevistas_educafro_2026-02-10.csv'
try:
    df = load_data(CSV_PATH)
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.stop()

if section == "Resumo Geral":
    st.header("Visão Geral do Cursinho")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Estudantes", len(df))
    
    # Race percentage calculation
    negros_count = len(df[df['Race_Group'].isin(['Pretos/as/es', 'Pardos/as/es'])])
    negros_pct = (negros_count / len(df) * 100) if len(df) > 0 else 0
    col2.metric("Negros (Pretos/Pardos)", f"{negros_pct:.1f}%")
    
    # Gender percentage calculation
    mulheres_count = len(df[df['Identidade de Gênero'] == 'Feminina'])
    mulheres_pct = (mulheres_count / len(df) * 100) if len(df) > 0 else 0
    col3.metric("Mulheres", f"{mulheres_pct:.1f}%")
    
    col4.metric("Frequência Média", "N/A") 

    st.info("Esta é uma análise de dados inicial com base nas entrevistas do cursinho Educafro de 2026.")
    st.subheader("Tabela de dados coletados até o momento - 24/02/2026")
    
    # Function to highlight workers (anyone with a work tie/link)
    def highlight_workers(row):
        is_worker = pd.notnull(row['Vínculo de Trabalho']) and row['Vínculo de Trabalho'] != 'Não'
        return ['background-color: #ffe6e6'] * len(row) if is_worker else [''] * len(row)

    # Apply styling and set index for sticky column
    if 'nome_completo' in df.columns:
        # Bold the index (nome_completo) using set_table_styles
        styled_df = df.set_index('nome_completo').style.apply(highlight_workers, axis=1)\
            .set_table_styles([{'selector': 'th.row_heading', 'props': [('font-weight', 'bold')]}])
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
            st.plotly_chart(viz.chart_1_race_composition(df), use_container_width=True)
        with col2:
            st.plotly_chart(viz.chart_2_gender_distribution(df), use_container_width=True)
        
        st.plotly_chart(viz.chart_3_race_by_gender(df), use_container_width=True)
        
        col_new1, col_new2 = st.columns(2)
        with col_new1:
            st.plotly_chart(viz.chart_18_orientation(df), use_container_width=True)
        with col_new2:
            st.plotly_chart(viz.chart_19_school_type(df), use_container_width=True)
        
        col3, col4 = st.columns(2)
        with col3:
            st.plotly_chart(viz.chart_4_age_groups(df), use_container_width=True)
        with col4:
            st.plotly_chart(viz.chart_5_geography(df), use_container_width=True)

elif section == "Eixo 2: Trabalho, Renda e Infrequência":
    st.header("Eixo 2: Trabalho, Renda e Infrequência")
    
    if len(df) == 0:
        st.warning("Nenhum dado completo encontrado no CSV.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(viz.chart_6_employment_general(df), use_container_width=True)
        with col2:
            st.plotly_chart(viz.chart_7_employment_by_gender(df), use_container_width=True)
        
        col_job1, col_job2 = st.columns(2)
        with col_job1:
            st.plotly_chart(viz.chart_8_job_categories(df), use_container_width=True)
        with col_job2:
            st.subheader("Vínculos Diversos")
            wc_jobs = viz.chart_8b_job_wordcloud(df)
            if wc_jobs:
                st.image(wc_jobs)
            else:
                st.write("Sem detalhes adicionais de vínculos.")
        
        col3, col4 = st.columns(2)
        with col3:
            st.plotly_chart(viz.chart_9_household_income(df), use_container_width=True)
        with col4:
            st.write("Dados baseados nas respostas de renda familiar.")
            st.plotly_chart(viz.chart_22_social_benefits(df), use_container_width=True)
        
        st.plotly_chart(viz.chart_20_parental_education(df), use_container_width=True)

        col5, col6 = st.columns(2)
        with col5:
            st.plotly_chart(viz.chart_11_tech_access(df), use_container_width=True)
        with col6:
            st.plotly_chart(viz.chart_11b_device_quality(df), use_container_width=True)
            
        st.plotly_chart(viz.chart_12_housing(df), use_container_width=True)
        
        col_new3, col_new4 = st.columns(2)
        with col_new3:
            st.plotly_chart(viz.chart_26_housing_type(df), use_container_width=True)
        with col_new4:
            st.plotly_chart(viz.chart_27_parenthood(df), use_container_width=True)
            
        st.plotly_chart(viz.chart_10_money_usage(df), use_container_width=True)
        st.plotly_chart(viz.chart_10b_cadunico(df), use_container_width=True)
        
        st.divider()
        st.subheader("Evasão e Infrequência")
        st.info("Os dados de infrequência não constam no formulário atual.")

elif section == "Eixo 3: Interesses Formativos":
    st.header("Eixo 3: Interesses Formativos")
    
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
        
        st.plotly_chart(viz.chart_23_transport_modes(df), use_container_width=True)

elif section == "Eixo 4: Saúde e Assistência":
    st.header("Eixo 4: Saúde e Assistência")
    
    if len(df) == 0:
        st.warning("Nenhum dado completo encontrado no CSV.")
    else:
        col7, col8 = st.columns(2)
        with col7:
            st.plotly_chart(viz.chart_21_health_access(df), use_container_width=True)
        with col8:
            st.plotly_chart(viz.chart_25_internet_signal(df), use_container_width=True)
            
        col9, col10 = st.columns(2)
        with col9:
            st.plotly_chart(viz.chart_28_disability(df), use_container_width=True)
        with col10:
            st.plotly_chart(viz.chart_29_blood_type(df), use_container_width=True)
            
        st.info("A maioria das informações de saúde são qualitativas e podem ser consultadas na tabela de dados no Resumo Geral.")

elif section == "Gestão e Equipe":
    st.header("Gestão e Equipe")
    
    if len(df) == 0:
        st.warning("Nenhum dado completo encontrado no CSV.")
    else:
        st.plotly_chart(viz.chart_30_interviewer_balance(df), use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.caption("Desenvolvido para Educafro Santos © 2026")
