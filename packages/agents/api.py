from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from packages.agents import models
from packages.agents.database import get_db

router = APIRouter(prefix="/agents", tags=["Agents"])

class AgentCreate(BaseModel):
    name: str
    role: str

class AgentResponse(BaseModel):
    id: int
    name: str
    role: str
    status: str
    successRate: str
    actions: int

    class Config:
        from_attributes = True

@router.post("", response_model=AgentResponse)
def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    db_agent = models.AgentModel(
        name=agent.name,
        role=agent.role,
        status="idle",
        success_rate="100%",
        actions=0
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    
    # Map snake_case to camelCase for the frontend
    return {
        "id": db_agent.id,
        "name": db_agent.name,
        "role": db_agent.role,
        "status": db_agent.status,
        "successRate": db_agent.success_rate,
        "actions": db_agent.actions
    }

@router.get("", response_model=List[AgentResponse])
def get_agents(db: Session = Depends(get_db)):
    agents = db.query(models.AgentModel).all()
    # Map for frontend
    return [
        {
            "id": a.id,
            "name": a.name,
            "role": a.role,
            "status": a.status,
            "successRate": a.success_rate,
            "actions": a.actions
        } for a in agents
    ]

@router.delete("/{agent_id}")
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = db.query(models.AgentModel).filter(models.AgentModel.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    db.delete(agent)
    db.commit()
    return {"ok": True}

@router.put("/{agent_id}/toggle")
def toggle_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = db.query(models.AgentModel).filter(models.AgentModel.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent.status = "paused" if agent.status in ["idle", "running"] else "idle"
    db.commit()
    db.refresh(agent)
    
    return {
        "id": agent.id,
        "name": agent.name,
        "role": agent.role,
        "status": agent.status,
        "successRate": agent.success_rate,
        "actions": agent.actions
    }
