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

def check_password():
    """Returns True if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        # Get password from secrets, or use a default/show error if missing
        try:
            correct_password = st.secrets["password"]
        except KeyError:
            st.error("Configuração de segurança ausente. Adicione 'password' nos Secrets do Streamlit.")
            st.stop()
            return

        if st.session_state["password"] == correct_password:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Por favor, insira a senha para acessar os dados:", 
            type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Por favor, insira a senha para acessar os dados:", 
            type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Senha incorreta")
        return False
    else:
        # Password correct.
        return True

if not check_password():
    st.stop()

st.markdown("---")

# Sidebar
st.sidebar.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_R0f8iI9RjV-mC09x8q8K_mX9y8j_H6D_9w&s", width=200) # Placeholder for Educafro Logo
st.sidebar.title("Navegação")
section = st.sidebar.radio("Ir para:", [
    "Resumo Geral",
    "Eixo 0: Secras de Referência do Estudante",
    "Eixo 1: Perfil Sociodemográfico", 
    "Eixo 2: Trabalho, Renda e Condições Socioeconômicas", 
    "Eixo 3: Mobilidade e Interesses Formativos",
    "Eixo 4: Saúde e Assistência",
    "Gestão e Operacionalização da Pesquisa"
])

# Load Data
CSV_PATH = 'data/entrevistas_consolidated.csv'
try:
    df = load_data(CSV_PATH)
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.stop()

def render_chart_with_stats(chart_func, df, column_name=None, custom_stats=None, **kwargs):
    """Renderiza um gráfico e adiciona uma legenda com estatísticas em baixo."""
    fig = chart_func(df)
    
    if fig is None:
        st.warning("Gráfico indisponível para os filtros selecionados.")
        return

    # Check if fig is a Plotly figure or an image buffer (WordCloud)
    if hasattr(fig, 'to_json'): # Plotly figure
        st.plotly_chart(fig, use_container_width=True, **kwargs)
    else: # Matplotlib/WordCloud buffer
        st.image(fig, use_container_width=True)
    
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
    **Base de dados atualizada em: 6 de abril de 2026**

    """)

    st.divider()
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Estudantes", len(df))
    
    # Race percentage calculation (excluding 'Indígena' to match chart 1 totals)
    df_with_race = df[df['Race_Group'].isin(['Pretos(as)', 'Pardos(as)', 'Brancos(as)'])]
    negros_count = len(df_with_race[df_with_race['Race_Group'].isin(['Pretos(as)', 'Pardos(as)'])])
    negros_pct = (negros_count / len(df_with_race) * 100) if len(df_with_race) > 0 else 0
    col2.metric("Pretos/Pardos", f"{negros_pct:.1f}%")
    
    # Gender percentage calculation
    mulheres_count = len(df[df['Identidade de Gênero'] == 'Feminina'])
    mulheres_pct = (mulheres_count / len(df) * 100) if len(df) > 0 else 0
    col3.metric("Mulheres", f"{mulheres_pct:.1f}%")

    # Workers (Synchronized with pink background condition in the table)
    # Highlighted if they have any work link that is not "Não"
    is_worker = df['Vínculo de Trabalho'].notna() & (df['Vínculo de Trabalho'] != 'Não') & (df['Vínculo de Trabalho'] != 'nan') & (df['Vínculo de Trabalho'] != '')
    trabalhadores_count = len(df[is_worker])
    col4.metric("Trabalhadores", trabalhadores_count)

    # PCD
    pcd_count = len(df[df['Possui Deficiência?'] == 'Sim'])
    col5.metric("PCD", pcd_count)

    # Children
    filhos_count = len(df[df['Tem Filhos?'] == 'Sim'])
    col6.metric("Com Filhos", filhos_count)

    # Function to generate indicator tags (professional)
    def get_indicators(row):
        tags = []
        if pd.notnull(row.get('Tem Filhos?')) and str(row.get('Tem Filhos?')).strip() == 'Sim':
            tags.append("[FIL]") # Children
        if (pd.notnull(row.get('Possui Deficiência?')) and str(row.get('Possui Deficiência?')).strip() == 'Sim') or \
           (pd.notnull(row.get('Familiar com Deficiência?')) and str(row.get('Familiar com Deficiência?')).strip() == 'Sim'):
            tags.append("[PCD]") # Disability
        if pd.notnull(row.get('Recebe Benefícios')) and str(row.get('Recebe Benefícios')).strip() == 'Sim':
            tags.append("[BEN]") # Benefits
        if row.get('Status_Emprego_Simplificado') == 'Empregado' or row.get('Employment_Status') == 'Empregado':
            tags.append("[TRB]") # Employment
        return " ".join(tags)

    # Prepare DataFrame for Display
    display_df = df.copy()
    display_df['nome_completo'] = display_df['nome_completo'].str.title()
    display_df.insert(0, 'Perfil', display_df.apply(get_indicators, axis=1))

    # Combined Styling Function
    def style_row(row):
        # 1. Background logic (Workers)
        is_worker = pd.notnull(row.get('Vínculo de Trabalho')) and row.get('Vínculo de Trabalho') != 'Não'
        row_bg = 'background-color: #FED7D7' if is_worker else '' 

        # 2. Text Color logic (Benefits)
        receives_benefits = pd.notnull(row.get('Recebe Benefícios')) and str(row.get('Recebe Benefícios')).strip() == 'Sim'
        name_color = 'color: #D63031; font-weight: bold' if receives_benefits else 'color: #2D3436; font-weight: bold'

        # Apply to all columns
        styles = [row_bg] * len(row)
        
        # Specific override for 'nome_completo' column
        if 'nome_completo' in row.index:
            name_idx = row.index.get_loc('nome_completo')
            styles[name_idx] = f"{row_bg}; {name_color}"
            
        return styles

    # Apply the styling
    styled_df = display_df.style.apply(style_row, axis=1)
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
    st.markdown("""
    <div style='background-color: #F8F9FA; padding: 10px; border-radius: 5px; border: 1px solid #E9ECEF;'>
        <small>
            <b>Legenda de Perfil:</b><br>
            <b>[FIL]</b> Tem Filhos | <b>[PCD]</b> Deficiência (Estudante/Família) | <b>[BEN]</b> Recebe Benefícios | <b>[TRB]</b> Estudante Trabalhador<br>
            <span style='color: #D63031;'><b>Nomes em Vermelho</b></span>: Recebe Benefícios Sociais | 
            <span style='background-color: #FED7D7; padding: 2px;'><b>Fundo Rosado</b></span>: Estudante Trabalhador (Risco de Infrequência)
        </small>
    </div>
    """, unsafe_allow_html=True)

