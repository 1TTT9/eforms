#-*- coding: utf-8 -*-

from __future__ import unicode_literals


from django.utils import timezone

from django.db import models

#from account.models import User
from django.contrib.auth.models import User

from constants import (
    FORM_LIST, STATE_LIST, ACT_LIST, PURPOSE_LIST, PAYWAY_LIST, Nemas)

from filer.fields.image import FilerImageField
#from filer.fields.file import FilerFileField


from uuid import uuid4 as UUID


"""
 model abstraction layer
"""

class AbstractEntity(models.Model):
    """Common attributes for all models"""
    creation_date = models.DateTimeField(u'創建日期', auto_now_add=True)
    last_updated = models.DateTimeField(u'上次更新', auto_now=True)

    class Meta(object):
        abstract = True

    @property
    def class_meta(self):
        """Returns class meta"""
        return self._meta

    @property
    def title(self):
        """Returns entity title"""
        return self.__class__.__name__

    @property
    def module_label(self):
        """Returns module label"""
        return self.class_meta.app_label

    @property
    def code0(self):
        """Returns a unique code"""
        return "{0}-{1}-{2}".format(
            self.class_meta.app_label,
            self.title,
            self.id)

    def __unicode__(self):
        """Returns ID"""
        return str(self.id)


class NemasEFMRequest03:

    title =  u'标题' 
    description =  u'描述'   

    project_code =  u'工代' 
    department   = u'部門'
    creator = u'创建者'
    review = u'審查'
    creation_date = u'創建日期'
    last_updated  = u'上次更新' 

    adv_payment = u'請款金額'
    purpose = u'用途'
    method = u'付款方式'
    adv_paydate =  u'付款日期'

    receiver_name = u'姓名/公司名稱'
    receiver_account = u'帳號'
    receiver_bank = u'開戶行地址'


    unknown_01 = u'實收金額'
    unknown_02 = u'報銷日期'
    unknown_03 = u'報銷抵銷金額'
    unknown_04 = u'歸還金額'


class EFMRequest03(models.Model):

    title = models.TextField(u'标题',blank=True, null=True,max_length=30)
    description = models.TextField(u'描述',blank=True, null=True)    

    project_code = models.TextField(u'工代', max_length=50)
    department   = models.TextField(u'部門',blank=True, null=True, max_length=50)
    creator = models.ForeignKey(User, verbose_name=u'创建者')    
    review = models.ForeignKey('EReview', verbose_name=u'審查')
    creation_date = models.DateTimeField(u'創建日期', auto_now_add=True)
    last_updated  = models.DateTimeField(u'上次更新', auto_now=True) 

    adv_payment = models.CharField(u'請款金額', max_length=50)
    purpose = models.CharField(u'用途',default='0',max_length=2, choices=PURPOSE_LIST)
    method = models.CharField(u'付款方式',default='0',max_length=2, choices=PAYWAY_LIST)
    adv_paydate =  models.DateTimeField(u'付款日期',blank=True, null=True)

    receiver_name = models.TextField(u'姓名/公司名稱', max_length=50)
    receiver_account = models.TextField(u'帳號', max_length=50)
    receiver_bank = models.TextField(u'開戶行地址', max_length=100)


    unknown_01 = models.CharField(u'實收金額',blank=True, null=True, max_length=50)
    unknown_02 = models.DateTimeField(u'報銷日期',blank=True, null=True, max_length=50)
    unknown_03 = models.CharField(u'報銷抵銷金額',blank=True, null=True, max_length=50)
    unknown_04 = models.CharField(u'歸還金額',blank=True, null=True, max_length=50)            

    class Meta:
        verbose_name = u'請款單'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __unicode__(self):
        return self.id

class SubEFM06(models.Model):

    efm06 = models.ForeignKey('EFMRequest06', verbose_name=u'費用報銷單', null=True)
    description = models.TextField(u'摘要', blank=True, max_length=100)
    cost = models.FloatField(default=0.0)
    proof = FilerImageField(null=True, blank=True)

    class Meta:
        verbose_name = u'明細'
        verbose_name_plural = verbose_name
        ordering = ['id']


class EFMRequest06(models.Model):

    title = models.TextField(u'标题',max_length=30)
    description = models.TextField(u'描述')

    project_code = models.TextField(u'工代', max_length=50)
    department   = models.TextField(u'部門', max_length=50)
    creator = models.ForeignKey(User, verbose_name=u'创建者')    
    review = models.ForeignKey('EReview', verbose_name=u'審查')
    creation_date = models.DateTimeField(u'創建日期', auto_now_add=True)
    last_updated  = models.DateTimeField(u'上次更新', auto_now=True) 

    class Meta:
        verbose_name = u'抬頭'
        verbose_name_plural = verbose_name
        ordering = ['id']


    def __unicode__(self):
        return self.project_code


class NemasEReview:
    title = u'标题'
    description = u'描述'

    status = u'状态'

    opinion = u'审批意见'

    act = u'状态'

    rep_time = u'回覆时间'

    create_time = u'创建时间'
    expire_time = u'期望时间'
    finish_time = u'完成时间'


