from __future__ import annotations
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from siyarix.core import AgentCore, AgentMode, AgentGoal, AgentResult
from siyarix.planner import ExecutionPlan, PlanStatus, PlanStep, StepStatus

@pytest.mark.asyncio
async def test_agent_execute_multi_wave():
    agent = AgentCore(mode=AgentMode.AUTONOMOUS)
    
    with patch.object(agent, "execute_goal", new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = AgentResult(
            goal="Test", 
            success=True, 
            findings=[{"vulnerability": "SQLi"}]
        )
        
        goal = AgentGoal(description="Find vulns")
        with patch.object(agent.planner_autonomous, "plan", new_callable=AsyncMock) as mock_plan:
            mock_plan.return_value = ExecutionPlan(goal="Test")
            res = await agent.execute_multi_wave(goal, max_waves=2)
            assert res.success is True
            mock_exec.assert_called()

@pytest.mark.asyncio
async def test_agent_execute_multi_wave_empty_findings():
    agent = AgentCore(mode=AgentMode.AUTONOMOUS)
    
    with patch.object(agent, "execute_goal", new_callable=AsyncMock) as mock_exec:
        mock_exec.return_value = AgentResult(goal="Test", success=True, findings=[])
        
        goal = AgentGoal(description="Find vulns")
        with patch.object(agent.planner_autonomous, "plan", new_callable=AsyncMock) as mock_plan:
            mock_plan.return_value = ExecutionPlan(goal="Test")
            res = await agent.execute_multi_wave(goal, max_waves=2)
            assert res.success is True

@pytest.mark.asyncio
async def test_agent_execute_subagent():
    agent = AgentCore(mode=AgentMode.AUTONOMOUS)
    mock_subagent = MagicMock()
    mock_subagent.start = AsyncMock()
    mock_subagent.shutdown = AsyncMock()
    mock_subagent.execute_goal = AsyncMock(return_value=AgentResult(goal="Test", success=True))
    
    with patch.object(agent, "create_subagent", return_value=mock_subagent):
        res = await agent.execute_subagent(role="Recon", goal="Scan network")
        assert res.success is True
        mock_subagent.execute_goal.assert_called_once()

@pytest.mark.asyncio
async def test_hybrid_fallback_with_tools():
    agent = AgentCore(mode=AgentMode.HYBRID)
    fail_plan = ExecutionPlan(goal="Test", status=PlanStatus.FAILED)
    
    step = MagicMock()
    step.status.value = "completed"
    step.tool = "nmap"
    fail_plan.steps = [step]
    
    with patch.object(agent, "_execute_autonomous", new_callable=AsyncMock) as mock_auto:
        mock_auto.return_value = AgentResult(goal="Test", success=False, plan=fail_plan)
        with patch.object(agent, "_execute_registry", new_callable=AsyncMock) as mock_reg:
            mock_reg.return_value = AgentResult(goal="Test", success=True)
            
            res = await agent.execute_goal(AgentGoal(description="Test"))
            assert res.success is True

@pytest.mark.asyncio
async def test_autonomous_failure_recovery():
    agent = AgentCore(mode=AgentMode.AUTONOMOUS)
    
    plan = ExecutionPlan(goal="Test", status=PlanStatus.COMPLETED)
    step = PlanStep(id="step_1", command="scan", tool="nmap")
    step.status = StepStatus.FAILED
    step.result = {"error": "Connection refused"}
    plan.steps = [step]

    with patch.object(agent._planner_autonomous, "plan", new_callable=AsyncMock) as mock_plan:
        mock_plan.return_value = plan
        with patch.object(agent._executor_autonomous, "execute_plan", new_callable=AsyncMock) as mock_exec:
            mock_exec.return_value = plan
            with patch.object(agent._validator, "validate_plan", new_callable=AsyncMock):
                with patch.object(agent._validator, "plan_recovery", new_callable=AsyncMock) as mock_rec:
                    from siyarix.validators import RecoveryAction, RecoveryPlan
                    modified_step = PlanStep(id="step_1", command="scan", tool="nmap", args={"retry": True})
                    mock_rec.return_value = RecoveryPlan(original_step=step, action=RecoveryAction.RETRY, modified_step=modified_step, message="Retry")
                    
                    with patch.object(agent, "_check_budget", new_callable=AsyncMock):
                        res = await agent.execute_goal(AgentGoal(description="Test"))
                        # Mock exec gets called twice: first run, then recovery retry run
                        assert mock_exec.call_count == 2
                        assert res.success is True
