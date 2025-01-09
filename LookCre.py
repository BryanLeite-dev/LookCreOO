import tkinter as tk
from tkinter import ttk, Tk, messagebox
from tkinter import simpledialog
from tkinter.filedialog import asksaveasfilename, askopenfilename
import json
from abc import ABC, abstractmethod

class RoupaArmario(ABC):
    def __init__(self, nome, tipo, tamanho):
        self.nome = nome
        self.tipo = tipo
        self.tamanho = tamanho

    @abstractmethod
    def descricao(self):
        pass

class Roupa(RoupaArmario):
    def __init__(self, nome, tipo, tamanho, cor, tecido, estilo):
        super().__init__(nome, tipo, tamanho)
        self.cor = cor
        self.tecido = tecido
        self.estilo = estilo

    def descricao(self):
        return (f"Roupa: {self.nome}, Tipo: {self.tipo}, Tamanho: {self.tamanho}, "
                f"Cor: {self.cor}, Tecido: {self.tecido}, Estilo: {self.estilo}")

class Look:
    def __init__(self, nome, descricao, roupas, itens=None):
        self.nome = nome
        self.descricao = descricao
        self.roupas = roupas  
        self.itens = itens if itens else []

    def detalhes(self):
        roupas_detalhes = "\n".join([roupa.descricao() for roupa in self.roupas])
        return f"Look: {self.nome}\nDescrição: {self.descricao}\nRoupas:\n\n{roupas_detalhes}\n"

class Armario:
    def __init__(self):
        self.itens = []
        self.looks = []

    def adicionar_item(self, item):
        if isinstance(item, RoupaArmario):
            self.itens.append(item)
        else:
            raise TypeError("O item deve ser do tipo RoupaArmario")

    def remover_item(self, item_nome):
        
        self.itens = [item for item in self.itens if item.nome != item_nome]

        looks_associados = [look for look in self.looks if any(item.nome == item_nome for item in look.roupas)]
        
        for look in looks_associados:
            self.remover_look_especifico(look.nome)
        
        if looks_associados:
            print(f"Os seguintes looks foram removidos: {[look.nome for look in looks_associados]}")
        else:
            print("Nenhum look foi afetado pela remoção do item.")

    def remover_look_especifico(self, nome_look):
        self.looks = [look for look in self.looks if look.nome != nome_look]
        print(f"O look '{nome_look}' foi removido com sucesso.")

    def listar_itens(self):
        return [item.descricao() for item in self.itens]

    def buscar_item(self, nome):
        for item in self.itens:
            if item.nome == nome:
                return item
        return None

    def editar_item(self, nome, novos_dados):
        item = self.buscar_item(nome)
        if item:
            if isinstance(item, Roupa):  
                item.nome = novos_dados.get('nome', item.nome)
                item.tipo = novos_dados.get('tipo', item.tipo)
                item.tamanho = novos_dados.get('tamanho', item.tamanho)
                item.cor = novos_dados.get('cor', item.cor)
                item.tecido = novos_dados.get('tecido', item.tecido)
                item.estilo = novos_dados.get('estilo', item.estilo)
            return True
        return False

    def criar_look(self, nome, descricao, nomes_roupas):
        roupas = []
        for nome_roupa in nomes_roupas:
            roupa = self.buscar_item(nome_roupa)
            if roupa:
                roupas.append(roupa)
            else:
                print(f"Roupa '{nome_roupa}' não encontrada e não será adicionada ao look.")
        if roupas:
            look = Look(nome, descricao, roupas)
            self.looks.append(look)
            return look
        else:
            print("Erro: Nenhuma roupa válida foi encontrada para criar o look.")
            return None

    def listar_looks(self):
        return [look.detalhes() for look in self.looks]
    
    def buscar_look(self, nome):
        
        for look in self.looks:
            if look.nome == nome:
                return look.detalhes()
        return None

    def editar_look(self, nome, novos_dados):
        look = next((look for look in self.looks if look.nome == nome), None)
        if look:
            look.nome = novos_dados.get('nome', look.nome)
            look.descricao = novos_dados.get('descricao', look.descricao)
            
            if 'roupas' in novos_dados:
                roupas = []
                for nome_roupa in novos_dados['roupas']:
                    roupa = self.buscar_item(nome_roupa)
                    if roupa:
                        roupas.append(roupa)
                if roupas:
                    look.roupas = roupas
                else:
                    print("Nenhuma roupa válida encontrada para o look.")
            return True
        return False
    
    def remover_look(self):
        if not self.looks:
            print("Não há looks cadastrados para remover.")
            return

        print("Looks disponíveis:")
        for i, look in enumerate(self.looks, start=1):
            print(f"{i}. {look.nome} - {look.descricao}")

        try:
            escolha = int(input("Digite o número do look que deseja remover: "))
            if 1 <= escolha <= len(self.looks):
                look_removido = self.looks.pop(escolha - 1)
                print(f"O look '{look_removido.nome}' foi removido com sucesso.")
            else:
                print("Opção inválida. Nenhum look foi removido.")
        except ValueError:
            print("Entrada inválida. Nenhum look foi removido.")

    def serializar_para_json(self, arquivo):
        with open(arquivo, 'w') as f:
            
            dados = {
                'itens': [item.__dict__ for item in self.itens],
                'looks': [
                    {'nome': look.nome, 'descricao': look.descricao, 'roupas': [roupa.nome for roupa in look.roupas]}
                    for look in self.looks
                ]
            }
            json.dump(dados, f, indent=4)

    def carregar_de_json(self, arquivo):
        with open(arquivo, 'r') as f:
            dados = json.load(f)
            self.itens = [] 
            self.looks = []  
           
            for item in dados['itens']:
                roupa = Roupa(item['nome'], item['tipo'], item['tamanho'], item['cor'], item['tecido'], item['estilo'])
                self.itens.append(roupa)
           
            for look in dados['looks']:
                roupas_look = [self.buscar_item(nome_roupa) for nome_roupa in look['roupas']]
                self.looks.append(Look(look['nome'], look['descricao'], roupas_look))

