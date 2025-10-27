# The Challenge: From Messy Claim Reports to Organized Queues

## Overview
In this exercise, you will design a multi-stage AI workflow that mimics a complex business process for an insurance company. The goal is to extract structured data from unstructured text, assess damage severity, and route claims to the appropriate processing queues.

## Challenge Objectives
- Extract structured information from free-form text.
- Assess damage severity based on extracted information.
- Route claims to the correct processing queue based on business rules.
- Implement validation checks at each stage to ensure data quality and decision accuracy.

## Instructions

1. **Open the Notebook**
   - Launch the exercise notebook from your Udacity classroom.

2. **Initial Setup**
   - Configure your API Key in the designated cell.

3. **Review Sample FNOL Texts**
   - Run the cell that defines `sample_fnols`. Read through a few examples to understand the input format. There's an optional `TODO` to add more texts if you wish to test further.

4. **Stage I: Information Extraction**
   - Study the `ClaimInformation` Pydantic model provided. This defines the structure your LLM needs to output for this stage.
   - **Your Task**: Complete the `info_extraction_system_prompt` by:
     - Assigning a role (e.g., "You are an expert data extraction AI specializing in insurance claims.")
     - Listing the keys to extract based on `ClaimInformation`.
     - Adding any extra instructions for handling missing information or date formats.
   - **Your Task**: Complete the `extract_claim_info` function by calling the gate check: `validated_info = gate1_validate_claim_info(response)`.
   - Run the cells to define these prompts and functions. Then run the cell that calls `extract_claim_info` for all `sample_fnols` and review the `extracted_claim_info_items`. Note any failures from Gate 1.

5. **Stage II: Severity Assessment**
   - Review the damage severity heuristics (Minor, Moderate, Major cost ranges) provided in the notebook markdown.
   - Study the `SeverityAssessment` Pydantic model.
   - **Your Task**: Complete the `severity_assessment_system_prompt` by:
     - Assigning a role (e.g., "You are an experienced auto damage claims adjuster.")
     - Providing instructions for classifying damage and estimating repair costs.
   - **Your Task**: Complete the `gate2_cost_range_ok` function by filling in the conditions to check if the `validated_severity.est_cost` falls outside the defined heuristic ranges.
   - Run the cells to define these prompts and functions. Then run the cell that calls `assess_severity` for your extracted claim items and review `severity_assessment_items`. Note any Gate 2 failures.

6. **Stage III: Queue Routing**
   - Review the queue routing rules and priority level descriptions provided in the notebook markdown.
   - Study the `ClaimRouting` Pydantic model.
   - **Your Task**: Complete the `queue_routing_system_prompt` by:
     - Assigning a role (e.g., "You are an AI claim routing system.")
     - Providing instructions for assigning claims to the correct queues based on severity.
   - The `gate3_validate_routing` and `route_claim` functions do not have learner `TODO`s for code changes but should be understood.
   - Run the cells to define the prompt and functions. Then run the cell that calls `route_claim` and review `routed_claim_items`. Note any Gate 3 failures.

7. **Review Outputs**
   - Run the cell that combines all outputs into a pandas DataFrame.
   - **Your Task**: Examine the final DataFrame. Does the end-to-end processing look correct for the sample claims? Did the gate checks catch any issues earlier?

## Conclusion
This exercise will help you develop a structured approach to processing unstructured data, ensuring accuracy and efficiency in claim management.

