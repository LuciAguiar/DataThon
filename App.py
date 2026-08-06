import streamlit as st
import pandas as pd
import joblib
import base64
import os

    
# Configuração da página
st.set_page_config(page_title="Passos Mágicos - Radar Pedagógico", page_icon="🔮", layout="wide")

# Carregar o NOVO modelo em cache
@st.cache_resource
def load_model():
    return joblib.load('modelo_passos_magicos_2023.pkl')

modelo = load_model()


# ==========================================
# MENU LATERAL (SIDEBAR)
# ==========================================
# Inserindo a logomarca da Associação
if os.path.exists("Passos-magicos.png"):
    st.sidebar.image("Passos-magicos.png", use_container_width=True)

st.sidebar.title("Navegação")

# Opções do menu 
menu = st.sidebar.radio(
    "Selecione a página:", 
    ["Analise Preditiva", "Dashboards Dados 2022 - 2024", "Documentação Executiva"]
)

st.sidebar.divider()
st.sidebar.info("Utilize este menu para navegar entre o simulador preditivo, as análises históricas e a documentação oficial.")

# ==========================================
# PÁGINA 1: ANÁLISE PREDITIVA
# ==========================================
if menu == "Analise Preditiva":
    st.title("Radar de Prevenção e Intervenção - Passos Mágicos 🔮")
    
    st.markdown("""
    Esta ferramenta permite simular o impacto dos indicadores acadêmicos e psicossociais 
    na classificação final do aluno (Pedra). Ajuste os valores abaixo para realizar uma **Análise What-If**.
    """)
    
    # Tabela de Referência Visual (Com Imagens JPG)
    st.markdown("### 📊 Tabela de Referência (INDE)")
    
    # TRUQUE DE LAYOUT: [1, 1, 1, 1, 4] 
    # As 4 primeiras colunas têm peso "1" (ficam estreitas e juntas).
    # A última coluna tem peso "4" (serve como um espaçador vazio enorme à direita).
    col_q, col_ag, col_am, col_t, espacador = st.columns([1, 1, 1, 1, 3])
    
    with col_q:
        if os.path.exists("Quartzo.jpg"):
            st.image("Quartzo.jpg", width=120) 
        else:
            st.caption("*(Imagem pendente)*")
        st.markdown("##### Quartzo")
        st.caption("(2,40 a 5,50)")
        
    with col_ag:
        if os.path.exists("Agata.jpeg"):
            st.image("Agata.jpeg", width=120)
        else:
            st.caption("*(Imagem pendente)*")
        st.markdown("##### Ágata")
        st.caption("(5,50 a 6,86)")
        
    with col_am:
        if os.path.exists("Ametista.jpeg"):
            st.image("Ametista.jpeg", width=120)
        else:
            st.caption("*(Imagem pendente)*")
        st.markdown("##### Ametista")
        st.caption("(6,86 a 8,23)")
        
    with col_t:
        if os.path.exists("Topazio.jpeg"):
            st.image("Topazio.jpeg", width=120)
        else:
            st.caption("*(Imagem pendente)*")
        st.markdown("##### Topázio")
        st.caption("(8,23 a 9,29)")

    st.divider()

    # ---------------------------------------------------------
    # ENTRADA DE DADOS (SLIDERS COM IPP)
    # ---------------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Indicadores Acadêmicos e Engajamento")
        
        st.markdown("**Notas das Disciplinas Base (Cálculo do IDA)**")
        nota_mat = st.slider("Matemática", 0.0, 10.0, 5.0, 0.1)
        nota_por = st.slider("Português", 0.0, 10.0, 5.0, 0.1)
        nota_ing = st.slider("Inglês", 0.0, 10.0, 5.0, 0.1)
        
        # Cálculo dinâmico do IDA
        ida = (nota_mat + nota_por + nota_ing) / 3
        st.info(f"**IDA Calculado (Média):** {ida:.2f}")
        
        st.markdown("**Outros Indicadores Acadêmicos**")
        ieg = st.slider("IEG - Indicador de Engajamento", 0.0, 10.0, 5.0, 0.1)
        
        # Novo IAN com Radio Button (horizontal para ficar mais elegante)
        ian_opcao = st.radio(
            "IAN - Adequação de Nível",
            options=["Em Fase", "Moderada", "Severa"],
            index=1,  # Inicia marcado no "Moderada" (equivalente ao 5.0 antigo)
            horizontal=True
        )
        
        # Lógica de tradução: converte o texto do botão no número exato para o modelo
        if ian_opcao == "Em Fase":
            ian = 10.0
        elif ian_opcao == "Moderada":
            ian = 5.0
        elif ian_opcao == "Severa":
            ian = 2.5
    with col2:
        st.subheader("Indicadores Psicossociais e de Base")
        ipp = st.slider("IPP - Indicador Psicopedagógico", 0.0, 10.0, 5.0, 0.1)
        ipv = st.slider("IPV - Ponto de Virada", 0.0, 10.0, 5.0, 0.1)
        ips = st.slider("IPS - Indicador Psicossocial", 0.0, 10.0, 5.0, 0.1)
        iaa = st.slider("IAA - Autoavaliação", 0.0, 10.0, 5.0, 0.1)

    st.divider()

    # Cálculo automático do INDE Oficial (com IPP)
    pesos = {'IAN': 0.1, 'IDA': 0.2, 'IEG': 0.2, 'IAA': 0.1, 'IPS': 0.1, 'IPV': 0.2, 'IPP': 0.1}
    inde_simulado = (ian*pesos['IAN'] + ida*pesos['IDA'] + ieg*pesos['IEG'] + 
                     iaa*pesos['IAA'] + ips*pesos['IPS'] + ipv*pesos['IPV'] + ipp*pesos['IPP'])

    st.write(f"**INDE Atual Simulado:** {inde_simulado:.2f}")

    # Botão de Predição
    if st.button("Simular Classificação (Pedra) no Próximo Ano", type="primary"):
        # A ordem deve ser estritamente igual a do treinamento:
        features = ['IAN', 'IDA', 'IEG', 'IAA', 'IPS', 'IPV', 'IPP', 'INDE_ATUAL']
        entrada = pd.DataFrame([[ian, ida, ieg, iaa, ips, ipv, ipp, inde_simulado]], columns=features)
        
        st.divider()
        st.subheader("Resultado da Predição:")

        # ---------------------------------------------------------
        # MOTOR DE DIAGNÓSTICO PEDAGÓGICO
        # ---------------------------------------------------------
        predicao = modelo.predict(entrada)[0]

        media_engajamento_psico = (ieg + ipv + ips + iaa) / 4
        descolamento_cognitivo = ida - media_engajamento_psico
       

        if predicao == 'Quartzo':
            st.error(f"🚨 Alerta Crítico: O aluno tem alto risco de rebaixamento para a pedra **{predicao}**.")
            st.markdown("### 🧠 Leitura do Algoritmo (Para o Educador):")
            
            if descolamento_cognitivo >= 2.0:
                st.write("""
                **Sinal de Evasão/Desmotivação:** O modelo detectou um alerta grave. Embora este aluno 
                tenha capacidade cognitiva (notas razoáveis/altas), o seu engajamento e indicadores 
                psicossociais estão desproporcionalmente baixos. Historicamente, alunos com este perfil 
                apresentam alto risco de abandono (evasão) ou regressão severa por falta de suporte emocional 
                ou falta de conexão com o propósito do projeto. **Ação recomendada: Foco no acolhimento e escuta ativa.**
                """)
            else:
                st.write("""
                **Defasagem Generalizada:** O aluno apresenta indicadores baixos tanto na frente acadêmica 
                quanto no engajamento. A inércia atual aponta para uma estagnação crítica. 
                **Ação recomendada: Necessidade de intervenção pedagógica de base e resgate de motivação.**
                """)
                
        elif predicao == 'Agata':
            st.warning(f"⚠️ Atenção: O aluno está projetado para a pedra **{predicao}**.")
            st.markdown("### 🧠 Leitura do Algoritmo (Para o Educador):")
            st.write("""
            **Perfil Mediano/Estagnado:** O modelo projeta este aluno na faixa de estabilidade inferior. 
            Isso geralmente ocorre quando os indicadores se mantêm em uma média morna (em torno de 5 ou 6), 
            sem picos de engajamento (IEG) ou de virada (IPV). O aluno está acompanhando, mas não está acelerando.
            **Ação recomendada: Criar pequenos desafios extracurriculares para tentar engatilhar um 'Ponto de Virada'.**
            """)
            
        elif predicao == 'Ametista':
            st.info(f"✅ Bom desempenho: O aluno está projetado para a pedra **{predicao}**.")
            st.markdown("### 🧠 Leitura do Algoritmo (Para o Educador):")
            st.write("""
            **Trilha de Desenvolvimento Saudável:** O algoritmo reconhece uma harmonia entre a absorção 
            de conteúdo (IDA) e a participação ativa do aluno. Os indicadores apontam para um estudante 
            engajado e com a base sólida, caminhando com segurança pelo programa.
            **Ação recomendada: Manter o acompanhamento atual e incentivar o protagonismo em sala.**
            """)
            
        elif predicao == 'Topazio':
            st.success(f"🏆 Excelência: O aluno está projetado para a pedra **{predicao}**.")
            st.markdown("### 🧠 Leitura do Algoritmo (Para o Educador):")
            st.write("""
            **Perfil de Alta Performance:** O modelo identificou os traços clássicos de excelência. 
            O alto nível de engajamento aliado ao desempenho acadêmico cria uma projeção de topo. 
            Este aluno já compreendeu o propósito da Associação e está voando.
            **Ação recomendada: Inserir o estudante em programas de mentoria, liderança ou desafios avançados para evitar o tédio acadêmico.**
            """)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.warning("**WARNING:** O modelo de dados foi treinado através de uma base histórica e os resultados apresentados precisam ser analisados com cautela pelo educador, visto que o modelo não tem acesso a todos os questionários de avaliação qualitativa dos alunos.", icon="⚠️")
		
		# ---------------------------------------------------------
        # NOVA LÓGICA: EXIBIR OS DADOS ENVIADOS AO MODELO
        # ---------------------------------------------------------
        with st.expander("🔍 Visualizar dados enviados ao modelo (Payload)"):
            st.write("Estes são os valores exatos que o algoritmo está usando para calcular a previsão:")
            # Exibe o DataFrame formatado na tela
            st.dataframe(entrada, use_container_width=True)
            

 # ==========================================
