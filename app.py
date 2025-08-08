import streamlit as st
from streamlit_option_menu import option_menu
from menu_extrair import exibir_menu_extrair
from menu_combinar import exibir_menu_combinar
from menu_marca_dagua import exibir_menu_marca_dagua
from menu_imagens import exibir_menu_imagens
from menu_relatorio import exibir_menu_relatorio

st.set_page_config(
    page_title="Powerful PDF",
    page_icon=":blue_book:",
    layout="wide"
    )

_, col2, _ = st.columns(3)

with col2:
  st.title("Powerful PDF")
  st.markdown("""

              ### Escolha a opção desejada abaixo:


              """)

entradas_menu = {
  'Extrair página':'file-earmark-pdf-fill',
  'Combine PDFs':'plus-square-fill',
  "Adicione marca d'água":'droplet-fill',
  'Imagem para PDF':'file-earmark-richtext-fill',
  'Excel para PDF':'file-earmark-spreadsheet-fill',
}


escolha = option_menu(
    menu_title=None,
    orientation='horizontal',
    options=list(entradas_menu.keys()),
    icons=list(entradas_menu.values()),
    default_index=0,
)

_, col2, _ = st.columns(3)
with col2:
  match escolha:
    case 'Extrair página':
      exibir_menu_extrair(coluna=col2)
      
    case 'Combine PDFs':
      exibir_menu_combinar(coluna=col2)

    case "Adicione marca d'água":
      exibir_menu_marca_dagua(coluna=col2)

    case 'Imagem para PDF':
      exibir_menu_imagens(coluna=col2)
  
    case 'Excel para PDF':
      exibir_menu_relatorio(coluna=col2)
    
