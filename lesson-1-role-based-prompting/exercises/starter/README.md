## Instructions
# Exercise: Historical Figure Persona

## Overview
In this exercise, you will put into practice the concept of role-based prompting by instructing an AI to adopt the persona of a famous historical figure for an interactive Q&A.

## Challenge
The goal is to craft a believable historical character. For example, if you want to "interview" Albert Einstein, a simple request might yield superficial responses. This exercise will guide you in shaping the AI's responses to truly reflect the personality and knowledge of the historical figure.

## Instructions

1. **Open the Notebook**
   - Launch the "Lesson 1: Role-Based Prompting (Agent Personas) - Historical Figure Interviewer" exercise notebook.

2. **Initial Setup**
   - Add your API key to the notebook.

3. **Step 1: Plain Prompt**
   - Locate the section "1. Plain Prompt".
   - Run the code cell that sends a `control_system_prompt` ("You are a helpful assistant.") and asks the `user_prompt` ("Can you tell me about relativity?").
   - Observe this initial, non-role-playing response. This serves as your control.

4. **Step 2: Baseline Historical Figure Prompt**
   - Go to section "2. Baseline Historical Figure Prompt".
   - You will see a `TODO`: `baseline_system_prompt = "**********."`
   - **Your Task**: Change this line to give the AI the basic role of Albert Einstein. For example:
     ```python
     baseline_system_prompt = "You are Albert Einstein."
     ```
   - Run this cell using the same `user_prompt` about relativity.
   - Review the AI's first attempt at portraying Einstein and use the "Observations" questions in the notebook to guide your thoughts.

5. **Step 3: Define Persona-Specific Attributes**
   - Move to section "3. Define Persona-Specific Attributes".
   - You will find several `TODO` items within the `persona_system_prompt` string, marked with `**********`.
   - **Your Task**: Fill in these attributes for Albert Einstein.
   - Run the cell and compare this response to the previous one. Note differences based on the "Observations" prompts.

6. **Step 4: Add Tone and Style Specifications**
   - Proceed to section "4. Add Tone and Style Specifications".
   - Find the `TODO` items in the `tone_system_prompt` string.
   - **Your Task**: Add specific details about Einstein's tone and conversational style.
   - Run this cell and observe how these specifications refine the AI's portrayal.

7. **Step 5: Q&A Session Format**
   - Navigate to section "5. Q&A Session Format".
   - Find the `TODO` in the `user_prompt` for three questions.
   - **Your Task**: Write three questions to ask "Albert Einstein," keeping in mind the 1950 context.
   - Run the cell and analyze "Einstein's" answers for consistency, historical appropriateness, and depth.

8. **Step 6: Reflection & Transfer**
   - Go to section "6. Reflection & Transfer".
   - In the markdown cell, find the `TODO` and type your thoughts on which prompt refinement you felt was most effective in creating an authentic persona and why.

## Conclusion
This exercise aims to enhance your skills in role-based prompting, allowing you to create engaging and contextually rich interactions with AI by embodying historical figures.

