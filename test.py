from sqlalchemy import func
from models import *
from sheets import Planilha

plan = Planilha()
print(plan.vars)

# with DBSession() as db_session:
#     res = db_session.query(func.sum(Step.waited)).select_from(Step).where(
#         Step.object.has(Object.case.has(Case.method == "individual"))
#     ).scalar()
#     print(res)
#     res = db_session.query(func.sum(Step.waited)).select_from(Step).where(
#         Step.object.has(Object.case.has(Case.method == "pipeline"))
#     ).scalar()
#     print(res)
