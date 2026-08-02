import streamlit as st
import pandas as pd
import joblib

# Configuração da página
st.set_page_config(page_title="Passos Mágicos - Radar Pedagógico", page_icon="🔮", layout="wide")

# Carregar o modelo em cache para otimizar a performance
@st.cache_resource
def load_model():
    return joblib.load('modelo_passos_magicos.pkl')

modelo = load_model()

# Interface Principal
st.title("Radar de Prevenção e Intervenção - Passos Mágicos 🔮")
st.markdown("""
Esta ferramenta permite simular o impacto dos indicadores acadêmicos e psicossociais 
na classificação final do aluno (Pedra). Ajuste os valores abaixo para realizar uma **Análise What-If**.
""")

st.divider()

# Layout em colunas para os sliders
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

# Cálculo automático do INDE Recalculado (a inércia) usando o novo IDA
pesos = {'IAN': 0.1111, 'IDA': 0.2222, 'IEG': 0.2222, 'IAA': 0.1111, 'IPS': 0.1111, 'IPV': 0.2222}
inde_simulado = (ian*pesos['IAN'] + ida*pesos['IDA'] + ieg*pesos['IEG'] + 
                 iaa*pesos['IAA'] + ips*pesos['IPS'] + ipv*pesos['IPV'])

st.write(f"**INDE Atual Simulado:** {inde_simulado:.2f}")

# Botão de Predição
if st.button("Simular Classificação (Pedra) no Próximo Ano", type="primary"):
    
    # Preparar o array de entrada com a mesma ordem das features do modelo
    # Note que a variável 'ida' agora carrega a média calculada automaticamente
    features = ['IAN', 'IDA', 'IEG', 'IAA', 'IPS', 'IPV', 'INDE_RECALCULADO']
    entrada = pd.DataFrame([[ian, ida, ieg, iaa, ips, ipv, inde_simulado]], columns=features)
    
    # Fazer a predição
    predicao = modelo.predict(entrada)[0]
    
    # Exibir resultado com estilização condicional
    st.subheader("Resultado da Predição:")
    
    if predicao == 'Quartzo':
        st.error(f"🚨 Alerta Crítico: O aluno tem alto risco de rebaixamento para a pedra **{predicao}**.")
    elif predicao == 'Agata':
        st.warning(f"⚠️ Atenção: O aluno está projetado para a pedra **{predicao}**.")
    elif predicao == 'Ametista':
        st.info(f"✅ Bom desempenho: O aluno está projetado para a pedra **{predicao}**.")
    elif predicao == 'Topazio':
        st.success(f"🏆 Excelência: O aluno está projetado para a pedra **{predicao}**.")