import getpass

class ContaBancaria:
    def __init__(self, titular, senha):
        self.titular = titular
        self.saldo = 0.0
        self.historico = []
        self.senha = senha
        self.numero_saques = 0
        self.LIMITE_SAQUES = 3
        self.limite_saque_diario = 500.0

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.historico.append(f"Depósito: +R${valor:.2f}")
            print(f"Depósito de R${valor:.2f} realizado com sucesso!")
        else:
            print("Valor de depósito inválido.")

    def sacar(self, valor):
        if valor <= 0:
            print("Valor de saque inválido.")
            return

        if self.numero_saques >= self.LIMITE_SAQUES:
            print("Número máximo de saques diários atingido.")
            return

        if valor > self.saldo:
            print("Saldo insuficiente para realizar o saque.")
            return

        if valor > self.limite_saque_diario:
            print("O valor do saque excede o limite diário de R$500.00.")
            return

        self.saldo -= valor
        self.historico.append(f"Saque: -R${valor:.2f}")
        self.numero_saques += 1
        print(f"Saque de R${valor:.2f} realizado com sucesso!")

    def transferir(self, valor, conta_destino):
        if valor <= 0:
            print("Valor de transferência inválido.")
            return

        if valor > self.saldo:
            print("Saldo insuficiente para realizar a transferência.")
            return

        self.saldo -= valor
        conta_destino.saldo += valor
        self.historico.append(f"Transferência para {conta_destino.titular}: -R${valor:.2f}")
        conta_destino.historico.append(f"Transferência recebida de {self.titular}: +R${valor:.2f}")
        print(f"Transferência de R${valor:.2f} para {conta_destino.titular} realizada com sucesso!")

    def exibir_extrato(self):
        print(f"\nExtrato da conta de {self.titular}:")
        if not self.historico:
            print("Não foram realizadas movimentações.")
        else:
            for transacao in self.historico:
                print(transacao)
        print(f"Saldo atual: R${self.saldo:.2f}")

class Banco:
    def __init__(self):
        self.contas = []

    def criar_conta(self, titular, senha):
        nova_conta = ContaBancaria(titular, senha)
        self.contas.append(nova_conta)
        print(f"Conta criada com sucesso para {titular}.")

    def autenticar(self, titular):
        for conta in self.contas:
            if conta.titular == titular:
                senha = getpass.getpass("Digite sua senha: ")
                if senha == conta.senha:
                    print("Autenticação realizada com sucesso!")
                    return conta
                else:
                    print("Senha incorreta.")
                    return None
        print("Conta não encontrada.")
        return None

# Sistema bancário interativo
def sistema_bancario():
    banco = Banco()

    while True:
        print("\n===== Bem-vindo ao Banco =====")
        print("[1] Criar Conta")
        print("[2] Acessar Conta")
        print("[3] Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            titular = input("Informe o nome do titular: ")
            senha = getpass.getpass("Crie uma senha: ")
            banco.criar_conta(titular, senha)

        elif opcao == "2":
            titular = input("Informe o nome do titular: ")
            conta = banco.autenticar(titular)
            
            if conta:
                while True:
                    print("\n=== Menu de Operações ===")
                    print("[d] Depositar")
                    print("[s] Sacar")
                    print("[t] Transferir")
                    print("[e] Exibir Extrato")
                    print("[q] Sair")
                    opcao_conta = input("Escolha uma opção: ").lower()

                    if opcao_conta == "d":
                        valor = float(input("Informe o valor do depósito: "))
                        conta.depositar(valor)

                    elif opcao_conta == "s":
                        valor = float(input("Informe o valor do saque: "))
                        conta.sacar(valor)

                    elif opcao_conta == "t":
                        titular_destino = input("Informe o nome do titular da conta de destino: ")
                        conta_destino = banco.autenticar(titular_destino)
                        if conta_destino:
                            valor = float(input("Informe o valor da transferência: "))
                            conta.transferir(valor, conta_destino)

                    elif opcao_conta == "e":
                        conta.exibir_extrato()

                    elif opcao_conta == "q":
                        print("Saindo da conta...")
                        break
                    else:
                        print("Opção inválida, tente novamente.")

        elif opcao == "3":
            print("Obrigado por utilizar o sistema bancário!")
            break

        else:
            print("Opção inválida, tente novamente.")

# Executa o sistema bancário
sistema_bancario()
