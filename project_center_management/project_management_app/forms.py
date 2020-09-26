from django import forms
from project_management_app.models import DepartmentName,SessionYearModel


class DateInput(forms.DateInput):
    input_type= "date"

class AddStudentForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off"}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off"}))
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))

    try:
        departmentname_list=[]
        departmentname=DepartmentName.objects.all()
        

        for departmentname in departmentname:
            small_departmentname=(departmentname.id,departmentname.department_name)
            departmentname_list.append(small_departmentname)
    except:
        departmentname_list=[]

    
    try:
        session_list=[]
        sessions=SessionYearModel.objects.all()
        
        for ses in sessions:
            small_ses=(ses.id,str(ses.session_start_year)+"    TO    "+str(ses.session_end_year))
            session_list.append(small_ses)
    except:
        session_list=[]
        
    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )

    department_name=forms.ChoiceField(label="Department Name",choices=departmentname_list,widget=forms.Select(attrs={"class":"form-control"}))
    gender=forms.ChoiceField(label="Gender",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id=forms.ChoiceField(label="Session Year",widget=forms.Select(attrs={"class":"form-control"}),choices=session_list)
    # profile_pic=forms.FileField(label="Profile Pic",widget=forms.FileInput(attrs={"class":"form-control"}))



class EditEmployeeForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off"}))
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))


    departmentname_list=[]
    # try:
    departmentname=DepartmentName.objects.all()
    for departmentnam in departmentname:
        small_departmentname=(departmentnam.id,departmentnam.department_name)
        departmentname_list.append(small_departmentname)
    # except:
    #     departmentname_list=[]

    session_list=[]
    try:
        sessions=SessionYearModel.objects.all()
        for ses in sessions:
            small_ses=(ses.id,str(ses.session_start_year)+"    TO    "+str(ses.session_end_year))
            session_list.append(small_ses)
    except:
        session_list=[]

    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )

    department_name=forms.ChoiceField(label="Department Name",choices=departmentname_list,widget=forms.Select(attrs={"class":"form-control"}))
    gender=forms.ChoiceField(label="Gender",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id=forms.ChoiceField(label="Session Year",widget=forms.Select(attrs={"class":"form-control"}),choices=session_list)
    # profile_pic=forms.FileField(label="Profile Pic",widget=forms.FileInput(attrs={"class":"form-control"}),required=False)