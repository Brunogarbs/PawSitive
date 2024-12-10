# PawSitive 🐾
Plataforma para Gestão de Imagens de Animais

## Sobre o Projeto
PawSitive é uma aplicação desenvolvida em Flask para facilitar o gerenciamento de imagens de animais, integrando um banco de dados PostgreSQL para armazenar e exibir imagens.

## Funcionalidades
* Upload e exibição de imagens de animais.
* Integração com PostgreSQL para gerenciamento de dados.
* Interface intuitiva e responsiva para interação com usuários.

## Tecnologias Utilizadas
* Linguagem: Python (Flask)
* Banco de Dados: PostgreSQL
* Frontend: HTML/CSS com Jinja2
* Hospedagem: Configuração local (ou especifique o serviço usado, como AWS, Heroku etc.)

## Estrutura do Projeto

```
PawSitive/  
│  
├── app.py             # Código principal da aplicação Flask  
├── templates/         # Arquivos HTML  
│   └── index.html     # Página inicial  
├── static/            # Recursos estáticos (CSS, imagens)  
├── requirements.txt   # Dependências do projeto  
└── README.md          # Documentação do projeto  
```
## Configuração e Execução
### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/PawSitive.git  
cd PawSitive  
```
### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv  
source venv/bin/activate  # Windows: venv\Scripts\activate  
```
### 3. Instale as dependências

```bash
pip install -r requirements.txt  
```
### 4. Configuração do banco de dados

* Configure o PostgreSQL com as credenciais abaixo (ou ajuste em app.py):
* Nome do banco: pawsitivedb
* Usuário: postgres
* Senha: sua_senha
* Execute o script SQL para criar a tabela imagens.

### 5. Inicie o servidor

```bash
flask run
```  
### 6. Acesse no navegador

```bash
URL padrão: http://127.0.0.1:5000
```
## Contribuição
Sinta-se à vontade para contribuir:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature (git checkout -b feature/sua-feature).
3. Envie suas alterações (git commit -m 'Adicionei minha feature').
5. Envie um pull request!

## Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
