import streamlit as st
import numpy as np
#import matplotlib.pyplot as plt

#usuarios = ["Felipe Fontes", "Jullia Nascimento"]
#atividades = ["Pesquisa", "Ligação","Mensagem", ,]

# Título
st.title('Calculadora Mivus de Funil')

# Colunas para organizar a visualização
col1, col2 = st.columns(2)

# Coluna 1 - Inputs do usuário
with col1:
    st.header('Insira seus números')
    
    # Entradas
    ligacoes = st.number_input('Quantas ligações ou abordagens foram feitas?', min_value=0)
    atendidas = st.number_input('Quantas ligações foram atendidas (ou abordagens respondidas)?', min_value=0)
    reunioes_agendadas = st.number_input('Quantas reuniões foram agendadas?', min_value=0)

    if st.button('Calcular'):
        # Cálculos das taxas de conversão
        if ligacoes > 0:
            taxa_atendimento = (atendidas / ligacoes) * 100
        else:
            taxa_atendimento = 0

        if atendidas > 0:
            taxa_reuniao = (reunioes_agendadas / atendidas) * 100
        else:
            taxa_reuniao = 0


# Cálculos das taxas de conversão
if ligacoes > 0:
    taxa_atendimento = (atendidas / ligacoes) * 100
else:
    taxa_atendimento = 0

if atendidas > 0:
    taxa_reuniao = (reunioes_agendadas / atendidas) * 100
else:
    taxa_reuniao = 0
       

# Coluna 2 - Funil de Vendas Visual
with col2:
        # Avaliação e recomendações
        st.subheader('Avaliação e Recomendações:')
        if ligacoes < 20:
            st.warning("Você abordou menos que o recomendado. Tente abordar entre 20 a 50 pessoas por dia.")
        else:
            st.success("Bateu a meta do dia :D")

        if taxa_atendimento < 25:
            st.warning("A taxa de atendimento está abaixo da média (30%). Considere revisar a qualidade das suas listas ou melhorar o script de abordagem.")
        else:
            st.success("A taxa de atendimento está boa!")

        if taxa_reuniao < 10:
            st.warning("A taxa de agendamento de reuniões está abaixo da média (10%). Talvez seja interessante aprimorar suas técnicas de persuasão nas ligações.")
        else:
            st.success("A taxa de agendamento de reuniões está no nível recomendado!")


            
     # Exibir as taxas de conversão calculadas
        st.subheader('Resultados')
        if taxa_atendimento == 0:
            st.write('Aguardando dados...')
        else:
            st.write(f'Taxa de Conversão de Ligações Atendidas: {taxa_atendimento:.2f}%')
            st.write(f'Taxa de Conversão de Reuniões Agendadas: {taxa_reuniao:.2f}%')
