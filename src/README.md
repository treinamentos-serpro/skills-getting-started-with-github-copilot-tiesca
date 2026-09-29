# API de Atividades da Mergington High School

Uma aplicação FastAPI bem simples que permite às pessoas estudantes visualizar e se inscrever em atividades extracurriculares.

## Funcionalidades

- Visualizar todas as atividades extracurriculares disponíveis
- Inscrever-se em atividades

## Primeiros passos

1. Instale as dependências:

   ```
   pip install fastapi uvicorn
   ```

2. Execute a aplicação:

   ```
   python app.py
   ```

3. Abra seu navegador e acesse:
   - Documentação da API: http://localhost:8000/docs
   - Documentação alternativa: http://localhost:8000/redoc

## Endpoints da API

| Método | Endpoint                                                          | Descrição                                                              |
| ------ | ----------------------------------------------------------------- | ---------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Retorna todas as atividades com seus detalhes e o número atual de participantes |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Inscreve em uma atividade                                              |

## Modelo de dados

A aplicação usa um modelo de dados simples, com identificadores significativos:

1. **Activities** — usa o nome da atividade como identificador:

   - Descrição
   - Horário
   - Número máximo de participantes permitido
   - Lista de e-mails das pessoas estudantes inscritas

2. **Students** — usa o e-mail como identificador:
   - Nome
   - Ano escolar

Todos os dados são armazenados em memória, o que significa que serão reiniciados quando o servidor for reiniciado.
