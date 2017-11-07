#-*- coding: utf-8 -*-
from django.template.loader import get_template, render_to_string
from django.template import RequestContext

from django.shortcuts import render, render_to_response, redirect

from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.db import transaction

from django.http import HttpResponse

from django.core.mail import EmailMessage, send_mail

from django.conf import settings


from constants import *

#from .models import Workorder

from .models import (
    get_erequests_by_efmid, 
    get_erequests_by_creator,
    init_erequest_by_efmid, 
    get_erequest_detail_by_pk,
    delete_erequest_object_by_pk,
    update_erequest_by_efmid,
    update_erequest_review_by_efmid,
    get_proofs_detail_by_pk
)

from .forms import get_form_by_efmid


from datetime import timedelta

def GetLocalTime(t):
    return (t + timedelta(hours=8)).strftime('%Y年%m月%d日 %H时%M分')

def GetLocalDate(t):
    return (t + timedelta(hours=8)).strftime('%Y年%m月%d日')    

from uuid import uuid4 as UUID


def _get_username(request):
    username = request.user.username
    for p in PRIVILUSER:
        if p.name == request.user.username:
            username = p.title
            break
    return username    


def _get_username_cn(name):
    username = name

    userObj = User.objects.get(username=username)

    username_new = ' '.join([userObj.last_name, userObj.first_name])

    username = [username if len(username_new) is 0 else username_new][0]
    return username  

def _get_list_page(l, page, count=10):
    lens = len(l)
    pages = lens/count
    rests = lens%count
    pages += [1 if rests>0 else 0][0]
    if page >= pages:
        #last page

        return l[0:[rests if rests>0 else count][0]]
    else:
        #others
        page = max(page, 1)
        return l[lens-count*page:lens-count*(page-1)]


