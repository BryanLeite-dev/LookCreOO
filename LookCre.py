import tkinter as tk
from tkinter import ttk, Tk, messagebox
from tkinter import simpledialog
from tkinter.filedialog import asksaveasfilename, askopenfilename
import json
from abc import ABC, abstractmethod

class RoupaArmario(ABC):
    def _init_(self, nome, tipo, tamanho):
        self.nome = nome
        self.tipo = tipo
        self.tamanho = tamanho

    @abstractmethod
    def descricao(self):
        pass

class Roupa(RoupaArmario):
    def _init_(self, nome, tipo, tamanho, cor, tecido, estilo):
        super()._init_(nome, tipo, tamanho)
        self.cor = cor
        self.tecido = tecido
        self.estilo = estilo

    def descricao(self):
        return (f"Roupa: {self.nome}, Tipo: {self.tipo}, Tamanho: {self.tamanho}, "
                f"Cor: {self.cor}, Tecido: {self.tecido}, Estilo: {self.estilo}")

class Look:
    def _init_(self, nome, descricao, roupas, itens=None):
        self.nome = nome
        self.descricao = descricao
        self.roupas = roupas  
        self.itens = itens if itens else []

    def detalhes(self):
        roupas_detalhes = "\n".join([roupa.descricao() for roupa in self.roupas])
        return f"Look: {self.nome}\nDescrição: {self.descricao}\nRoupas:\n\n{roupas_detalhes}\n"

