#-*- coding:utf8 -*-

from django import forms

from .models import EFMRequest03, EReview, get_erequest_detail_by_pk



class TestForm_EFMRequest03(forms.ModelForm):

	
	project_code = forms.CharField(error_messages={'required':
		u'{0} 欄不得為空'.format(unicode(EFMRequest03._meta.get_field('project_code').verbose_name))}, 
		widget=forms.TextInput(attrs={'class': "form-control"}), 
		label=unicode(EFMRequest03._meta.get_field('project_code').verbose_name))

	department = forms.CharField(error_messages={'required':
		u'{0} 欄不得為空'.format(unicode(EFMRequest03._meta.get_field('department').verbose_name))}, 	 
		widget=forms.TextInput(attrs={'class': "form-control"}), 
		label=unicode(EFMRequest03._meta.get_field('department').verbose_name))

	receiver_name = forms.CharField(error_messages={'required': 
		u'{0} 欄不得為空'.format(unicode(EFMRequest03._meta.get_field('receiver_name').verbose_name))}, 	 
		widget=forms.TextInput(attrs={'class': "form-control"}), 
		label=unicode(EFMRequest03._meta.get_field('receiver_name').verbose_name))

	receiver_account = forms.CharField(error_messages={'required':
		u'{0} 欄不得為空'.format(unicode(EFMRequest03._meta.get_field('receiver_account').verbose_name))}, 	 
		widget=forms.TextInput(attrs={'class': "form-control"}), 
		label=unicode(EFMRequest03._meta.get_field('receiver_account').verbose_name))

	receiver_bank = forms.CharField(error_messages={'required':
		u'{0} 欄不得為空'.format(unicode(EFMRequest03._meta.get_field('receiver_bank').verbose_name))}, 	 
		widget=forms.TextInput(attrs={'class': "form-control"}), 
		label=unicode(EFMRequest03._meta.get_field('receiver_bank').verbose_name))

	adv_payment = forms.CharField(error_messages={'required':
		u'{0} 欄不得為空'.format(unicode(EFMRequest03._meta.get_field('adv_payment').verbose_name))}, 	 
		widget=forms.TextInput(attrs={'class': "form-control"}), 
		label=unicode(EFMRequest03._meta.get_field('adv_payment').verbose_name))
	

	class Meta:
		model = EFMRequest03
		field_args = {
            "first_name" : {
                "error_messages" : {
                    "required" : "此欄不得為空!"
                }
            }
        }

		#fields = ('title', 'description',)
		fields = '__all__'
		exclude = [
			'title', 'description',
			'creator', 'review', 'creation_date', 'last_updated'
		]
		widgets = {

            #'creator': forms.TextInput(attrs={"type":"hidden"}),
            #'review': forms.TextInput(attrs={"type":"hidden"}),
            #'creation_date': forms.TextInput(attrs={"type":"hidden"}),
            #'last_updated': forms.TextInput(attrs={"type":"hidden"}), 
            
            #'project_code': forms.TextInput(attrs={'class': "form-control"}),           
            #'department': forms.TextInput(attrs={'class': "form-control"}),           
            #'receiver_name': forms.TextInput(attrs={'class': "form-control"}),           
            #'receiver_account': forms.TextInput(attrs={'class': "form-control"}),           
            #'receiver_bank': forms.TextInput(attrs={'class': "form-control"}),
            #'adv_payment': forms.TextInput(attrs={'class': "form-control"}),			

			'adv_paydate': forms.DateInput(attrs={'class': "form-control", 'placeholder': "YYYY-MM-DD"}),

			'unknown_02': forms.DateInput(attrs={'class': "form-control", 'placeholder': "YYYY-MM-DD"}),
            'unknown_01': forms.TextInput(attrs={'class': "form-control"}),
            'unknown_03': forms.TextInput(attrs={'class': "form-control"}),           
            'unknown_04': forms.TextInput(attrs={'class': "form-control"}),           

            'purpose': forms.Select(attrs={'class': "form-control"}),           
            'method': forms.Select(attrs={'class': "form-control"}),           
		}


class TestForm_Review(forms.ModelForm):

	class Meta:
		model = EReview
		#fields = ('title', 'description',)
		fields = '__all__'
		exclude = [
			'opinion_01','opinion_02','opinion_03','opinion_04', 'opinion_05',
			'act_01', 'act_02', 'act_03', 'act_04', 'act_05',
			'rep_time_01', 'rep_time_02', 'rep_time_03', 'rep_time_04', 'rep_time_05',
			'create_time', 'expire_time', 'finish_time',
			'creation_date', 'last_updated',
		]
		widgets = {
            'creator': forms.TextInput(attrs={"type":"hidden"}),
            'status': forms.TextInput(attrs={"type":"hidden"}),
            'efmid': forms.TextInput(attrs={"type":"hidden"}),
		}



def get_form_by_efmid(efmid, tk = None, post_data = None):

	if efmid == '3':
		"""
		if tk is None:
			if post_data is None:
				return TestForm_EFMRequest03()
			else:
				return TestForm_EFMRequest03(post_data)
		else:
			if post_data is None:
				return TestForm_EFMRequest03(instance=get_erequest_detail_by_pk(efmid, tk))
			else:
				return TestForm_EFMRequest03(post_data, instance=get_erequest_detail_by_pk(efmid, tk))
		"""
		return TestForm_EFMRequest03(
			post_data or None, 
			instance = [None if tk is None else get_erequest_detail_by_pk(efmid, tk)][0])
	return None
