import streamlit as st
import pandas as pd
import joblib
import base64
import os
    
# Configuração da página
st.set_page_config(page_title="Passos Mágicos - Radar Pedagógico", page_icon="🔮", layout="Medium")

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
    na classificação final do aluno (Pedra). Ajuste os valores abaixo para realizar uma **Análise Preditiva**.
    """)
    
    # Tabela de Referência Visual (Com Imagens JPG)
    st.markdown("### 📊 Tabela de Referência (INDE)")
    
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
        
        ida = (nota_mat + nota_por + nota_ing) / 3
        st.info(f"**IDA Calculado (Média):** {ida:.2f}")
        
        st.markdown("**Outros Indicadores Acadêmicos**")
        ieg = st.slider("IEG - Indicador de Engajamento", 0.0, 10.0, 5.0, 0.1)
        
        ian_opcao = st.radio(
            "IAN - Adequação de Nível",
            options=["Em Fase", "Moderada", "Severa"],
            index=1,
            horizontal=True
        )
        
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

    # Cálculo automático do INDE Oficial
    pesos = {'IAN': 0.1, 'IDA': 0.2, 'IEG': 0.2, 'IAA': 0.1, 'IPS': 0.1, 'IPV': 0.2, 'IPP': 0.1}
    inde_simulado = (ian*pesos['IAN'] + ida*pesos['IDA'] + ieg*pesos['IEG'] + 
                     iaa*pesos['IAA'] + ips*pesos['IPS'] + ipv*pesos['IPV'] + ipp*pesos['IPP'])

    st.write(f"**INDE Atual Simulado:** {inde_simulado:.2f}")

    if st.button("Simular Classificação (Pedra) no Próximo Ano", type="primary"):
        features = ['IAN', 'IDA', 'IEG', 'IAA', 'IPS', 'IPV', 'IPP', 'INDE_ATUAL']
        entrada = pd.DataFrame([[ian, ida, ieg, iaa, ips, ipv, ipp, inde_simulado]], columns=features)
        
        st.divider()
        st.subheader("Resultado da Predição:")

        # ---------------------------------------------------------
        # PREDIÇÃO E LEITURA DO ALGORITMO
        # ---------------------------------------------------------
        predicao = modelo.predict(entrada)[0]

        media_engajamento_psico = (ieg + ipv + ips + iaa) / 4
       
        if predicao == 'Quartzo':
            st.error(f"🚨 Alerta Crítico: O aluno tem alto risco de rebaixamento para a pedra **{predicao}**.")
            st.markdown("### 🧠 Leitura do Algoritmo (Para o Educador):")
            
            # Cenário 1: Voo de Galinha (Muito esforço, sem resultado)
            if ieg >= 7.0 and ida < 6.0:
                st.write("""
                **Esforço Não Convertido:** O modelo detectou um alerta grave. O aluno apresenta um alto engajamento (IEG), mas uma severa deficiência acadêmica (IDA). A inércia atual aponta para frustração iminente: ele se esforça, mas não vê os resultados nas notas.
                **Ação recomendada: Intervenção urgente na metodologia de estudo, técnicas de retenção e aulas de nivelamento.**
                """)
            # Cenário 2: Inteligente, mas desconectado
            elif ida >= 7.0 and media_engajamento_psico < 6.0:
                st.write("""
                **Sinal de Evasão/Desmotivação:** O aluno tem capacidade cognitiva (notas boas), mas o seu engajamento e indicadores psicossociais estão desproporcionalmente baixos. Alunos com este perfil apresentam risco de abandono por falta de conexão com o propósito. 
                **Ação recomendada: Foco no acolhimento emocional e escuta ativa.**
                """)
            # Cenário 3: Defasagem real (Tudo baixo)
            else:
                st.write("""
                **Defasagem Generalizada:** O aluno apresenta indicadores críticos tanto na frente acadêmica quanto no engajamento. A inércia atual aponta para uma estagnação severa na base.
                **Ação recomendada: Necessidade de intervenção pedagógica de base e resgate total de motivação.**
                """)
                
        elif predicao == 'Agata':
            st.warning(f"⚠️ Atenção: O aluno está projetado para a pedra **{predicao}**.")
            st.markdown("### 🧠 Leitura do Algoritmo (Para o Educador):")
            
            # Cenário de Risco Oculto (Engajamento mascarando nota ruim)
            if ieg >= 8.0 and ida < 6.0:
                 st.write("""
                 **Alerta de Mascaramento (Risco Oculto):** A classificação 'Ágata' está sendo sustentada quase que exclusivamente pelo alto engajamento (IEG), mascarando uma base acadêmica frágil. Sem notas que sustentem a evolução, a queda no próximo ciclo é quase certa.
                 **Ação recomendada: Focar imediatamente no reforço das disciplinas base, aproveitando a boa vontade atual do aluno.**
                 """)
            else:
                 st.write("""
                 **Perfil Estável:** O modelo projeta este aluno na faixa de estabilidade inferior. Os indicadores acompanham a média, mas sem picos de aceleração expressivos.
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
            O alto nível de engajamento aliado ao excelente desempenho acadêmico cria uma projeção de topo. 
            Este aluno compreendeu perfeitamente o propósito e está acelerando.
            **Ação recomendada: Inserir o estudante em programas de mentoria, liderança ou desafios avançados para evitar o tédio acadêmico.**
            """)
        
        # ---------------------------------------------------------
        # NOVO: MOTOR DE DIAGNÓSTICO PREVENTIVO (ALERTAS DE QUEDA)
        # ---------------------------------------------------------
        st.divider()
        st.subheader("Radar de Risco e Diagnóstico Pedagógico")

        # 1. Alerta de Ilusão de Desempenho (Descolamento IAA vs IDA)
        if (iaa - ida) >= 2.0:
            st.warning("⚠️ **Ilusão de Desempenho:** O aluno avalia o próprio desempenho muito acima da realidade acadêmica. Este é um forte preditor de frustração e rebaixamento de nível no próximo ano.")

        # 2. Alerta de Esforço Não Convertido (Descolamento IEG vs IDA)
        if (ieg - ida) >= 2.5:
            st.warning("⚠️ **Esforço Não Convertido:** O engajamento está alto, mas não se reflete nas notas. É necessário intervir na metodologia de estudo antes que ocorra esgotamento e desmotivação.")

        # 3. Alerta de Limiar Acadêmico Invisível (para alunos que não foram preditos como Quartzo)
        if ida < 6.0 and predicao in ["Agata", "Ametista", "Topazio"]:
            st.warning("⚠️ **Base Acadêmica Frágil:** A classificação geral está protegida pelo engajamento, mas a nota acadêmica (IDA) já se encontra em zona de risco crítico para o próximo ciclo.")
            
        # Caso nenhum alerta seja disparado
        if (iaa - ida) < 2.0 and (ieg - ida) < 2.5 and (ida >= 6.0 or predicao == "Quartzo"):
             st.success("✅ **Nenhum alerta preditivo adicional detectado.** O aluno apresenta indicadores proporcionais e consistentes com a sua base.")

        st.divider()
        # Alerta Customizado em HTML/CSS
        st.markdown("""
        <div style="background-color: #f0f2f6; 
                    padding: 15px; 
                    border-radius: 8px; 
                    border-left: 6px solid #4f8bf9; 
                    color: #31333F;
                    margin-bottom: 20px;">
            <span style="font-size: 1.1em;">⚠️</span> 
            <strong>AVISO IMPORTANTE:</strong> O modelo de dados foi treinado através de uma base 
            histórica e os resultados apresentados precisam ser analisados com cautela pelo educador, 
            visto que o modelo não tem acesso a todos os questionários de avaliação qualitativa dos alunos.
        </div>
        """, unsafe_allow_html=True)
        with st.expander("🔍 Visualizar dados enviados ao modelo (Payload)"):
            st.write("Estes são os valores exatos que o algoritmo está usando para calcular a previsão:")
            st.dataframe(entrada, use_container_width=True)
            

# ==========================================
# PÁGINA 2: DASHBOARDS
# ==========================================
elif menu == "Dashboards Dados 2022 - 2024":
    st.title("Histórico de Análises 📈")
    st.write("Abaixo estão as visualizações gráficas das análises e métricas do modelo treinado.")
    
    dashboards = [
       {
            "arquivo": "analise_por_pedra.png",
            "titulo": "Convergência de Indicadores (IDA vs. IEG)",
            "explicacao": "O engajamento (IEG) funciona como o motor de arranque, mas não sustenta a alta performance sozinho. Na fase Quartzo, o IEG (5.61) é mais de 60% superior ao desempenho acadêmico (IDA: 3.46). Conforme o aluno avança, essa lacuna se fecha rapidamente, chegando a uma diferença de apenas 14% no Topázio. O insight é claro: para tirar o aluno do Quartzo, foca-se na base acadêmica; para transformar um Ametista em Topázio, o desafio é nivelar a cognição ao alto engajamento que ele já possui."
        },       
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
    
    for dash in dashboards:
        st.subheader(dash["titulo"])
        
        if os.path.exists(dash["arquivo"]):
            st.image(dash["arquivo"], use_container_width=True)
            st.info(f"**Análise dos Dados:** {dash['explicacao']}")
        else:
            st.warning(f"A imagem '{dash['arquivo']}' não foi encontrada no diretório. Por favor, faça o upload no GitHub.")
            
        st.divider()

# ==========================================
# PÁGINA 3: DOCUMENTAÇÃO EXECUTIVA
# ==========================================
elif menu == "Documentação Executiva":
    st.title("Documentação Oficial 📄")
    st.write("Acesse abaixo o documento técnico detalhando a modelagem preditiva e as regras de negócio.")
    
    caminho_pdf = "Documentação.pdf"
    
    if os.path.exists(caminho_pdf):
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
        
        with open(caminho_pdf, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.error("O arquivo 'Documentação.pdf' não foi encontrado no repositório. Por favor, verifique o nome exato e faça o upload no GitHub.")