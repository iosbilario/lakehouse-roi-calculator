# 💰 Calculadora de ROI para Lakehouse na AWS

Este mini-aplicativo interativo, desenvolvido com Streamlit, permite calcular o Retorno sobre Investimento (ROI) ao migrar para uma arquitetura Lakehouse na AWS, comparando os custos com uma infraestrutura on-premise.

## Visão Geral

A ferramenta simula os custos de armazenamento (S3), processamento (Glue) e consulta (Athena) em um ambiente Lakehouse na AWS, contrastando-os com um custo on-premise fornecido pelo usuário. O ROI é então calculado e um resumo executivo é gerado por inteligência artificial (OpenAI) para CFOs.

## Setup Local

Para executar este aplicativo localmente, siga os passos abaixo:

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd lakehouse_roi_app
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: .venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure sua chave da OpenAI:**
    Crie um diretório `.streamlit` na raiz do projeto e, dentro dele, crie um arquivo `secrets.toml` com o seguinte conteúdo:
    ```toml
    openai_api_key = "SUA_CHAVE_OPENAI_AQUI"
    ```
    Substitua `SUA_CHAVE_OPENAI_AQUI` pela sua chave de API real da OpenAI.

5.  **Execute o aplicativo:**
    ```bash
    streamlit run app.py
    ```
    O aplicativo será aberto no seu navegador padrão.

## Custo Estimado AWS (Base de Cálculo)

Os cálculos de custo na AWS são baseados nas seguintes premissas (valores de referência e podem variar):

*   **Amazon S3:** R$ 23/TB-mês (custo de armazenamento)
*   **AWS Glue:** R$ 0.44 por DPU-hora (custo médio por DPU para jobs Spark)
*   **Amazon Athena:** R$ 5/TB-scanned (custo por dados consultados)

## Checklist LGPD

Este aplicativo foi desenvolvido com foco em privacidade e não coleta ou armazena dados pessoais. No entanto, ao utilizar a API da OpenAI, é importante considerar:

*   **Dados de Entrada:** Certifique-se de que nenhum dado pessoal ou sensível seja inserido nos campos de input que serão enviados para a API da OpenAI.
*   **Anonimização:** A prompt gerada para a OpenAI (`Explique para um CFO o ROI de {roi:.2%} migrando para lakehouse.`) não contém informações pessoais.
*   **Chave de API:** A chave da OpenAI deve ser tratada como credencial sensível e não deve ser exposta publicamente (por isso o uso de `secrets.toml`).
*   **Retenção de Dados:** Verifique a política de retenção de dados da OpenAI para entender como os dados enviados para a API são tratados e por quanto tempo são armazenados.

---

Desenvolvido por Manus AI para Velotax.

