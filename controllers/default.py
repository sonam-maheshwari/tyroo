# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
def index():
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def test():
    x=mail.send(to=['sonammaheshwari72@gmail.com'],
          subject='hello',
          # If reply_to is omitted, then mail.settings.sender is used
          reply_to='smsonam.maheshwari@gmail.com',
          message='hi there')

    return x

def createRule():
    import json
    data = db(db.campaign.id>0).select()
    ruleQuery = db((db.campaign_rule.id>0)&
                   (db.campaign_rule.campaign_id == db.campaign.id)).select()
    
    # return BEAUTIFY(data)
    # temp = []
    # for val in data:
    #     temp.append(val)

    return locals()

def saveRule():

    import datetime,json
    name = request.vars.name
    rule = request.vars.rule
    campaign = json.loads(request.vars.campaigns)
    datetimepicker =request.vars.datetimepicker
    status = request.vars.status
    # raise ValueError(requestvars)

    time=datetime.datetime.strptime(datetimepicker, '%H:%M')

    for val in campaign:
        db.campaign_rule.update_or_insert((db.campaign_rule.id == request.vars.id),
                                name=name,
                                campaign_id=val,
                                schedule_time=time,
                                status=status,
                                conditions=rule,
                                next_run_time = datetime.datetime.now().date)
    # raise ValueError(request.vars)

    return "success"

def caampaign_name():
    import json
    data = db(db.caampaign.id>0).select()
    temp = []
    for val in data:
        temp.append(val)
    return json.dumps(temp)

def createData():
    import datetime
    import random 
    data = db(db.campaign.id>0).select()
    hour = request.vars.hour if request.vars.hour else 0
    campaign_ids = [val.id for val in data]
    # materic_list = ['clicks','Installs','impressions','spend']
    for row in campaign_ids:
        # for row1 in materic_list:
        db.campaign_metric.insert(campaign_id=row,
                                    impression=random.randrange(1000,100000, 2),
                                    clicks=random.randrange(1,50, 2),
                                    spend=random.randrange(10,50, 2),
                                    install=random.randrange(1,20, 2),
                                    metric_time= datetime.datetime.now()+datetime.timedelta(hours=hour)

                                    )


def checkCampaign():
    import re
    import datetime

    import smtplib
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

def test():
    import smtplib

    message = """From: From Person <from@fromdomain.com>
    To: To Person <to@todomain.com>
    MIME-Version: 1.0
    Content-type: text/html
    Subject: SMTP HTML e-mail test

    This is an e-mail message to be sent in HTML format

    <b>This is HTML message.</b>
    <h1>This is headline.</h1>
    """

    # try:
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail('sonammaheshwari72@gmail.com', 'sonammaheshwari72@gmail.com', message)         
    print "Successfully sent email"
    # except SMTPException:
    #    print "Error: unable to send email"