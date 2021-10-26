

## ESTE REPO CONTÉM UMA VERSÃO MOCK DE UMA PÁGINA WEB QUE ACESSA BANCOS DE DADOS



## Instalação:  

	### Dependências

	-- Necessário ter o docker instalado e configurado, veja: https://docs.docker.com


## Configuração:  

	-- Para configurar a página, edite o arquivo <strong>app.py<\strong>, nele está contido o código backend  
	-- No arquivo <strong>Dockerfile</strong> voce pode mudar o diretório do arquivo .py e também o nome.  
		Preste atenção ao comando COPY pois é nele que podemos colocar outros arquivos (como html por exemplo)  
	-- Em tese o arquivo docker-compose.yml não deve ser alterado  
	-- Normalmente você deve conseguir abrir o site em: http://localhost:5000/ ou http://127.0.0.1:5000/  

## instalação automática:

	-- Para instalar de forma automática, execute o script buildAndRun.sh
