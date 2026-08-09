import streamlit as st
import pandas as pd
import joblib
import base64
import os
    
# Configuração da página
st.set_page_config(page_title="Passos Mágicos - Radar Pedagógico", layout="wide")

# ---------------------------------------------------------
# INJEÇÃO DE CSS CUSTOMIZADO (DESIGN PROFISSIONAL)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Estilizar o botão principal de simulação */
    div.stButton > button:first-child {
        background-color: #1e3a8a; /* Azul escuro corporativo */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #3b6bce; /* Azul mais claro no hover */
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    /* Suavizar as linhas divisórias (st.divider) */
    hr {
        margin-top: 1.5em;
        margin-bottom: 1.5em;
        border: 0;
        border-top: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# Carregar o NOVO modelo em cache
@st.cache_resource
def load_model():
    return joblib.load('modelo_passos_magicos_2023.pkl')

modelo = load_model()

# ==========================================
# MENU LATERAL (SIDEBAR)
# ==========================================
if os.path.exists("Passos-magicos.png"):
    st.sidebar.image("Passos-magicos.png", use_container_width=True)

st.sidebar.title("Navegação")

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
    
 # ---------------------------------------------------------
    # CABEÇALHO INSTITUCIONAL COM IMAGEM DE FUNDO
    # ---------------------------------------------------------
    def get_image_base64(caminho_imagem):
        if os.path.exists(caminho_imagem):
            with open(caminho_imagem, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        return ""

    fundo_b64 = get_image_base64("Imagem-Fundo.png")
    
    estilo_fundo = f"background-image: url('data:image/png;base64,{fundo_b64}'); background-size: cover; background-position: center;" if fundo_b64 else "background-color: #0f172a;"

    st.markdown(f"""
    <div style="text-align: center; 
                padding: 45px 25px; 
                {estilo_fundo} 
                border-radius: 10px; 
                margin-bottom: 30px; 
                border-bottom: 4px solid #38bdf8; 
                box-shadow: 0px 4px 15px rgba(0,0,0,0.3);">
        <h1 style="color: #ffffff; 
                   text-shadow: 3px 3px 6px rgba(0,0,0,1), 0px 0px 20px rgba(0,0,0,0.8); 
                   margin-bottom: 5px; 
                   font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
            Radar de Prevenção e Intervenção
        </h1>
        <h4 style="color: #ffffff; 
                   text-shadow: 2px 2px 4px rgba(0,0,0,1), 0px 0px 15px rgba(0,0,0,1); 
                   font-weight: 500; 
                   letter-spacing: 0.5px;
                   margin-top: 0px;">
            Motor de Diagnóstico Pedagógico - Associação Passos Mágicos
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Esta ferramenta permite simular o impacto dos indicadores acadêmicos e psicossociais 
    na classificação final do aluno, determinada pela Pedra. Ajuste os valores abaixo para realizar uma **Análise Preditiva**.
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
    # ENTRADA DE DADOS
    # ---------------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        # Título principal da coluna (Tamanho 4)
        st.markdown("#### 📚 Frente Acadêmica")
        
        # Subtítulo (Tamanho 5)
        st.markdown("##### 📝 Composição de Notas (IDA)")
        nota_mat = st.slider("Matemática", 0.0, 10.0, 5.0, 0.1)
        nota_por = st.slider("Português", 0.0, 10.0, 5.0, 0.1)
        nota_ing = st.slider("Inglês", 0.0, 10.0, 5.0, 0.1)
        
        ida = (nota_mat + nota_por + nota_ing) / 3
        st.metric(label="📊 IDA Calculado (Média das Notas)", value=f"{ida:.2f}")
        
        # Subtítulo (Tamanho 5) padronizado
        st.markdown("#### 🎯 Participação e Nivelamento")
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
        # Título principal da coluna (Tamanho 4)
        st.markdown("#### 🧠 Frente Psicossocial")
        
        # Subtítulo (Tamanho 5) padronizado
        st.markdown("##### 🧭 Indicadores Comportamentais")
        ipp = st.slider("IPP - Indicador Psicopedagógico", 0.0, 10.0, 5.0, 0.1)
        ipv = st.slider("IPV - Ponto de Virada", 0.0, 10.0, 5.0, 0.1)
        ips = st.slider("IPS - Indicador Psicossocial", 0.0, 10.0, 5.0, 0.1)
        iaa = st.slider("IAA - Autoavaliação", 0.0, 10.0, 5.0, 0.1)

    st.divider()
    # Cálculo automático do INDE Oficial
    pesos = {'IAN': 0.1, 'IDA': 0.2, 'IEG': 0.2, 'IAA': 0.1, 'IPS': 0.1, 'IPV': 0.2, 'IPP': 0.1}
    inde_simulado = (ian*pesos['IAN'] + ida*pesos['IDA'] + ieg*pesos['IEG'] + 
                     iaa*pesos['IAA'] + ips*pesos['IPS'] + ipv*pesos['IPV'] + ipp*pesos['IPP'])

    st.metric(
        label="🎯 INDE Atual Simulado (Projeção Matemática)", 
        value=f"{inde_simulado:.2f}",
        help="Este índice é calculado dinamicamente com base nos pesos oficiais da associação."
    )
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Simular Classificação (Pedra) no Próximo Ano", type="primary"):
        features = ['IAN', 'IDA', 'IEG', 'IAA', 'IPS', 'IPV', 'IPP', 'INDE_ATUAL']
        entrada = pd.DataFrame([[ian, ida, ieg, iaa, ips, ipv, ipp, inde_simulado]], columns=features)
        
        st.divider()
        st.subheader("Resultado da Predição:")

        # ---------------------------------------------------------
        # PREDIÇÃO E LEITURA DO ALGORITMO (ATUALIZADA)
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
        # MOTOR DE DIAGNÓSTICO PREVENTIVO (ALERTAS DE QUEDA)
        # ---------------------------------------------------------
        st.divider()
        st.subheader("Radar de Risco e Diagnóstico Pedagógico")

        # 1. Alerta de Ilusão de Desempenho (Descolamento IAA vs IDA)
        if (iaa - ida) >= 2.0:
            st.warning("⚠️ **Ilusão de Desempenho:** O aluno avalia o próprio desempenho muito acima da realidade acadêmica. Este é um forte preditor de frustração e rebaixamento de nível no próximo ano.")

        # 2. Alerta de Esforço Não Convertido (Descolamento IEG vs IDA)
        if (ieg - ida) >= 2.5:
            st.warning("⚠️ **Esforço Não Convertido:** O engajamento está alto, mas não se reflete nas notas. É necessário intervir na metodologia de estudo antes que ocorra esgotamento e desmotivação.")

        # 3. Alerta de Limiar Acadêmico Invisível
        if ida < 6.0 and predicao in ["Agata", "Ametista", "Topazio"]:
            st.warning("⚠️ **Base Acadêmica Frágil:** A classificação geral está protegida pelo engajamento, mas a nota acadêmica (IDA) já se encontra em zona de risco crítico para o próximo ciclo.")
            
        # Caso nenhum alerta seja disparado
        if (iaa - ida) < 2.0 and (ieg - ida) < 2.5 and (ida >= 6.0 or predicao == "Quartzo"):
             st.success("✅ **Nenhum alerta preditivo adicional detectado.** O aluno apresenta indicadores proporcionais e consistentes com a sua base.")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # ---------------------------------------------------------
        # AVISO CUSTOMIZADO DE TREINAMENTO (HTML/CSS)
        # ---------------------------------------------------------
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
    st.write("Abaixo estão algumas visualizações gráficas das análises e métricas do modelo treinado. A análise completa consta no documento PDF que pode ser acessado através do menu 'Documentação Executiva'")
    
    dashboards = [
       {
            "arquivo": "analise_por_pedra.png",
            "titulo": "Convergência de Indicadores (IDA vs. IEG)",
            "explicacao": "O engajamento (IEG) funciona como o motor de arranque, mas não sustenta a alta performance sozinho. Na fase Quartzo, o IEG (5.61) é mais de 60% superior ao desempenho acadêmico (IDA: 3.46). Conforme o aluno avança, essa lacuna se fecha rapidamente, chegando a uma diferença de apenas 14% no Topázio. O insight é claro: para tirar o aluno do Quartzo, foca-se na base acadêmica; para transformar um Ametista em Topázio, o desafio é nivelar a cognição ao alto engajamento que ele já possui."
        },       
         {
            "arquivo": "ida_por_fase_ano.png",
            "titulo": "Evolução IDA ao Longo dos Anos",
            "explicacao": "O gráfico revela que 2023 funcionou como um ano de forte tração e pico de Desempenho Acadêmico (IDA) para a maioria das turmas. Em 2024, nota-se uma leve retração em fases iniciais e intermediárias (como 2 e 3), refletindo o choque natural com o aumento da complexidade curricular. O grande destaque positivo fica com as **Fases 5 e 6**, que mantiveram crescimento contínuo. A extrema volatilidade da **Fase 7** reforça a necessidade de analisá-la isoladamente para evitar distorções globais."
        },
        {
            "arquivo": "ips_preditivo.png",
            "titulo": "Influência do IPS Atual no IDA/IEG Do Ano Seguinte",
            "explicacao": "Os gráficos evidenciam que a estabilidade emocional e social (IPS) atua como um forte preditor do sucesso acadêmico. Alunos que sofreram quedas significativas tanto em desempenho (IDA) quanto em engajamento (IEG) já apresentavam, no ano anterior, um alicerce psicossocial consideravelmente mais baixo e instável (caixas vermelhas). Em contrapartida, estudantes que mantiveram ou evoluíram em suas métricas sustentavam uma base psicossocial sólida (caixas verdes com medianas altas). O insight gerado é direto: fragilidades psicossociais não tratadas hoje se convertem em defasagem acadêmica no próximo ciclo."
        },
        {
             "arquivo": "evolucao_influencia_ipv_labels.png",
             "titulo": "Influência do IPV Atual nos Indicadores Do Ano Seguinte",
             "explicacao": "O gráfico revela uma mudança estrutural na dinâmica que leva um aluno ao 'Ponto de Virada' (IPV). O destaque absoluto é a disparada da influência do **Indicador Psicopedagógico (IPP)**, cuja correlação saltou drasticamente para 0.75 em 2024, assumindo a liderança como o maior motor de transformação. O Engajamento (IEG) também ganhou tração (0.58), enquanto o peso do Desempenho Acadêmico (IDA) permaneceu estável. O insight para a equipe é claro: o salto definitivo de desenvolvimento do aluno não é mais tracionado isoladamente pelas notas, mas está profundamente dependente do suporte psicopedagógico e de sua dedicação ativa."
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
    st.write("Acesse abaixo o documento com as análises detalhadas dos dados.")
    
    caminho_pdf = "Projeto Passos Magicos.pdf"
    
    if os.path.exists(caminho_pdf):
        with open(caminho_pdf, "rb") as pdf_file:
            st.download_button(
                label="⬇️ Baixar Documentação em PDF",
                data=pdf_file,
                file_name="Projeto Passos Magicos.pdf",
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