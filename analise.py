import streamlit as st
import numpy as np

# Título
st.title('Calculadora Mivus de Funil')

# Colunas para organizar a visualização
col1, col2 = st.columns(2)

# Coluna 1 - Inputs do usuário
with col1:
    st.header('Insira seus números')
    
    # Entradas
    ligacoes = st.number_input('Quantas ligações foram feitas?', min_value=0)
    atendidas = st.number_input('Quantas ligações foram atendidas?', min_value=0)
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



       

# Coluna 2 - Funil de Vendas Visual
with col2:
     # Exibir as taxas de conversão calculadas


        # Avaliação e recomendações
        st.subheader('Avaliação e Recomendações:')
        if ligacoes < 50:
            st.warning("Você abordou menos que o recomendado. Tente abordar entre 50 a 100 novas pessoas semanalmente.")
        
        if taxa_atendimento < 30:
            st.warning("A taxa de atendimento está abaixo da média (30%). Considere revisar a qualidade das suas listas ou melhorar o script de abordagem.")
        else:
            st.success("A taxa de atendimento está boa!")

        if taxa_reuniao < 10:
            st.warning("A taxa de agendamento de reuniões está abaixo da média (10%). Talvez seja interessante aprimorar suas técnicas de persuasão nas ligações.")
        else:
            st.success("A taxa de agendamento de reuniões está no nível recomendado!")


try:
        st.subheader('Resultados')
        st.write(f'Taxa de Conversão de Ligações Atendidas: {taxa_atendimento:.2f}%')
        st.write(f'Taxa de Conversão de Reuniões Agendadas: {taxa_reuniao:.2f}%')
        st.write(f'Taxa de Conversão de Reuniões para Vendas: {taxa_fechamento:.2f}%')

except:
    print("Vamos começar?")