@login_required
def list_eform(request, *args, **kwargs):
    print "->{0}".format(request.path)

    isUpdated = request.path == "/eforms/UpdateRequest"

    request_identifier = FORM_LIST[0][0]
    requests = []

    block_num = 0
    can_approve = False
    for p in PRIVILUSER:
        if p.pri <20:
            continue

        if p.name == request.user.username:
            can_approve = True
            block_num = p.block_num
            break

    username = _get_username_cn(request.user.username)#_get_username(request)

    can_account = request.user.username == NemasPU.accounting.name #PRIVILUSER[0]['name']
    is_admin = request.user.username == NemasPU.admin.name #PRIVILUSER[5]['name']

    cans =  {
        'can_edit_activity': is_admin,
        'can_approve_activity': can_approve,
        'can_account_activity': can_account or is_admin,
        'can_approve': can_approve,
    }

    pid = request.GET.get('pid', "")
    page = int(request.GET.get('page', 1))
    efm_req = None
    for p,pname in FORM_LIST:

        if isUpdated and p != pid:
            continue

        forms_total = get_erequests_by_efmid(p)

        if not can_approve and not can_account:
            userObj = User.objects.get(username=request.user)
            forms_total = get_erequests_by_creator(p, userObj)        

        if isUpdated:
            paginator = Paginator(forms_total, 10)
            page = min(page, paginator.num_pages)

        ordered_forms = _get_list_page(forms_total, page)        
        ordered_forms = reversed(ordered_forms)        

        tasks = []
        task_undo_size = 0; task_done_size = 0; task_rejected_size = 0;
        for form in ordered_forms:

            #if not can_approve and not can_account and not is_admin and form.creator.username != request.user.username:
            #    continue

            k = {
                'td_num': (page-1) * 10 + len(tasks) + 1,            
                'id': form.id,
                'project_code': form.project_code,
                'status': form.review.status,
                'creator': _get_username_cn(form.creator.username),
                'act_01': int(form.review.act_01),#ACT_LIST[int(form.review.act_01)][1],
                'act_02': int(form.review.act_02),#ACT_LIST[int(form.review.act_02)][1],
                'act_03': int(form.review.act_03),#ACT_LIST[int(form.review.act_03)][1],
                'act_04': int(form.review.act_04),#ACT_LIST[int(form.review.act_04)][1],
                'act_05': int(form.review.act_05),#ACT_LIST[int(form.review.act_04)][1],                
                'creation_date': GetLocalDate(form.creation_date), #form.creation_date + timedelta(hours=8),
                'last_updated': GetLocalTime(form.last_updated), #orm.last_updated + timedelta(hours=8),
                'can_approve2_activity': can_approve,
                'can_view_activity': form.creator.username == request.user.username or can_approve or can_account or is_admin,                
            }

            r = form.review
            act_num = ""
            if request.user.username == NemasPU.supervisor.name:
                act_num = "act_01"
                if k['act_01'] is Acts.approved and k['act_02'] is not Acts.rejected:
                    k['can_approve2_activity'] = False


            elif request.user.username == NemasPU.ma.name:
                act_num = "act_02"
                if k['act_01'] is not Acts.approved or (k['act_02'] is Acts.approved and k['act_03'] is not Acts.rejected):
                    k['can_approve2_activity'] = False


            elif request.user.username == NemasPU.manager.name:
                act_num = "act_03"
                if k['act_02'] is not Acts.approved or (k['act_03'] is Acts.approved and k['act_04'] is not Acts.rejected):
                    k['can_approve2_activity'] = False


            elif request.user.username == NemasPU.vp.name:
                act_num = "act_04"
                if k['act_03'] is not Acts.approved:
                    k['can_approve2_activity'] = False             


            elif request.user.username == NemasPU.accounting.name:
                act_num = "act_05"
                if k['act_04'] is Acts.approved and form.review.status == STATE_LIST[2][0]:
                    k['can_approve2_activity'] = True


            if len(act_num)>0 and act_num != "act_05":
                #priv
                if form.review.status != '1':
                    task_done_size += 1
                elif k[act_num] == 0:
                    task_undo_size += 1
                else:
                    task_done_size += 1
            else:
                #normal
                if form.review.status == "1":
                    task_undo_size += 1
                else:
                    task_done_size += 1

            tasks.append(k)

        efm_req = { 
              #'pid':pid, 'pname':pname, 'num_requests': len(forms_total),
              'pid':p, 'pname':pname, 'num_requests': len(forms_total), 'pu':[p.title for p in PRIVILUSER[1:5]],
              'tasks': tasks, 'task_size':len(tasks), 'task_undo_size':task_undo_size, 'task_done_size':task_done_size, 'task_rejected_size': task_rejected_size,
              'code':UUID().get_hex()
            }
    	requests.append(efm_req)

    page_title = u'工表清單'
    description = u'以在线表单为入口,通过增加多级审核及反馈机制,打通企业外部信息收集和内部电子数据流转过程。'

    review_state = [{'id':a, 'val':b} for a,b in ACT_LIST]
    form_state = [{'id':a, 'val':b} for a,b in STATE_LIST]
    if isUpdated:
        collapsed = True
        return render(request, 'eform_sub_list.html', locals())        
    else:
        return render(request, 'eform_list.html', locals())



