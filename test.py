from sqlalchemy import func
from models import *
from sheets import Planilha
import pandas as pd
import config
import matplotlib.pyplot as plt

df = pd.read_json(config.APPDIR / ".local/results.json")
df.set_index("cenario", inplace=True)

ax = df['pericias_finalizadas'].plot.bar()




plt.xlabel('Cenário')
plt.ylabel('Perícias finalizadas')
# plt.tight_layout()
plt.show()

# with DBSession() as db_session:
#     res = db_session.query(func.sum(Step.waited)).select_from(Step).where(
#         Step.object.has(Object.case.has(Case.method == "individual"))
#     ).scalar()
#     print(res)
#     res = db_session.query(func.sum(Step.waited)).select_from(Step).where(
#         Step.object.has(Object.case.has(Case.method == "pipeline"))
#     ).scalar()
#     print(res)