# PÁGINA 2: DASHBOARDS
# ==========================================
elif menu == "Dashboards Dados 2022 - 2024":
    st.title("Histórico de Análises 📈")
    st.write("Abaixo estão as visualizações gráficas das análises e métricas do modelo treinado.")
    
    # Criamos uma lista de dicionários vinculando a imagem ao seu texto explicativo
    dashboards = [
        {
 "arquivo": "analise_por_pedra.png",
            "titulo": "Análise Distribuição das Médias dos Indicadores por Classificação (Pedra)",
            "explicacao": "Esta análise mostra onde os educadores devem concentrar esforços. Alunos da pedra Quartzo já possuem algum engajamento (IEG: 5.61), mas sofrem com uma defasagem crítica na aprendizagem (IDA: 3.46). À medida que o aluno evolui para Ametista e Topázio, a lacuna entre o desempenho acadêmico e o engajamento diminui. O indicador psicossocial (IPS) mantém-se estável em todos os níveis, indicando que o foco de resgate para alunos em risco deve ser primariamente acadêmico."        },
        {
            "arquivo": "evolucao_qtd_pedras.png",
            "titulo": "Evolução Quantidade de Alunos por Pedra",
            "explicacao": "Escreva aqui a análise do Gráfico 2. Destaque os principais padrões de engajamento ou notas que você deseja que a equipe pedagógica perceba."
        },
        {
            "arquivo": "ingressantes_idade.png",
            "titulo": "",
            "explicacao": "Este gráfico demonstra o desempenho atual do algoritmo de Machine Learning. Destaca-se o salto no Recall (Sensibilidade) para a pedra Quartzo, atingindo 40% graças ao balanceamento (SMOTE), permitindo uma identificação precoce e mais apurada de alunos com alto risco de evasão."
        }
    ]
    
    # Laço de repetição atualizado para renderizar o título, a imagem e a caixa de texto
    for dash in dashboards:
        st.subheader(dash["titulo"])
        
        if os.path.exists(dash["arquivo"]):
            st.image(dash["arquivo"], use_container_width=True)
            # A caixa explicativa logo abaixo da imagem
            st.info(f"**Análise dos Dados:** {dash['explicacao']}")
        else:
            st.warning(f"A imagem '{dash['arquivo']}' não foi encontrada no diretório. Por favor, faça o upload no GitHub.")
            
        st.divider() # Cria a linha separadora entre os gráficos
               
