# Munder Difflin Multi-Agent System: Final Project Report

## 1. Introduction
This report presents the design, implementation, and evaluation of a multi-agent system developed for the Beaver's Choice Paper Company. The company faced operational challenges in inventory management, customer quoting, and order finalization, which posed risks of revenue loss.

The goal of this project was to create an automated, reliable solution using a multi-agent architecture. Leveraging the **smolagents** framework, the system orchestrates specialized agents to streamline inventory checks, quote generation, and order processing, ensuring accurate, responsive, and efficient operations.

---

## 2. System Architecture and Design
The system centers on an **OrchestratorAgent** that manages workflow execution by delegating tasks to specialized worker agents. This modular architecture ensures maintainability, scalability, and clear separation of concerns.

The initial implementation employed a prompt-driven orchestration using `managed_agents`. While workable, this pattern did not provide enough control over multi-stage workflows and made debugging more difficult. To improve reliability and transparency, the system was refactored to a **tool-based orchestration model**:

- **Current Design**: Introduces the `handle_customer_request` tool within the OrchestratorAgent for deterministic workflow routing.
- **AnalysisAgent**: Converts QuotingAgent output into structured JSON, enabling predictable branching logic.

The original `managed_agents` version remains in `project_starter.py` for reference.

![System Architecture Diagram](munder_difflin_agent_architecture.png)

### 2.1. Agent Workflow
1. **User Request & Normalization**:  
   `normalize_item_names` uses TF-IDF similarity to map ambiguous user input to canonical inventory items.
2. **Orchestration**:  
   OrchestratorAgent coordinates the workflow across quoting, analysis, inventory, and ordering.
3. **Quoting & Analysis**:  
   - QuotingAgent generates itemized quotes including pricing, availability, and delivery estimates.  
   - AnalysisAgent extracts structured decision signals (e.g., `FINALIZE_ORDER`, `REORDER_STOCK`, `CANNOT_FULFILL`).
4. **Execution**:  
   - **FINALIZE_ORDER**: InventoryAgent confirms stock; OrderingAgent finalizes the transaction.  
   - **REORDER_STOCK**: InventoryAgent replenishes stock; OrderingAgent finalizes afterward.  
   - **CANNOT_FULFILL**: The workflow terminates gracefully.
5. **Final Response**:  
   OrchestratorAgent composes a polished, user-friendly answer.

### 2.2. Agent Roles
| Agent | Role & Responsibilities |
|-------|--------------------------|
| **OrchestratorAgent** | Central workflow controller; delegates work to other agents based on analysis. |
| **QuotingAgent** | Generates pricing, delivery estimates, and discount-adjusted quotes. |
| **InventoryAgent** | Performs stock checks, reorders, financial checks, and proactive maintenance. |
| **OrderingAgent** | Finalizes customer orders by creating sales transactions. |
| **AnalysisAgent** | Interprets QuotingAgent output and decides the next workflow action. |

---

## 3. Evaluation and Performance
The system was tested using `quote_requests_sample.csv` with results logged in `test_results.csv`.

### 3.1. Strengths
- **Successful Fulfillment**: Many orders processed end-to-end with correct updates to inventory and cash balance.
- **Accurate Constraint Handling**: The system correctly prevented orders when stock was insufficient or delivery requirements could not be met.
- **Structured Decision-Making**: The AnalysisAgent successfully guided the workflow using consistent JSON outputs.

### 3.2. Areas for Improvement
1. **Response Formatting**: Some user-facing responses contain raw JSON fragments or internal error-style phrasing. Improving natural-language synthesis would enhance clarity.
2. **Multi-Item Requests**: Sequential item handling may produce confusing mixed outcomes if one item is unavailable. Future iterations could support partial fulfillment or structured user prompts.

---

### 3.3. Bug Discovered During Evaluation & Fix Implemented

During evaluation, a critical discrepancy was identified between the **OrchestratorAgent** and the **OrderingAgent** that prevented successful order finalization.

#### Problem: Parameter Mismatch
- The **OrchestratorAgent** forwarded order details using the field **`total_price`**.  
- The original **OrderingAgent** prompt required **`price_per_unit`**, a parameter not provided anywhere in the workflow.  
- Because the OrderingAgent prompt strictly required all fields, it was unable to call the `finalize_order()` tool in most cases, resulting in:
  - No sales transactions recorded  
  - No inventory reductions  
  - No cash balance updates  
  - Apparent “completion” of requests without backend execution  

This issue only became visible during full end-to-end evaluation.

#### Fix Implemented
To resolve the issue, the following improvements were made:

1. **OrderingAgent Prompt Updated**  
   The prompt was rewritten to expect a single field:  
   - `price` (interpreted as the total price)

2. **Explicit Field Mapping Added**  
   The prompt now clarifies:  
   > “The Orchestrator will provide `total_price`. Use this value as `price`.”

3. **Removed Incorrect Fields**  
   All references to `price_per_unit` were removed.

After this fix, the OrderingAgent correctly produced tool calls such as:
   `finalize_order(item_name="A4 Paper", quantity=3, price=12.00, date="2025-04-15")`


#### Outcome After Fix
- Sales transactions began logging properly.  
- Inventory decreased as expected.  
- Cash balance updated after each fulfilled order.  
- Overall system behavior matched the project requirements.

This debugging process reinforced the importance of aligned prompts, consistent data schemas between agents, and holistic pipeline testing.

---

## 4. Conclusion
The multi-agent system effectively automates Beaver's Choice Paper Company's inventory, quoting, and order-processing workflows. The modular architecture, combined with structured inter-agent communication, results in a reliable and scalable solution.

The debugging effort—particularly solving the OrderingAgent parameter mismatch—highlighted the value of:
- clear interface contracts between agents,  
- deterministic tool-calling prompts, and  
- end-to-end workflow validation.

While improvements remain possible in user-facing response quality and multi-item handling, the final system provides a robust foundation for operational efficiency and future expansion.

---
