# app/jobs/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask
import logging

# Importa os jobs registrados
from app.jobs.backup_job import executar_backup
from app.jobs.email_reminder import enviar_lembretes
from app.financeiro.jobs.vencimento_notifier import notificar_vencimentos

scheduler = BackgroundScheduler()
logger = logging.getLogger(__name__)


def iniciar_agendador(app: Flask):
    """
    Inicia o agendador com os jobs definidos e registra no contexto Flask.
    """
    if not scheduler.running:
        scheduler.start()
        logger.info("Agendador de tarefas iniciado.")

        # Job de backup diário às 2h da manhã
        scheduler.add_job(
            func=executar_backup,
            trigger=CronTrigger(hour=2, minute=0),
            id="backup_diario",
            name="Backup diário do banco de dados",
            replace_existing=True
        )

        # Job de lembretes por e-mail a cada hora
        scheduler.add_job(
            func=lambda: enviar_lembretes(app),
            trigger=IntervalTrigger(hours=1),
            id="lembrete_email",
            name="Envio de lembretes por e-mail a cada hora",
            replace_existing=True
        )

        # Job de vencimentos financeiros diário às 8h
        scheduler.add_job(
            func=notificar_vencimentos,
            trigger=CronTrigger(hour=8, minute=0),
            id="notificar_vencimentos",
            name="Notificação de vencimentos financeiros",
            replace_existing=True
        )

        logger.info("Jobs agendados com sucesso.")
