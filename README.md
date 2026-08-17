# Rememberfy 🤖

Bot de Telegram para guardar tareas y enviarte recordatorios en la fecha y hora que indiques.

## Características

- Crear tareas desde Telegram con formato simple.
- Ver tareas registradas por usuario.
- Limpiar todas tus tareas guardadas.
- Programar recordatorios automáticos con `job_queue`.
- Persistencia local con SQLite + SQLAlchemy.

## Tecnologías

- Python 3
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- SQLAlchemy
- APScheduler
- python-dotenv
- SQLite

## Requisitos

- Python 3.10+ (recomendado)
- Token de bot de Telegram (BotFather)

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/Miguelecf/Rememberfy.git
cd Rememberfy
```

2. Crea y activa un entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Instala dependencias:

```bash
pip install -r requirements.txt
```

## Configuración

Crea un archivo `.env` en la raíz del proyecto:

```env
MI_TOKEN=tu_token_de_telegram
```

## Ejecutar el bot

```bash
python bot.py
```

Si todo está bien configurado, verás:

```text
Bot corriendo...
```

## Uso en Telegram

### Comandos disponibles

- `/start` → Muestra bienvenida y comandos.
- `/nueva_tarea` → Te pide una tarea con formato de 4 líneas.
- `/ver_tareas` → Lista tus tareas actuales.
- `/limpiar_tareas` → Elimina todas tus tareas.

### Formato de nueva tarea

Cuando uses `/nueva_tarea`, envía exactamente 4 líneas:

```text
Nombre de tarea
HH:MM
dd/mm/aaaa
Descripción
```

Ejemplo:

```text
Comprar regalo
19:30
25/12/2026
Buscar regalo para cumpleaños
```

## Estructura del proyecto

```text
.
├── bot.py          # Lógica principal del bot y handlers de Telegram
├── tasks.py        # Modelo Task y operaciones de base de datos
├── requirements.txt
└── README.md
```

## Notas

- La base de datos `rememberfy.db` se crea automáticamente.
- El proyecto está en estado de prueba y puede evolucionar.
