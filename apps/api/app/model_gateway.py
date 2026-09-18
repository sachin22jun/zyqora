from dataclasses import dataclass
@dataclass
class ModelResult: text:str; input_tokens:int=0; output_tokens:int=0; cost_usd:float=0.0
class MockProvider:
 def generate(self,system,prompt): return ModelResult(f"ZYQORA demo output for: {prompt[:500]}")
class ModelGateway:
 def __init__(self,provider=None): self.provider=provider or MockProvider()
 def generate(self,system,prompt): return self.provider.generate(system,prompt)