def exibir_menu():
    print("\n=== Menu do Armário de Roupas ===")
    print("Adicionar item")
    print("Listar itens")
    print("Buscar item")
    print("Editar item")
    print("Remover item")   
    print("Criar look")
    print("Listar looks")
    print("Buscar looks")
    print("Editar look")
    print("Remover look")
    print("Salvar armário em JSON")
    print("Carregar armário de JSON")
    print("Sair")

class ArmarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Armário")
        self.armario = Armario()
       
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)
       
        self.frame_itens = ttk.Frame(notebook)
        self.frame_looks = ttk.Frame(notebook)
        self.frame_gerenciamento = ttk.Frame(notebook)

        notebook.add(self.frame_itens, text="Roupas")
        notebook.add(self.frame_looks, text="Looks")
        notebook.add(self.frame_gerenciamento, text="Gerenciamento")

        self._configurar_aba_itens()
        self._configurar_aba_looks()
        self._configurar_aba_gerenciamento()

    def _configurar_aba_itens(self):
        ttk.Label(self.frame_itens, text="Gerenciamento de Roupas", font=("Arial", 16)).pack(pady=10)

        ttk.Button(self.frame_itens, text="Adicionar Roupa", command=self.adicionar_item).pack(pady=5, fill="x")
        ttk.Button(self.frame_itens, text="Listar Roupas", command=self.listar_itens).pack(pady=5, fill="x")
        ttk.Button(self.frame_itens, text="Buscar Roupa", command=self.buscar_item).pack(pady=5, fill="x")
        ttk.Button(self.frame_itens, text="Editar Roupa", command=self.editar_item).pack(pady=5, fill="x")
        ttk.Button(self.frame_itens, text="Remover Roupa", command=self.remover_item).pack(pady=5, fill="x")

    def _configurar_aba_looks(self):
        ttk.Label(self.frame_looks, text="Gerenciamento de Looks", font=("Arial", 16)).pack(pady=10)

        ttk.Button(self.frame_looks, text="Criar Look", command=self.criar_look).pack(pady=5, fill="x")
        ttk.Button(self.frame_looks, text="Listar Looks", command=self.listar_looks).pack(pady=5, fill="x")
        ttk.Button(self.frame_looks, text="Buscar Look", command=self.buscar_look).pack(pady=5, fill="x")
        ttk.Button(self.frame_looks, text="Editar Look", command=self.editar_look).pack(pady=5, fill="x")
        ttk.Button(self.frame_looks, text="Remover Look", command=self.remover_look).pack(pady=5, fill="x")

    def _configurar_aba_gerenciamento(self):
        ttk.Label(self.frame_gerenciamento, text="Gerenciamento do Armário", font=("Arial", 16)).pack(pady=10)

        ttk.Button(self.frame_gerenciamento, text="Carregar Armário de JSON", command=self.carregar_de_json).pack(pady=5, fill="x")
        ttk.Button(self.frame_gerenciamento, text="Salvar Armário em JSON", command=self.salvar_em_json).pack(pady=5, fill="x")
       
    def adicionar_item(self):
        messagebox.showinfo("Adicionar Roupa", "Funcionalidade de adicionar item.")

    def listar_itens(self):
        messagebox.showinfo("Listar Roupas", "Funcionalidade de listar itens.")

    def buscar_item(self):
        messagebox.showinfo("Buscar Roupa", "Funcionalidade de buscar item.")

    def editar_item(self):
        messagebox.showinfo("Editar Roupa", "Funcionalidade de editar item.")

    def remover_item(self):
        messagebox.showinfo("Remover Roupa", "Funcionalidade de remover item.")

    def criar_look(self):
        messagebox.showinfo("Criar Look", "Funcionalidade de criar look.")

    def listar_looks(self):
        messagebox.showinfo("Listar Looks", "Funcionalidade de listar looks.")

    def buscar_look(self):
        messagebox.showinfo("Buscar Look", "Funcionalidade de buscar look.")

    def editar_look(self):
        messagebox.showinfo("Editar Look", "Funcionalidade de editar look.")

    def remover_look(self):
        messagebox.showinfo("Remover Look", "Funcionalidade de remover look.")

    def salvar_em_json(self):
        messagebox.showinfo("Salvar Armário", "Funcionalidade de salvar armário.")

    def carregar_de_json(self):
        messagebox.showinfo("Carregar Armário", "Funcionalidade de carregar armário.")

def centralizar_janela(root, largura=400, altura=300):
   
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()

    pos_x = (largura_tela - largura) // 2
    pos_y = (altura_tela - altura) // 2

    root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

if __name__ == "__main__":
    root = Tk()
    centralizar_janela(root, largura=400, altura=300)
    app = ArmarioApp(root)
    root.mainloop()