class CreateEFormActivity(LoginRequiredMixin, generic.View):

    #Generic view to initiate activity
    def get(self, request, *args, **kwargs):
        #GET request handler for Create operation
        print "({0}.{1}) {2}, {3}, {4}".format(type(self).__name__, CreateEFormActivity.get.__name__, request.path, args, kwargs)
        page_title = ''
        for pid, pname in FORM_LIST:
            if pid == kwargs['pk']:
                page_title = pname
                break

        description = u'表格說明：..............'
        subtitle = u'表單新增'
        username = _get_username_cn(request.user.username)
        form = get_form_by_efmid(kwargs['pk'])
        pid = kwargs['pk']
        if pid == NemasEFMRequest06.EFMID:
            proof_desp = NemasEFMRequest06.proof_description
            proof_cost = NemasEFMRequest06.proof_cost
            proof_file = NemasEFMRequest06.proof_file

        return render(request, 'eform_edit.html', locals())

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        #POST request handler for Create operation
        print "({0}.{1}) {2}, {3}, {4}".format(type(self).__name__, CreateEFormActivity.post.__name__, request.path, args, kwargs)        

        page_title = ''
        for pid, pname in FORM_LIST:
            if pid == kwargs['pk']:
                page_title = pname
        description = u'表格說明：..............'
        subtitle = u'表單新增'


        pid = kwargs['pk']
        if pid == NemasEFMRequest06.EFMID:
            proof_desp = NemasEFMRequest06.proof_description
            proof_cost = NemasEFMRequest06.proof_cost
            proof_file = NemasEFMRequest06.proof_file


        form = get_form_by_efmid(kwargs['pk'], post_data = request.POST)
        if form.is_valid():
            page_title += u" 細目"
            description = u'表格說明：..............'

            userObj = User.objects.get(username=request.user)
            #print "valid =>", form.cleaned_data['project_code'], form.cleaned_data['department'], userObj
            form_renderred = init_erequest_by_efmid(kwargs['pk'], form, creator=userObj, http_request=request)

            username = _get_username_cn(request.user.username)

            form_renderred.creation_date = GetLocalTime(form_renderred.creation_date)
            for a,b in STATE_LIST:
                if a == form_renderred.review.status:
                    form_renderred.status = b
                    break

            requests = []
            requests.append(form_renderred)
            html_content = render_to_string('eform_add_basic.html', locals())
            send_mail(
                u'{0} - {1} ({2})'.format(SYSTEM_TITLE, subtitle, username),
                html_content,
                settings.EMAIL_HOST_USER,
                settings.EMAIL_GROUP_CREATION,
                fail_silently = False,
                html_message=html_content
            )
            return render(request, 'eform_detail_0.html', locals())
        else:
            return render(request, 'eform_edit.html', locals())


class ViewEFormActivity(LoginRequiredMixin, generic.DetailView):

    #Generic view to initiate activity
    def get(self, request, *args, **kwargs):
        #GET request handler for Create operation
        print "({0}.{1}) {2}, {3}, {4}".format(type(self).__name__, ViewEFormActivity.get.__name__, request.path, args, kwargs)        

        page_title = ''
        for pid, pname in FORM_LIST:
            if pid == kwargs['pk']:
                page_title = pname
        description = u'表格檢視：..............'

        form = get_erequest_detail_by_pk(kwargs['pk'], kwargs['tk'])
        requests = [{
                'project_code': form.project_code,
                'status': STATE_LIST[int(form.review.status)][1],
                'creator': form.creator.username,
                'act_01': ACT_LIST[int(form.review.act_01)][1],
                'act_02': ACT_LIST[int(form.review.act_02)][1],
                'act_03': ACT_LIST[int(form.review.act_03)][1],
                'act_04': ACT_LIST[int(form.review.act_04)][1],
                'creation_date': GetLocalTime(form.creation_date), #form.creation_date + timedelta(hours=8),
        }]
        return render(request, 'eform_detail_2.html', locals())



def parseUTF8(s):
    return [s.encode('utf-8') if isinstance(s, unicode) else s][0]    


