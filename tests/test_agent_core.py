from __future__ import annotations
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import os
from siyarix.core import AgentCore, AgentMode, AgentStatus, AgentGoal, AgentResult
from siyarix.planner import ExecutionPlan, PlanStatus, PlanStep, StepStatus

@pytest.fixture
def agent():
    return AgentCore(mode=AgentMode.AUTONOMOUS)

def test_agent_properties(agent):
    assert agent.status == AgentStatus.IDLE
    assert agent.mode == AgentMode.AUTONOMOUS

@pytest.mark.asyncio
async def test_execute_registry_mode():
    ag = AgentCore(mode=AgentMode.REGISTRY)
    plan = ExecutionPlan(goal="Test", status=PlanStatus.COMPLETED)
    
    with patch.object(ag.executor_registry, "execute_plan", new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = plan
        with patch.object(ag.validator, "validate_plan", new_callable=AsyncMock) as mock_val:
            mock_val.return_value = (True, [])
            res = await ag.execute_goal(AgentGoal(description="Test"), plan=plan)
            assert res.success is True

@pytest.mark.asyncio
async def test_execute_autonomous_mode():
    ag = AgentCore(mode=AgentMode.AUTONOMOUS)
    plan = ExecutionPlan(goal="Test", status=PlanStatus.COMPLETED)
    
    with patch.object(ag.executor_autonomous, "execute_plan", new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = plan
        with patch.object(ag.validator, "validate_plan", new_callable=AsyncMock) as mock_val:
            mock_val.return_value = (True, [])
            with patch.object(ag, "_check_budget", new_callable=AsyncMock):
                res = await ag.execute_goal(AgentGoal(description="Test"), plan=plan)
                assert res.success is True

@pytest.mark.asyncio
async def test_execute_hybrid_mode_success():
    ag = AgentCore(mode=AgentMode.HYBRID)
    plan = ExecutionPlan(goal="Test", status=PlanStatus.COMPLETED)
    
    with patch.object(ag, "_execute_autonomous", new_callable=AsyncMock) as mock_auto:
        mock_auto.return_value = AgentResult(goal="Test", success=True, plan=plan)
        res = await ag.execute_goal(AgentGoal(description="Test"), plan=plan)
        assert res.success is True
        mock_auto.assert_called_once()

@pytest.mark.asyncio
async def test_execute_hybrid_mode_fallback():
    ag = AgentCore(mode=AgentMode.HYBRID)
    fail_plan = ExecutionPlan(goal="Test", status=PlanStatus.FAILED)
    success_plan = ExecutionPlan(goal="Test", status=PlanStatus.COMPLETED)
    
    with patch.object(ag, "_execute_autonomous", new_callable=AsyncMock) as mock_auto:
        mock_auto.return_value = AgentResult(goal="Test", success=False, plan=fail_plan)
        with patch.object(ag, "_execute_registry", new_callable=AsyncMock) as mock_reg:
            mock_reg.return_value = AgentResult(goal="Test", success=True, plan=success_plan)
            
            res = await ag.execute_goal(AgentGoal(description="Test"), plan=fail_plan)
            assert res.success is True
            mock_reg.assert_called_once()

@pytest.mark.asyncio
async def test_execute_interactive_mode():
    ag = AgentCore(mode=AgentMode.INTERACTIVE)
    plan = ExecutionPlan(goal="Test", status=PlanStatus.COMPLETED)
    
    with patch.object(ag.executor_autonomous, "execute_plan", new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = plan
        with patch.object(ag.validator, "validate_plan", new_callable=AsyncMock) as mock_val:
            mock_val.return_value = (True, [])
            with patch.object(ag, "_check_budget", new_callable=AsyncMock):
                with patch("builtins.input", return_value="y"):
                    res = await ag.execute_goal(AgentGoal(description="Test"), plan=plan)
                    assert res.success is True

@pytest.mark.asyncio
async def test_agent_check_budget(agent):
    agent._usage_tracker = MagicMock()
    agent._usage_tracker.session_totals.return_value = MagicMock(total_tokens=9999999, estimated_cost_usd=0.0)
    agent._max_tokens_per_session = 1000
    
    from siyarix.exceptions import BudgetExceededError
    with pytest.raises(BudgetExceededError):
        await agent._check_budget()
