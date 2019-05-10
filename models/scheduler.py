from gluon.scheduler import Scheduler
import datetime
scheduler = Scheduler(db)



def task_add():
    db.campaign.insert(name='amazon')
    db.commit()
    return 



scheduler.queue_task(task_add, start_time=datetime.datetime.now(),timeout = 60,period=90000 ,repeat=1)
