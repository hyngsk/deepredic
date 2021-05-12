import logging
from gunicorn import glogging


class CustomGunicornLogger(glogging.Logger):
    def setup(self, cfg):
        super().setup(cfg)

        # Add filters to Gunicorn logger
        logger = logging.getLogger("gunicorn.access")
        logger.handlers = logger.handlers
        logger.setLevel(logger.level)
        logger.addFilter(HealthCheckFilter())


class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        print(record.name, record.msg, record.levelname)
        return 'ELB-HealthChecker' not in record.getMessage()


logger_class = CustomGunicornLogger
loglevel = 'DEBUG'
accesslog = 'access_log'
