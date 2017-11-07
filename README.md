# eforms


Simple Approval check system (Complex Chinese)


My first try to implement a simple and easy-to-use approval checker system with django MVC framework and bootstrap in 3 weeks after work. Most of my codes is written and referred from [ActivFlow](https://github.com/faxad/ActivFlow) and slight change for bussiness reasons. 


Installation guide:
1. ceate virtual environment for developement
> virtualenv [MY_PROJECT]
2. activate virtual env
> soruce ./sy_viewflow/bin/activate
3. install all dependencies
> pip install -r requirements.txt
4. Make a copy of this 
5. run it
> python manage.py runserver [MY_IP:MY_PORT]


## ■ Update 2017/11/06
1. move naming class NemasXX to constants.py
2. implement pagination function and re-index request in form-list request
3. add new request cost_reimbursement form
4. install [django-form-utils](https://github.com/carljm/django-form-utils)
5. some tips to upload file [an step-by-step explanation for uploading files](https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html), also [hwo to cope with InmemoryUploadFile issues](https://stackoverflow.com/questions/20635332/how-to-programmatically-fill-or-create-filer-fields-image-filerimagefield)

## ■ Update 2017/10/30

NOTE: 
1. have to modify SMTP parameters on setting.py for specified need
2. have to add MAIL_ACCOUNT on send_mail function on views.py

TO-DO-List:
1. add more forms and requests based on current structure
2. optimize source codes (it's terribly ugly)
3. may add more intelligent search functions


