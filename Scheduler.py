from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler

from datautil import add_EMAs, data_setup
from upbit import Upbit


class Scheduler:
    _instance = None

    @classmethod
    def _getInstance(cls):
        return cls._instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls._instance = cls(*args, **kargs)
        cls.instance = cls._getInstance
        return cls._instance

    def __init__(self):
        self.upbit = Upbit()
        self.sched = BackgroundScheduler()
        self.sched.start()
        self.job_id = ''
        data_setup()

    def __del__(self):
        self.shutdown()

    def shutdown(self):
        self.sched.shutdown()

    def kill_scheduler(self, job_id):
        try:
            self.sched.remove_job(job_id)
        except JobLookupError as err:

            return "fail to stop Scheduler: {err}".format(err=err)

    def Every1Hour(self):
        filename = 'Every1Hour.csv'
        with open(filename) as f:
            df = self.upbit.get_1hour_candle('KRW-BTC')
            df.to_csv(filename, index=True, mode='a', encoding='utf-8', header=False)
        add_EMAs(filename)

    def Every15Minutes(self):
        filename = 'Every15Minutes.csv'
        with open(filename) as f:
            df = self.upbit.get_15minutes_candle('KRW-BTC')
            df.to_csv(filename, index=True, mode='a', encoding='utf-8', header=False)
        add_EMAs(filename)

    def scheduler(self, type, job_id):
        if type == 'cron':
            if job_id == 'Every1Hour':
                self.sched.add_job(self.Every1Hour,
                                   type,
                                   hour='*',  # 매 시간
                                   minute='0',  # 0분
                                   second='5',  # 5초에
                                   id=job_id)
                return "{type} Scheduler Start".format(type=type)
            elif job_id == 'Every15Minutes':
                self.sched.add_job(self.Every15Minutes,
                                   type,
                                   hour='*',  # 매 시간
                                   minute='*/15',  # 15분마다
                                   second='5',  # 5초에
                                   id=job_id)
                return "{type} Scheduler Start".format(type=type)
