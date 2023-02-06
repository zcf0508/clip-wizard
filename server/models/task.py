from datetime import datetime

from server import BaseModel, db


class Task(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64), unique=True)
    file = db.Column(db.String(256))
    status = db.Column(db.Integer, default=0) # 0-wait 1-running 2-finished 3-failed
    res = db.Column(db.Text)
    err = db.Column(db.String(256)) # error_msg
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, uuid, file) -> None:
        self.uuid = uuid
        self.file = file
        self.status = 1

    def __repr__(self):
        return f'<Task {self.uuid}>'
