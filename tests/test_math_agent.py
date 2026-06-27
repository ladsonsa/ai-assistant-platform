from ai_assistant_platform.agents.mathematical_agent import MathematicalAgent

agent = MathematicalAgent()

result = agent.solve("addition", 2, 3)

assert result == 5
