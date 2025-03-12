import os
import logging
import asyncio
import threading
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from flask import Flask

# Configuration du bot
API_TOKEN = os.getenv("API_TOKEN")  # Remplace par ton token Telegram
if not API_TOKEN:
    raise ValueError("❌ API_TOKEN manquant ! Vérifie tes variables d'environnement.")

bot = Bot(token=API_TOKEN)

# Dispatcher et Router
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)  # Ajout du routeur dans le Dispatcher

# Gestion des messages contenant une vidéo ou une image
@router.message()
async def handle_media_message(message: Message):
    try:
        if message.video or message.photo:
            await message.delete()
            formatted_text = "Titre -\nGenre -"

            if message.video:
                await message.answer_video(video=message.video.file_id, caption=formatted_text)
            elif message.photo:
                await message.answer_photo(photo=message.photo[-1].file_id, caption=formatted_text)

    except Exception as e:
        logging.error(f"❌ Erreur lors du traitement du message : {e}")

# Création du serveur Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Le bot Telegram est en cours d'exécution."

def run_flask():
    try:
        port = int(os.getenv("PORT", 6045))  # Port dynamique fourni par Render
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        logging.error(f"❌ Erreur lors du démarrage de Flask : {e}")

async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)

async def main():
    try:
        await on_startup()
        logging.info("✅ Bot Telegram lancé avec succès !")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logging.error(f"❌ Erreur dans l'exécution du bot : {e}")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Démarrer Flask dans un thread
    threading.Thread(target=run_flask, daemon=True).start()

    # Démarrer l'event loop
    asyncio.run(main())
