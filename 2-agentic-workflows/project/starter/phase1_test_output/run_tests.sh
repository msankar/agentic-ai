
#!/bin/bash

# Script to run all Phase 1 agent tests
# Make sure you have activated your virtual environment and set up .env before running


echo ""
echo "======================================================================"
echo "Test 1: DirectPromptAgent"
echo "======================================================================"
python direct_prompt_agent.py
echo ""
echo "Press Enter to continue to next test..."
read

echo ""
echo "======================================================================"
echo "Test 2: AugmentedPromptAgent"
echo "======================================================================"
python augmented_prompt_agent.py
echo ""
echo "Press Enter to continue to next test..."
read

echo ""
echo "======================================================================"
echo "Test 3: KnowledgeAugmentedPromptAgent"
echo "======================================================================"
python knowledge_augmented_prompt_agent.py
echo ""
echo "Press Enter to continue to next test..."
read

echo ""
echo "======================================================================"
echo "Test 4: RAGKnowledgePromptAgent"
echo "======================================================================"
python rag_knowledge_prompt_agent.py
echo ""
echo "Press Enter to continue to next test..."
read

echo ""
echo "======================================================================"
echo "Test 5: EvaluationAgent"
echo "======================================================================"
python evaluation_agent.py
echo ""
echo "Press Enter to continue to next test..."
read

echo ""
echo "======================================================================"
echo "Test 6: RoutingAgent"
echo "======================================================================"
python routing_agent.py
echo ""
echo "Press Enter to continue to next test..."
read

echo ""
echo "======================================================================"
echo "Test 7: ActionPlanningAgent"
echo "======================================================================"
python action_planning_agent.py
echo ""

echo ""
echo "======================================================================"
echo "Phase 1 Tests Completed!"
echo "======================================================================"
echo