class ViewBasicEFormActivity(LoginRequiredMixin, generic.DetailView):

    #Generic view to initiate activity
    def get(self, request, *args, **kwargs):
        #GET request handler for Create operation
        print "({0}.{1}) {2}, {3}, {4}".format(type(self).__name__, ViewBasicEFormActivity.get.__name__, request.path, args, kwargs)                

        form = get_erequest_detail_by_pk(kwargs['pk'], kwargs['tk'])
        innerHTMList = [ '<table class="table">' ]
        if kwargs['pk'] == NemasEFMRequest03.EFMID:
            innerHTMList.append('<tr><th scope="row" rowspan="3">{0}</th><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td></tr>'.format(
                parseUTF8(NemasEFMRequest03.creator),
                "姓名",
                parseUTF8(form.creator.last_name),
                parseUTF8(NemasEFMRequest03.creation_date),
                parseUTF8(GetLocalTime(form.creation_date))
            ))

            innerHTMList.append('<tr><th scope="row">{0}</th><td>{1}</td><td>{2}</td><td>{3}</td></tr>'.format(
                parseUTF8(NemasEFMRequest03.department),
                parseUTF8(form.department),
                parseUTF8(NemasEFMRequest03.adv_paydate),            
                ["" if form.adv_paydate in [None, ""] else GetLocalDate(form.adv_paydate) ][0]
            ))

            innerHTMList.append('<tr><td>{0}</td><td colspan="3">{1}</td></tr>'.format(
                parseUTF8(NemasEFMRequest03.project_code),
                parseUTF8(form.project_code),
            ))                

            innerHTMList.append('<tr><th scope="row" rowspan="3">{0}</th><td>{1}</td><td colspan="3">{2}</td></tr>'.format(
                "收款人/單位",
                parseUTF8(NemasEFMRequest03.receiver_name),
                parseUTF8(form.receiver_name),
            ))

            innerHTMList.append('<tr><td>{0}</td><td colspan="3">{1}</td></tr>'.format(
                parseUTF8(NemasEFMRequest03.receiver_account),
                parseUTF8(form.receiver_account),
            ))                     

            innerHTMList.append('<tr><td>{0}</td><td colspan="3">{1}</td></tr>'.format(
                parseUTF8(NemasEFMRequest03.receiver_bank),
                parseUTF8(form.receiver_bank),
            ))                     

            innerHTMList.append('<tr><th scope="row">{0}</th><td colspan="4">{1}</td></tr>'.format(
                parseUTF8(NemasEFMRequest03.adv_payment),
                parseUTF8(form.adv_payment),
            ))                     

            innerHTMList.append('<tr><th scope="row">{0}</th><td colspan="2">{1}</td><th scope="row">{2}</th><td>{3}</td></tr>'.format(
                parseUTF8(NemasEFMRequest03.purpose),
                parseUTF8(PURPOSE_LIST[int(form.purpose)][1]),
                parseUTF8(NemasEFMRequest03.method),
                parseUTF8(PAYWAY_LIST[int(form.method)][1]),            
            ))
        elif kwargs['pk'] == NemasEFMRequest06.EFMID:

            username = form.creator.last_name+form.creator.first_name
            innerHTMList.append('<tr><th>{0}</th><td colspan="3">{1}</td><th>{2}</th><td>{3}</td></tr>'.format(
                    parseUTF8( NemasEFMRequest06.creator), 
                    parseUTF8(username), 
                    parseUTF8(NemasEFMRequest06.project_code), 
                    parseUTF8(form.project_code)
            ))

            innerHTMList.append('<tr><th>{0}</th><td>{1}</td><th>{2}</th><td colspan="3">{3}</td></tr>'.format(
                    parseUTF8( NemasEFMRequest06.department), 
                    parseUTF8(form.department), 
                    parseUTF8(NemasEFMRequest06.creation_date), 
                    parseUTF8(GetLocalTime(form.creation_date))
            ))
            innerHTMList.append('<tr><th colspan="4">{0}</th><th>{1}</th><th>{2}</th></tr>'.format(
                    parseUTF8( NemasEFMRequest06.proof_description), 
                    parseUTF8( NemasEFMRequest06.proof_cost), 
                    parseUTF8( NemasEFMRequest06.proof_file),                                         
            ))

            proofs = get_proofs_detail_by_pk(kwargs['pk'], form)

            for proof in proofs:
                innerHTMList.append('<tr><td colspan="4">{0}</td><td>{1}</td><td><a href="{2}">{3}</a></td></tr>'.format(
                    parseUTF8( proof.description), 
                    parseUTF8( proof.cost), 
                    parseUTF8( proof.proof.url),                                   
                    parseUTF8( ''.join([[proof.proof.original_filename if len(proof.proof.original_filename)<10 else proof.proof.original_filename[:10]][0], '...'])),  
                ))


        innerHTMList.append('</table>')
        repl = "".join(innerHTMList)
        return HttpResponse(repl)


