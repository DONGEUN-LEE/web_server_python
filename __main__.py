from wsgiref.simple_server import make_server
import falcon
import json
import datetime
import decimal
import bcrypt
import jwt
import os
from json import JSONEncoder
from dotenv import load_dotenv
from database import init_db, Session, SQLAlchemySessionManager
from models import Plans, Users

load_dotenv(verbose=True)


class LoginRes(JSONEncoder):
    token = ""
    message = ""

    def default(self, o):
        return o.__dict__


class RootResource:
    def on_get(self, req, resp):
        resp.text = 'Hello World!'


class PlansResource:
    def on_get(self, req, resp):
        queries = self.session.query(Plans)
        entries = [dict(siteId=q.site_id, stageId=q.stage_id, operId=q.oper_id, resourceId=q.resource_id,
                        productId=q.product_id, planQty=q.plan_qty, startTime=q.start_time, endTime=q.end_time) for q in queries]
        resp.text = (json.dumps(entries, sort_keys=True,
                     indent=4, default=json_default))


class LoginResource:
    def on_post(self, req, resp):
        raw_data = json.load(req.bounded_stream)
        email = raw_data.get('email')
        password = raw_data.get('password')
        user = self.session.query(Users).filter(Users.email == email).one()
        # b = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        loginRes = LoginRes()
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            secret = os.getenv('SECRET_KEY')
            loginRes.token = jwt.encode(
                {"email": email}, secret, algorithm="HS256")
            loginRes.message = 'Success'
        else:
            loginRes.message = 'Fail'
        # do your job
        resp.body = json.dumps(loginRes, cls=LoginRes)


def json_default(value):
    if isinstance(value, datetime.date):
        return value.strftime('%Y-%m-%d')
    elif isinstance(value, decimal.Decimal):
        return float(value)
    raise TypeError('not JSON serializable')

app = falcon.API(middleware=[
    SQLAlchemySessionManager(Session),
])

root = RootResource()
plans = PlansResource()
login = LoginResource()

app.add_route('/', root)
app.add_route('/api/plan', plans)
app.add_route('/api/login', login)

if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')
        init_db()
        httpd.serve_forever()
