import streamlit as st
import requests
import json

usuarios = ["Kactus Contabilidade", "Sales Box", "Planos Consultoria", "Solarce Energia"]

# Configuração da página
st.set_page_config(page_title="Minha aplicação", page_icon=":shark:", layout="wide")

# Tema escuro
st.markdown(
    """
    <style>
    body {
        background-color: #212121; 
        color: #ffffff; 
    }
    .stButton>button {
        background-color: #007bff; 
        color: #ffffff; 
    }
    /* Outros estilos personalizados, se necessário */
    </style>
    """,
    unsafe_allow_html=True,
)

# Carregando a logo
logo = "caminho_para_sua_logo.png"  # Substitua pelo caminho correto
st.sidebar.image(logo, use_column_width=True)

# Opções do menu lateral
opcao = st.sidebar.selectbox(
    "Selecione uma opção:",
    ("Verificar Dados CNPJ", "Calculadora de Funil")  # Ordem das opções invertida
)

# Função para mostrar a calculadora de funil
def mostrar_calculadora_funil():
    st.title('Calculadora Mivus de Funil')
    st.write("---")

    st.sidebar.subheader("Selecione seu perfil abaixo:")
    usuario_selecionado = st.sidebar.selectbox(
        "",
        (usuarios),
        index=None,
        placeholder="Selecione seu usuário",
    )

    st.sidebar.write("Você é:", usuario_selecionado)

    col1, col2 = st.columns(2)

    with col1:
        st.header('Insira seus números')
        
        ligacoes = st.number_input('Quantas ligações ou abordagens foram feitas?', min_value=0)
        atendidas = st.number_input('Quantas ligações foram atendidas (ou abordagens respondidas)?', min_value=0)
        reunioes_agendadas = st.number_input('Quantas reuniões foram agendadas?', min_value=0)

        if st.button('Calcular'):
            if ligacoes > 0:
                taxa_atendimento = (atendidas / ligacoes) * 100
            else:
                taxa_atendimento = 0

            if atendidas > 0:
                taxa_reuniao = (reunioes_agendadas / atendidas) * 100
            else:
                taxa_reuniao = 0

            with col2:
                st.subheader('Avaliação e Recomendações:')
                if ligacoes == 0:
                    st.warning("Aguardando dados...")
                elif ligacoes < 20:
                    st.warning("Você abordou menos que o recomendado. Tente abordar entre 20 a 50 pessoas por dia.")
                else:
                    st.success("Bateu a meta do dia :D")

                if taxa_atendimento == 0:
                    st.warning("Aguardando dados...")
                elif taxa_atendimento < 25:
                    st.warning("A taxa de atendimento está abaixo da média (30%). Considere revisar a qualidade das suas listas ou melhorar o script de abordagem.")
                else:
                    st.success("A taxa de atendimento está boa!")

                if taxa_reuniao == 0:
                    st.warning("Aguardando dados...")
                elif taxa_reuniao < 10:
                    st.warning("A taxa de agendamento de reuniões está abaixo da média (10%). Talvez seja interessante aprimorar suas técnicas de persuasão nas ligações.")
                else:
                    st.success("A taxa de agendamento de reuniões está no nível recomendado!")

                st.subheader('Resultados')
                if taxa_atendimento == 0:
                    st.write('Aguardando dados...')
                else:
                    st.write(f'Taxa de Conversão de Ligações Atendidas: {taxa_atendimento:.2f}%')
                    st.write(f'Taxa de Conversão de Reuniões Agendadas: {taxa_reuniao:.2f}%')

# Função para mostrar a consulta de CNPJ
def mostrar_consulta_cnpj():
    st.title("Consultor de CNPJ Mivus")

    cnpj_input = st.text_input("Digite o CNPJ:", "")
    cnpj_input = cnpj_input.replace(".", "").replace("-", "").replace("/", "")
    if st.button("Consultar"):
        if cnpj_input:
            consulta_cnpj(cnpj_input)
        else:
            st.warning("Por favor, digite um CNPJ.")

def consulta_cnpj(cnpj):
    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
    querystring = {"token": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXX", "cnpj": "06990590000123", "plugin": "RF"} 
    response = requests.request("GET", url, params=querystring)

    if response.status_code == 200:
        resp = json.loads(response.text)

        data_abertura = resp.get('abertura', 'Não disponível')
        situacao = resp.get('situacao', 'Não disponível')
        nome_fantasia = resp.get('fantasia', 'Não disponível')
        porte = resp.get('porte', 'Não disponível')
        complemento = resp.get('complemento', '')
        data_situacao = resp.get('data_situacao', 'Não disponível')
        numero_socios = len(resp.get('qsa', []))  

        st.markdown("---") 

        st.header(f"Informações da Empresa - CNPJ: {resp.get('cnpj', 'Não encontrado')}")

        st.subheader("Dados principais:")
        st.write(f"Nome: {resp.get('nome', 'Não disponível')}")
        st.write(f"Nome Fantasia: {nome_fantasia}")
        st.write(f"Data de Abertura: {data_abertura}")
        st.write(f"Situação: {situacao}")
        st.write(f"Porte: {porte}")
        
        st.subheader("Endereço:")
        st.write(f"{resp.get('logradouro', '')}, {resp.get('numero', '')} {complemento} - {resp.get('bairro', '')} - {resp.get('municipio', '')} ({resp.get('uf', '')}) - CEP: {resp.get('cep', '')}")

        st.subheader("Outras Informações:")
        st.write(f"Atividade Principal: {resp.get('atividade_principal', [{}])[0].get('text', 'Não disponível')}")
        st.write(f"E-mail: {resp.get('email', 'Não disponível')}")
        st.write(f"Telefone: {resp.get('telefone', 'Não disponível')}")
        st.write(f"Data da Situação: {data_situacao}")
        st.write(f"Número de Sócios: {numero_socios}")

        # Encontrar e exibir o administrador
        st.subheader("Administrador:")
        administrador = None
        for socio in resp.get('qsa', []):
            if "administrador" in socio['qual'].lower():
                administrador = socio['nome']
                break

        if administrador:
            st.write(administrador)
        else:
            st.write("Nenhum administrador encontrado.")

        st.subheader("Sócios:")
        if numero_socios > 0:
            for socio in resp['qsa']:
                st.write(f"- {socio['nome']} ({socio['qual']})")
        else:
            st.write("Nenhum sócio encontrado.")

    elif response.status_code == 404:
        st.error("CNPJ não encontrado.")
    else:
        st.error("Ocorreu um erro ao consultar o CNPJ. Verifique o CNPJ e tente novamente.")


# Mostrar a opção selecionada
if opcao == "Calculadora de Funil":
    mostrar_calculadora_funil()
elif opcao == "Verificar Dados CNPJ":
    mostrar_consulta_cnpj()