class ViewReviewEFormActivity(LoginRequiredMixin, generic.DetailView):

    #Generic view to initiate activity
    def get(self, request, *args, **kwargs):
        #GET request handler for Create operation
        print "({0}.{1}) {2}, {3}, {4}".format(type(self).__name__, ViewBasicEFormActivity.get.__name__, request.path, args, kwargs)                

        form = get_erequest_detail_by_pk(kwargs['pk'], kwargs['tk'])

        innerHTMList = [ '<table class="table">' ]

        if kwargs['pk'] == NemasEFMRequest03.EFMID:

            innerHTMList.append('<tr><th scope="row" rowspan="3">{0}</th><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td></tr>'.format(
                parseUTF8(NemasEFMRequest03.creator),
                "姓名",
                parseUTF8(form.creator.last_name),
                parseUTF8(NemasEFMRequest03.creation_date),
                parseUTF8(GetLocalTime(form.creation_date))
            ))

            innerHTMList.append('<tr><th scope="row">{0}</th><td>{1}</td><td>{2}</td><td>{3}</td></tr>'.format(
                parseUTF8(NemasEFMRequest03.department),
                parseUTF8(form.department),
                parseUTF8(NemasEFMRequest03.adv_paydate),            
                ["" if form.adv_paydate in [None, ""] else GetLocalDate(form.adv_paydate) ][0]
            ))

            innerHTMList.append('<tr><td>{0}</td><td colspan="3">{1}</td></tr>'.format(
                parseUTF8(NemasEFMRequest03.project_code),
                parseUTF8(form.project_code),
            ))                

            innerHTMList.append('<tr><th scope="row" rowspan="3">{0}</th><td>{1}</td><td colspan="3">{2}</td></tr>'.format(
                "收款人/單位",
                parseUTF8(NemasEFMRequest03.receiver_name),
                parseUTF8(form.receiver_name),
            ))

            innerHTMList.append('<tr><td>{0}</td><td colspan="3">{1}</td></tr>'.format(
                parseUTF8(NemasEFMRequest03.receiver_account),
                parseUTF8(form.receiver_account),
            ))                     

            innerHTMList.append('<tr><td>{0}</td><td colspan="3">{1}</td></tr>'.format(
                parseUTF8(NemasEFMRequest03.receiver_bank),
                parseUTF8(form.receiver_bank),
            ))                     

            innerHTMList.append('<tr><th scope="row">{0}</th><td colspan="4">{1}</td></tr>'.format(
                parseUTF8(NemasEFMRequest03.adv_payment),
                parseUTF8(form.adv_payment),
            ))                     

            innerHTMList.append('<tr><th scope="row">{0}</th><td colspan="2">{1}</td><th scope="row">{2}</th><td>{3}</td></tr>'.format(
                parseUTF8(NemasEFMRequest03.purpose),
                parseUTF8(PURPOSE_LIST[int(form.purpose)][1]),

                parseUTF8(NemasEFMRequest03.method),
                parseUTF8(PAYWAY_LIST[int(form.method)][1]),            
            ))
        elif kwargs['pk'] == NemasEFMRequest06.EFMID:
            username = form.creator.last_name+form.creator.first_name
            innerHTMList.append('<tr><th>{0}</th><td colspan="3">{1}</td><th>{2}</th><td>{3}</td></tr>'.format(
                    parseUTF8( NemasEFMRequest06.creator), 
                    parseUTF8(username), 
                    parseUTF8(NemasEFMRequest06.project_code), 
                    parseUTF8(form.project_code)
            ))

            innerHTMList.append('<tr><th>{0}</th><td>{1}</td><th>{2}</th><td colspan="3">{3}</td></tr>'.format(
                    parseUTF8( NemasEFMRequest06.department), 
                    parseUTF8(form.department), 
                    parseUTF8(NemasEFMRequest06.creation_date), 
                    parseUTF8(GetLocalTime(form.creation_date))
            ))
            innerHTMList.append('<tr><th colspan="4">{0}</th><th>{1}</th><th>{2}</th></tr>'.format(
                    parseUTF8( NemasEFMRequest06.proof_description), 
                    parseUTF8( NemasEFMRequest06.proof_cost), 
                    parseUTF8( NemasEFMRequest06.proof_file),                                         
            ))

            proofs = get_proofs_detail_by_pk(kwargs['pk'], form)

            for proof in proofs:
                innerHTMList.append('<tr><td colspan="4">{0}</td><td>{1}</td><td><a href="{2}">{3}</a></td></tr>'.format(
                    parseUTF8( proof.description), 
                    parseUTF8( proof.cost), 
                    parseUTF8( proof.proof.url),                                   
                    parseUTF8( ''.join([[proof.proof.original_filename if len(proof.proof.original_filename)<10 else proof.proof.original_filename[:10]][0], '...'])),  
                ))


        td_class=["", "bg-success", "bg-danger"]
        innerHTMList.append('<tr class="{2}"><th scope="row">{0}</th><td colspan="5">{1}</td></tr>'.format(
            #parseUTF8(PRIVILUSER[1]['name_title']),
            #PRIVILUSER[1].title,
            parseUTF8(NemasPU.supervisor.title),
            ["" if parseUTF8(form.review.opinion_01) is None else parseUTF8(form.review.opinion_01)][0],
            parseUTF8(td_class[int(form.review.act_01)]),
        ))
        innerHTMList.append('<tr class="{2}"><th scope="row">{0}</th><td colspan="5">{1}</td></tr>'.format(
            #parseUTF8(PRIVILUSER[2]['name_title']),
            parseUTF8(NemasPU.ma.title),
            ["" if parseUTF8(form.review.opinion_02) is None else parseUTF8(form.review.opinion_02)][0],
            parseUTF8(td_class[int(form.review.act_02)]),            
        ))
        innerHTMList.append('<tr class="{2}"><th scope="row">{0}</th><td colspan="5">{1}</td></tr>'.format(
            #parseUTF8(PRIVILUSER[3]['name_title']),
            parseUTF8(NemasPU.manager.title),
            ["" if parseUTF8(form.review.opinion_03) is None else parseUTF8(form.review.opinion_03)][0],
            parseUTF8(td_class[int(form.review.act_03)]),            
        ))                     
        innerHTMList.append('<tr class="{2}"><th scope="row">{0}</th><td colspan="5">{1}</td></tr>'.format(
            #parseUTF8(PRIVILUSER[4]['name_title']),
            parseUTF8(NemasPU.vp.title),
            ["" if parseUTF8(form.review.opinion_04) is None else parseUTF8(form.review.opinion_04)][0],
            parseUTF8(td_class[int(form.review.act_04)]),            
        ))                     
        innerHTMList.append('</table>')
        repl = "".join(innerHTMList)
        return HttpResponse(repl)


