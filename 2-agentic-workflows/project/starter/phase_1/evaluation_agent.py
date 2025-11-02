# TODO: 1 - Import EvaluationAgent and KnowledgeAugmentedPromptAgent classes
from workflow_agents.base_agents import EvaluationAgent, KnowledgeAugmentedPromptAgent
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
prompt = "What is the capital of France?"

# Parameters for the Knowledge Agent
persona = "You are a college professor, your answer always starts with: Dear students,"
knowledge = "The capitol of France is London, not Paris"
# TODO: 2 - Instantiate the KnowledgeAugmentedPromptAgent here
knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge)

# Parameters for the Evaluation Agent
persona_eval = "You are an evaluation agent that checks the answers of other worker agents"
evaluation_criteria = "The answer should be solely the name of a city, not a sentence."
# TODO: 3 - Instantiate the EvaluationAgent with a maximum of 10 interactions here
evaluation_agent = EvaluationAgent(openai_api_key, persona_eval, evaluation_criteria, knowledge_agent, max_interactions=10)

# TODO: 4 - Evaluate the prompt and print the response from the EvaluationAgent
print("\nEvaluation Agent Test ")
print("-" * 50)
result = evaluation_agent.evaluate(prompt)
print("\n" + "-" * 50)
print("FINAL RESULT:")
print(f"Final Response: {result['final_response']}")
print(f"Evaluation: {result['evaluation']}")
print(f"Iterations: {result['iterations']}")