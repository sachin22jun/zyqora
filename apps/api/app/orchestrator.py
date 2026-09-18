from .model_gateway import ModelGateway
from .agents import AGENTS
def execute_agent(slug,instructions):
 d=AGENTS[slug];r=ModelGateway().generate(d["system"],instructions);return {"title":d["name"],"content":r.text,"usage":{"cost_usd":r.cost_usd}}