class EditEFormActivity(LoginRequiredMixin, generic.View):

    #Generic view to initiate activity
    def get(self, request, *args, **kwargs):
        print "({0}.{1}) {2}, {3}, {4}".format(type(self).__name__, EditEFormActivity.get.__name__, request.path, args, kwargs)                

        page_title = ''
        for pid, pname in FORM_LIST:
            if pid == kwargs['pk']:
                page_title = pname
        description = u'表格說明：..............'
        subtitle = u'表單修改'

        form = get_form_by_efmid(kwargs['pk'], tk = kwargs['tk'])
        return render(request, 'eform_edit.html', locals())

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        #POST request handler for Create operation
        print "({0}.{1}) {2}, {3}, {4}".format(type(self).__name__, EditEFormActivity.post.__name__, request.path, args, kwargs)                

        page_title = ''
        for pid, pname in FORM_LIST:
            if pid == kwargs['pk']:
                page_title = pname
        description = u'表格說明：..............'
        subtitle = u'表單修改'

        form = get_form_by_efmid(kwargs['pk'], tk = kwargs['tk'], post_data = request.POST)
        if form.is_valid():
            page_title += " 細目"
            description = u'表格說明：..............'

            form = update_erequest_by_efmid(kwargs['pk'], kwargs['tk'], form) 

            for a,b in STATE_LIST:
                if a == form.review.status:
                    form.review.status = b
                    break
            requests = [{
                    'project_code': form.project_code,
                    'status':  form.review.status,
                    'creator': form.creator.username,
                    'act_01': ACT_LIST[int(form.review.act_01)][1],
                    'act_02': ACT_LIST[int(form.review.act_02)][1],
                    'act_03': ACT_LIST[int(form.review.act_03)][1],
                    'act_04': ACT_LIST[int(form.review.act_04)][1],
                    'creation_date': GetLocalTime(form.creation_date), #form.creation_date + timedelta(hours=8),
            }]

            return render(request, 'eform_detail_0.html', locals())
        else:
            return render(request, 'eform_edit.html', locals())


