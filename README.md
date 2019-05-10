# tyroo
## Requirements

# Install python


# Install web2py - 

1. cd /home and mkdir www-dev

2. cd www-dev
3. wget http://www.web2py.com/examples/static/web2py_src.zip
4. unzip -x web2py_src.zip
5.cd web2py and run sudo python web2py.py

### Once the server is started, web2py will redirect to the screen with following mentioned URL − http://127.0.0.1:8000/


## Steps - 

###### Front End URL -
	Sign up page -
		http://127.0.0.1:8000/tyroo/default/user/login
	You can add a new rule for campaign from below rule-
	1.http://127.0.0.1:8000/tyroo/default/createRule 

###### create dummy data for campaign -

	http://127.0.0.1:8000/tyroo/default/createData?hour=2

## database structure - 
	You can check database structure here
	http://127.0.0.1:8000/tyroo/appadmin
	Give admin access - 
	 insert a new record from auth_group
	 insert auth_membership 

## Schduler Service Run - 
	cd /home/www-dev/web2py
	run sudo python web2py.py -K tyroo


## Main file
	1. controllers/default.py
	2.views/default/createRule.html
	3.models/db.py
	4.models/scheduler.py





   