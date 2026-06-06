from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from app.models.database import SessionLocal
from app.models.product import Product
from app.services.ai_service import AIService


class PDFReport:

    @staticmethod
    def gerar_pdf():

        db = SessionLocal()
        produtos = db.query(Product).all()
        db.close()

        doc = SimpleDocTemplate("relatorio_inventario.pdf")

        styles = getSampleStyleSheet()
        story = []

        titulo = Paragraph("RELATÓRIO DE INVENTÁRIO COM IA", styles["Title"])
        story.append(titulo)
        story.append(Spacer(1, 20))

        for produto in produtos:

            estado = AIService.prever_stock(produto.quantidade)

            texto = f"ID: {produto.id} | Nome: {produto.nome} | Preço: {produto.preco} | Quantidade: {produto.quantidade} | IA: {estado}"

            p = Paragraph(texto, styles["Normal"])
            story.append(p)
            story.append(Spacer(1, 10))

        doc.build(story)