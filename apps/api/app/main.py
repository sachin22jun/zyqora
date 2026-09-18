from fastapi import FastAPI,Depends,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from redis import Redis
from rq import Queue
from .db import Base,engine,get_db,SessionLocal
from .models import Agent,Task
from .schemas import TaskCreate,AgentOut,TaskOut
from .agents import AGENTS
from .config import settings
app=FastAPI(title="ZYQORA API",version="0.1.0")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:3000"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
@app.on_event("startup")
def startup():
 Base.metadata.create_all(engine)
 with SessionLocal() as db:
  for slug,d in AGENTS.items():
   if not db.query(Agent).filter(Agent.slug==slug).first(): db.add(Agent(slug=slug,name=d["name"],category=d["category"],description=d["system"],price=0,config=d))
  db.commit()
@app.get("/health")
def health(): return {"status":"ok","service":"zyqora-api"}
@app.get("/api/v1/agents",response_model=list[AgentOut])
def agents(db:Session=Depends(get_db)): return db.query(Agent).all()
@app.post("/api/v1/agents/{slug}/tasks",response_model=TaskOut,status_code=202)
def create_task(slug:str,p:TaskCreate,db:Session=Depends(get_db)):
 a=db.query(Agent).filter(Agent.slug==slug).first()
 if not a: raise HTTPException(404,"Agent not found")
 t=Task(agent_id=a.id,instructions=p.instructions,status="QUEUED");db.add(t);db.commit();db.refresh(t)
 Queue("zyqora",connection=Redis.from_url(settings.redis_url)).enqueue("app.worker.run_task",t.id);return t
@app.get("/api/v1/tasks/{task_id}",response_model=TaskOut)
def task(task_id:str,db:Session=Depends(get_db)):
 t=db.get(Task,task_id)
 if not t: raise HTTPException(404,"Task not found")
 return t
