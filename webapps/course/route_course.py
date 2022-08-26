# ######################### #
#     Tuwaiq Dashboard      #
#       Courses Page        #
# ######################### #

from fastapi import APIRouter,Request, Response, Depends, status
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta

from db.repository.login import get_current_user_from_token
from db.models.AdminUser import AdminUser
from routers.admin import get_admin
from routers.course import get_all_courses, create, get_courses_by_id, edit_course, get_by_member
from routers.submission import get_submission_by_course_id, get_approved_by_course_id, get_ordered_by_score, edit_submission
from schemas.Course import CourseCreate
from schemas.Submission import SubmissionRow
from webapps.base import templates

router = APIRouter(include_in_schema=False)

@router.get("/courses")
async def courses(request:Request, auth: AdminUser = Depends(get_current_user_from_token)):
    courses = get_all_courses()
    for course in courses:
        course.submissions = len(get_submission_by_course_id(course.id))
        course.instructor = get_admin(course.created_by_id).username
        course.status = ["Closed", "Opened"][int(course.status)]
    return templates.TemplateResponse("courses/courses.html", {
        "request": request,
        "courses": courses
        })

@router.get("/courses{member_id}")
async def courses(request:Request, member_id: int, auth: AdminUser = Depends(get_current_user_from_token)):
    courses = get_by_member(member_id)
    for course in courses:
        course.submissions = len(get_submission_by_course_id(course.id))
        course.instructor = get_admin(course.created_by_id).username
        course.status = ["Closed", "Opened"][int(course.status)]
    return templates.TemplateResponse("courses/courses.html", {
        "request": request,
        "courses": courses
        })

@router.get("/ccourse")
async def create_courses(request:Request, auth: AdminUser = Depends(get_current_user_from_token)):
    return templates.TemplateResponse("courses/create_course.html", {
        "request": request,
        })

@router.post("/ccourse")
async def create_courses(response: Response, request:Request, auth: AdminUser = Depends(get_current_user_from_token)):
    form = await request.form()
    name = form.get("name")
    des = form.get("description")
    req = form.get("requirement")
    sdate = datetime.strptime(form.get("sdate"), f'%Y-%m-%d')
    duration = int(form.get("duration"))
    num_trainees = int(form.get("trainees"))
    diff = form.get("difficulty")
    end_date = sdate + timedelta(days= duration)

    course = CourseCreate(name = name,
    description= des,
    requirements= req, 
    start_date= sdate, 
    end_date = end_date,
    num_trainees = num_trainees,
    diffculty= diff)
    create(course, auth)
    
    return RedirectResponse(url="/courses", status_code=status.HTTP_302_FOUND)

@router.get("/trainess{id}")
async def trainess(request:Request, id: int, auth: AdminUser = Depends(get_current_user_from_token)):
    course = get_courses_by_id(id)
    submissions = get_approved_by_course_id(id)
    list = []
    for submission in submissions:
            list.append(SubmissionRow(
                id = submission.id,
                course_name = course.name,
                name = submission.name,
                email = submission.email,
                phone = submission.phone,
                linkedin = submission.linkedin,
                github = submission.github,
                score = submission.score,
                Approved = ["Pending", "Approved"][int(submission.Approved)],
                date = submission.date
                ))
    return templates.TemplateResponse("courses/trainees.html", {
        "request": request,
        "course_name": course.name,
        "submissions": list
        })

@router.get("/validate{id}")
async def validate(request:Request, id: int, auth: AdminUser = Depends(get_current_user_from_token)):
    course = get_courses_by_id(id)
    course.status = False
    edit_course(course.id, course)
    submissions = get_ordered_by_score(id)[:course.num_trainees]
    list = []
    for submission in submissions:
        edit_submission(submission.id, True)
        list.append(SubmissionRow(
            id = submission.id,
            course_name = course.name,
            name = submission.name,
            email = submission.email,
            phone = submission.phone,
            linkedin = submission.linkedin,
            github = submission.github,
            score = submission.score,
            Approved = ["Pending", "Approved"][int(submission.Approved)],
            date = submission.date
            ))
    return templates.TemplateResponse("courses/trainees.html", {
        "request": request,
        "course_name": course.name,
        "submissions": list
    })