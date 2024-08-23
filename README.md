# Django Template Project

Este é um projeto template para aplicações Django, criado para servir como ponto de partida para novos projetos. O template inclui configurações básicas, estrutura de pastas, e exemplos de uso para facilitar o desenvolvimento e a implementação. Ele foi construído com base no [template padrão do site do django](https://docs.djangoproject.com/en/5.1/intro/).

## Estrutura do Projeto

```bash
django_template/
├── polls/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
    ├── static/
        ├── css/
        ├── images/
        └── js/
    ├── templates/
        ├── base.html
        └── index.html
├── mysite/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .gitignore
├── manage.py
└── README.md
```

## Pré-requisitos

- Python 3.8+
- Django 4.0+
- Virtualenv (opcional, mas recomendado)

## Configuração do Ambiente

1. Clone este repositório:
   ```bash
   git clone https://github.com/PedroMatumoto/django_template.git
   ```
   
2. Navegue até o diretório do projeto:
   ```bash
   cd django_template
   ```

3. Crie e ative um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows use `venvScriptsactivate`
   ```

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

5. Realize as migrações iniciais:
   ```bash
   python manage.py migrate
   ```

6. Inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

7. Acesse a aplicação no navegador via `http://127.0.0.1:8000/`.

## Estrutura de Diretórios

- **app/**: Contém a aplicação Django com seus modelos, views, e arquivos de migração.
- **django_template/**: Configurações do projeto, incluindo URLs e configurações do Django.
- **static/**: Arquivos estáticos (CSS, JavaScript, imagens) que serão servidos pela aplicação.
- **templates/**: Arquivos HTML que serão renderizados pelas views.

## Funcionalidades

Este template oferece:

- Configuração básica de um projeto Django
- Estrutura para arquivos estáticos e templates
- Exemplo de views e templates para facilitar a personalização

## Contribuição

Sinta-se à vontade para abrir issues e pull requests para melhorias e novas funcionalidades.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
EOF
