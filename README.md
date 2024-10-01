# Status das Linhas de Transporte

Este projeto é uma skill para a Alexa que permite aos usuários consultar o status das linhas de transporte da Viamobilidade. A skill utiliza web scraping para coletar informações atualizadas sobre o estado das linhas de transporte, como "Operação Normal", "Operação Parcial" ou "Operação Interrompida".

## Funcionalidades

- **Verificar Status**: Usuários podem perguntar sobre o status das linhas de transporte e receber respostas detalhadas, incluindo razões para o status atual.
- **Ajuda**: Fornece informações sobre como usar a skill.
- **Tratamento de Erros**: Responde de forma adequada em caso de erros ou falhas na solicitação.

## Tecnologias Utilizadas

- Python
- BeautifulSoup: Para web scraping das informações do site da Viamobilidade.
- AWS Lambda: Para implementar a skill.
- ask-sdk-core: Para construir a skill da Alexa.

## Pré-requisitos

Antes de executar o projeto, você precisa ter:

- Python 3.x instalado.
- A biblioteca `requests` e `beautifulsoup4` instaladas. Você pode instalá-las usando o pip:

```bash
pip install requests beautifulsoup4 ask-sdk-core


Como Usar

	1.	Configurar a Skill na AWS:
	•	Crie uma nova skill na Alexa Developer Console.
	•	Configure a interação, definindo as intents necessárias (como CheckStatusIntent).
	•	Faça o upload do código como uma função Lambda.
	2.	Testar a Skill:
	•	Use o simulador da Alexa Developer Console ou um dispositivo habilitado para Alexa.
	•	Diga “Alexa, perguntar o status das linhas de transporte” para obter o status atual.

Estrutura do Código

Funções Principais

	•	get_status(): Coleta e processa informações do site da Viamobilidade para extrair o status das linhas.
	•	CheckStatusIntentHandler: Trata a intenção CheckStatusIntent e fornece a resposta ao usuário.
	•	HelpIntentHandler: Fornece ajuda sobre como usar a skill.
	•	CancelAndStopIntentHandler: Trata intenções de cancelamento e parada.
	•	ErrorHandler: Gerencia erros e fornece feedback ao usuário.

Exemplo de Resposta

Quando um usuário pergunta sobre o status, a skill retorna uma resposta como:


"A linha X está com status de Operação Normal. A última atualização foi em 01/10/2024 12:00:00."

Contribuição

Contribuições são bem-vindas! Se você deseja melhorar este projeto, sinta-se à vontade para abrir um pull request ou criar um issue.

Licença

Este projeto está licenciado sob a MIT License.

Sinta-se à vontade para personalizar o conteúdo conforme necessário!