from agent.graph import agente

def main():
    print("Secretário virtual iniciado. Digite 'sair' para encerrar.\n")
    historico = []

    while True:
        mensagem = input("Paciente: ")
        if mensagem.lower().strip() == "sair":
            break

        historico.append({"role": "user", "content": mensagem})
        resposta = agente.invoke({"messages": historico})

        ultima_mensagem = resposta["messages"][-1]
        print(f"Agente: {ultima_mensagem.content}\n")

        historico = resposta["messages"]


if __name__ == "__main__":
    main()