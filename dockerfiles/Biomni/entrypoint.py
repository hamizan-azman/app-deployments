"""Launch Biomni Gradio demo."""
import os
from biomni.agent import A1

llm = os.environ.get("BIOMNI_LLM", "claude-sonnet-4-20250514")
agent = A1(path="/app/data", llm=llm)
agent.launch_gradio_demo(server_name="0.0.0.0")
