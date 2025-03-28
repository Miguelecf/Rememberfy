import datetime
from telegram import Update, Bot
from apscheduler.schedulers.background import BackgroundScheduler
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
)
from dotenv import load_dotenv
from tasks import add_task, get_tasks, Task, delete_tasks
import os
import re  # Agregar al inicio del archivo

load_dotenv()

TOKEN = os.getenv("MI_TOKEN")

if TOKEN is None:
    print("No se encontró el token")
    exit()


# Comando /start
async def start(update: Update, context: CallbackContext):
    mensaje = (
        "¡Hola! 👋 ¡Bienvenido/a a Rememberfy recuerda que estoy en un estado de prueba! 🌟\n\n"
        "Por ahora solo puedo recordarte 5 tareas\n\n"
        "Me alegro mucho de tenerte por aquí 🤗\n\n"
        "Mis comandos por ahora son:\n\n"
        "1️⃣/start:  para volver al menu principal\n"
        "2️⃣/nueva_tarea:  para agregar una nueva tarea\n"
        "3️⃣/ver_tareas: para ver tus tareas\n"
        "4️⃣/limpiar_tareas: para limpiar tus tareas\n"
    )
    await update.message.reply_text(mensaje)


# Manejo de mensajes, recordemos que solo tiene que recibir tareas.
async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    try:
        lineas = text.split("\n")

        # Validar número de líneas
        if len(lineas) != 4:
            return await update.message.reply_text(
                "❌ Error: Debes incluir exactamente 4 líneas (título, hora, fecha y descripción)."
            )

        titulo = lineas[0]
        hora = lineas[1]
        fecha = lineas[2]
        descripcion = lineas[3]

        # Validar formato de hora (HH:MM)
        patron_hora = r"^([01]\d|2[0-3]):([0-5]\d)$"
        if not re.match(patron_hora, hora):
            print("Entre en la validacion de hora")
            return await update.message.reply_text(
                "❌ Error: La hora debe estar en formato HH:MM (24h). Ejemplo: 08:30 o 23:45"
            )

        # Validar formato de fecha (dd/mm/aaaa)
        patron_fecha = r"^(0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])/(202[5-9]|20[3-9]\d)$"
        if not re.match(patron_fecha, fecha):
            print("Entre en la validacion de fecha")
            return await update.message.reply_text(
                "❌ Error: La fecha debe estar en formato dd/mm/aaaa y el año debe ser 2025 o posterior. Ejemplo: 25/12/2025"
            )

        user_id = update.effective_user.id
        add_task(titulo, hora, fecha, descripcion, user_id)
        await programar_recordatorio(
            context, update.effective_chat.id, titulo, hora, fecha, descripcion
        )
        await update.message.reply_text(
            f"✅ Tarea agregada exitosamente:\n"
            f"📝 Título: {titulo}\n"
            f"⏰ Hora: {hora}\n"
            f"📅 Fecha: {fecha}\n"
            f"📋 Descripción: {descripcion}"
        )
    except Exception as e:
        print(e)
        await update.message.reply_text(
            "❌ Error al procesar la tarea. Asegúrate de seguir el formato correcto."
        )


# comando /nueva_tarea
async def nueva_tarea(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Por favor, ingresa tu tarea en el siguiente formato:\n\n"
        "📝 Nombre de tarea\n"
        "⏰ Hora (HH:MM) de 24h en hora militar\n"
        "📅 Fecha (dd/mm/aaaa)\n"
        "📋 Descripción"
    )
    # El siguiente mensaje será manejado por handle_message


async def ver_tareas(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    tasks = get_tasks(user_id)
    for task in tasks:
        await update.message.reply_text(
            f"📝Tarea: {task.title}\n⏰Hora: {task.hour}\n📅Fecha: {task.date.strftime('%d/%m/%Y')}\n📋Descripción: {task.description}"
        )


async def limpiar_tareas(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    delete_tasks(user_id)
    await update.message.reply_text("✅ Tareas limpiadas exitosamente")


async def enviar_mensaje_programado(context: CallbackContext):
    job = context.job
    chat_id = job.data["chat_id"]
    titulo = job.data["titulo"]
    hora = job.data["hora"]
    fecha = job.data["fecha"]
    descripcion = job.data["descripcion"]

    mensaje = (
        f"⏰ ¡Recordatorio de tarea!\n"
        f"📝 Título: {titulo}\n"
        f"⏰ Hora: {hora}\n"
        f"📅 Fecha: {fecha}\n"
        f"📋 Descripción: {descripcion}"
    )

    await context.bot.send_message(chat_id=chat_id, text=mensaje)


async def programar_recordatorio(
    context: CallbackContext,
    chat_id: int,
    titulo: str,
    hora: str,
    fecha: str,
    descripcion: str,
):
    try:
        # Convertir fecha y hora a datetime
        fecha_hora = datetime.datetime.strptime(f"{fecha} {hora}", "%d/%m/%Y %H:%M")
        ahora = datetime.datetime.now()

        # Calcular segundos hasta el envío
        segundos_hasta_envio = (fecha_hora - ahora).total_seconds()

        if segundos_hasta_envio > 0:
            context.job_queue.run_once(
                enviar_mensaje_programado,
                segundos_hasta_envio,
                data={
                    "chat_id": chat_id,
                    "titulo": titulo,
                    "hora": hora,
                    "fecha": fecha,
                    "descripcion": descripcion,
                },
            )

    except ValueError as e:
        print(f"Error al programar recordatorio: {e}")


# Configuración del bot
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("nueva_tarea", nueva_tarea))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler("ver_tareas", ver_tareas))
    app.add_handler(CommandHandler("limpiar_tareas", limpiar_tareas))

    print("Bot corriendo...")
    app.run_polling()


if __name__ == "__main__":
    main()
