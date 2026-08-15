from sqlalchemy import Column, Integer, String
from packages.agents.database import Base

class AgentModel(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String)
    status = Column(String, default="idle")
    success_rate = Column(String, default="100%")
    actions = Column(Integer, default=0)
