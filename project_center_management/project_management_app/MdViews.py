from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from project_management_app.models import CustomUser, Department,DepartmentName,Projects,Employee,SessionYearModel,FeedBackEmployee,FeedBackDepartment,LeaveReportEmployee,LeaveReportDepartment,Attendence,AttendenceReport
from django.core.files.storage import FileSystemStorage
from project_management_app.forms import AddStudentForm,EditEmployeeForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json





def admin_home(request):
    employee_count=Employee.objects.all().count()
    department_count=Department.objects.all().count()
    departmentname_count=DepartmentName.objects.all().count()
    project_count=Projects.objects.all().count()


    departmentname_all=DepartmentName.objects.all()
    departmentname_list=[]
    project_count_list=[]
    employee_count_list_in_departmentname=[]
    for departmentname in departmentname_all:
        projects=Projects.objects.filter(departmentname_id=departmentname.id).count()
        employees=Employee.objects.filter(departmentname_id=departmentname.id).count()
        departmentname_list.append(departmentname.department_name)
        project_count_list.append(projects)

        employee_count_list_in_departmentname.append(employees)

    projects_all=Projects.objects.all()
    project_list=[]
    employee_count_list_in_project=[]
    for project in projects_all:
        departmentname=DepartmentName.objects.get(id=project.departmentname_id.id)
        employee_count1=Employee.objects.filter(departmentname_id=departmentname.id).count()
        project_list.append(project.project_name)
        employee_count_list_in_project.append(employee_count1)


    return render(request,"md_template/home_content.html",{"employee_count":employee_count,"department_count":department_count,"departmentname_count":departmentname_count,"project_count":project_count,"departmentname_list":departmentname_list,"project_count_list":project_count_list,"employee_count_list_in_departmentname":employee_count_list_in_departmentname,"project_list":project_list,"employee_count_list_in_project":employee_count_list_in_project})

def add_department(request):
    departmentname=DepartmentName.objects.all()
    return render(request,"md_template/add_department_template.html",{"departmentname": departmentname})

def add_department_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_department')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        # departmentname_id=request.POST.get('department_name')

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            user.department.address = address
            # departmentname_obj=DepartmentName.objects.get(id=departmentname_id)
            # user.departmentname.departmentname_id=departmentname_obj
            user.save()
            messages.success(request, "Department Added Successfully!")
            return redirect('/add_department')
        except:
            messages.error(request, "Failed to Add Department!")
            return redirect('/add_department')

def add_departmentname(request):
    return render(request,"md_template/add_departmentname_template.html")

def add_departmentname_save(request):
    if request.method!='POST':
        return HttpResponseRedirect("Method Not Allowed")
    else:
        department_name=request.POST.get('department_name')
        try:
            department_name_model=DepartmentName(department_name=department_name)
            department_name_model.save()
            messages.success(request, "Successfully Added New Department!")
            return redirect('/add_departmentname')
        except:
            messages.error(request, "Failed to Add Department!")
            return redirect('/add_departmentname')


def add_employee(request):
    form=AddStudentForm()
    # sessions=SessionYearModel.objects.all()
    return render(request,'md_template/add_employee_template.html',{"form":form})


def add_employee_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_employee')
    else:
        # form=AddStudentForm(request.POST,request.FILES)
        form=AddStudentForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            session_year_id= form.cleaned_data['session_year_id']
            departmentname_id=form.cleaned_data['department_name']
            gender=form.cleaned_data['gender']

            # profile_pic=request.FILES['profile_pic']
            # fs=FileSystemStorage()
            # filename=fs.save(profile_pic.name,profile_pic)
            # profile_pic_url=fs.url(filename)

            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
                user.employee.address = address
                departmentname_obj=DepartmentName.objects.get(id=departmentname_id)
                user.employee.departmentname_id=departmentname_obj
                sesson_year=SessionYearModel.objects.get(id=session_year_id)
                user.employee.session_year_id=sesson_year
                user.employee.gender=gender
                # user.employee.profile_pic=profile_pic_url
                user.save()
                messages.success(request, "Employee Added Successfully!")
                return redirect('/add_employee')
            except:
                messages.error(request, "Failed to Add Employye!")
                return redirect('/add_employee')
        else:
            form=AddStudentForm(request.POST,request.FILES)
            return render(request,'md_template/add_employee_template.html',{"form":form})


