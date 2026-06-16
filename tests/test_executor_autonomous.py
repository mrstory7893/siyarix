import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from siyarix.executor_autonomous import AutonomousExecutor

@pytest.fixture
def mock_tool_registry():
    with patch("siyarix.registry.ToolRegistry") as mock:
        registry = MagicMock()
        mock.return_value = registry
        yield registry

@pytest.fixture
def executor(mock_tool_registry):
    return AutonomousExecutor(registry=mock_tool_registry)

def test_executor_init(executor):
    assert executor._registry is not None

@pytest.mark.asyncio
async def test_execute_plan_empty(executor):
    plan = MagicMock()
    plan.steps = []
    res = await executor.execute_plan(plan, live_display=False)
    assert res == plan

@pytest.mark.asyncio
async def test_execute_plan_mock_task(executor):
    plan = MagicMock()
    task = MagicMock()
    task.tool = "nmap"
    task.args = {"target": "127.0.0.1"}
    task.command = "nmap 127.0.0.1"
    plan.steps = [task]
    
    with patch.object(executor, "_exec_one", new_callable=AsyncMock) as mock_exec_task:
        with patch("siyarix.shell_review.review_and_confirm", return_value="run"):
            mock_exec_task.return_value = (task, {"status": "success", "output": "test"})
            res = await executor.execute_plan(plan, live_display=False)
            mock_exec_task.assert_called_once()

@pytest.mark.asyncio
async def test_execute_task_tool_not_found(executor, mock_tool_registry):
    task = MagicMock()
    task.tool = "nonexistent"
    task.command = None
    task.args = {}
    
    mock_tool_registry.execute = AsyncMock(return_value={"error": "not found"})
    res = await executor._execute_tool_step(task)
    assert "not found" in str(res.get("error", "")).lower()

@pytest.mark.asyncio
async def test_execute_task_tool_success(executor, mock_tool_registry):
    task = MagicMock()
    task.tool = "nmap"
    task.command = None
    task.args = {"target": "127.0.0.1"}
    
    mock_tool_registry.execute = AsyncMock(return_value={"status": "success", "output": "nmap output"})
    
    res = await executor._execute_tool_step(task)
    assert res is not None

@pytest.mark.asyncio
async def test_review_commands(executor):
    plan = MagicMock()
    step1 = MagicMock(command="echo hi", tool="raw")
    step2 = MagicMock(command=None, tool="nmap")
    plan.steps = [step1, step2]
    
    with patch("siyarix.shell_review.review_and_confirm", return_value="echo hi"):
        assert await executor._review_commands(plan) is True
        
    with patch("siyarix.shell_review.review_and_confirm", return_value=None):
        assert await executor._review_commands(plan) is False

@pytest.mark.asyncio
async def test_execute_shell_command(executor):
    step = MagicMock(command="echo test", timeout=1)
    state = MagicMock()
    
    with patch("siyarix.subprocess_utils.safe_run_async_stream", new_callable=AsyncMock) as mock_run:
        mock_run.return_value = MagicMock(exit_code=0)
        res = await executor._execute_shell_command(step, state)
        assert res["status"] == "success"

@pytest.mark.asyncio
async def test_exec_one_no_dependencies(executor):
    step = MagicMock(command="echo hi", tool="raw")
    state = MagicMock()
    
    with patch.object(executor, "_execute_shell_command", new_callable=AsyncMock) as mock_shell:
        mock_shell.return_value = {"status": "success", "output": "hi"}
        with patch.object(executor, "_try_parse_output") as mock_parse:
            mock_parse.return_value = {"status": "success", "output": "hi", "parsed": True}
            returned_step, res = await executor._exec_one(step, state)
            assert res["status"] == "success"

@pytest.mark.asyncio
async def test_execute_batch_exception(executor):
    plan = MagicMock()
    task = AsyncMock(side_effect=Exception("Batch error"))
    res = await executor._execute_batch(plan, [task()], [])
    assert res is plan

def test_try_parse_output(executor):
    step = MagicMock(tool="nmap")
    result = {"status": "success", "output": "raw string"}
    
    mock_parser_registry = MagicMock()
    mock_parser_registry.has_parser.return_value = True
    mock_parser_registry.parse.return_value = {"parsed_key": "val"}
    
    executor._registry._parser_registry = mock_parser_registry
    
    res = executor._try_parse_output(step, result)
    assert res["findings"] == {"parsed_key": "val"}
