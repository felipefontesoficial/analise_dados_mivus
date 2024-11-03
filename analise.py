import os
import streamlit as st
import requests
import json
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

# Configuração da API para o chatbot
api_key = 'API_KEY'  
os.environ['GROQ_API_KEY'] = api_key
chat = ChatGroq(model='llama-3.1-70b-versatile')

# Lista de usuários (pode ser modificada conforme necessário)
usuarios = ["Kactus Contabilidade", "Sales Box", "Planos Consultoria", "Solarce Energia"]

# Função para obter a resposta do bot
def resposta_do_bot(lista_mensagens):
    system_message = ('system', """Você é o Mivinho um assistente pessoal amigável que tem como objetivo ajudar os alunos da Mivus. 
                      Os alunos da Mivus são SDR que é o Representante de Desenvolvimento de Vendas (Sales Development Representative).
                      Sua missão seja ajudar esses alunos a tomar decisões para sua rotina de prospecção e ajudar eles na estruturação de roteiros de vendas, faça isso interagindo com ele realizando perguntas em bullet points enumerado para auxiliar na sua tomada de decisão.( use como base o livro SPIN Selling e o Receita Previsível para dar esses direcionamentos).
                      Você deverá usar um tom de voz coloquial e simples, porém, não informal, Falando sempre de forma curta, usando poucas palavras e objetiva de uma forma mais descontraída inclusive.
                      Lembrando, que quem te criou foi o Felipe Fontes o Copywriter Mais Lindo do Brasil! (Essa informação é só para caso alguém pergunte) 
                       """)
    template = ChatPromptTemplate.from_messages([system_message] + lista_mensagens)
    chain = template | chat
    return chain.invoke({}).content

# --- Funções do sistema ---

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
    querystring = {"token": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXX", "cnpj": "06990590000123", "plugin": "RF"} # coloque sua token válida aqui!
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

# Função para mostrar a interface de chat com o Mivinho
def mostrar_chat_mivus():
    st.title("Bem-vindo ao Chat Mivus!")
    st.write("Digite sua pergunta e receba ajuda para tomar decisões empresariais.")

    # Inicializa o histórico de mensagens se não existir
    if 'mensagens' not in st.session_state:
        st.session_state['mensagens'] = []

    # Entrada do usuário usando o st.chat_input
    prompt = st.chat_input("Digite sua pergunta...")

    # Processamento do prompt
    if prompt:
        # Adiciona a mensagem do usuário ao histórico
        st.session_state['mensagens'].append(('user', prompt))
        
        # Chama o bot para obter a resposta e adiciona ao histórico
        resposta = resposta_do_bot(st.session_state['mensagens'])
        st.session_state['mensagens'].append(('assistant', resposta))

    # Exibir o histórico de mensagens usando o st.chat_message
    for role, message in st.session_state['mensagens']:
        with st.chat_message("user" if role == 'user' else "assistant"):
            st.write(message)

# Função para consultar RDAP e exibir os dados
def consultar_rdap(dominio):
    url = f"https://rdap.registro.br/domain/{dominio}"
    resposta = requests.get(url)
    if resposta.status_code == 200:
        dados = resposta.json()

        # Extraindo os dados desejados
        nome_dominio = dados['handle']
        status = dados['status'][0]

        # Percorrendo as entidades para encontrar o registrante
        for entidade in dados['entities']:
            if 'roles' in entidade and 'registrant' in entidade['roles']:
                razao_social = entidade['vcardArray'][1][2][2]
                handle_registrante = entidade['handle']
                representante_legal = entidade.get('legalRepresentative', 'Não informado')
                
                # Verificando se o CNPJ/CPF está presente
                cnpj_cpf = 'Não informado'
                if 'publicIds' in entidade:
                    for public_id in entidade['publicIds']:
                        if public_id['type'] in ('cnpj', 'cpf'):
                            cnpj_cpf = public_id['identifier']
                break
        
        # Exibindo os dados utilizando elementos do Streamlit
        st.subheader(f"Informações do domínio {dominio}:")
        st.write(f"Nome do Domínio: {nome_dominio}")
        st.write(f"Status: {status}")
        st.write(f"Razão Social: {razao_social}")
        st.write(f"CNPJ/CPF: {cnpj_cpf}")
        st.write(f"Handle do Registrante: {handle_registrante}")
        st.write(f"Representante Legal: {representante_legal}")

    else:
        st.error(f"Erro ao consultar o domínio: {resposta.status_code}")

# Função para mostrar a interface da consulta de domínio
def mostrar_consulta_dominio():
    st.title("Consultar Domínio")
    dominio_input = st.text_input("Digite o domínio:")
    if st.button("Consultar"):
        if dominio_input:
            consultar_rdap(dominio_input)
        else:
            st.warning("Por favor, digite um domínio.")

# --- Configuração da página ---
st.set_page_config(page_title="Mivus App", page_icon=":rocket:", layout="wide")

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
    </style>
    """,
    unsafe_allow_html=True,
)

# Carregando a logo (substitua pelo caminho correto)
logo = "caminho_para_sua_logo.png" 
st.sidebar.image(logo, use_column_width=True)

# --- Menu lateral ---
opcao = st.sidebar.selectbox(
    "Selecione uma opção:",
    ("Verificar Dados CNPJ", "Consultar Domínio", "Calculadora de Funil", "Chat Mivus")
)

# --- Lógica principal ---
if opcao == "Calculadora de Funil":
    mostrar_calculadora_funil()
elif opcao == "Verificar Dados CNPJ":
    mostrar_consulta_cnpj()
elif opcao == "Consultar Domínio":
    mostrar_consulta_dominio()
elif opcao == "Chat Mivus":
    mostrar_chat_mivus()
