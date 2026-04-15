import pandas as pd
from data_loader import load_data
from export_pdf import generate_student_profile_pdf
import os

def main():
    try:
        print("Carregando dados...")
        df = load_data('data/entrevistas_consolidated.csv')
        
        print("Gerando PDF completo (40 graficos)... Isso pode levar alguns segundos.")
        pdf_bytes = generate_student_profile_pdf(df)
        
        output_path = 'artifacts/Relatorio_Completo_Educafro_2026.pdf'
        os.makedirs('artifacts', exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(pdf_bytes)
            
        print(f"PDF gerado com sucesso em: {os.path.abspath(output_path)}")
        print(f"Tamanho do arquivo: {len(pdf_bytes) / 1024:.2f} KB")
        
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