class DeleteEFormActivity(LoginRequiredMixin, generic.DetailView):
    #Generic view to initiate activity
    def get(self, request, *args, **kwargs):
        #GET request handler for Create operation
        print "({0}.{1}) {2}, {3}, {4}".format(type(self).__name__, DeleteEFormActivity.get.__name__, request.path, args, kwargs)
        fs = delete_erequest_object_by_pk(kwargs['pk'], kwargs['tk'])
        repl = '<B>ok</B>'
        return HttpResponse(repl)        


class ApproveEFormActivity(LoginRequiredMixin, generic.View):
    #Generic view to initiate activity
    def get(self, request, *args, **kwargs):
        #GET request handler for Create operation
        print "({0}.{1}) {2}, {3}, {4}".format(type(self).__name__, ApproveEFormActivity.get.__name__, request.path, args, kwargs)                                

        opt = request.GET.get('opt', '')
        comment = request.GET.get('comment', '')
        
        subtitle = u'表單审批'
        username = _get_username_cn(request.user.username)        


        if opt not in ['', None]:
            print "YOU GOT A MESSAGE", opt, comment.encode('utf-8')
            form,t = update_erequest_review_by_efmid(kwargs['pk'], kwargs['tk'], request.user.username, opt, comment)

            requests = [{
                    'project_code': form.project_code,
                    'status': STATE_LIST[int(form.review.status)][1],
                    'creator': _get_username_cn(form.creator.username),
                    'creation_date': GetLocalTime(form.creation_date), #form.creation_date + timedelta(hours=8),                    
                    'man': username,
                    'opt': [STATE_LIST[int(opt)] if request.user.username == NemasPU.accounting else ACT_LIST[int(opt)]][0][1],
                    'comment': comment,
                    'approve_date': GetLocalTime(t),
            }]


            html_content = render_to_string('eform_approve_basic.html', locals())
            send_mail(
                u'{0} - {1} ({2})'.format(SYSTEM_TITLE, subtitle, form.project_code),
                html_content,
                settings.EMAIL_HOST_USER,
                settings.EMAIL_GROUP_APPROVAL,
                fail_silently = False,
                html_message=html_content
            )

        return HttpResponse("Roger that.")

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        #POST request handler for Create operation
        print "({0}.{1}) {2}, {3}, {4}".format(type(self).__name__, ApproveEFormActivity.post.__name__, request.path, args, kwargs)                                

        return HttpResponse("Roger that.")


@login_required
def homepage(request):
    return redirect('/eforms/')

"""
test 
"""
@login_required
def test_menu(request):
    food1 = { 'name':'番茄炒蛋', 'price':60, 'comment':'好吃', 'is_spicy':False }
    food2 = { 'name':'蒜泥白肉', 'price':100, 'comment':'人氣推薦', 'is_spicy':True }
    foods = [food1,food2]
    #return render_to_response('menu.html',locals())
    return render(request, 'menu.html', locals())