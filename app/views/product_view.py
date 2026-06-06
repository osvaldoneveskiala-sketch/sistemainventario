import customtkinter as ctk

from app.models.database import SessionLocal
from app.models.product import Product

from app.services.ai_service import AIService


class ProductView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.pack(fill="both", expand=True)

        self.produto_edicao = None

        titulo = ctk.CTkLabel(
            self,
            text="Gestão de Produtos",
            font=("Arial", 28, "bold")
        )

        titulo.pack(pady=20)

        self.nome_entry = ctk.CTkEntry(
            self,
            placeholder_text="Nome do Produto",
            width=300
        )

        self.nome_entry.pack(pady=10)

        self.preco_entry = ctk.CTkEntry(
            self,
            placeholder_text="Preço",
            width=300
        )

        self.preco_entry.pack(pady=10)

        self.quantidade_entry = ctk.CTkEntry(
            self,
            placeholder_text="Quantidade",
            width=300
        )

        self.quantidade_entry.pack(pady=10)

        self.salvar_button = ctk.CTkButton(
            self,
            text="Salvar Produto",
            command=self.salvar_produto
        )

        self.salvar_button.pack(pady=20)

        self.message = ctk.CTkLabel(
            self,
            text=""
        )

        self.message.pack(pady=10)

        self.lista_frame = ctk.CTkFrame(self)

        self.lista_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.listar_produtos()

    def salvar_produto(self):

        nome = self.nome_entry.get()
        preco = self.preco_entry.get()
        quantidade = self.quantidade_entry.get()

        try:

            db = SessionLocal()

            if self.produto_edicao:

                produto = db.query(Product).filter(
                    Product.id == self.produto_edicao
                ).first()

                if produto:

                    produto.nome = nome
                    produto.preco = float(preco)
                    produto.quantidade = int(quantidade)

                    db.commit()

                    self.message.configure(
                        text="Produto atualizado com sucesso!"
                    )

                self.produto_edicao = None

                self.salvar_button.configure(
                    text="Salvar Produto"
                )

            else:

                novo_produto = Product(
                    nome=nome,
                    preco=float(preco),
                    quantidade=int(quantidade)
                )

                db.add(novo_produto)

                db.commit()

                self.message.configure(
                    text="Produto salvo com sucesso!"
                )

            db.close()

            self.nome_entry.delete(0, "end")
            self.preco_entry.delete(0, "end")
            self.quantidade_entry.delete(0, "end")

            self.listar_produtos()

        except Exception as erro:

            self.message.configure(
                text=f"Erro: {erro}"
            )

    def carregar_produto(self, produto):

        self.produto_edicao = produto.id

        self.nome_entry.delete(0, "end")
        self.preco_entry.delete(0, "end")
        self.quantidade_entry.delete(0, "end")

        self.nome_entry.insert(0, produto.nome)
        self.preco_entry.insert(0, str(produto.preco))
        self.quantidade_entry.insert(0, str(produto.quantidade))

        self.salvar_button.configure(
            text="Atualizar Produto"
        )

    def eliminar_produto(self, produto_id):

        db = SessionLocal()

        produto = db.query(Product).filter(
            Product.id == produto_id
        ).first()

        if produto:

            db.delete(produto)

            db.commit()

        db.close()

        self.message.configure(
            text="Produto eliminado com sucesso!"
        )

        self.listar_produtos()

    def listar_produtos(self):

        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        db = SessionLocal()

        produtos = db.query(Product).all()

        db.close()

        titulo_lista = ctk.CTkLabel(
            self.lista_frame,
            text="Produtos Cadastrados",
            font=("Arial", 22, "bold")
        )

        titulo_lista.pack(pady=10)

        for produto in produtos:

            item_frame = ctk.CTkFrame(self.lista_frame)

            item_frame.pack(
                fill="x",
                padx=10,
                pady=5
            )

            previsao = AIService.prever_stock(
                produto.quantidade
            )

            texto = (
                f"ID: {produto.id} | "
                f"Nome: {produto.nome} | "
                f"Preço: {produto.preco} | "
                f"Quantidade: {produto.quantidade} | "
                f"IA: {previsao}"
            )

            label = ctk.CTkLabel(
                item_frame,
                text=texto,
                anchor="w"
            )

            label.pack(
                side="left",
                padx=10,
                pady=10
            )

            btn_editar = ctk.CTkButton(
                item_frame,
                text="Editar",
                width=80,
                command=lambda p=produto: self.carregar_produto(p)
            )

            btn_editar.pack(
                side="right",
                padx=5
            )

            btn_delete = ctk.CTkButton(
                item_frame,
                text="Eliminar",
                width=100,
                fg_color="red",
                command=lambda id=produto.id: self.eliminar_produto(id)
            )

            btn_delete.pack(
                side="right",
                padx=5
            )