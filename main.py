import customtkinter as ctk

from app.models.database import engine, Base, SessionLocal
from app.models.user import User

from app.views.login_view import LoginView


Base.metadata.create_all(bind=engine)

db = SessionLocal()

admin = db.query(User).filter(User.username == "admin").first()

if not admin:
    novo_admin = User(
        username="admin",
        password="1234"
    )
    db.add(novo_admin)
    db.commit()

db.close()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Sistema Inteligente de Inventário")
app.geometry("1000x650")

LoginView(app)

app.mainloop()