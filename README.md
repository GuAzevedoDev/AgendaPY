# AgendaPY

Sistema de agendamento para salao de beleza, em producao para um cliente real.

🔗 Em produção: [studiomaliazevedo.com.br](https://studiomaliazevedo.com.br)

## Sobre o projeto

O AgendaPY e um sistema web completo para gestao de agendamentos de um salao de beleza, cobrindo desde o cadastro de clientes e login de funcionarios até a ficha de anamnese publica e o controle de horarios. O projeto esta hospedado em uma VPS e roda em producao atendendo o negocio real.

## Funcionalidades

- Login e gestao de funcionarios
- Agendamento de horarios com calendario Flatpickr (localizado em pt-BR)
- Ficha de anamnese publica para novos clientes
- Mascara de moeda no padrao brasileiro
- Protecao CSRF (Flask-WTF) e rate limiting (Flask-Limiter)
- Soft delete de usuarios

## Stack tecnologica

- **Backend:** Python, Flask, Jinja2
- **Banco de dados:** PostgreSQL
- **Infraestrutura:** Docker, Docker Compose, Traefik (proxy reverso e HTTPS automatico via Let's Encrypt), Gunicorn
- **Deploy:** VPS (Hostinger), com fluxo de deploy via `git pull` + `docker compose up -d --build`

## Arquitetura

O projeto segue uma organizacao em camadas:

```
controllers/   # Rotas e camada de entrada das requisicoes
services/      # Regras de negocio
repositories/  # Acesso a dados
models/        # Modelos ORM
views/         # Templates Jinja2
migrations/    # Migracoes do banco de dados
scripts/       # Scripts auxiliares
```

## Licenca

Este e um projeto proprietario, desenvolvido para um cliente real. Veja o arquivo [LICENSE](./LICENSE) para mais detalhes sobre os termos de uso.

## Autor

Desenvolvido por [Gustavo Azevedo](https://github.com/GuAzevedoDev).