def add_project(request):
    departmentname=DepartmentName.objects.all()
    department=CustomUser.objects.filter(user_type='2')
    context = {
        "department": department,
        "departmentname": departmentname
    }
    return render(request,"md_template/add_project_template.html",context)

def add_project_save(request):
    if request.method!='POST':
        messages.error(request, "Invalid Method ")
        return redirect('add_project')
    else:
        project_name=request.POST.get("project_name")
        project_details=request.POST.get("project_details")
        departmentname_id=request.POST.get("department_name")
        departmentname=DepartmentName.objects.get(id=departmentname_id)
        department_id=request.POST.get("department")
        department=CustomUser.objects.get(id=department_id)
        try:
            projects=Projects(project_name=project_name,departmentname_id=departmentname,department_id=department,project_details=project_details)
            projects.save()
            messages.success(request, "Project Added Successfully!")
            return redirect('/add_project')
        except:
            messages.error(request, "Failed to Add Project!")
            return redirect('/add_project')


def manage_department(request):
    department=Department.objects.all()
    context = {
        "department": department,
        
    }
    return render(request,"md_template/manage_department_template.html",context)


def manage_employee(request):
    employee=Employee.objects.all()
    session=SessionYearModel.objects.all()
    context = {
        "employee": employee,
        "session":session
        
    }
    return render(request,"md_template/manage_employee_template.html",context)


def manage_departmentname(request):
    departmentname=DepartmentName.objects.all()
    context = {
        "departmentname": departmentname,
        
    }
    return render(request,"md_template/manage_departmentname_template.html",context)


def manage_project(request):
    project=Projects.objects.all()
    context = {
        "project": project,
        
    }
    return render(request,"md_template/manage_project_template.html",context)


def edit_department(request,department_id):
    department=Department.objects.get(admin=department_id)
    return render(request,"md_template/edit_department_template.html",{"department": department,"id":department_id})

