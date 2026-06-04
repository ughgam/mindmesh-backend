import trafilatura
import fitz 
from sqlalchemy.orm import Session
import models

from vector_store import index_article_in_vector_db

def extract_web_content(url: str) -> str:
    downloaded = trafilatura.fetch_url(url)
    if downloaded:
        return trafilatura.extract(downloaded) 
    return None

def extract_pdf_content(file_bytes: bytes) -> str:
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def process_web_extraction_background(article_id: int, user_id: int, url: str, db: Session):
    extracted_text = extract_web_content(url)
    
    if extracted_text:
        article = db.query(models.Article).filter(models.Article.id == article_id).first()
        if article:
            article.extracted_text = extracted_text
            db.commit()
            
            index_article_in_vector_db(
                article_id=article.id, 
                text=extracted_text,
                user_id=user_id, 
                title=article.title, 
                url=article.url
            )
            
def process_pdf_extraction_background(article_id: int, user_id: int, file_bytes: bytes, db: Session):
    extracted_text = extract_pdf_content(file_bytes)

    if extracted_text:
        article = db.query(models.Article).filter(models.Article.id == article_id).first()
        if article:
            article.extracted_text = extracted_text
            db.commit()

            index_article_in_vector_db(
                article_id=article.id,
                user_id=user_id,
                text=extracted_text,
                title=article.title,
                url=article.url
            )