# ==========================================
# PÁGINA 2: DASHBOARDS
# ==========================================
elif menu == "Dashboards Dados 2022 - 2024":
    st.title("Histórico de Análises 📈")
    st.write("Abaixo estão as visualizações gráficas das análises e métricas do modelo treinado.")
    
    imagens = ["analise_por_pedra.png", "evolucao_qtd_pedras.png", "ingressantes_idade.png"]
    
    for img in imagens:
        if os.path.exists(img):
            st.image(img, use_container_width=True)
            st.divider()
        else:
            st.warning(f"A imagem '{img}' não foi encontrada no diretório. Por favor, faça o upload no GitHub.")

# ==========================================
# PÁGINA 3: DOCUMENTAÇÃO EXECUTIVA
# ==========================================
elif menu == "Documentação Executiva":
    st.title("Documentação Oficial 📄")
    st.write("Acesse abaixo o documento técnico detalhando a modelagem preditiva e as regras de negócio.")
    
    caminho_pdf = "Documentação.pdf"
    
    if os.path.exists(caminho_pdf):
        # Botão para quem preferir baixar o arquivo
        with open(caminho_pdf, "rb") as pdf_file:
            st.download_button(
                label="⬇️ Baixar Documentação em PDF",
                data=pdf_file,
                file_name="Documentação.pdf",
                mime="application/pdf",
                type="primary"
            )
        
        st.divider()
        st.markdown("### Visualização do Documento")
        
        # Renderiza o PDF para leitura na própria tela do aplicativo
        with open(caminho_pdf, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.error("O arquivo 'Documentação.pdf' não foi encontrado no repositório. Por favor, verifique o nome exato e faça o upload no GitHub.")