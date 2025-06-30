# app.py

import streamlit as st
import openai

st.set_page_config(layout="wide", page_title="Calcule o ROI do seu Lakehouse")

st.title("💰 Calcule o ROI do seu Lakehouse")

# Sliders/inputs
vol_ingested = st.slider("TB ingeridos/mês", 1, 100, 10)
spark_jobs = st.slider("Spark jobs/dia", 1, 500, 50)
on_prem_cost = st.number_input("Custo on-prem (R$/mês)", value=30000)

if st.button("➡️ Resumo em 5 linhas"):
    # Lógica de cálculo
    s3 = vol_ingested * 23  # R$ 23/TB-mês
    glue = spark_jobs * 0.44  # custo médio por DPU
    athena = vol_ingested * 5  # R$ 5/TB-scanned
    cloud_cost = s3 + glue + athena
    roi = (on_prem_cost - cloud_cost) / cloud_cost

    st.subheader("Resultados:")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Custo Cloud Estimado (R$/mês)", value=f"R$ {cloud_cost:,.2f}")
    with col2:
        st.metric(label="ROI", value=f"{roi:.2%}")

    # Chamada OpenAI
    openai.api_key = st.secrets["openai_api_key"]
    prompt = f"Explique para um CFO o ROI de {roi:.2%} migrando para lakehouse."

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        openai_summary = response.choices[0].message.content
        st.success(openai_summary)
    except Exception as e:
        st.error(f"Erro ao chamar a OpenAI: {e}")


