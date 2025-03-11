import logging
import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from flask import Flask
import threading

# Configuration du bot
API_TOKEN = "7928221931:AAHPDAS0vrdc8pZGTXlRHJJlDdhySz-uYy0"  # Remplace par ton token Telegram
bot = Bot(token=API_TOKEN)

# Dispatcher et Router
dp = Dispatcher()
router = Router()
dp.include_router(router)  # Ajout du routeur dans le Dispatcher

# Gestion des messages contenant une vidéo ou une image
@router.message()
async def handle_media_message(message: Message):
    # Vérifier si le message contient une vidéo ou une image
    if message.video or message.photo:
        # Supprimer l'ancien message
        await message.delete()
        
        # Texte formaté
        formatted_text = "Titre -\nGenre -"
        
        # Envoyer le nouveau message avec la vidéo ou l'image
        if message.video:
            await message.answer_video(video=message.video.file_id, caption=formatted_text)
        elif message.photo:
            await message.answer_photo(photo=message.photo[-1].file_id, caption=formatted_text)

# Création du serveur Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Le bot Telegram est en cours d'exécution."

def run_flask():
    app.run(host='0.0.0.0', port=6045)

async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)

async def main():
    await on_startup()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    threading.Thread(target=run_flask, daemon=True).start()
    asyncio.run(main())