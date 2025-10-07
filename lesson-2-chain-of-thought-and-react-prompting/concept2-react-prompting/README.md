# Exercise: ReACT Prompting

## Overview
In this exercise, you will transform a Retail Demand Analyst from a Chain-of-Thought (CoT) based reasoner into a true ReAct agent. Your challenge is to build the core components of this agent, allowing it to think, act, and use its tools effectively.

## Challenge
You will create a comprehensive ReAct system prompt and implement the orchestration loop in Python, enabling the agent to interact with its tools and environment over multiple steps to solve a problem.

## Instructions

1. **Open the Notebook**
   - In the file explorer, navigate to the correct notebook for this exercise and open it:
     ```
     /workspace/chain-of-thought-and-react-prompting/exercises/concept2-react-prompting/starter/lesson-2-chain-of-thought-and-react-prompting-part-ii.ipynb
     ```

2. **Initial Setup & API Key**
   - Run the first few cells to import libraries and load the data.
   - In the cell for the OpenAI client setup, add your API key where indicated by the `TODO`.

3. **Create the ReAct System Prompt**
   - Navigate to the section "2. Create a ReACT prompt that can call tools".
   - Find the `TODO` inside the `react_system_prompt` string.
   - **Your Task**: Following the structure demonstrated with the Logistics Coordinator example, complete this system prompt. You must include:
     - **Role and Instructions**: Define the agent's role and explain the `THINK/ACT` cycle it must follow.
     - **Tool Definitions**: Clearly define the four available tools: `calculator`, `get_sales_data`, `call_weather_api`, and `final_answer`. For each tool, include a description and an example of its input and output.
     - **An Example Interaction**: Provide a complete, multi-turn example showing how the agent should reason, act, and use observations to solve a simple problem.

4. **Implement the Tool-Calling Logic**
   - Proceed to the section "3. Tool Calling Parsing and Calling".
   - The notebook provides a `safe_eval` function to prevent security issues. Your first task is in the `calculator` function.
   - **Your Task**: Inside the `calculator` function, complete the `TODO` by calling the `safe_eval` function and ensuring the result is returned as a float.

5. **Create the ReAct Loop**
   - Navigate to "4. Create the ReACT Loop".
   - Find the `TODO` items inside the `while True:` loop.
   - **Your Task**: Complete the logic for the loop. This involves:
     - Calling the `get_completion` function to get the `react_response` from the AI.
     - Calling the `get_observation_message` function to parse the `react_response` and get the `observation_message`.
     - Appending the assistant's response and the user's observation to the `messages` list to maintain the conversation history.

6. **Run and Reflect**
   - Execute the loop and observe the turn-by-turn output. Watch how the agent first calls `get_sales_data`, then uses the `calculator` to find the spike, then calls the `call_weather_api` for that specific date, and finally uses `final_answer`.
   - Compare this dynamic process to the single-prompt CoT approach from the previous exercise.

## Conclusion
This exercise will help you understand how to create a more flexible, reliable, and powerful AI system by implementing the ReAct prompting approach.

