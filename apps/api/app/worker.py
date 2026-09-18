from redis import Redis
from rq import Worker,Queue
from .config import settings
from .db import SessionLocal
from .models import Task,Agent,TaskEvent
from .orchestrator import execute_agent
def run_task(task_id):
 with SessionLocal() as db:
  t=db.get(Task,task_id)
  if not t:return
  a=db.get(Agent,t.agent_id);t.status="PROCESSING";db.commit()
  try:t.output=execute_agent(a.slug,t.instructions);t.status="COMPLETED";db.add(TaskEvent(task_id=t.id,event_type="TASK_COMPLETED",payload={}))
  except Exception as e:t.status="FAILED";db.add(TaskEvent(task_id=t.id,event_type="TASK_FAILED",payload={"error":str(e)[:500]}))
  db.commit()
if __name__=="__main__":
 r=Redis.from_url(settings.redis_url);Worker([Queue("zyqora",connection=r)],connection=r).work()
