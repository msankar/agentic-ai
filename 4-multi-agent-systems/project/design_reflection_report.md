# Munder Difflin Multi-Agent System: Final Project Report

## 1. Introduction
This report presents the design, implementation, and evaluation of a multi-agent system developed for the Beaver's Choice Paper Company. The company faced operational challenges in inventory management, customer quoting, and order finalization, which posed risks of revenue loss.  

The goal of this project was to create an automated, reliable solution using a multi-agent architecture. Leveraging the **smolagents** framework, the system orchestrates specialized agents to streamline inventory checks, quote generation, and order processing, ensuring accurate, responsive, and efficient operations.

---

## 2. System Architecture and Design
The system centers on an **OrchestratorAgent** that manages workflow execution by delegating tasks to specialized worker agents. This modular architecture ensures maintainability, scalability, and clear separation of concerns.  

The initial implementation employed a prompt-driven orchestration with `managed_agents`. While functional, this approach occasionally resulted in errors due to workflow complexity and LLM misinterpretation. To improve reliability, the system was refactored:

- **Current Design**: Introduces the `handle_customer_request` tool within the OrchestratorAgent.
- **AnalysisAgent**: Parses outputs from the QuotingAgent into structured JSON to dictate the next workflow step, reducing ambiguity and improving consistency.

The original `managed_agents` code remains in `project_starter.py` for reference.

![System Architecture Diagram](munder_difflin_agent_architecture.png)

### 2.1. Agent Workflow
1. **User Request & Normalization**: `normalize_item_names` uses TF-IDF similarity to map ambiguous user input to official inventory items.
2. **Orchestration**: OrchestratorAgent coordinates the workflow.
3. **Quoting & Analysis**:  
   - QuotingAgent generates quotes with pricing, stock, and delivery estimates.  
   - AnalysisAgent converts the quote into a JSON decision: `FINALIZE_ORDER`, `REORDER_STOCK`, or `CANNOT_FULFILL`.
4. **Execution**:
   - `FINALIZE_ORDER`: InventoryAgent confirms stock → OrderingAgent finalizes sale.  
   - `REORDER_STOCK`: InventoryAgent places order → OrderingAgent finalizes if stock is replenished.  
   - `CANNOT_FULFILL`: Process terminates, user receives an appropriate message.
5. **Final Response**: OrchestratorAgent synthesizes a polished, natural-language response for the user.

### 2.2. Agent Roles
| Agent | Role & Responsibilities |
|-------|------------------------|
| **OrchestratorAgent** | Central workflow controller; manages agent coordination without executing business logic. |
| **QuotingAgent** | Generates customer quotes, evaluates pricing, and applies discounts. |
| **InventoryAgent** | Manages stock levels, reorders, and financial authorization. |
| **OrderingAgent** | Finalizes sales transactions, ensuring sufficient stock. |
| **AnalysisAgent** | Interprets QuotingAgent output and returns structured JSON to guide workflow decisions. |

---

## 3. Evaluation and Performance
The system was tested using `quote_requests_sample.csv` and results logged in `test_results.csv`.

### 3.1. Strengths
- **Successful Fulfillment**: Correctly processed multiple orders, updating inventory and cash balance as expected.
- **Constraint Adherence**: Identified unfulfillable requests, preventing invalid orders.
- **Structured Decision-Making**: Properly handled low-stock scenarios and reorder requirements.

### 3.2. Areas for Improvement
1. **Response Formatting**: Some final outputs appear as raw JSON or error-like messages. Enhancing OrchestratorAgent’s response parsing could standardize user-facing text.
2. **Multi-Item Requests**: Sequential handling can produce confusing results if one item is unavailable. Future improvements could support partial fulfillment and clear user prompts.

---

## 4. Conclusion
The multi-agent system effectively automates Beaver's Choice Paper Company's inventory, quoting, and sales workflows. By leveraging a structured orchestration with specialized agents, the system achieves reliability and efficiency while maintaining scalability. While further refinements are possible—particularly in response formatting and complex order handling—the current implementation provides a strong foundation for operational excellence.

