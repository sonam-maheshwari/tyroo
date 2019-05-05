from gluon.scheduler import Scheduler
scheduler = Scheduler(db)


def task_add(a, b):
    return a + b



scheduler.queue_task(task_add, pvars=dict(a=1, b=2))
