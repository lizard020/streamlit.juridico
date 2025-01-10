O app se trata de um app feito no framework Streamlit para visualização de uma base de dados de um deparatamento jurídico.
A arquitetura dos scripts utilizados se dá desta forma:
📂 paginas/
 ┣ 📂 __pycache__/
 ┣ 📄 pag1.py
 ┣ 📄 pag2.py
 ┗ 📄 pag3.py
📄 login.py
📄 readcsv.py
📄 stdash.py
Nesta lista, a página inicial de abertura é a pagina login.py, que tem a estrutura da pagina de login e se conecta com as credenciais armazenadas no secrets do Stremlit.
Validada a entrada do usuário, é aberto o stdash.py, que contém a estrutura geral do dashboard. Antes de qualquer coisa, ao ser acionado, este scripts importa o módulo readcsv.py, que utiliza chaves AWS, também armazenadas no secrets, para fazer uma consulta a um bucket no sistema AWS S3, onde está armazenada a base de dados CSV.
Por fim, uma vez carregada a base de dados, o script impor os módulos de cada do diretório "paginas", no qual cada módulo corresponde a uma aba do dashboard. Dentro destes módulos estão as funções e variáveis que transformam os dados em gráficos e tabelas para, por fim, serem disponibilzados na estrutura Streamlit do arquivo stdash.py
