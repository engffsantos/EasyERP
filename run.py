# run.py

from app import create_app
from app.jobs.scheduler import iniciar_agendador
import os

app = create_app()

# Ativa o agendador de tarefas se não estiver em modo de teste
if not app.config.get("TESTING", False):
    iniciar_agendador(app)

if __name__ == "__main__":
    # Modo desenvolvimento
    host = os.getenv("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_RUN_PORT", 5000))
    debug = app.config.get("DEBUG", True)

    app.run(host=host, port=port, debug=debug)
