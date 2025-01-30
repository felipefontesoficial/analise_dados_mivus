import streamlit as st

st.set_page_config(
    layout="wide",
    page_title="App Mivus"
)


logo = "caminho_para_sua_logo.png" 
st.sidebar.image(logo, use_container_width=True)  # Atualizado para o parâmetro correto
st.sidebar.write("Feito por: [Mivus Academy](https://www.mivus.com.br)")

st.title("Olá, Querido Lendário 😀")
st.write("Agora, tudo o que você precisa estará organizado em um só lugar.")

st.markdown("---") # Separador

#Título da Coluna

#col1, col2 = st.columns([0.7, 0.3])
#col1.subheader(":balloon: Desafio 70 Leads em 1 Semana ")
#col2.write("**Data:** 02/12 à 06/12/2024")

#st.write("\n") #Espaço em branco


# Apresentação do desafio

#st.markdown("""**Regras do Desafio:**
