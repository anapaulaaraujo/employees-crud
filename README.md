# CRUD

API REST para cadastro de funcionários

### Tecnologias utilizadas

- Python
- Tornado
- JWT
- Pymongo

### Instalação do projeto

1. Clone o repositorio

```python
git clone https://github.com/anapaulaaraujo/employees-crud.git
```

1. Acesse a pasta do projeto pelo terminal

```python
cd employees-crud
```

1. Inicie a API

```python
python main.py
```

> Você pode testar a API usando o Postman
> 

### Estrutura

Em uma API RESTful, os endpoints (URLs) definem a estrutura da API e como os usuários finais acessam os dados de nosso aplicativo usando os métodos HTTP - GET, POST, PUT, DELETE (CRUD)

| Ação | HTML | URL | Descriçao |
| --- | --- | --- | --- |
| Criar | POST | /nutemployee | Cria um funcionario, validando as informações passadas pelo “body” da requisição e inseri no banco de dados |
| Ler | GET | /nutemployee | Seleciona a lista de funcionarios existente no banco de dados |
| Ler | GET | /nutemployee/:name | Seleciona um funcionario especifico no banco de dados, usando um URL dinamica |
| Editar | PUT | /nutemployee/:name | Edita informações de um funcionario especifico usando um URL dinamica |
| Deletar | DELETE | /nutemployee/:name | Deleta do banco de dados um funcionario especifico usanddo uma URL dinamica |
| Criar | POST | /signauth | Cria um usuario com permissão para acessar o banco de dados |
| Criar | POST | /loginauth | Login de um usuario cadastrado no banco de dados e geração de token |

### Exemplo de payload para POST da URL /nutemployee

```json
{
	  "name":"teste",
    "birth_date":"21/10/1996",
    "gender":"M",
    "email":"teste@gmail.com",
    "cpf":"119.119.119-11",
    "start_date":"10/2020",
    "team":"backend"
}
```

### Exemplo de payload para POST da URL /signauth

```json
{
   "email":"usuario@rh.com",
   "senha": "crud"
}
```