class EReview(models.Model):

    title = models.TextField(u'标题',blank=True, null=True,max_length=30)
    description = models.TextField(u'描述', null=True,blank=True)

    status = models.CharField(u'状态',default='0',max_length=5, choices=STATE_LIST)

    opinion_01 = models.TextField(u'审批意见01',blank=True, null=True,max_length=100)
    opinion_02 = models.TextField(u'审批意见02',blank=True, null=True,max_length=100)
    opinion_03 = models.TextField(u'审批意见03',blank=True, null=True,max_length=100)
    opinion_04 = models.TextField(u'审批意见04',blank=True, null=True,max_length=100)

    opinion_05 = models.TextField(u'會計意见04',blank=True, null=True,max_length=100)

    act_01 = models.CharField(u'状态01',default='0',max_length=2, choices=ACT_LIST)
    act_02 = models.CharField(u'状态02',default='0',max_length=2, choices=ACT_LIST)
    act_03 = models.CharField(u'状态03',default='0',max_length=2, choices=ACT_LIST)
    act_04 = models.CharField(u'状态04',default='0',max_length=2, choices=ACT_LIST)      

    act_05 = models.CharField(u'状态05',default='0',max_length=2, choices=ACT_LIST)

    rep_time_01 = models.DateTimeField(u'回覆时间01',blank=True, null=True)
    rep_time_02 = models.DateTimeField(u'回覆时间02',blank=True, null=True)
    rep_time_03 = models.DateTimeField(u'回覆时间03',blank=True, null=True)
    rep_time_04 = models.DateTimeField(u'回覆时间04',blank=True, null=True)

    rep_time_05 = models.DateTimeField(u'回覆时间05',blank=True, null=True)    

    create_time = models.DateTimeField(u'创建时间',auto_now_add=True)
    expire_time = models.DateTimeField(u'期望时间',blank=True, null=True)
    finish_time = models.DateTimeField(u'完成时间',auto_now=True, null=True)

    class Meta:
        verbose_name = u'審查'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __unicode__(self):
        return str(self.id)


def init_erequest_by_efmid(efmid, fo, creator):

    if efmid == '3':
        r = EReview(status='1')
        r.save()
        f= EFMRequest03(
            project_code=fo.cleaned_data['project_code'],
            department=fo.cleaned_data['department'],

            adv_payment=fo.cleaned_data['adv_payment'],
            adv_paydate=fo.cleaned_data['adv_paydate'],
            purpose=fo.cleaned_data['purpose'],
            method=fo.cleaned_data['method'],

            receiver_name=fo.cleaned_data['receiver_name'],
            receiver_account=fo.cleaned_data['receiver_account'],
            receiver_bank=fo.cleaned_data['receiver_bank'],

            unknown_01=fo.cleaned_data['unknown_01'],
            unknown_02=fo.cleaned_data['unknown_02'],
            unknown_03=fo.cleaned_data['unknown_03'],
            unknown_04=fo.cleaned_data['unknown_04'],
            
            creator=creator,
            review=r
        )
        f.save()
        return f
    else:
        return None
    
def update_erequest_by_efmid(efmid, tk, fo):

    if efmid == '3':
        f = get_erequest_detail_by_pk(efmid, tk)
        f.project_code=fo.cleaned_data['project_code']
        f.department=fo.cleaned_data['department']

        f.adv_payment=fo.cleaned_data['adv_payment']
        f.adv_paydate=fo.cleaned_data['adv_paydate']
        f.purpose=fo.cleaned_data['purpose']
        f.method=fo.cleaned_data['method']

        f.receiver_name=fo.cleaned_data['receiver_name']
        f.receiver_account=fo.cleaned_data['receiver_account']
        f.receiver_bank=fo.cleaned_data['receiver_bank']

        f.unknown_01=fo.cleaned_data['unknown_01']
        f.unknown_02=fo.cleaned_data['unknown_02']
        f.unknown_03=fo.cleaned_data['unknown_03']
        f.unknown_04=fo.cleaned_data['unknown_04']
        f.save()
        return f

    else:
        return None


def update_erequest_review_by_efmid(efmid, pid, man, opt, comment):

    if efmid == '3':
        e = EFMRequest03.objects.get(id=pid)
        r = e.review
        t =  timezone.now()

        if opt == ACT_LIST[2][0]:
            r.status = STATE_LIST[3][0]
        elif opt == ACT_LIST[1][0] and man not in [Nemas.vp, Nemas.accounting]:
            r.status = STATE_LIST[1][0]


        if man == Nemas.supervisor:
            r.act_01 = opt
            r.opinion_01 = comment
            r.rep_time_01 =t

            r.act_02 = "0"
            r.rep_time_02 = t

        elif man == Nemas.ma:
            r.act_02 = opt
            r.opinion_02 = comment
            r.rep_time_02 = t

            r.act_03 = "0"
            r.rep_time_03 = t

        elif man == Nemas.manager:
            r.act_03 = opt
            r.opinion_03 = comment
            r.rep_time_03 = t 

            r.act_04 = "0"
            r.rep_time_04 = t 

        elif man == Nemas.vp:
            r.act_04 = opt
            r.opinion_04 = comment
            r.rep_time_04 = t 

            if opt == ACT_LIST[1][0]:
                r.status = STATE_LIST[2][0]

            r.act_05 = "0"
            r.rep_time_05 = t 

        elif man == Nemas.accounting:
            #r.act_05 = opt
            #r.opinion_05 = comment
            r.rep_time_05 = t 

            r.status = opt


        r.save()
        return e, t
    else:
        return None


def delete_erequest_object_by_pk(efmid, pid):

    if efmid == '3':
        e = EFMRequest03.objects.get(id=pid)
        e.review.delete()
        return e.delete()
    else:
        return None



def get_erequest_detail_by_pk(efmid, pid):

    if efmid == '3':
        return EFMRequest03.objects.get(id=pid)
    else:
        return None


def get_erequests_by_efmid(efmid=''):

    if efmid == '3':
        ss =  EFMRequest03.objects.all()
        return ss


    elif efmid == '6':
        return EFMRequest06.objects.all()
    return ERequest.objects.all()
    """
    if len(filtered_name)==0:
        return ERequest.objects.all()
    return ERequest.objects.filter(efmid=filtered_name)
    """