class Armario:
    def _init_(self):
        self.itens = []
        self.looks = []

    def adicionar_item(self, item):
        if isinstance(item, RoupaArmario):
            self.itens.append(item)
        else:
            raise TypeError("O item deve ser do tipo RoupaArmario")

    def remover_item(self, item_nome):
        
        item_removido = next((item for item in self.itens if item.nome == item_nome), None)

        if not item_removido:
            print(f"Item '{item_nome}' não encontrado no armário.")
            return

        self.itens.remove(item_removido)

        looks_afetados = [look for look in self.looks if any(roupa.nome == item_nome for roupa in look.roupas)]

        for look in looks_afetados:
            self.remover_look_especifico(look.nome)

        if looks_afetados:
            print(f"Os seguintes looks foram removidos: {[look.nome for look in looks_afetados]}")
        else:
            print(f"Item '{item_nome}' removido. Nenhum look foi afetado.")
                
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
                'itens': [item._dict_ for item in self.itens],
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
    def _init_(self, root):
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
        self._janela_adicionar_item()

    def remover_item(self):
            if not self.armario.itens:
                messagebox.showinfo("Aviso", "Não há itens cadastrados para remover.")
                return

            janela = tk.Toplevel(self.root)
            janela.title("Remover Item")

            ttk.Label(janela, text="Selecione um item para remover:", font=("Arial", 12)).pack(pady=10)

            frame_lista = ttk.Frame(janela)
            frame_lista.pack(padx=10, pady=10)

            for item in self.armario.itens:
                button = tk.Button(frame_lista, text=item.nome, command=lambda i=item: self._confirmar_remocao_item(i, janela))
                button.pack(pady=5)

            ttk.Button(janela, text="Cancelar", command=janela.destroy).pack(pady=10)

    def _confirmar_remocao_item(self, item, janela):
        
        looks_afetados = [look for look in self.armario.looks if item in look.itens]

        if messagebox.askyesno("Confirmação", f"Deseja remover o item '{item.nome}' e os looks associados?"):
            
            for look in looks_afetados:
                self.armario.looks.remove(look)

            self.armario.itens.remove(item)

            mensagem_look = (
                f"\nOs seguintes looks foram removidos:\n{', '.join([look.nome for look in looks_afetados])}"
                if looks_afetados else "\nNenhum look foi afetado."
            )
            messagebox.showinfo(
                "Remoção Concluída",
                f"O item '{item.nome}' foi removido com sucesso.{mensagem_look}",
            )
        else:
            messagebox.showinfo("Cancelado", "A remoção do item foi cancelada.")

        janela.destroy()




    def listar_itens(self):
        itens = self.armario.listar_itens()
        if itens:
            itens_str = "\n\n".join(itens)
            messagebox.showinfo("Itens no Armário", itens_str)
        else:
            messagebox.showinfo("Itens no Armário", "O armário está vazio.")

    def buscar_look(self):
        nome = simpledialog.askstring("Buscar Look", "Digite o nome do look:")
        if nome:
            detalhes = self.armario.buscar_look(nome)
            if detalhes:
                messagebox.showinfo("Look Encontrado", detalhes)
            else:
                messagebox.showerror("Erro", "Look não encontrado.")


    def buscar_item(self):
        nome = simpledialog.askstring("Buscar Item", "Digite o nome do item:")
        if nome:
            item = self.armario.buscar_item(nome)
            if item:
                messagebox.showinfo("Item Encontrado", item.descricao())
            else:
                messagebox.showerror("Erro", "Item não encontrado.")

    def editar_item(self):
        self._janela_editar_item()

    def criar_look(self):
        self._janela_criar_look()

    def listar_looks(self):
        looks = self.armario.listar_looks()
        if looks:
            looks_str = "\n\n".join(looks)
            messagebox.showinfo("Looks Criados", looks_str)
        else:
            messagebox.showinfo("Looks Criados", "Nenhum look foi criado ainda.")

    def editar_look(self):
        self._janela_editar_look()

    def remover_look(self):
        if not self.armario.looks:
            messagebox.showinfo("Aviso", "Não há looks cadastrados para remover.")
            return

        janela = tk.Toplevel(self.root)
        janela.title("Remover Look")

        ttk.Label(janela, text="Selecione o look que deseja remover:", font=("Arial", 12)).pack(pady=10)

        frame_lista = ttk.Frame(janela)
        frame_lista.pack(padx=10, pady=10)

        for look in self.armario.looks:
            button = ttk.Button(frame_lista, text=look.nome, 
                                command=lambda l=look: self._confirmar_remocao_look(l, janela))
            button.pack(fill="x", pady=5)

        ttk.Button(janela, text="Cancelar", command=janela.destroy).pack(pady=10)

    def _confirmar_remocao_look(self, look, janela):
        if messagebox.askyesno("Confirmação", f"Deseja remover o look '{look.nome}'?"):
            self.armario.looks.remove(look)
            messagebox.showinfo("Sucesso", f"O look '{look.nome}' foi removido com sucesso.")
            janela.destroy()
        else:
            messagebox.showinfo("Cancelado", "A remoção do look foi cancelada.")

    def salvar_em_json(self):
        arquivo = asksaveasfilename(defaultextension=".json", filetypes=[("Arquivos JSON", "*.json")])
        if arquivo:
            self.armario.serializar_para_json(arquivo)
            messagebox.showinfo("Sucesso", "Armário salvo com sucesso!")

    def carregar_de_json(self):
        arquivo = askopenfilename(filetypes=[("Arquivos JSON", "*.json")])
        if arquivo:
            self.armario.carregar_de_json(arquivo)
            messagebox.showinfo("Sucesso", "Armário carregado com sucesso!")

    def _janela_adicionar_item(self):
        janela = tk.Toplevel(self.root)
        janela.title("Adicionar Item")

        ttk.Label(janela, text="Nome da Roupa:").grid(row=0, column=0, pady=5, sticky="w")
        entrada_nome = ttk.Entry(janela, width=30)
        entrada_nome.grid(row=0, column=1, pady=5)

        ttk.Label(janela, text="Tipo da Roupa:").grid(row=1, column=0, pady=5, sticky="w")
        entrada_tipo = ttk.Entry(janela, width=30)
        entrada_tipo.grid(row=1, column=1, pady=5)

        ttk.Label(janela, text="Tamanho da Roupa:").grid(row=2, column=0, pady=5, sticky="w")
        entrada_tamanho = ttk.Entry(janela, width=30)
        entrada_tamanho.grid(row=2, column=1, pady=5)

        ttk.Label(janela, text="Cor da Roupa:").grid(row=3, column=0, pady=5, sticky="w")
        entrada_cor = ttk.Entry(janela, width=30)
        entrada_cor.grid(row=3, column=1, pady=5)

        ttk.Label(janela, text="Tecido da Roupa:").grid(row=4, column=0, pady=5, sticky="w")
        entrada_tecido = ttk.Entry(janela, width=30)
        entrada_tecido.grid(row=4, column=1, pady=5)

        ttk.Label(janela, text="Estilo da Roupa:").grid(row=5, column=0, pady=5, sticky="w")
        entrada_estilo = ttk.Entry(janela, width=30)
        entrada_estilo.grid(row=5, column=1, pady=5)

        def salvar_item():
            nome = entrada_nome.get().strip()
            tipo = entrada_tipo.get().strip()
            tamanho = entrada_tamanho.get().strip()
            cor = entrada_cor.get().strip()
            tecido = entrada_tecido.get().strip()
            estilo = entrada_estilo.get().strip()

            if not nome or not tipo or not tamanho or not cor or not tecido or not estilo:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
                return

            roupa = Roupa(nome, tipo, tamanho, cor, tecido, estilo)
            self.armario.adicionar_item(roupa)
            messagebox.showinfo("Sucesso", f"Roupa '{nome}' adicionada com sucesso!")
            janela.destroy()

        ttk.Button(janela, text="Salvar", command=salvar_item).grid(row=6, column=0, pady=10)
        ttk.Button(janela, text="Cancelar", command=janela.destroy).grid(row=6, column=1, pady=10)


    def _janela_editar_item(self):
        janela = tk.Toplevel(self.root)
        janela.title("Editar Item")

        ttk.Label(janela, text="Nome da Roupa (a ser editado):").grid(row=0, column=0, pady=5, sticky="w")
        entrada_nome = ttk.Entry(janela, width=30)
        entrada_nome.grid(row=0, column=1, pady=5)

        def buscar_item_editar():
            nome = entrada_nome.get().strip()
            item = self.armario.buscar_item(nome)
            
            if item:
                entrada_tipo.delete(0, tk.END)
                entrada_tipo.insert(0, item.tipo)

                entrada_tamanho.delete(0, tk.END)
                entrada_tamanho.insert(0, item.tamanho)

                entrada_cor.delete(0, tk.END)
                entrada_cor.insert(0, item.cor)

                entrada_tecido.delete(0, tk.END)
                entrada_tecido.insert(0, item.tecido)

                entrada_estilo.delete(0, tk.END)
                entrada_estilo.insert(0, item.estilo)

                messagebox.showinfo("Item encontrado", f"Item '{nome}' encontrado. Pode editá-lo.")
            else:
                messagebox.showerror("Erro", "Item não encontrado.")

        ttk.Label(janela, text="Novo Tipo:").grid(row=1, column=0, pady=5, sticky="w")
        entrada_tipo = ttk.Entry(janela, width=30)
        entrada_tipo.grid(row=1, column=1, pady=5)

        ttk.Label(janela, text="Novo Tamanho:").grid(row=2, column=0, pady=5, sticky="w")
        entrada_tamanho = ttk.Entry(janela, width=30)
        entrada_tamanho.grid(row=2, column=1, pady=5)

        ttk.Label(janela, text="Nova Cor:").grid(row=3, column=0, pady=5, sticky="w")
        entrada_cor = ttk.Entry(janela, width=30)
        entrada_cor.grid(row=3, column=1, pady=5)

        ttk.Label(janela, text="Novo Tecido:").grid(row=4, column=0, pady=5, sticky="w")
        entrada_tecido = ttk.Entry(janela, width=30)
        entrada_tecido.grid(row=4, column=1, pady=5)

        ttk.Label(janela, text="Novo Estilo:").grid(row=5, column=0, pady=5, sticky="w")
        entrada_estilo = ttk.Entry(janela, width=30)
        entrada_estilo.grid(row=5, column=1, pady=5)

        def salvar_edicao():
            nome = entrada_nome.get().strip()
            tipo = entrada_tipo.get().strip()
            tamanho = entrada_tamanho.get().strip()
            cor = entrada_cor.get().strip()
            tecido = entrada_tecido.get().strip()
            estilo = entrada_estilo.get().strip()

            novos_dados = {
                'nome': nome,  
                'tipo': tipo,
                'tamanho': tamanho,
                'cor': cor,
                'tecido': tecido,
                'estilo': estilo
            }

            if not nome or not tipo or not tamanho or not cor or not tecido or not estilo:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
                return
            
            if self.armario.editar_item(nome, novos_dados):
                messagebox.showinfo("Sucesso", f"Item '{nome}' editado com sucesso!")
                janela.destroy()
            else:
                messagebox.showerror("Erro", "Não foi possível editar o item.")

        ttk.Button(janela, text="Buscar Item", command=buscar_item_editar).grid(row=6, column=0, pady=10)
        ttk.Button(janela, text="Salvar Alterações", command=salvar_edicao).grid(row=6, column=1, pady=10)
        ttk.Button(janela, text="Cancelar", command=janela.destroy).grid(row=6, column=2, pady=10)


    def _janela_criar_look(self):
        janela = tk.Toplevel(self.root)
        janela.title("Criar Look")

        ttk.Label(janela, text="Nome do Look:").grid(row=0, column=0, pady=5, sticky="w")
        entrada_nome = ttk.Entry(janela, width=30)
        entrada_nome.grid(row=0, column=1, pady=5)

        ttk.Label(janela, text="Descrição do Look:").grid(row=1, column=0, pady=5, sticky="w")
        entrada_descricao = ttk.Entry(janela, width=30)
        entrada_descricao.grid(row=1, column=1, pady=5)

        ttk.Label(janela, text="Selecione as roupas:").grid(row=2, column=0, pady=5, sticky="w")
        roupas_disponiveis = self.armario.listar_itens()
        roupas_var = tk.StringVar(value=roupas_disponiveis)
        lista_roupas = tk.Listbox(janela, listvariable=roupas_var, selectmode="multiple", height=10, width=50)
        lista_roupas.grid(row=2, column=1, pady=5)

        def criar_look():
            nome = entrada_nome.get().strip()
            descricao = entrada_descricao.get().strip()
            selecao_indices = lista_roupas.curselection()

            if not nome or not descricao:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
                return

            if not selecao_indices:
                messagebox.showerror("Erro", "Selecione pelo menos uma roupa.")
                return

            nomes_roupas = [roupas_disponiveis[i].split(",")[0].split(":")[1].strip() for i in selecao_indices]
            look = self.armario.criar_look(nome, descricao, nomes_roupas)

            if look:
                messagebox.showinfo("Sucesso", f"Look '{nome}' criado com sucesso!")
                janela.destroy()
            else:
                messagebox.showerror("Erro", "Nenhuma roupa válida foi encontrada para criar o look.")

        ttk.Button(janela, text="Criar", command=criar_look).grid(row=3, column=0, pady=10)
        ttk.Button(janela, text="Cancelar", command=janela.destroy).grid(row=3, column=1, pady=10)
    def _confirmar_remocao_item(self, item, janela):
        
        looks_afetados = [look for look in self.armario.looks if any(roupa.nome == item.nome for roupa in look.roupas)]

        if messagebox.askyesno("Confirmação", f"Deseja remover o item '{item.nome}' e os looks associados?"):
          
            self.armario.itens.remove(item)
            for look in looks_afetados:
                self.armario.remover_look_especifico(look.nome)

            mensagem_look = (
                f"\nOs seguintes looks foram removidos:\n{', '.join([look.nome for look in looks_afetados])}"
                if looks_afetados else "\nNenhum look foi afetado."
            )
            messagebox.showinfo(
                "Remoção Concluída",
                f"O item '{item.nome}' foi removido com sucesso.{mensagem_look}",
            )
        else:
            messagebox.showinfo("Cancelado", "A remoção do item foi cancelada.")

        janela.destroy()

    def _janela_editar_look(self):
        janela = tk.Toplevel(self.root)
        janela.title("Editar Look")

        ttk.Label(janela, text="Selecione o Look:").grid(row=0, column=0, pady=5, sticky="w")
        looks_disponiveis = [look.nome for look in self.armario.looks]
        if not looks_disponiveis:
            messagebox.showerror("Erro", "Nenhum look disponível para edição.")
            janela.destroy()
            return

        look_var = tk.StringVar(value=looks_disponiveis[0])
        combo_looks = ttk.Combobox(janela, textvariable=look_var, values=looks_disponiveis, state="readonly")
        combo_looks.grid(row=0, column=1, pady=5)

        ttk.Label(janela, text="Novo Nome:").grid(row=1, column=0, pady=5, sticky="w")
        entrada_nome = ttk.Entry(janela, width=30)
        entrada_nome.grid(row=1, column=1, pady=5)

        ttk.Label(janela, text="Nova Descrição:").grid(row=2, column=0, pady=5, sticky="w")
        entrada_descricao = ttk.Entry(janela, width=30)
        entrada_descricao.grid(row=2, column=1, pady=5)

        ttk.Label(janela, text="Roupas disponíveis:").grid(row=3, column=0, pady=5, sticky="w")
        roupas_disponiveis = self.armario.listar_itens()
        roupas_var = tk.StringVar(value=roupas_disponiveis)
        lista_roupas = tk.Listbox(janela, listvariable=roupas_var, selectmode="multiple", height=10, width=50)
        lista_roupas.grid(row=3, column=1, pady=5)

        def carregar_dados_look(*args):
            nome_look = look_var.get()
            look = next((look for look in self.armario.looks if look.nome == nome_look), None)
            if look:
                entrada_nome.delete(0, tk.END)
                entrada_nome.insert(0, look.nome)
                entrada_descricao.delete(0, tk.END)
                entrada_descricao.insert(0, look.descricao)

                lista_roupas.selection_clear(0, tk.END)
                for idx, roupa in enumerate(roupas_disponiveis):
                    nome_roupa = roupa.split(",")[0].split(":")[1].strip()
                    if nome_roupa in [r.nome for r in look.roupas]:
                        lista_roupas.selection_set(idx)

        combo_looks.bind("<<ComboboxSelected>>", carregar_dados_look)
        carregar_dados_look()

        def salvar_edicao():
            nome_atual = look_var.get()
            novo_nome = entrada_nome.get().strip()
            nova_descricao = entrada_descricao.get().strip()
            selecao_indices = lista_roupas.curselection()

            if not novo_nome or not nova_descricao:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
                return

            nomes_roupas = [roupas_disponiveis[i].split(",")[0].split(":")[1].strip() for i in selecao_indices]

            novos_dados = {
                "nome": novo_nome,
                "descricao": nova_descricao,
                "roupas": nomes_roupas
            }

            if self.armario.editar_look(nome_atual, novos_dados):
                messagebox.showinfo("Sucesso", f"Look '{novo_nome}' editado com sucesso!")
                janela.destroy()
            else:
                messagebox.showerror("Erro", "Não foi possível editar o look.")

        ttk.Button(janela, text="Salvar", command=salvar_edicao).grid(row=4, column=0, pady=10)
        ttk.Button(janela, text="Cancelar", command=janela.destroy).grid(row=4, column=1, pady=10)


def centralizar_janela(root, largura=400, altura=300):
   
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()

    pos_x = (largura_tela - largura) // 2
    pos_y = (altura_tela - altura) // 2

    root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

if _name_ == "_main_":
    root = Tk()
    centralizar_janela(root, largura=400, altura=300)
    app = ArmarioApp(root)
    root.mainloop()
