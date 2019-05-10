from gluon.scheduler import Scheduler
import datetime
scheduler = Scheduler(db)



# def task_add():
#     db.campaign.insert(name='amazon')
#     db.commit()
#     return 


def checkCampaign():
    import re
    import datetime
    ruleQuery = db((db.campaign_rule.id>0)&
                   (db.campaign_rule.campaign_id == db.campaign.id)&(db.campaign_rule.next_run_time != None)).select()

    activeQuery = ruleQuery.find(lambda x:x.campaign_rule.status == 'activated')
    deactivateQuery = ruleQuery.find(lambda x:(x.campaign_rule.status == 'dectivated')&
                                                ((x.campaign_rule.next_run_time <= datetime.datetime.now().date())&
                                                    ((x.campaign_rule.next_run_time >= datetime.datetime.now().time()))))
    if deactivateQuery:
        deactivateList = [y.campaign_rule.id for y in deactivateQuery]
        db(db.campaign_rule.id.belongs(deactivateList)).update(status = 'activated')
        db.commit()
    # return BEAUTIFY(activeQuery)

    if activeQuery:
        tempList = []
        for val in activeQuery:
            matricQuery = db((db.campaign_metric.campaign_id == val.campaign.id)).select(orderby=~db.campaign_metric.id).first()
            impressions = matricQuery.impression
            clicks = matricQuery.clicks
            spend = matricQuery.spend
            install = matricQuery.install
            eCPM = spend * 1000 / impressions
            eCPC = spend / clicks
            eCPI =spend / install
            conditions = val.campaign_rule.conditions

            try:
                ans =  eval(conditions)
                tempList.append(val.campaign_rule.id)
                if ans:
                    db(db.campaign_rule.id == val.campaign.id).update(status='deactivate',
                                                                    next_run_time=datetime.datetime.now().date()+datetime.timedelta(days=1)
                                                                    )

                    db.commit()
                    mail.send(to=['sonammaheshwari72@gmail.com'],
                                      subject='hello',
                                      reply_to='smsonam.maheshwari@gmail.com',
                                      message=' Stop campaign')
            except:
                pass

    return 1



scheduler.queue_task(checkCampaign, prevent_drift=True,start_time=datetime.datetime.now(),timeout = 60,period=9000 ,repeat=1)
