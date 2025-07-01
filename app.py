# app.py

import streamlit as st
import base64
from datetime import datetime

# Configuração da página
st.set_page_config(
    layout="centered", 
    page_title="Calcule o ROI do seu Lakehouse",
    page_icon="💰"
)

# Função para gerar PDF do relatório
def generate_pdf_report(vol_ingested, spark_jobs, on_prem_cost, s3, glue, athena, cloud_cost, roi):
    report_content = f"""
# Relatório de ROI - Migração para Lakehouse AWS

**Data:** {datetime.now().strftime("%d/%m/%Y %H:%M")}

## Parâmetros de Entrada
- **TB ingeridos/mês:** {vol_ingested} TB
- **Spark jobs/dia:** {spark_jobs} jobs
- **Custo on-premise atual:** R$ {on_prem_cost:,.2f}

## Custos AWS Estimados
- **Amazon S3 (Armazenamento):** R$ {s3:.2f}/mês
- **AWS Glue (Processamento):** R$ {glue:.2f}/mês  
- **Amazon Athena (Consultas):** R$ {athena:.2f}/mês
- **Total Cloud:** R$ {cloud_cost:.2f}/mês

## Análise de ROI
- **Economia Mensal:** R$ {on_prem_cost - cloud_cost:,.2f}
- **ROI:** {roi:.2%}
- **Economia Anual:** R$ {(on_prem_cost - cloud_cost) * 12:,.2f}

## Metodologia de Cálculo
O ROI é calculado usando a fórmula:
**ROI = (Custo On-Premise - Custo Cloud) / Custo Cloud**

### Premissas de Custo AWS:
- **S3:** R$ 23/TB-mês (armazenamento padrão)
- **Glue:** R$ 0,44 por DPU-hora (processamento Spark)
- **Athena:** R$ 5/TB-scanned (consultas SQL)

---
*Relatório gerado pela Calculadora de ROI - LBP Tecnologia*
"""
    return report_content

