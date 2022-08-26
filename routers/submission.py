from fastapi import Depends, APIRouter, status
from datetime import date
from dateutil.relativedelta import relativedelta
import pickle

from internal import oauth2
from db.models.AdminUser import AdminUser
from db.repository import submission as submissionDB
from db.repository.login import get_current_user_from_token
from schemas.Submission import SubmissionCreate
from .scraping.github_api import get_projects, github_user, social_rating
from .scraping.linkedin import Scrapping

router = APIRouter(
    prefix='/submission',
    tags=['Submissions']
    )

score_model = pickle.load(open("routers/ml_models/score.pkl", "rb"))

def score(submission: SubmissionCreate):
    github = github_user(submission.github)
    disipline = 1
    connections, certificates, experience, projects = map(int, Scrapping(submission.linkedin).values())
    projects += get_projects(github)
    sociality = social_rating(github, connections)
    feature = [disipline, projects, certificates, experience, submission.speciality, sociality, submission.occupation, submission.age]
    score = score_model.predict([feature])[0]
    submission.score = round(score, 2)

@router.post('/create', status_code=status.HTTP_201_CREATED)
def create(submission: SubmissionCreate, auth: AdminUser = Depends(get_current_user_from_token)):
    score(submission)
    return submissionDB.create(submission=submission)

@router.get('/get', status_code=status.HTTP_200_OK)
def get_submission_by_id(id: int, auth: AdminUser = Depends(oauth2.get_current_user)):
    return submissionDB.get(id=id)

@router.get('/getSub_mem', status_code=status.HTTP_200_OK)
def get_submission_by_member_id(id: int, auth: AdminUser = Depends(oauth2.get_current_user)):
    return submissionDB.get_by_member_id(id)

@router.get('/getApprovedSub_mem', status_code=status.HTTP_200_OK)
def get_approved_submission_by_member(id: int, auth: AdminUser = Depends(oauth2.get_current_user)):
    submissions = get_submission_by_member_id(id)
    for submission in submissions:
        if submission.Approved:
            return submission
    return None

@router.get('/getSub_cou', status_code=status.HTTP_200_OK)
def get_submission_by_course_id(id: int, auth: AdminUser = Depends(oauth2.get_current_user)):
    return submissionDB.get_by_course_id(id)

@router.get('/getSub_app', status_code=status.HTTP_200_OK)
def get_approved_by_course_id(id: int, auth: AdminUser = Depends(oauth2.get_current_user)):
    return submissionDB.get_approved_by_course_id(id)

@router.get('/getSub_score', status_code=status.HTTP_200_OK)
def get_ordered_by_score(id: int, auth: AdminUser = Depends(oauth2.get_current_user)):
    return submissionDB.get_by_scores(id)

@router.get('/getAll', status_code=status.HTTP_200_OK)
def get_all_submissions(auth: AdminUser = Depends(oauth2.get_current_user)):
    return submissionDB.get_all()

@router.get('/getYear_Submissions', status_code=status.HTTP_200_OK)
def get_all_submissions_year(auth: AdminUser = Depends(oauth2.get_current_user)):
    year = [len(submissionDB.get_month_submissions(date.today() - relativedelta(months=n))) for n in range(11, -1, -1)]
    return year

@router.put('/edit', status_code=status.HTTP_202_ACCEPTED)
def edit_submission(id: int, approved: bool, auth: AdminUser = Depends(oauth2.get_current_user)):
    return submissionDB.edit(id, approved)

@router.delete('/delete', status_code=status.HTTP_200_OK)
def delete_submission(id : int, auth: AdminUser = Depends(oauth2.get_current_user)):
    return submissionDB.delete(id)