elif section == "Eixo 0: Secras de Referência do Estudante":
    st.header("🔹 Eixo 0 — Secras de Referência do Estudante")

    if len(df) == 0:
        st.warning("Nenhum dado completo encontrado no CSV.")
    else:
        st.markdown("Esta seção acompanha o status e o CRAS de cada estudante para fins de inscrição no CadÚnico.")

        # ── Elegibilidade ao CadÚnico ────────────────────────────────────────
        # Salário mínimo 2026: R$ 1.518,00
        # Critérios: renda familiar total ≤ 3 SM (R$ 4.554,00)
        #            OU renda per capita ≤ ½ SM (R$ 759,00)
        # Como não temos nº de pessoas por faixa de renda per capita com precisão,
        # classificamos pela renda familiar total usando as faixas do formulário.

        ELEGIVEL_RENDA = {
            # Faixas claramente abaixo de 3 SM (R$ 4.554,00)
            "De R$ 1.046,00 R$ 2080,00":    "✅ Elegível",
            "De R$ 2081,00 a R$ 3.120,00":  "✅ Elegível",
            "De R$ 3.120,00 a R$ 4.160,00": "✅ Elegível",
            # R$ 4.161 a R$ 5.200 — parte inferior abaixo de 3 SM; marcamos como provável
            "De R$ 4.161,00 a 5.200,00":    "⚠️ Verificar (pode ser elegível)",
            # Acima de 3 SM
            "Acima de R$ 5.201,00":          "❌ Não elegível",
            # Declarados como Outro — requer análise manual
            "Outro":                          "⚠️ Verificar",
            "Outro:":                         "⚠️ Verificar",
        }

        def check_cadunico_elegibility(row):
            # Se já tem CadÚnico, não precisa requerer
            cadunico_val = str(row.get('CadÚnico', '')).strip().lower()
            if 'sim' in cadunico_val:
                return "✅ Já possui CadÚnico"
            renda = str(row.get('Renda Familiar', '')).strip()
            return ELEGIVEL_RENDA.get(renda, "⚠️ Verificar")

        df_eixo0 = df.copy()
        df_eixo0['Pode Requerer CadÚnico?'] = df_eixo0.apply(check_cadunico_elegibility, axis=1)

        # ── Métricas de elegibilidade ────────────────────────────────────────
        total = len(df_eixo0)
        ja_tem    = (df_eixo0['Pode Requerer CadÚnico?'] == "✅ Já possui CadÚnico").sum()
        elegiveis = (df_eixo0['Pode Requerer CadÚnico?'] == "✅ Elegível").sum()
        verificar = df_eixo0['Pode Requerer CadÚnico?'].str.startswith("⚠️").sum()
        nao_eleg  = (df_eixo0['Pode Requerer CadÚnico?'] == "❌ Não elegível").sum()

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("👥 Total de Estudantes", total)
        col_m2.metric("✅ Já possuem CadÚnico", ja_tem)
        col_m3.metric("📋 Elegíveis (sem CadÚnico)", elegiveis)
        col_m4.metric("⚠️ Verificar / Não elegíveis", verificar + nao_eleg)

        st.info(
            "**Critérios de Elegibilidade ao CadÚnico (Lei nº 10.836/2004):** "
            "Renda familiar total de até **3 salários mínimos** (R\\$ 4.554,00 em 2026) "
            "**ou** renda mensal per capita de até **meio salário mínimo** (R\\$ 759,00)."
        )

        st.divider()

        # ── Tabela principal ─────────────────────────────────────────────────
        display_cols = ['nome_completo', 'Bairro', 'CRAS de Referência', 'Renda Familiar',
                        'CadÚnico', 'Pode Requerer CadÚnico?']
        available_cols = [c for c in display_cols if c in df_eixo0.columns]

        subset_df = df_eixo0[available_cols].copy()
        if 'nome_completo' in subset_df.columns:
            subset_df['nome_completo'] = subset_df['nome_completo'].str.title()

        def style_eixo_0(row):
            val = str(row.get('Pode Requerer CadÚnico?', ''))
            if 'Já possui' in val:
                return ['background-color: #D4EDDA; color: #155724'] * len(row)
            elif val.startswith('✅'):
                return ['background-color: #CCE5FF; color: #004085'] * len(row)
            elif val.startswith('⚠️'):
                return ['background-color: #FFF3CD; color: #856404'] * len(row)
            elif val.startswith('❌'):
                return ['background-color: #F8D7DA; color: #721C24'] * len(row)
            return [''] * len(row)

        styled_subset = subset_df.style.apply(style_eixo_0, axis=1)
        st.dataframe(styled_subset, use_container_width=True, hide_index=True)

        st.markdown("""
        <div style='background-color: #F8F9FA; padding: 10px; border-radius: 5px; border: 1px solid #E9ECEF;'>
            <small>
                <span style='background-color: #D4EDDA; color: #155724; padding: 2px;'><b>Verde escuro</b></span> Já possui CadÚnico &nbsp;|&nbsp;
                <span style='background-color: #CCE5FF; color: #004085; padding: 2px;'><b>Azul</b></span> Elegível (sem CadÚnico) — prioridade para inscrição &nbsp;|&nbsp;
                <span style='background-color: #FFF3CD; color: #856404; padding: 2px;'><b>Amarelo</b></span> Verificar renda declarada &nbsp;|&nbsp;
                <span style='background-color: #F8D7DA; color: #721C24; padding: 2px;'><b>Vermelho</b></span> Renda acima do limite
            </small>
        </div>
        """, unsafe_allow_html=True)

