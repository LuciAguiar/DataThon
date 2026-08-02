import streamlit as st
import pandas as pd
import joblib
import base64
import os

# Configuração da página
st.set_page_config(page_title="Passos Mágicos - Radar Pedagógico", page_icon="🔮", layout="wide")

# Carregar o modelo em cache para otimizar a performance
@st.cache_resource
def load_model():
    return joblib.load('modelo_passos_magicos.pkl')

modelo = load_model()

# ==========================================
# MENU LATERAL (SIDEBAR)
# ==========================================
st.sidebar.title("Navegação 🧭")
menu = st.sidebar.radio(
    "Selecione a página:", 
    ["Aplicativo Predição", "Histórico", "Documentação"]
)
st.sidebar.divider()
st.sidebar.info("Utilize este menu para navegar entre o simulador preditivo, as análises históricas e a documentação oficial.")

# ==========================================
# PÁGINA 1: APLICATIVO PREDIÇÃO
# ==========================================
if menu == "Aplicativo Predição":
    st.title("Radar de Prevenção e Intervenção - Passos Mágicos 🔮")
    
    st.markdown("""
    Esta ferramenta permite simular o impacto dos indicadores acadêmicos e psicossociais 
    na classificação final do aluno (Pedra). Ajuste os valores abaixo para realizar uma **Análise What-If**.
    """)
    
    # ---------------------------------------------------------
    # NOVA TABELA DE REFERÊNCIA VISUAL (COM IMAGENS JPG)
    # ---------------------------------------------------------
    st.markdown("### 📊 Tabela de Referência (INDE)")
    
    # Criamos 4 colunas proporcionais na tela para exibir as pedras lado a lado
    col_q, col_ag, col_am, col_t = st.columns(4)
    
    with col_q:
        # Verifica se a imagem existe antes de tentar exibi-la para evitar erros na tela
        if os.path.exists("Quartzo.jpg"):
            st.image("Quartzo.jpg", use_column_width=True)
        else:
            st.caption("*(Imagem quartzo.jpg pendente)*")
        st.markdown("##### Quartzo")
        st.caption("INDE: 2,405 a 5,506")
        
    with col_ag:
        if os.path.exists("Agata.jpg"):
            st.image("Agata.jpg", use_column_width=True)
        else:
            st.caption("*(Imagem agata.jpg pendente)*")
        st.markdown("##### Ágata")
        st.caption("INDE: 5,506 a 6,868")
        
    with col_am:
        if os.path.exists("Ametista.jpg"):
            st.image("Ametista.jpg", use_column_width=True)
        else:
            st.caption("*(Imagem ametista.jpg pendente)*")
        st.markdown("##### Ametista")
        st.caption("INDE: 6,868 a 8,230")
        
    with col_t:
        if os.path.exists("Topazio.jpg"):
            st.image("Topazio.jpg", use_column_width=True)
        else:
            st.caption("*(Imagem topazio.jpg pendente)*")
        st.markdown("##### Topázio")
        st.caption("INDE: 8,230 a 9,294")

    st.divider()

    # ---------------------------------------------------------
    # ENTRADA DE DADOS (SLIDERS)
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
        ian = st.slider("IAN - Adequação de Nível", 0.0, 10.0, 5.0, 0.1)

    with col2:
        st.subheader("Indicadores Psicossociais")
        ipv = st.slider("IPV - Ponto de Virada", 0.0, 10.0, 5.0, 0.1)
        ips = st.slider("IPS - Indicador Psicossocial", 0.0, 10.0, 5.0, 0.1)
        iaa = st.slider("IAA - Autoavaliação", 0.0, 10.0, 5.0, 0.1)

    st.divider()

    # Cálculo automático do INDE Recalculado
    pesos = {'IAN': 0.1111, 'IDA': 0.2222, 'IEG': 0.2222, 'IAA': 0.1111, 'IPS': 0.1111, 'IPV': 0.2222}
    inde_simulado = (ian*pesos['IAN'] + ida*pesos['IDA'] + ieg*pesos['IEG'] + 
                     iaa*pesos['IAA'] + ips*pesos['IPS'] + ipv*pesos['IPV'])

    st.write(f"**INDE Atual Simulado:** {inde_simulado:.2f}")

    # Botão de Predição
    if st.button("Simular Classificação (Pedra) no Próximo Ano", type="primary"):
        features = ['IAN', 'IDA', 'IEG', 'IAA', 'IPS', 'IPV', 'INDE_RECALCULADO']
        entrada = pd.DataFrame([[ian, ida, ieg, iaa, ips, ipv, inde_simulado]], columns=features)
        
        predicao = modelo.predict(entrada)[0]
        
        st.subheader("Resultado da Predição:")
        if predicao == 'Quartzo':
            st.error(f"🚨 Alerta Crítico: O aluno tem alto risco de rebaixamento para a pedra **{predicao}**.")
        elif predicao == 'Agata':
            st.warning(f"⚠️ Atenção: O aluno está projetado para a pedra **{predicao}**.")
        elif predicao == 'Ametista':
            st.info(f"✅ Bom desempenho: O aluno está projetado para a pedra **{predicao}**.")
        elif predicao == 'Topazio':
            st.success(f"🏆 Excelência: O aluno está projetado para a pedra **{predicao}**.")

# ==========================================
# PÁGINA 2: HISTÓRICO (IMAGENS)
# ==========================================
elif menu == "Histórico":
    st.title("Histórico de Análises 📈")
    st.write("Abaixo estão as visualizações gráficas das análises e métricas do modelo treinado.")
    
    # Lista com o nome dos arquivos das imagens
    imagens = ["grafico1.jpg", "grafico2.jpg", "metricas_modelo.png"]
    
    for img in imagens:
        if os.path.exists(img):
            st.image(img, use_column_width=True)
            st.divider()
        else:
            st.warning(f"A imagem '{img}' não foi encontrada no diretório. Por favor, faça o upload no GitHub.")

# ==========================================
# PÁGINA 3: DOCUMENTAÇÃO (PDF)
# ==========================================
elif menu == "Documentação":
    st.title("Documentação Oficial 📄")
    st.write("Acesse abaixo o documento técnico detalhando a modelagem preditiva e as regras de negócio.")
    
    caminho_pdf = "Documentacao.pdf"
    
    if os.path.exists(caminho_pdf):
        with open(caminho_pdf, "rb") as pdf_file:
            st.download_button(
                label="⬇️ Baixar Documentação em PDF",
                data=pdf_file,
                file_name="Documentacao.pdf",
                mime="application/pdf"
            )
        
        st.markdown("### Visualização do Documento")
        with open(caminho_pdf, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.error("O arquivo 'Documentacao.pdf' não foi encontrado no repositório. Por favor, verifique o nome exato e faça o upload no GitHub.")