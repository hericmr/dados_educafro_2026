# Dashboard de Análise Educafro 2026

Este projeto automatiza a visualização dos dados sociodemográficos e de interesse dos alunos da Educafro Santos, baseando-se no formulário de 2026.

## Como Executar Localmente

1. **Crie um ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicie o Dashboard:**
   ```bash
   streamlit run app.py
   ```

## Como Hospedar no Streamlit Cloud (Online e Grátis)

1. Vá para [share.streamlit.io](https://share.streamlit.io).
2. Conecte sua conta do GitHub.
3. Clique em **"New app"**.
4. Selecione este repositório (`hericmr/dados_educafro_2026`), o branch `main` e o arquivo `app.py`.
5. Clique em **"Deploy!"**.

## Estrutura do Projeto

- `app.py`: Interface principal do Streamlit.
- `data_loader.py`: Lógica de carregamento e limpeza de dados (Mapeamento snake_case).
- `visualizations.py`: Funções para geração dos 17 gráficos do relatório original.
- `requirements.txt`: Lista de bibliotecas necessárias.

---
Desenvolvido para Educafro Santos © 2026
