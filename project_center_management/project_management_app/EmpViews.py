from django.shortcuts import render,redirect
from project_management_app.models import Employee,DepartmentName,Projects,LeaveReportEmployee,FeedBackEmployee,CustomUser,Attendence,AttendenceReport
from django.contrib import messages
from django.http import HttpResponse
import datetime



def employee_home(request):
    employee_obj=Employee.objects.get(admin=request.user.id)
    attendance_total=AttendenceReport.objects.filter(employee_id=employee_obj).count()
    attendance_present=AttendenceReport.objects.filter(employee_id=employee_obj,status=True).count()
    attendance_absent=AttendenceReport.objects.filter(employee_id=employee_obj,status=False).count()
    departmentname=DepartmentName.objects.get(id=employee_obj.departmentname_id.id)
    total_project=Projects.objects.filter(departmentname_id=departmentname).count()

    project_name=[]
    data_present=[]
    data_absent=[]
    project_data=Projects.objects.filter(departmentname_id=employee_obj.departmentname_id)
    for project in project_data:
        attendance=Attendence.objects.filter(projects_id=project.id)
        attendance_present_count=AttendenceReport.objects.filter(attendence_id__in=attendance,status=True,employee_id=employee_obj.id).count()
        attendance_absent_count=AttendenceReport.objects.filter(attendence_id__in=attendance,status=False,employee_id=employee_obj.id).count()
        project_name.append(project.project_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)



    return render(request,"employee_template/employee_home_template.html",{"total_attendance":attendance_total,"absent_attendance":attendance_absent,"present_attendance":attendance_present,"total_project":total_project,"data_name":project_name,"data1":data_present,"data2":data_absent})


def employee_view_attendence(request):
    employee=Employee.objects.get(admin=request.user.id)
    departmentname=employee.departmentname_id
    projects=Projects.objects.filter(departmentname_id=departmentname)
    return render(request,"employee_template/employee_view_attendance.html",{"projects":projects})



def employee_view_attendence_post(request):
    project_id=request.POST.get("project")
    start_date=request.POST.get("start_date")
    end_date=request.POST.get("end_date")

    start_data_parse=datetime.datetime.strptime(start_date,'%Y-%m-%d').date()
    end_data_parse=datetime.datetime.strptime(end_date,'%Y-%m-%d').date()
    project_obj=Projects.objects.get(id=project_id)
    user_object=CustomUser.objects.get(id=request.user.id)
    emp_obj=Employee.objects.get(admin=user_object)
    attendance=Attendence.objects.filter(attendence_date__range=(start_data_parse,end_data_parse),projects_id=project_obj)
    attendance_reports=AttendenceReport.objects.filter(attendence_id__in=attendance,employee_id=emp_obj)

    for attendance_report in attendance_reports:
        print("DAte : "+str(attendance_report.attendence_id.attendence_date),"Status :"+str(attendance_report.status))

    return render(request,"employee_template/employee_attendance_data.html",{"attendance_reports":attendance_reports})

    

def employee_apply_leave(request):
    employee_obj=Employee.objects.get(admin=request.user.id)
    leave_date=LeaveReportEmployee.objects.filter(employee_id=employee_obj)
    return render(request,"employee_template/employee_apply_leave.html",{"leave_date":leave_date})


def employee_apply_leave_save(request):
    if request.method!='POST':
        return redirect("employee_apply_leave")
    else:
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get("leave_reason")

        employee_obj=Employee.objects.get(admin=request.user.id)
        try:
            leave_report=LeaveReportEmployee(employee_id=employee_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied For Leave")
            return redirect('/employee_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave!")
            return redirect('/employee_apply_leave')



def employee_feedback(request):
    employee_id=Employee.objects.get(admin=request.user.id)
    feedback_data=FeedBackEmployee.objects.filter(employee_id=employee_id)
    return render(request,"employee_template/employee_feedback.html",{"feedback_data":feedback_data})



def employee_feedback_save(request):
    if request.method!='POST':
        return redirect("employee_feedback")

    else:
        feedback_msg=request.POST.get("feedback_msg")

        employee_obj=Employee.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackEmployee(employee_id=employee_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return redirect('/employee_feedback')
        except:
            messages.error(request, "Failed to Sent Feedback!")
            return redirect('/employee_feedback')



def employee_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"employee_template/employee_profile.html",{"user":user})


def employee_profile_save(request):
    if request.method!='POST':
        return redirect("employee_profile")
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
            return redirect('/employee_profile')
        except:
            messages.error(request, "Failed to Update Profile!")
            return redirect('/employee_profile')