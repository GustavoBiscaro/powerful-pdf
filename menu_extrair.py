import streamlit as st
import pypdf

from pathlib import Path
from utilidades import pegar_dados_pdf

def exibir_menu_extrair(coluna):
  with coluna:
    st.markdown("""
    ## Extrair Página de um PDF

    Escolha um arquivo em PDF para extrair uma página.


                """)

    arquivo_pdf = st.file_uploader(
      label='Selecione o arquivo PDF...',
      type='pdf',
      accept_multiple_files=False,
      )

    if arquivo_pdf:
      botoes_desativados = False
    else:
      botoes_desativados = True

    numero_pagina = st.number_input('Página para extrair', min_value=1, disabled=botoes_desativados)
    clicou_processar = st.button('Clique para processar o arquivo PDF...',
                                use_container_width=True)
    if clicou_processar:
      dados_pdf = extrair_pagina_pdf(arquivo_pdf=arquivo_pdf, numero_pagina=numero_pagina)
      if dados_pdf is None:
        st.warning(f'PDF não possuí página de número {numero_pagina}!')
        return
      nome_arquivo = f'{Path(arquivo_pdf.name).stem}_pg{numero_pagina:03d}.pdf'
   
      st.download_button(
        'Clique para fazer download do arquivo PDF...',
        type='primary',
        data=dados_pdf,
        file_name=nome_arquivo,
        mime='application/pdf',
        use_container_width=True
        )

def extrair_pagina_pdf(arquivo_pdf, numero_pagina):
    leitor = pypdf.PdfReader(arquivo_pdf)
    try:
       pagina = leitor.pages[numero_pagina - 1]
    except IndexError:
        return None
    escritor = pypdf.PdfWriter()
    escritor.add_page(pagina)
    dados_pdf = pegar_dados_pdf(escritor=escritor)
    return dados_pdf


    