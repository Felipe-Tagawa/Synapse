# Synapse - Agente de IA Secretário para Marcação de Consultas Médicas

## Visão geral

Agente de IA que atua como secretário virtual de uma clínica ou hospital, auxiliando pacientes a marcar, remarcar e cancelar consultas médicas por meio de conversação natural (texto ou voz), sem depender de atendimento humano para as tarefas mais simples do dia a dia.

## Problema que resolve

Marcação de consultas costuma esbarrar em filas de atendimento telefônico, horário comercial limitado e retrabalho manual da recepção para conferir agenda, especialidade e disponibilidade. O agente reduz esse atrito ao ficar disponível 24/7 e automatizar o fluxo de agendamento, deixando a equipe humana livre para casos mais complexos.

## Funcionalidades principais

- Entendimento de linguagem natural para identificar a intenção do paciente (marcar, remarcar, cancelar, tirar dúvida)
- Consulta à agenda dos médicos em tempo real
- Sugestão de horários compatíveis com a especialidade solicitada
- Confirmação da consulta e envio de lembretes (WhatsApp, SMS ou e-mail)
- Escalonamento para atendente humano quando o agente não resolve o caso
- Registro do histórico de interação para auditoria

## Arquitetura

1. **Camada de conversação (LLM + Agente)**: modelo de linguagem responsável por interpretar a mensagem do paciente e decidir a próxima ação. Orquestração feita com LangChain ou LangGraph.
   Referência: https://python.langchain.com/docs/introduction/

2. **Camada de ferramentas (tools)**: funções que o agente pode chamar, como consultar agenda, criar evento e cancelar evento.

3. **Camada de dados**: banco de dados com pacientes, médicos, especialidades e horários disponíveis, implementado em PostgreSQL.

## Fluxo de funcionamento (exemplo)

1. Paciente envia mensagem: "Quero marcar uma consulta com cardiologista"
2. Agente identifica intenção e especialidade
3. Agente consulta a agenda disponível via tool
4. Agente sugere 2 ou 3 horários
5. Paciente escolhe um horário
6. Agente confirma o agendamento e envia lembrete próximo à data

## Tecnologias utilizadas

- Python
- LangChain / LangGraph para orquestração do agente
- Llama 3.1 como modelo de LLM (gratuito, contexto reduzido)
- PostgreSQL para persistência

## Status atual

O projeto utiliza dados semeados (gerados artificialmente) para simular pacientes, médicos e horários. O banco de dados PostgreSQL já está implementado, permitindo a migração futura para uma base de dados real.

## Considerações de privacidade e segurança

Por lidar com dados de saúde, o projeto precisa considerar a LGPD (Lei Geral de Proteção de Dados), especialmente por envolver dados sensíveis do paciente. É importante criptografar dados em trânsito e em repouso, e limitar o acesso do agente apenas às informações estritamente necessárias para o agendamento.
Referência: https://www.gov.br/anpd/pt-br/assuntos/noticias/lei-geral-de-protecao-de-dados-pessoais-lgpd

## Possíveis expansões

- Triagem inicial de sintomas para direcionar à especialidade correta
- Integração com prontuário eletrônico
- Envio automático de pré-consulta (formulários, exames necessários)

## Referências gerais

- LangChain (orquestração de agentes): https://python.langchain.com/docs/introduction/
- LGPD: https://www.gov.br/anpd/pt-br/assuntos/noticias/lei-geral-de-protecao-de-dados-pessoais-lgpd
