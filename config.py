import os
from pathlib import Path
ROOT=Path(__file__).resolve().parent
class Config:
 SECRET_KEY=os.environ.get('SECRET_KEY','change-this-development-key')
 SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL',f"sqlite:///{ROOT/'instance'/'inventory.db'}")
 SQLALCHEMY_TRACK_MODIFICATIONS=False