def edit_department_save(request):
    if request.method!='POST':
        messages.error(request, "Invalid Method ")
        return redirect('edit_department')
    else:
        department_id=request.POST.get("department_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.get(id=department_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            department_model=Department.objects.get(admin=department_id)
            department_model.address=address
            department_model.save()
            messages.success(request, "Department Edited Successfully!")
            return redirect('/edit_department/'+department_id)
        except:
            messages.error(request, "Failed to Edit Department!")
            return redirect('/edit_department/'+department_id)
        
def edit_employees(request,employee_id):
    request.session['employee_id']=employee_id
    employee=Employee.objects.get(admin=employee_id)
    form=EditEmployeeForm()
    form.fields['email'].initial=employee.admin.email
    form.fields['first_name'].initial=employee.admin.first_name
    form.fields['last_name'].initial=employee.admin.last_name
    form.fields['username'].initial=employee.admin.username
    form.fields['address'].initial=employee.address
    form.fields['department_name'].initial=employee.departmentname_id.id
    form.fields['gender'].initial=employee.gender
    form.fields['session_year_id'].initial=employee.session_year_id.id
    # form.fields['profile_pic'].initial=employee.profile_pic
    context = {
        "id":employee_id,
        "form":form,
        "username":employee.admin.username
    }
    return render(request,"md_template/edit_employee_template.html",context)

def edit_employee_save(request):
    if request.method!='POST':
        messages.error(request, "Invalid Method ")
        return redirect('edit_employees')
    else:
        employee_id=request.session.get("employee_id")
        if employee_id==None:
            return redirect("/manage_employee")


        form=EditEmployeeForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            session_year_id=form.cleaned_data['session_year_id']
            departmentname_id=form.cleaned_data['department_name']
            gender=form.cleaned_data['gender']

            # if request.FILES.get('profile_pic',False):
            #     profile_pic=request.FILES['profile_pic']
            #     fs=FileSystemStorage()
            #     filename=fs.save(profile_pic.name,profile_pic)
            #     profile_pic_url=fs.url(filename)
            # else:
            #     profile_pic_url=None
            try:
                user=CustomUser.objects.get(id=employee_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()
                del request.session['employee_id']
            
                employee=Employee.objects.get(admin=employee_id)
                employee.address=address
                session_year=SessionYearModel.objects.get(id=session_year_id)
                employee.session_year_id=session_year
                employee.gender=gender
                departmentname=DepartmentName.objects.get(id=departmentname_id)
                employee.departmentname_id=departmentname
                # employee.profile_pic=profile_pic_url
                employee.save()
                messages.success(request, "Employee Edited Successfully!")
                return redirect('/edit_employees/'+employee_id)
            except:
                messages.error(request, "Failed to Edit Employee!")
                return redirect('/edit_employees/'+employee_id)

        else:
            form=EditEmployeeForm(request.POST)
            employee=Employee.objects.get(admin=employee_id)
            return render(request,"md_template/edit_employee_template.html",{"form":form,"id":employee_id,"username":employee.admin.username})


def edit_project(request,project_id):
    project=Projects.objects.get(id=project_id)
    departmentname=DepartmentName.objects.all()
    department=CustomUser.objects.filter(user_type=2)
    project=Projects.objects.get(id=project_id)
    return render(request,"md_template/edit_project_template.html",{"project":project,"departmentname":departmentname,"department":department,"id":project_id})



def edit_project_save(request):
    if request.method!='POST':
        messages.error(request, "Invalid Method ")
        return redirect('edit_project')
    else:
        project_id=request.POST.get("project_id")
        project_name=request.POST.get("project_name")
        project_details=request.POST.get("project_details")
        department_id=request.POST.get("department")
        departmentname_id=request.POST.get("department_name")
        try:
            project=Projects.objects.get(id=project_id)
            project.project_name=project_name
            project.project_details=project_details
            department=CustomUser.objects.get(id=department_id)
            project.department_id=department
            departmentname=DepartmentName.objects.get(id=departmentname_id)
            project.departmentname_id=departmentname
            project.save()
            messages.success(request, "Project Edited Successfully!")
            return redirect('/edit_project/'+project_id)
        except:
            messages.error(request, "Failed to Edit Project!")
            return redirect('/edit_project/'+project_id)

def edit_departmentname(request,departmentname_id):
    departmentname=DepartmentName.objects.get(id=departmentname_id)
    return render(request,"md_template/edit_departmentname_template.html",{"departmentname" : departmentname,"id":id})

def edit_departmentname_save(request):
    if request.method!='POST':
        messages.error(request, "Invalid Method ")
        return redirect('edit_employees')
    else:
        departmentname_id=request.POST.get("departmentname_id")
        department_name=request.POST.get("department_name")
        try:
            departmentname=DepartmentName.objects.get(id=departmentname_id)
            departmentname.department_name=department_name
            departmentname.save()
            messages.success(request, "Department Name Edited Successfully!")
            return redirect('/edit_departmentname/'+departmentname_id)
        except:
            messages.error(request, "Failed to Edit Department Name!")
            return redirect('/edit_departmentname/'+departmentname_id)


def manage_session(request):
    return render(request,"md_template/manage_session_template.html")

def add_session_save(request):
    if request.method!="POST":
        return HttpResponseRedirect("manage_session")
    else:
        session_start_year=request.POST.get("session_start")
        session_end_year=request.POST.get("session_end")
        try:
            sessionyear=SessionYearModel(session_start_year=session_start_year,session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Session Added Successfully!")
            return redirect('/manage_session')
        except:
            messages.error(request, "Failed to Add Session!")
            return redirect('/manage_session')


def department_feedback_message(request):
    feedbacks=FeedBackDepartment.objects.all()
    return render(request,"md_template/department_feedback_template.html",{"feedbacks":feedbacks})

@csrf_exempt
def department_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")


    try:
        feedback=FeedBackDepartment.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()

        return HttpResponse("True")
        # messages.success(request, "Project Edited Successfully!")
        # return redirect('/edit_project/'+project_id)
    except:
        return HttpResponse("True")
        # messages.error(request, "Failed to Edit Project!")
        # return redirect('/edit_project/'+project_id)    



def employee_feedback_message(request):
    feedbacks=FeedBackEmployee.objects.all()
    return render(request,"md_template/employee_feedback_template.html",{"feedbacks":feedbacks})


@csrf_exempt
def employee_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")


    try:
        feedback=FeedBackEmployee.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()

        return HttpResponse("True")
        # messages.success(request, "Project Edited Successfully!")
        # return redirect('/edit_project/'+project_id)
    except:
        return HttpResponse("True")
        # messages.error(request, "Failed to Edit Project!")
        # return redirect('/edit_project/'+project_id)



def employee_leave_view(request):
    leaves=LeaveReportEmployee.objects.all()
    return render(request,"md_template/employee_leave_view.html",{"leaves":leaves})


def employee_approve_leave(request,leave_id):
    leave=LeaveReportEmployee.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return redirect("employee_leave_view")
    

def employee_disapproved_leave(request,leave_id):
    leave=LeaveReportEmployee.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return redirect("employee_leave_view")


def department_leave_view(request):
    leaves=LeaveReportDepartment.objects.all()
    return render(request,"md_template/department_leave_view.html",{"leaves":leaves})


def department_approve_leave(request,leave_id):
    leave=LeaveReportDepartment.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return redirect("department_leave_view")
    

def department_disapproved_leave(request,leave_id):
    leave=LeaveReportDepartment.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return redirect("department_leave_view")



def admin_view_attendance(request):
    projects=Projects.objects.all()
    session_year_id=SessionYearModel.objects.all()
    return render(request,"md_template/admin_view_attendance.html",{"projects":projects,"session_year_id":session_year_id})


@csrf_exempt
def admin_get_attendance_dates(request):
    project=request.POST.get("project")
    session_year_id=request.POST.get("session_year_id")

    project_obj=Projects.objects.get(id=project)
    session_year_obj=SessionYearModel.objects.get(id=session_year_id)
    attendance=Attendence.objects.filter(projects_id=project_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendence_date":str(attendance_single.attendence_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)

@csrf_exempt
def admin_get_attendance_employee(request):
    attendence_date=request.POST.get("attendence_date")

    attendance=Attendence.objects.get(id=attendence_date)

    attendance_data=AttendenceReport.objects.filter(attendence_id=attendance)
    
    list_data=[]
    for employee in attendance_data:
        data_small={"id":employee.employee_id.admin.id,"name":employee.employee_id.admin.first_name+"  "+employee.employee_id.admin.last_name,"ststus":employee.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)


@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse("True")
    else:
        return HttpResponse("False")



@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse("True")
    else:
        return HttpResponse("False")



def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"md_template/admin_profile.html",{"user":user})


def admin_profile_save(request):
    if request.method!='POST':
        return redirect("admin_profile")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("change_password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully!")
            return redirect('/admin_profile')
        except:
            messages.error(request, "Failed to Update Profile!")
            return redirect('/admin_profile')



def delete_department(request,department_id):
    department=Department.objects.get(admin=department_id)
    department.delete()
    return redirect("manage_department")


def delete_employee(request,employee_id):
    employee=Employee.objects.get(admin=employee_id)
    employee.delete()
    return redirect("manage_employee")


def delete_departmentname(request,departmentname_id):
    departmentname=DepartmentName.objects.get(id=departmentname_id)
    departmentname.delete()
    return redirect("manage_departmentname")


def delete_project(request,projects_id):
    project=Projects.objects.get(id=projects_id)
    project.delete()
    return redirect("manage_project")