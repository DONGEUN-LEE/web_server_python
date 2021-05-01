from sqlalchemy import Column, Integer, String, DateTime, Numeric
from database import Base


class Plans(Base):
    __tablename__ = 'plans'
    id = Column(Integer, primary_key=True)
    site_id = Column(String(250))
    stage_id = Column(String(250))
    oper_id = Column(String(250))
    resource_id = Column(String(250))
    product_id = Column(String(250))
    plan_qty = Column(Numeric)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    def __init__(self, site_id, stage_id, oper_id, resource_id, product_id, plan_qty, start_time, end_time):
        self.site_id = site_id
        self.stage_id = stage_id
        self.oper_id = oper_id
        self.resource_id = resource_id
        self.product_id = product_id
        self.plan_qty = plan_qty
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return "<TbTest('%d', '%s', '%s'>" % (self.id, str(self.datetime), self.string)


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250))
    password = Column(String(250))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return "<Users('%d', '%s', '%s'>" % (self.id, self.email, self.password)
