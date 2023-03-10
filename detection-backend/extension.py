from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


db = SQLAlchemy()
cors = CORS(resources={r'/*':{'origins':'*'}})
