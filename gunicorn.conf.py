import logging
from gunicorn import glogging


class CustomGunicornLogger(glogging.Logger):

    def setup(self, cfg):
        super().setup(cfg)

        # Add filters to Gunicorn logger
        logger = logging.getLogger("gunicorn.access")
        logger.addFilter(HealthCheckFilter())


class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        logging.info(record.name, record.msg, record.levelname)
        return 'GET /' not in record.getMessage()


logger_class = CustomGunicornLogger
loglevel = 'DEBUG'
errorlog = '/deepredic/error_log.txt'
accesslog = '/deepredic/access_log.txt'