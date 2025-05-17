from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
import requests
from bs4 import BeautifulSoup

TOKEN = "7621865459:AAHlugoxS7hoozEPQaSlqtgG4Vr2Y337xEw"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Menga kitob nomini yuboring, men sizga PDF qidirib topaman.")

async def search_books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    results = []

    # PDFDrive qidiruv
    url1 = f"https://www.pdfdrive.com/search?q={query.replace(' ', '+')}&searchin=en"
    res1 = requests.get(url1)
    soup1 = BeautifulSoup(res1.content, "html.parser")
    books = soup1.select(".file-right > h2 > a")
    for book in books[:5]:
        title = book.get_text(strip=True)
        link = "https://www.pdfdrive.com" + book["href"]
        results.append(("PDFDrive: " + title, link))

    # Ziyo.uz qidiruv
    url2 = f"https://ziyo.uz/uz/search?q={query.replace(' ', '+')}"
    res2 = requests.get(url2)
    soup2 = BeautifulSoup(res2.content, "html.parser")
    zbooks = soup2.select("div.col-md-9 h4 > a")
    for book in zbooks[:5]:
        title = book.get_text(strip=True)
        link = "https://ziyo.uz" + book["href"]
        results.append(("Ziyo.uz: " + title, link))

    if not results:
        await update.message.reply_text("Afsus, kitob topilmadi.")
        return

    buttons = [
        [InlineKeyboardButton(text=title, url=url)]
        for title, url in results
    ]

    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("Quyidagilardan tanlang:", reply_markup=reply_markup)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_books))
    app.run_polling()

if __name__ == "__main__":
    main()
