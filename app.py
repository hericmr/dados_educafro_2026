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
    "Eixo 3: Interesses Formativos"
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

    st.info("Este dashboard exibe dados extraídos exclusivamente do formulário de 2026.")

    st.subheader("Tabela de Dados Completa")
    st.dataframe(df, use_container_width=True)

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
        
        st.plotly_chart(viz.chart_8_job_categories(df), use_container_width=True)
        
        col3, col4 = st.columns(2)
        with col3:
            st.plotly_chart(viz.chart_9_household_income(df), use_container_width=True)
        with col4:
            st.markdown("### Renda e Pobreza")
            st.write("Dados baseados nas respostas de renda familiar.")

        col5, col6 = st.columns(2)
        with col5:
            st.plotly_chart(viz.chart_11_tech_access(df), use_container_width=True)
        with col6:
            st.plotly_chart(viz.chart_11b_device_quality(df), use_container_width=True)
            
        st.plotly_chart(viz.chart_12_housing(df), use_container_width=True)
        
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

st.sidebar.markdown("---")
st.sidebar.caption("Desenvolvido para Educafro Santos © 2026")
