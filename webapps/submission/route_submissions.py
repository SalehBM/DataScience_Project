# ######################### #
#     Tuwaiq Dashboard      #
#     Submission Pages      #
# ######################### #

from fastapi import APIRouter, Request, Depends
from datetime import date, timedelta
import re

from webapps.base import templates
from db.repository.login import get_current_user_from_token
from db.models.AdminUser import AdminUser
from routers.submission import create, get_all_submissions, delete_submission, get_submission_by_course_id, get_submission_by_member_id
from routers.course import get_courses_by_id, get_all_incoming_courses
from schemas.Submission import SubmissionRow, SubmissionCreate
import internal.status_codes 
 
router = APIRouter(include_in_schema=False)

@router.get("/submissions")
async def submissions(request:Request, auth: AdminUser = Depends(get_current_user_from_token)):
    submissions = get_all_submissions()
    list = []
    for submission in submissions:
        course = get_courses_by_id(id=submission.course_id)

        if course is None:
            delete_submission(submission.id)
        else:
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
                date = submission.date,
            ))
    return templates.TemplateResponse("pages/submissions.html", {
        "request": request,
        "submissions": list
        })

@router.get("/submissions{course_id}")
async def course_submission(request:Request, course_id: int, auth: AdminUser = Depends(get_current_user_from_token)):
    submissions =  get_submission_by_course_id(course_id)
    list = []
    for submission in submissions:
        course = get_courses_by_id(id=submission.course_id)

        if course is None:
            delete_submission(submission.id)
        else:
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
                date = submission.date,
            ))
    return templates.TemplateResponse("pages/submissions.html", {
        "request": request,
        "submissions": list
        })

@router.get("/apply")
async def apply(request:Request):
    courses = get_all_incoming_courses()
    for course in courses:
        course.viewname = f"{course.name} - {(course.start_date - date.today() - timedelta(days=3)).days} Days left"
    return templates.TemplateResponse("pages/apply.html", {
        "request": request,
        "courses": courses
        })     

@router.post("/apply")
async def apply(request:Request):
    form = await request.form()
    name, age, email, phone, occupation, speciallity, linkedin, github, course = form.values()
    if "linkedin.com" in linkedin:
        linkedin = linkedin.replace("/", "")
        linkedin = re.sub("(?:.*.comin)", "", linkedin)
    if "github.com" in github:
        github = re.sub("(?:.*.com\/)", "", github)

    print(github)

    try:
        submission_obj = SubmissionCreate(course_id= course, 
        name= name, 
        email= email, 
        age= age, 
        phone= phone, 
        speciality= speciallity,
        occupation= occupation, 
        linkedin= linkedin, 
        github= github, 
        score= 0.0)

        create(submission_obj)
        return templates.TemplateResponse("pages/success.html", {
            "request": request,
            "message": f"We received your apply {name}."
        })
    except:
        return templates.TemplateResponse("pages/exception.html", {
            "request": request,
            "status_code": 406,
            "status_message": internal.status_codes.codes[406],
            "details": "Not Acceptable!"
        })