#-*- coding:utf8 -*-

from django import forms

from .models import (
	EFMRequest03, EReview, 
	EFMRequest05, EFMRequest06,
	get_erequest_detail_by_pk)

from constants import *



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

class TestForm_EFMRequest05(forms.ModelForm):
	
	project_code = forms.CharField(error_messages={'required':
		u'{0} 欄不得為空'.format(unicode(EFMRequest03._meta.get_field('project_code').verbose_name))}, 
		widget=forms.TextInput(attrs={'class': "form-control"}), 
		label=unicode(EFMRequest03._meta.get_field('project_code').verbose_name))

	department = forms.CharField(error_messages={'required':
		u'{0} 欄不得為空'.format(unicode(EFMRequest03._meta.get_field('department').verbose_name))}, 	 
		widget=forms.TextInput(attrs={'class': "form-control"}), 
		label=unicode(EFMRequest03._meta.get_field('department').verbose_name))

	car_plate = forms.CharField(error_messages={'required': 
		u'{0} 欄不得為空'.format(NemasEFMRequest05.car_plate )}, 	 
		widget=forms.TextInput(attrs={'class': "form-control"}), 
		label=unicode(NemasEFMRequest05.car_plate))

	car_companion = forms.CharField(error_messages={'required': 
		u'{0} 欄不得為空'.format(NemasEFMRequest05.car_companion )}, 	 
		widget=forms.TextInput(attrs={'class': "form-control"}), 
		label=unicode(NemasEFMRequest05.car_companion))

	car_reason = forms.CharField(error_messages={'required': 
		u'{0} 欄不得為空'.format(NemasEFMRequest05.car_reason )}, 	 
		widget=forms.TextInput(attrs={'class': "form-control"}), 
		label=unicode(NemasEFMRequest05.car_reason))

	car_place = forms.CharField(error_messages={'required': 
		u'{0} 欄不得為空'.format(NemasEFMRequest05.car_place )}, 	 
		widget=forms.TextInput(attrs={'class': "form-control"}), 
		label=unicode(NemasEFMRequest05.car_place))

	car_mile = forms.CharField(error_messages={'required': 
		u'{0} 欄不得為空'.format(NemasEFMRequest05.car_mile )}, 	 
		widget=forms.TextInput(attrs={'class': "form-control"}), 
		label=unicode(NemasEFMRequest05.car_mile))
	
	car_go_time_plan = forms.CharField(error_messages={'required': 
		u'{0} 欄不得為空'.format(NemasEFMRequest05.car_go_time_plan )}, 	 
		widget=forms.DateInput(attrs={'class': "form-control", 'placeholder': "YYYY-MM-DD HH:mm"}), 		
		label=unicode(NemasEFMRequest05.car_go_time_plan))

	car_back_time_plan = forms.CharField(error_messages={'required': 
		u'{0} 欄不得為空'.format(NemasEFMRequest05.car_back_time_plan )},
		widget=forms.DateInput(attrs={'class': "form-control", 'placeholder': "YYYY-MM-DD HH:mm"}), 		
		label=unicode(NemasEFMRequest05.car_back_time_plan))

	car_go_time_real = forms.CharField(error_messages={'required': 
		u'{0} 欄不得為空'.format(NemasEFMRequest05.car_go_time_real )}, 	 
		widget=forms.DateInput(attrs={'class': "form-control", 'placeholder': "YYYY-MM-DD HH:mm"}), 		
		label=unicode(NemasEFMRequest05.car_go_time_real))

	car_back_time_real = forms.CharField(error_messages={'required': 
		u'{0} 欄不得為空'.format(NemasEFMRequest05.car_back_time_real )}, 	 
		widget=forms.DateInput(attrs={'class': "form-control", 'placeholder': "YYYY-MM-DD HH:mm"}), 		
		label=unicode(NemasEFMRequest05.car_back_time_real))

	class Meta:
		model = EFMRequest05
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
		}


class TestForm_EFMRequest06(forms.ModelForm):
	
	project_code = forms.CharField(error_messages={'required':
		u'{0} 欄不得為空'.format(unicode(EFMRequest03._meta.get_field('project_code').verbose_name))}, 
		widget=forms.TextInput(attrs={'class': "form-control"}), 
		label=unicode(EFMRequest03._meta.get_field('project_code').verbose_name))

	department = forms.CharField(error_messages={'required':
		u'{0} 欄不得為空'.format(unicode(EFMRequest03._meta.get_field('department').verbose_name))}, 	 
		widget=forms.TextInput(attrs={'class': "form-control"}), 
		label=unicode(EFMRequest03._meta.get_field('department').verbose_name))


	"""
	def __init__(self, *args, **kwargs):
		super(TestForm_EFMRequest06, self).__init__(*args, **kwargs)
		for x in range(10):
			file = {
				'cost_{0}'.format(x) : forms.DecimalField(
					#error_messages={'required': u'{0} 欄不得為空'.format(EFMRequest06.proof_cost)},
					#widget=forms.NumberInput(attrs={'style': 'width:12ch',}),
					widget=forms.NumberInput(attrs={'class': 'form-control'}),					
					label=NemasEFMRequest06.proof_cost,
					max_digits=10,
					decimal_places=2)
				,
    			'file_{0}'.format(x) : forms.FileField(
					label=NemasEFMRequest06.proof_file,

					widget=forms.ClearableFileInput(
						attrs={'multiple': False}))
    			,
				'desp_{0}'.format(x) : forms.CharField(
					#error_messages={'required': u'{0} 欄不得為空'.format(EFMRequest06.proof_description)}, 
					widget=forms.Textarea(attrs={'class':'form-control', 'rows':4, 'cols':50}), 
					label=NemasEFMRequest06.proof_description)
			}
			self.fields.update(file)
	"""
	class Meta:
		model = EFMRequest06
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

	if efmid == NemasEFMRequest03.EFMID:
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

	elif efmid == NemasEFMRequest05.EFMID:
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
		return TestForm_EFMRequest05(
			post_data or None, 
			instance = [None if tk is None else get_erequest_detail_by_pk(efmid, tk)][0])


	elif efmid == NemasEFMRequest06.EFMID:
		return TestForm_EFMRequest06(
			post_data or None, 
			instance = [None if tk is None else get_erequest_detail_by_pk(efmid, tk)][0])		

	else:
		return None
