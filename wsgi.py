import logging

from Scheduler import Scheduler
from app import app

if __name__ == "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info(Scheduler.instance().scheduler('cron', "Every1Hour"))
    app.logger.info(Scheduler.instance().scheduler('cron', "Every15Minutes"))

    app.run()
