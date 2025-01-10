def load_data():
    import boto3
    import pandas as pd
    from io import StringIO
    import streamlit as st

    # Acessando as credenciais do secrets.toml
    access_key = st.secrets["aws"]["access_key"]
    secret_access_key = st.secrets["aws"]["secret_access_key"]

    # Configura o cliente S3 com as credenciais
    s3_client = boto3.client('s3',
                            aws_access_key_id=access_key,
                            aws_secret_access_key=secret_access_key,
                            region_name='sa-east-1')  # Ajuste para sua região

    # Nome do bucket e do arquivo
    bucket_name = 'mee-analise.juridica1'
    file_key = 'data-coca.csv'

    # Baixa o arquivo CSV diretamente do S3
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)

    # Lê o conteúdo do CSV
    csv_content = response['Body'].read().decode('utf-8')

    # Converte para DataFrame
    df = pd.read_csv(StringIO(csv_content))

    return df