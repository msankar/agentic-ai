# Starter

This folder contains the starter Jupyter notebook for the exercise.

## Instructions

1. Open the Jupyter notebook in the starter folder.
2. Follow the instructions in the notebook.
3. Save your work.
4. Move on to the solution folder when you're ready.

# Exercise: Organize Your Workspace

## Overview
In this exercise, you will refine a series of prompts to guide a Language Model (LLM) in creating and explaining a practical one-hour plan to organize your personal work area.

## Challenge
Your workspace is in need of organization. A simple request like "organize my workspace" may yield a generic plan that doesn't fit your specific needs. This exercise will help you transform a general AI assistant into a focused, insightful planner.

## Instructions

1. **Navigate to the Notebook**
   - Open the following notebook in the file explorer: 
     ```
     /workspace/introduction-to-prompting-for-llm-reasoning-and-planning/starter/introduction-to-prompting-for-llm-reasoning-and-planning.ipynb
     ```

2. **Initial Setup & API Key**
   - Add your API key from the cloud resources tab above.

3. **Step 1: Generic Prompt**
   - Locate the section "1. Generic Prompt".
   - Run the code cell that defines `plain_system_prompt` and `user_prompt`, then calls `get_completion` to get the `baseline_response`.
   - Observe the output and review the "Observations" questions in the notebook.

4. **Step 2: Add a Professional Role**
   - Go to the section "2. Add a Professional Role".
   - Modify the line for `role_system_prompt` to assign a professional role to the LLM. For example:
     ```python
     role_system_prompt = "You are an expert professional organizer and productivity coach."
     ```
   - Run this cell to define the new system prompt and get `role_response`.

5. **Step 3: Introduce Concrete Constraints**
   - Proceed to "3. Introduce Concrete Constraints".
   - Add specific constraints to the system prompt. For example:
     ```python
     constraints_system_prompt = f"{role_system_prompt}. The plan must be achievable in one hour and require no purchases, using only existing household items."
     ```
   - Run the cell to get `constraints_response`.

6. **Step 4: Request Step-by-Step Reasoning**
   - Navigate to "4. Request Step-by-Step Reasoning".
   - Modify the prompt to ask the LLM to explain its reasoning. For example:
     ```python
     reasoning_system_prompt = (f"{constraints_system_prompt}. Explain your reasoning for each step of the plan in a thoughtful way before presenting the final checklist.")
     ```
   - Run the cell to obtain `reasoning_response`.

7. **Step 5: Reflection & Transfer**
   - Move to "5. Reflection & Transfer".
   - Type your thoughts on which prompt tweak had the most significant impact and why.
   - List two other situations where the same prompt-refinement pattern could help.

8. **Bonus: Apply What You've Learned**
   - Define your own `custom_system_prompt` and `user_prompt` for a new scenario.
   - Uncomment the lines to send your custom prompt and see the results.

## Conclusion
This exercise aims to enhance your skills in prompt engineering, enabling you to create tailored and actionable strategies using LLMs.

