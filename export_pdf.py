import pandas as pd
from fpdf import FPDF
import visualizations as viz
import plotly.io as pio
import io
import os
from datetime import datetime
import tempfile

class EducafroPDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.set_text_color(29, 53, 87) # viz.COLORS['primary']
        self.cell(0, 10, 'Educafro | Perfil dos Estudantes 2026', border=False, ln=1, align='C')
        self.set_font('helvetica', 'I', 10)
        self.set_text_color(108, 117, 125) # viz.COLORS['neutral']
        self.cell(0, 10, f'Relat\u00f3rio Consolidado - Gerado em {datetime.now().strftime("%d/%m/%Y %H:%M")}', border=False, ln=1, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(169, 169, 169)
        self.cell(0, 10, f'P\u00e1gina {self.page_no()}/{{nb}}', align='C')

    def chapter_title(self, title):
        self.set_font('helvetica', 'B', 12)
        self.set_fill_color(233, 236, 239)
        self.set_text_color(29, 53, 87)
        self.cell(0, 10, f'  {title}', ln=1, fill=True)
        self.ln(2)

    def section_title(self, title):
        self.set_font('helvetica', 'B', 10)
        self.set_text_color(29, 53, 87)
        self.cell(0, 8, title, ln=1)
        # No LN here to keep chart close

    def add_plotly_chart(self, fig, width=160):
        if fig is None:
            return
        try:
            # High resolution export for better print quality
            img_bytes = pio.to_image(fig, format='png', width=1000, height=600, scale=2)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
                tmpfile.write(img_bytes)
                tmp_path = tmpfile.name
            
            page_width = self.w - 2 * self.l_margin
            x = self.l_margin + (page_width - width) / 2
            
            # Check if there is enough space on page, otherwise add page
            if (self.get_y() + 80) > (self.h - 20):
                self.add_page()
            
            self.image(tmp_path, x=x, w=width)
            os.unlink(tmp_path)
            self.ln(3)
        except Exception as e:
            self.set_font('helvetica', 'I', 8)
            self.set_text_color(230, 57, 70)
            self.cell(0, 10, f'Erro ao renderizar gr\u00e1fico Plotly: {str(e)}', ln=1)

    def add_wordcloud(self, buf, width=140):
        if buf is None:
            return
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
                tmpfile.write(buf.getvalue())
                tmp_path = tmpfile.name
            
            page_width = self.w - 2 * self.l_margin
            x = self.l_margin + (page_width - width) / 2
            
            if (self.get_y() + 60) > (self.h - 20):
                self.add_page()

            self.image(tmp_path, x=x, w=width)
            os.unlink(tmp_path)
            self.ln(3)
        except Exception as e:
            self.cell(0, 10, f'Erro ao renderizar WordCloud: {str(e)}', ln=1)

def generate_student_profile_pdf(df):
    pdf = EducafroPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- PAGE 1: RESUMO ---
    pdf.add_page()
    pdf.chapter_title("Resumo Geral e Indicadores-Chave")
    
    total = len(df)
    mulheres = (len(df[df['Identidade de Gênero'] == 'Feminina']) / total * 100) if total > 0 else 0
    pcd = len(df[df['Possui Deficiência?'] == 'Sim'])
    filhos = len(df[df['Tem Filhos?'] == 'Sim'])
    trabalha = len(df[(df['Vínculo de Trabalho'].notna()) & (df['Vínculo de Trabalho'] != 'Não')])

    pdf.set_font('helvetica', '', 11)
    text = (f"- Total de estudantes: {total}\n"
            f"- Representatividade feminina: {mulheres:.1f}%\n"
            f"- Estudantes com defici\u00eancia: {pcd}\n"
            f"- Estudantes que s\u00e3o pais/m\u00e3es: {filhos}\n"
            f"- Estudantes trabalhadores (Risco de evas\u00e3o): {trabalha}\n")
    pdf.multi_cell(0, 8, text)
    pdf.ln(5)

    # --- EIXO 1: SOCIODEMOGRÁFICO ---
    pdf.chapter_title("Eixo 1: Perfil Sociodemogr\u00e1fico")
    
    charts_eixo1 = [
        ("Composi\u00e7\u00e3o Racial", viz.chart_1_race_composition),
        ("Distribui\u00e7\u00e3o por G\u00eanero", viz.chart_2_gender_distribution),
        ("Ra\u00e7a por G\u00eanero", viz.chart_3_race_by_gender),
        ("Orientação Sexual", viz.chart_18_orientation),
        ("Tipo de Escola", viz.chart_19_school_type),
        ("Faixas Et\u00e1rias", viz.chart_4_age_groups),
        ("Cidades de Origem", viz.chart_5_geography),
        ("Estado Civil", viz.chart_31_marital_status)
    ]
    
    for title, func in charts_eixo1:
        pdf.section_title(title)
        pdf.add_plotly_chart(func(df))
    
    pdf.section_title("Origem Profissional Familiar (Nuvem)")
    pdf.add_wordcloud(viz.chart_38_parental_professions_cloud(df))

    # --- EIXO 2: TRABALHO E RENDA ---
    pdf.add_page()
    pdf.chapter_title("Eixo 2: Trabalho, Renda e Condi\u00e7\u00f5es Socioecon\u00f4micas")
    
    charts_eixo2 = [
        ("Situa\u00e7\u00e3o de Trabalho (Geral)", viz.chart_6_employment_general),
        ("Emprego por G\u00eanero", viz.chart_7_employment_by_gender),
        ("V\u00ednculos de Trabalho", viz.chart_8_job_categories),
        ("Renda Familiar Mensal", viz.chart_9_household_income),
        ("Recebimento de Benef\u00edcios Sociais", viz.chart_22_social_benefits),
        ("Escolaridade dos Pais", viz.chart_20_parental_education),
        ("Ajuda no Sustento Familiar", viz.chart_36_household_sustenance),
        ("Detalhamento de Benef\u00edcios", viz.chart_33_benefits_breakdown),
        ("Seguran\u00e7a Alimentar (Cesta B\u00e1sica)", viz.chart_39_food_security),
        ("In\u00edcio da Jornada de Trabalho", viz.chart_42_work_start_hours),
        ("Acesso \u00e0 Internet", viz.chart_11_tech_access),
        ("Qualidade do Dispositivo/Conex\u00e3o", viz.chart_11b_device_quality),
        ("Condi\u00e7\u00e3o de Moradia", viz.chart_12_housing),
        ("Tipo de Moradia", viz.chart_26_housing_type),
        ("Estudantes com Filhos", viz.chart_27_parenthood),
        ("Uso do Dinheiro do Trabalho", viz.chart_10_money_usage),
        ("Cadastro \u00danico (Cad\u00danico)", viz.chart_10b_cadunico)
    ]
    
    for title, func in charts_eixo2:
        pdf.section_title(title)
        pdf.add_plotly_chart(func(df))

    pdf.section_title("Detalhamento de V\u00ednculos (Nuvem)")
    pdf.add_wordcloud(viz.chart_8b_job_wordcloud(df))

    # --- EIXO 3: MOBILIDADE E INTERESSES ---
    pdf.add_page()
    pdf.chapter_title("Eixo 3: Mobilidade e Interesses Formativos")
    
    pdf.section_title("Temas de Interesse (Nuvem)")
    pdf.add_wordcloud(viz.chart_16_interests(df))
    
    pdf.section_title("Cursos Desejados (Nuvem)")
    pdf.add_wordcloud(viz.chart_17_courses(df))

    charts_eixo3 = [
        ("Meio de Transporte", viz.chart_23_transport_modes),
        ("Necessidade de Aux\u00edlio Transporte", viz.chart_37_transport_subsidy),
        ("Disponibilidade para Estudo", viz.chart_40_study_availability)
    ]
    for title, func in charts_eixo3:
        pdf.section_title(title)
        pdf.add_plotly_chart(func(df))

    # --- EIXO 4: SAÚDE E ASSISTÊNCIA ---
    pdf.add_page()
    pdf.chapter_title("Eixo 4: Sa\u00fade e Assist\u00eancia")
    
    charts_eixo4 = [
        ("Cobertura de Sa\u00fade", viz.chart_21_health_access),
        ("Sinal de Internet Local", viz.chart_25_internet_signal),
        ("Representa\u00e7\u00e3o de Defici\u00eancias", viz.chart_28_disability),
        ("Tipo Sangu\u00edneo", viz.chart_29_blood_type),
        ("Uso de Subst\u00e2ncias", viz.chart_34_substance_use),
        ("Configura\u00e7\u00e3o Familiar (Mora com quem)", viz.chart_35_family_context)
    ]
    for title, func in charts_eixo4:
        pdf.section_title(title)
        pdf.add_plotly_chart(func(df))

    pdf.section_title("Perfil de Sa\u00fade e Necessidades (Nuvem)")
    pdf.add_wordcloud(viz.chart_41_health_needs_cloud(df))

    # --- GESTÃO ---
    pdf.add_page()
    pdf.chapter_title("Gest\u00e3o e Operacionaliza\u00e7\u00e3o")
    pdf.section_title("Entrevistas por Entrevistador(a)")
    pdf.add_plotly_chart(viz.chart_30_interviewer_balance(df))

    return bytes(pdf.output())