# CSS customizado para estilo calculadora iOS
st.markdown("""
<style>
    /* Importar fonte SF Pro Display similar ao iOS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Reset e configurações gerais */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
        min-height: 100vh;
    }
    
    /* Container principal da calculadora */
    .calculator-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        max-width: 500px;
        margin: 0 auto;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Título principal */
    .main-title {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a1a;
        text-align: center;
        margin-bottom: 1.5rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Estilo dos sliders */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    .stSlider > div > div > div > div > div {
        background: white;
        border: 3px solid #667eea;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Estilo dos inputs */
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid #e1e5e9;
        border-radius: 15px;
        padding: 12px 16px;
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Botão principal */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 15px 30px;
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
    }
    
    /* Métricas */
    .metric-container {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .metric-container h3 {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        font-weight: 500;
        color: #666;
        margin-bottom: 0.5rem;
    }
    
    .metric-container p {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a1a;
        margin: 0;
    }
    
    /* Labels dos inputs */
    .stSlider label, .stNumberInput label {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #333;
        font-size: 1rem;
    }
    
    /* Mensagem informativa */
    .stInfo {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 15px;
        padding: 1rem;
    }
    
    /* Seção de resultados */
    .results-section {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 1.5rem;
        margin-top: 2rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    
    .results-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Seção de metodologia */
    .methodology-section {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    /* Rodapé */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        color: rgba(255, 255, 255, 0.8);
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
    }
    
    .footer a {
        color: white;
        text-decoration: none;
        font-weight: 600;
    }
    
    .footer a:hover {
        text-decoration: underline;
    }
    
    /* Botão de download */
    .download-button {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 10px 20px;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
        margin-top: 1rem;
    }
    
    .download-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
    }

    /* Esconder elementos específicos do Streamlit que podem causar blocos em branco */
    .stApp > header {
        display: none !important; /* Esconde o cabeçalho padrão do Streamlit */
    }
    .stApp > footer {
        display: none !important; /* Esconde o rodapé padrão do Streamlit */
    }
    
    /* CORREÇÃO ESPECÍFICA: Remover blocos brancos vazios */
    /* Esconder containers vazios que aparecem como blocos brancos */
    .stApp div[data-testid="stVerticalBlock"]:empty {
        display: none !important;
    }
    
    /* Esconder elementos vazios que criam blocos brancos */
    .stApp div[data-testid="element-container"]:empty {
        display: none !important;
    }
    
    /* Remover espaçamentos de containers vazios */
    .stApp div:empty {
        display: none !important;
    }
    
    /* Esconder blocos de markdown vazios */
    .stMarkdown:empty {
        display: none !important;
    }
    
    /* Remover containers de coluna vazios */
    .stApp div[data-testid="column"]:empty {
        display: none !important;
    }
    
    /* Esconder elementos de layout vazios */
    .element-container:empty {
        display: none !important;
    }
    
    /* Remover espaçamento superior desnecessário */
    .main .block-container {
        padding-top: 0.5rem !important;
        margin-top: 0 !important;
    }
    
    /* Ajustar o container principal para remover espaços em branco */
    .stApp {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Remover espaçamento do elemento main */
    .main {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Corrigir espaçamentos entre seções */
    .stMarkdown {
        margin-bottom: 0.5rem !important;
        margin-top: 0.5rem !important;
    }
    
    /* Remover espaçamentos excessivos dos containers de elementos */
    .element-container {
        margin-bottom: 0.5rem !important;
        margin-top: 0.5rem !important;
    }
    
    /* Ajustar espaçamento dos botões */
    .stButton {
        margin-bottom: 1rem !important;
        margin-top: 0.5rem !important;
    }
    
    /* Remover espaços em branco de divs vazias do Streamlit */
    .stApp div[data-testid="stVerticalBlock"] > div:empty {
        display: none !important;
    }
    
    /* Ajustar espaçamento das seções de resultados */
    .results-section {
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Remover espaçamentos desnecessários entre elementos */
    .stApp > div > div > div > div {
        margin-bottom: 0.5rem !important;
    }
    /* Ajuste para o botão de download */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 10px 20px;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
        margin-top: 1rem;
        width: auto; /* Ajusta a largura para não ocupar 100% */
    }
    .stDownloadButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Container principal
st.markdown("""<div class="calculator-container">""", unsafe_allow_html=True)

# Título
st.markdown("""<h1 class="main-title">💰 Calcule o ROI do seu Lakehouse</h1>""", unsafe_allow_html=True)

# Seção de metodologia (sempre visível)
with st.expander("📚 Como é calculado o ROI?", expanded=False):
    st.markdown("""
    ### 🧮 Metodologia de Cálculo
    
    O **ROI (Return on Investment)** é calculado usando a fórmula:
    
    ```
    ROI = (Custo On-Premise - Custo Cloud) / Custo Cloud
    ```
    
    ### 💰 Premissas de Custo AWS:
    - **Amazon S3:** R$ 23/TB-mês (armazenamento padrão)
    - **AWS Glue:** R$ 0,44 por DPU-hora (processamento Spark)
    - **Amazon Athena:** R$ 5/TB-scanned (consultas SQL)
    
    ### 📊 Exemplo:
    Se seu custo on-premise é R$ 30.000/mês e o custo estimado na AWS é R$ 300/mês:
    - **Economia:** R$ 29.700/mês
    - **ROI:** 9.900% (99x retorno)
    
    *Os valores são estimativas baseadas em preços de referência da AWS.*
    """)

# Inputs com estilo melhorado
st.markdown("### 📊 Parâmetros de Entrada")

col1, col2 = st.columns(2)

with col1:
    vol_ingested = st.slider("TB ingeridos/mês", 1, 100, 10, help="Volume de dados ingeridos mensalmente")
    
with col2:
    spark_jobs = st.slider("Spark jobs/dia", 1, 500, 50, help="Número de jobs Spark executados diariamente")

on_prem_cost = st.number_input("Custo on-prem (R$/mês)", value=30000, help="Custo atual da infraestrutura on-premise")

# Botão de cálculo
if st.button("🚀 Calcular ROI"):
    # Lógica de cálculo
    s3 = vol_ingested * 23  # R$ 23/TB-mês
    glue = spark_jobs * 0.44  # custo médio por DPU
    athena = vol_ingested * 5  # R$ 5/TB-scanned
    cloud_cost = s3 + glue + athena
    roi = (on_prem_cost - cloud_cost) / cloud_cost

    # Resultados
    st.markdown("""<div class="results-section">""", unsafe_allow_html=True)
    st.markdown("""<h2 class="results-title">📈 Resultados</h2>""", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="💰 Custo Cloud Estimado (R$/mês)", 
            value=f"R$ {cloud_cost:,.2f}",
            delta=f"R$ {on_prem_cost - cloud_cost:,.2f} economia"
        )
    with col2:
        st.metric(
            label="📊 ROI", 
            value=f"{roi:.2%}",
            delta="Retorno sobre investimento"
        )
    
    # Breakdown dos custos
    st.markdown("### 💡 Detalhamento dos Custos AWS")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🗄️ Amazon S3", f"R$ {s3:.2f}")
    with col2:
        st.metric("⚙️ AWS Glue", f"R$ {glue:.2f}")
    with col3:
        st.metric("🔍 Amazon Athena", f"R$ {athena:.2f}")
    
    # Análise adicional
    st.markdown("### 📊 Análise Financeira")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💵 Economia Anual", f"R$ {(on_prem_cost - cloud_cost) * 12:,.2f}")
    with col2:
        payback_months = cloud_cost / (on_prem_cost - cloud_cost) if (on_prem_cost - cloud_cost) > 0 else 0
        st.metric("⏱️ Payback", f"{payback_months:.1f} meses" if payback_months > 0 else "Imediato")
    
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    # Botão para gerar relatório PDF
    st.markdown("### 📄 Relatório Detalhado")
    
    # Gerar conteúdo do relatório
    report_content = generate_pdf_report(vol_ingested, spark_jobs, on_prem_cost, s3, glue, athena, cloud_cost, roi)
    
    # Botão de download
    st.download_button(
        label="📥 Baixar Relatório PDF",
        data=report_content,
        file_name=f"relatorio_roi_lakehouse_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
        mime="text/markdown",
        help="Baixe um relatório detalhado em formato Markdown"
    )
    
    st.success("✅ Cálculo realizado com sucesso!")

st.markdown("""</div>""", unsafe_allow_html=True)

# Rodapé
st.markdown("""
<div class="footer">
    Desenvolvido por <a href="https://is.gd/xaV8Iq" target="_blank">LBP Tecnologia</a> 
    <br>
    <small>Calculadora de ROI para Lakehouse na AWS</small>
</div>
""", unsafe_allow_html=True)



