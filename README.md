# eforms
========

Simple Approval check system (Complex Chinese)

## ■ Update 2017/10/30

My first try to implement a simple and easy-to-use approval checker system with django MVC framework and bootstrap in 3 weeks after work. Most of my codes is written and referred from [ActivFlow](https://github.com/faxad/ActivFlow) and slight change for bussiness reasons. 


Installation guide:
1. ceate virtual environment for developement
> environment [MY_PROJECT]
2. activate virtual env
> soruce ./sy_viewflow/bin/activate
3. install all dependencies
> pip install -r requirements.txt
4. Make a copy of this 
5. run it
> python manage.py runserver [MY_IP:MY_PORT]

NOTE: 
1. have to modify SMTP parameters on setting.py for specified need
2. have to add MAIL_ACCOUNT on send_mail function on views.py

TO-DO-List:
1. optimize source codes (it's terribly ugly)
2. add more forms and requests
2. may add more intelligent search functions.