elif section == "Eixo 1: Perfil Sociodemográfico":
    st.header("Eixo 1: Perfil Sociodemográfico")
    
    if len(df) == 0:
        st.warning("Nenhum dado completo encontrado no CSV.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            render_chart_with_stats(viz.chart_1_race_composition, df, 'Race_Group')
        with col2:
            # Gera estatísticas de gênero dinamicamente (Modelo A: MULHER TRANS agrupada em Feminina)
            _trans = ['MULHER TRANS', 'Mulher trans', 'mulher trans', 'Mulher Trans']
            _g_series = df['Identidade de Gênero'].replace(_trans, 'Feminina').value_counts()
            _n = _g_series.sum()
            _trans_count = df['Identidade de Gênero'].isin(_trans).sum()
            _parts = [f"{lbl}: {cnt} ({cnt/_n*100:.1f}%)" for lbl, cnt in _g_series.items()]
            _nota = f" — Nota: {_trans_count} estudante(s) se declarou mulher trans (inclusa em Feminina)." if _trans_count > 0 else ""
            gender_note = " | ".join(_parts) + _nota
            render_chart_with_stats(viz.chart_2_gender_distribution, df, custom_stats=gender_note)
        
        nota_chart3 = f"Nota: {_trans_count} estudante(s) se declarou mulher trans (inclusa em Feminina)." if _trans_count > 0 else ""
        render_chart_with_stats(viz.chart_3_race_by_gender, df, custom_stats=nota_chart3 if nota_chart3 else None)
        
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

        col5, col6 = st.columns(2)
        with col5:
            render_chart_with_stats(viz.chart_31_marital_status, df, 'Estado Civil')
        
        st.subheader("Origem Profissional Familiar")
        render_chart_with_stats(viz.chart_38_parental_professions_cloud, df)

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
        
        col_sust1, col_sust2 = st.columns(2)
        with col_sust1:
            render_chart_with_stats(viz.chart_36_household_sustenance, df, 'Ajuda no Sustento Familiar?')
        with col_sust2:
            render_chart_with_stats(viz.chart_33_benefits_breakdown, df)

        st.subheader("Segurança Alimentar e Trabalho")
        col_vulner1, col_vulner2 = st.columns(2)
        with col_vulner1:
            render_chart_with_stats(viz.chart_39_food_security, df)
        with col_vulner2:
            render_chart_with_stats(viz.chart_42_work_start_hours, df)

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
        render_chart_with_stats(viz.chart_37_transport_subsidy, df, 'transporte_auxilio')
        
        st.subheader("Disponibilidade de presença")
        render_chart_with_stats(viz.chart_40_study_availability, df)

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
        
        col11, col12 = st.columns(2)
        with col11:
            render_chart_with_stats(viz.chart_34_substance_use, df, 'Uso de Substâncias')
        with col12:
            render_chart_with_stats(viz.chart_35_family_context, df)
            
        st.subheader("Necessidades de Saúde")
        render_chart_with_stats(viz.chart_41_health_needs_cloud, df)

elif section == "Gestão e Operacionalização da Pesquisa":
    st.header("🔹 Gestão e Operacionalização da Pesquisa")
    
    if len(df) == 0:
        st.warning("Nenhum dado completo encontrado no CSV.")
    else:
        render_chart_with_stats(viz.chart_30_interviewer_balance, df, 'Entrevistador')

st.sidebar.markdown("---")
st.sidebar.caption("Desenvolvido por Heric Moura para Educafro Valongo © 2026")
