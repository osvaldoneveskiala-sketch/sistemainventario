import customtkinter as ctk

from app.models.database import SessionLocal
from app.models.user import User
from app.views.dashboard_view import DashboardView


class LoginView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.master = master

        self.pack(fill="both", expand=True)

        # Título
        titulo = ctk.CTkLabel(
            self,
            text="Login do Sistema",
            font=("Arial", 28, "bold")
        )

        titulo.pack(pady=30)

        # Campo username
        self.username_entry = ctk.CTkEntry(
            self,
            placeholder_text="Username",
            width=300
        )

        self.username_entry.pack(pady=10)

        # Campo password
        self.password_entry = ctk.CTkEntry(
            self,
            placeholder_text="Password",
            show="*",
            width=300
        )

        self.password_entry.pack(pady=10)

        # Botão login
        login_button = ctk.CTkButton(
            self,
            text="Entrar",
            command=self.login
        )

        login_button.pack(pady=20)

        # Mensagem
        self.message = ctk.CTkLabel(
            self,
            text=""
        )

        self.message.pack(pady=10)

    def login(self):

        username = self.username_entry.get()
        password = self.password_entry.get()

        db = SessionLocal()

        user = db.query(User).filter(
            User.username == username,
            User.password == password
        ).first()

        if user:

            self.destroy()

            DashboardView(self.master)

        else:

            self.message.configure(
                text="Username ou password incorretos!"
            )

        db.close()