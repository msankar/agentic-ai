# Exercise: COT Prompting

## Overview
In this exercise, you will act as a **Retail Demand Analyst** to analyze a sudden, unexpected sales spike for a specific product. Your task is to craft a Chain-of-Thought (CoT) prompt that guides the AI to sift through various datasets and identify the cause of the sales spike.

## Challenge
You will provide the AI with multiple datasets, including sales figures, promotion schedules, weather reports, and competitor pricing data. The goal is to create a prompt that effectively helps the AI analyze this information and form a logical hypothesis about the cause of the sales spike.

## Instructions

1. **Open the Notebook**
   - In the file explorer, navigate to the correct notebook for this exercise and open it:
     ```
     /workspace/chain-of-thought-and-react-prompting/exercises/concept1-chain-of-thoughts/starter/lesson-2-chain-of-thought-and-react-prompting-part-i.ipynb
     ```

2. **Initial Setup & API Key**
   - Run the first few cells to import the necessary libraries and helper functions.
   - In the cell for the OpenAI client setup, add your API key where indicated by the `TODO`.

3. **Review the Data**
   - Run the cells under the "A Closer Look at the Data" section.
   - Familiarize yourself with the four different data sources (`sales_df`, `promotions_df`, `weather_df`, `competitor_pricing_df`). Manually look through the data and the plots to see if you can spot the sales spike and any potential causes yourself. This will help you evaluate the AI's performance later.

4. **Craft a Simple CoT Prompt**
   - Navigate to the section "2. Crafting a Simple CoT Prompt".
   - You will find a `TODO` item within the `system_prompt_explicit_cot` variable.
   - **Your Task**: Modify this line to create your first CoT prompt. Your prompt should instruct the AI to act as a "meticulous Retail Demand Analyst" and to "Think step by step" to analyze the provided data and hypothesize the causes for any sales spikes.

5. **Craft a More Developed CoT Prompt**
   - Proceed to the section "3. Crafting a More Developed CoT Prompt". Here, we want to guide the AI more explicitly and ask for a structured output.
   - Find the `TODO` for the `user_prompt_developed_cot` variable.
   - **Your Task**: Write a more detailed user prompt that gives the AI a specific sequence of steps to follow in its analysis. Your instructions should ask it to:
     - Find all sales spikes for each product.
     - For each spike, identify the date, the sales increase, and the possible causes by looking at all the different data sources.
     - Start its response with the structured analysis and conclude by identifying the single largest spike in a specific JSON format (the format is provided in the notebook).

6. **Run and Reflect**
   - Execute the final cells to send your developed prompt to the AI and parse the response.
   - Review the AI's final analysis and the structured JSON output. Did it correctly identify the spike for "Product 5" on January 12th? How good was its reasoning?

## Conclusion
This exercise will help you understand the limits of the CoT approach and set the stage for exploring more dynamic methods in the next exercise.
