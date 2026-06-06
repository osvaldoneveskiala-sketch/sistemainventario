import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from app.views.product_view import ProductView
from app.models.database import SessionLocal
from app.models.product import Product
from app.services.ai_service import AIService


class DashboardView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.pack(fill="both", expand=True)

        menu = ctk.CTkFrame(self, width=200, corner_radius=0)
        menu.pack(side="left", fill="y")

        titulo = ctk.CTkLabel(
            menu,
            text="INVENTÁRIO IA",
            font=("Arial", 22, "bold")
        )
        titulo.pack(pady=30)

        btn_dashboard = ctk.CTkButton(
            menu,
            text="Dashboard",
            command=self.mostrar_dashboard
        )
        btn_dashboard.pack(pady=10, padx=20)

        btn_produtos = ctk.CTkButton(
            menu,
            text="Produtos",
            command=self.mostrar_produtos
        )
        btn_produtos.pack(pady=10, padx=20)

        btn_logout = ctk.CTkButton(
            menu,
            text="Logout",
            fg_color="red"
        )
        btn_logout.pack(side="bottom", pady=20, padx=20)

        self.conteudo = ctk.CTkFrame(self)
        self.conteudo.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.mostrar_dashboard()

    def limpar_conteudo(self):
        for widget in self.conteudo.winfo_children():
            widget.destroy()

    def mostrar_dashboard(self):

        self.limpar_conteudo()

        titulo = ctk.CTkLabel(
            self.conteudo,
            text="Dashboard Principal",
            font=("Arial", 30, "bold")
        )
        titulo.pack(pady=10)

        db = SessionLocal()
        produtos = db.query(Product).all()
        db.close()

        total_produtos = len(produtos)
        total_stock = sum(p.quantidade for p in produtos)

        cards = ctk.CTkFrame(self.conteudo)
        cards.pack(pady=10)

        card1 = ctk.CTkFrame(cards, width=200, height=100)
        card1.grid(row=0, column=0, padx=20)

        ctk.CTkLabel(
            card1,
            text=f"Produtos\n{total_produtos}",
            font=("Arial", 20, "bold")
        ).place(relx=0.5, rely=0.5, anchor="center")

        card2 = ctk.CTkFrame(cards, width=200, height=100)
        card2.grid(row=0, column=1, padx=20)

        ctk.CTkLabel(
            card2,
            text=f"Stock\n{total_stock}",
            font=("Arial", 20, "bold")
        ).place(relx=0.5, rely=0.5, anchor="center")

        alertas = ctk.CTkFrame(self.conteudo)
        alertas.pack(fill="x", pady=10)

        ctk.CTkLabel(
            alertas,
            text="Alertas Inteligentes",
            font=("Arial", 20, "bold")
        ).pack(pady=5)

        for p in produtos:

            estado = AIService.prever_stock(p.quantidade)

            cor = "red" if estado == "Stock Baixo" else "orange" if estado == "Stock Médio" else "green"

            ctk.CTkLabel(
                alertas,
                text=f"{p.nome} - {estado}",
                text_color=cor
            ).pack()

        grafico_frame = ctk.CTkFrame(self.conteudo)
        grafico_frame.pack(fill="both", expand=True, pady=10)

        nomes = [p.nome for p in produtos]
        quantidades = [p.quantidade for p in produtos]

        fig = plt.Figure(figsize=(6, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(nomes, quantidades)
        ax.set_title("Stock dos Produtos")

        canvas = FigureCanvasTkAgg(fig, grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def mostrar_produtos(self):
        self.limpar_conteudo()
        ProductView(self.conteudo)