# Exercise: Prompt Refinement

## Overview
In this exercise, you will apply the principles of **Prompt Instruction Refinement** to improve the effectiveness of a Language Model (LLM) in analyzing recipes against a list of dietary restrictions.

## Challenge
You will start with a basic prompt and iteratively refine it to enhance the LLM's ability to provide detailed and accurate dietary analyses. The goal is to ensure that the LLM can handle ambiguities, explain its reasoning, and provide structured output.

## Instructions

1. **Open the Notebook**
   - Launch the exercise notebook from your Udacity classroom.

2. **Initial Setup**
   - Add your API Key in the designated cell.

3. **Review Sample Data**
   - Load `sample_recipes` and `dietary_restrictions`. Familiarize yourself with this data as it will be used for testing your prompts.

4. **Initial Prompt and Evaluation**
   - Examine the `initial_prompt` and the `format_prompt` function (using Jinja2 for templating).
   - Test the `initial_prompt` with the "Classic Spaghetti Bolognese" recipe.
   - **Your Task**: Observe the `initial_response`. Note its structure and the classifications it provides. Is it giving explanations? How does it handle dietary restrictions?

5. **Prompt Component Analysis**
   - Read through the "Prompt Component Analysis" and "Initial Analysis of Problems" sections in the notebook. This guides you to think about what's lacking in the `initial_prompt`.

6. **Prompt Refinement Iteration 1**
   - This cell contains your first `TODO`. You need to complete the definitions for various dietary restrictions and provide clear guidelines for the classification logic.
   - **Your Task**: Fill in the `**********` placeholders. 
   - After filling in the `TODOs`, test `refined_prompt_1` with the same spaghetti recipe.
   - **Your Task**: Observe the `Iteration 1 response`. Notice how the output now includes explanations and critical ingredients due to your improved prompt.

7. **Prompt Refinement Iteration 2**
   - This cell contains your second `TODO`. You'll add more guidance on handling common ambiguities in recipes and complete an example within the prompt.
   - **Your Task**: Fill in the `**********` placeholders in the "Handling ambiguities" section. 
   - After filling in the `TODOs`, test `refined_prompt_2` with the "Vegetable Stir Fry" recipe.
   - **Your Task**: Analyze the `Iteration 2 response`. Does the LLM handle ambiguities (like "soy sauce" for gluten-free, or "sesame seeds" for nut-free) more thoughtfully now?

8. **Testing with Multiple Recipes**
   - Test your `refined_prompt_2` with the "Chocolate Chip Cookies" recipe.
   - **Your Task**: Observe the response. Check if the classifications and explanations are consistent and accurate for this different type of recipe (e.g., how it handles "butter" for dairy-free/vegan, "all-purpose flour" for gluten-free, and "chopped nuts (optional)" for nut-free).

## Conclusion
This exercise will help you develop skills in crafting precise prompts that lead to better, more informative responses from LLMs, ultimately enhancing their utility in real-world applications.

