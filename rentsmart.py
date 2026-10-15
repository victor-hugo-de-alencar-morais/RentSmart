import csv

# ==========================================
# CLASSES DE MODELO (ORIENTAÇÃO A OBJETOS)
# ==========================================

class Imovel:
    #Classe base representando um imóvel genérico.
    def __init__(self, tipo, valor_base):
        self.tipo = tipo
        self.valor_base = valor_base
        self.taxa_contratual = 2000.00
        self.valor_aluguel_calculado = 0.0

    def calcular_aluguel(self):
        # Método a ser sobrescrito pelas classes filhas (Polimorfismo)
        pass

class Apartamento(Imovel):
    def __init__(self, quartos, vaga_garagem, possui_criancas):
        super().__init__("Apartamento", 700.00)
        self.quartos = quartos
        self.vaga_garagem = vaga_garagem
        self.possui_criancas = possui_criancas

    def calcular_aluguel(self):
        total = self.valor_base
        
        # Regra de quartos
        if self.quartos == 2:
            total += 200.00
            
        # Regra de garagem
        if self.vaga_garagem > 0:
            total += 300.00 # 1 vaga permitida e cobrada
            
        # Regra de desconto
        if not self.possui_criancas:
            desconto = total * 0.05
            total -= desconto
            
        self.valor_aluguel_calculado = total
        return total

class Casa(Imovel):
    def __init__(self, quartos, vaga_garagem):
        super().__init__("Casa", 900.00)
        self.quartos = quartos
        self.vaga_garagem = vaga_garagem

    def calcular_aluguel(self):
        total = self.valor_base
        
        # Regra de quartos
        if self.quartos == 2:
            total += 250.00
            
        # Regra de garagem
        if self.vaga_garagem > 0:
            total += 300.00
            
        self.valor_aluguel_calculado = total
        return total

class Estudio(Imovel):
    def __init__(self, vagas_garagem):
        super().__init__("Estúdio", 1200.00)
        self.vagas_garagem = vagas_garagem

    def calcular_aluguel(self):
        total = self.valor_base
        
        # Regra de garagem específica para estúdio
        if self.vagas_garagem > 0:
            if self.vagas_garagem <= 2:
                total += 250.00
            else:
                total += 250.00 + ((self.vagas_garagem - 2) * 60.00)
                
        self.valor_aluguel_calculado = total
        return total

# ==========================================
# CLASSE DE SERVIÇO E REGRAS DE ORÇAMENTO
# ==========================================

class Orcamento:
    #Classe responsável por processar o orçamento e gerar o CSV.
    def __init__(self, imovel, parcelas_taxa):
        self.imovel = imovel
        self.parcelas_taxa = parcelas_taxa
        self.valor_parcela_taxa = self.imovel.taxa_contratual / parcelas_taxa
        self.imovel.calcular_aluguel()

    def exibir_resumo(self):
        print("\n" + "="*40)
        print(" RESUMO DO ORÇAMENTO - RENTSMART")
        print("="*40)
        print(f"Tipo de Imóvel...: {self.imovel.tipo}")
        print(f"Aluguel Mensal...: R$ {self.imovel.valor_aluguel_calculado:.2f}")
        print(f"Taxa Contratual..: R$ 2000.00 (Em {self.parcelas_taxa}x de R$ {self.valor_parcela_taxa:.2f})")
        print("="*40)

    def gerar_csv(self):
        nome_arquivo = "projecao_locacao.csv"
        try:
            with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Mes", "Valor do Aluguel", "Parcela Taxa Contrato", "Valor Total do Mes"])
                
                for mes in range(1, 13):
                    aluguel = self.imovel.valor_aluguel_calculado
                    parcela_taxa = self.valor_parcela_taxa if mes <= self.parcelas_taxa else 0.0
                    total_mes = aluguel + parcela_taxa
                    
                    writer.writerow([mes, f"R$ {aluguel:.2f}", f"R$ {parcela_taxa:.2f}", f"R$ {total_mes:.2f}"])
                    
            print(f" Sucesso! Arquivo '{nome_arquivo}' gerado com a projeção de 12 meses.")
        except Exception as e:
            print(f" Erro ao gerar o arquivo CSV: {e}")

# ==========================================
# FUNÇÃO PRINCIPAL E INTERFACE DE USUÁRIO
# ==========================================

def menu_principal():
    print("Bem-vindo ao sistema RentSmart - R.M Imóveis")
    print("1 - Apartamento")
    print("2 - Casa")
    print("3 - Estúdio")
    
    while True:
        try:
            opcao = int(input("Escolha o tipo de imóvel (1-3): "))
            if opcao in [1, 2, 3]:
                break
            print("Opção inválida.")
        except ValueError:
            print("Digite um número válido.")

    imovel_selecionado = None

    if opcao == 1:
        quartos = int(input("Quantidade de quartos (1 ou 2)? "))
        vagas = int(input("Deseja vaga de garagem? (0 para não, 1 para sim): "))
        criancas_str = input("Possui crianças? (s/n): ").strip().lower()
        possui_criancas = True if criancas_str == 's' else False
        imovel_selecionado = Apartamento(quartos, vagas, possui_criancas)

    elif opcao == 2:
        quartos = int(input("Quantidade de quartos (1 ou 2)? "))
        vagas = int(input("Deseja vaga de garagem? (0 para não, 1 para sim): "))
        imovel_selecionado = Casa(quartos, vagas)

    elif opcao == 3:
        vagas = int(input("Quantas vagas de garagem deseja? (0 para nenhuma): "))
        imovel_selecionado = Estudio(vagas)

    # Coleta regra de parcelamento comum a todos
    while True:
        try:
            parcelas = int(input("Em quantas vezes deseja parcelar a taxa contratual de R$2000 (1 a 5)? "))
            if 1 <= parcelas <= 5:
                break
            print("O parcelamento deve ser entre 1 e 5 vezes.")
        except ValueError:
            print("Digite um número válido.")

    # Processamento final
    orcamento = Orcamento(imovel_selecionado, parcelas)
    orcamento.exibir_resumo()
    orcamento.gerar_csv()

if __name__ == "__main__":
    menu_principal()