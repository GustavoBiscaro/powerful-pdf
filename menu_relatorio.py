import streamlit as st
import tempfile
import pypdf

from pathlib import Path
from utilidades import pegar_dados_pdf
from projeto_pdf_excel.gerar_relatorio import CONFIG, main as gerar_relatorio_pdf

def exibir_menu_relatorio(coluna):
  with coluna:
    st.markdown("""
    ## Gerar relatório PDF

    Selecione um arquivo em Excel para gerar um relatório:


                """)

    arquivo_excel = st.file_uploader(
      label='Selecione o arquivo Excel...',
      type='xlsx',
      accept_multiple_files=False,
      )

    if arquivo_excel:
      botoes_desativados = False
    else:
      botoes_desativados = True
      
    col1, col2 = st.columns(2)
    with col1:
      seletor_ano = st.selectbox("Ano", range(2020, 2025), disabled=botoes_desativados)
    with col2:
      seletor_mes = st.selectbox("Mês", range(1, 13), disabled=botoes_desativados)

    clicou_processar = st.button('Clique para processar o arquivo em Excel...',
                                use_container_width=True)
    if clicou_processar:
      dados_pdf = pegar_dados_do_relatorio_em_pdf(arquivo_excel, seletor_ano, seletor_mes)
      if dados_pdf is None:
        st.warning(f'Excel não possuí dados para ano {seletor_ano} e mês {seletor_mes}')
        return
      nome_arquivo = f'relatorio.pdf'
   
      st.download_button(
        'Clique para fazer download do arquivo PDF...',
        type='primary',
        data=dados_pdf,
        file_name=nome_arquivo,
        mime='application/pdf',
        use_container_width=True
        )

def pegar_dados_do_relatorio_em_pdf(arquivo_excel, seletor_ano, seletor_mes):
  # Configurar o mês de referência para o relatório
  mes_referencia = f'{seletor_ano} - {seletor_mes:02d}'
  CONFIG['mes_referencia'] = mes_referencia

  # Configurar caminho temporário para os dados do excel
  with tempfile.TemporaryDirectory() as pasta_temp:
    caminho_temp = Path(pasta_temp)
    CONFIG['pasta_dados'] = caminho_temp
    CONFIG['pasta_output'] = caminho_temp

    # Inserindo dados nas pastas temporárias
    with open(caminho_temp / 'dados.xlsx', 'wb') as arq_excel_temp:
      dados_excel = arquivo_excel.getvalue()
      arq_excel_temp.write(dados_excel)

      # Rodando função do relatório
      try:
          gerar_relatorio_pdf(**CONFIG)
      except ValueError:
        return None

    # Ler dados do relatório
    nome_output = caminho_temp / f'Relatório Mensal - {mes_referencia}.pdf'
    with open(nome_output, 'rb') as relatorio_pdf:
        dados_pdf = relatorio_pdf.read()
    return dados_pdf
    

    