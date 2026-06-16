import pytest
import json
from unittest.mock import MagicMock, AsyncMock, patch

from siyarix.core.pipeline import CommandPipeline, PipelineStep, PipelineResult
from siyarix.core.swarm import SwarmRouter, SwarmTask, ReconAgent, ExploitAgent, ReportAgent
from siyarix.core.learning import ContinuousLearning, Experience

def test_pipeline_parse():
    pipeline = CommandPipeline()
    
    steps = pipeline.parse("scan 127.0.0.1")
    assert len(steps) == 1
    assert steps[0].instruction == "scan 127.0.0.1"
    
    steps = pipeline.parse("scan | grep open | report")
    assert len(steps) == 3
    assert steps[1].instruction == "grep open"
    
    steps = pipeline.parse("scan then report")
    assert len(steps) == 2
    
    steps = pipeline.parse("scan and then exploit")
    assert len(steps) == 2
    
    steps = pipeline.parse("scan followed by report")
    assert len(steps) == 2

@pytest.mark.asyncio
async def test_pipeline_execute():
    pipeline = CommandPipeline()
    steps = [PipelineStep(instruction="test 1", step_id="1"), PipelineStep(instruction="test 2", step_id="2")]
    
    async def mock_executor(step, ctx):
        if step.instruction == "test 1":
            return {"status": "completed", "findings": ["A"], "output": "Done 1"}
        elif step.instruction == "test 2":
            return {"status": "failed"}
    
    result = await pipeline.execute(steps, mock_executor)
    assert result.steps_completed == 1
    assert result.steps_failed == 1
    assert result.success is False
    assert result.all_findings == ["A"]

@pytest.mark.asyncio
async def test_pipeline_execute_exception():
    pipeline = CommandPipeline()
    steps = [PipelineStep(instruction="fail", step_id="1")]
    
    async def mock_executor(step, ctx):
        raise ValueError("Boom")
        
    result = await pipeline.execute(steps, mock_executor)
    assert result.steps_failed == 1
    assert result.success is False

@pytest.mark.asyncio
async def test_swarm_router():
    router = SwarmRouter()
    
    with patch("asyncio.sleep", new_callable=AsyncMock):
        res = await router.run_campaign("127.0.0.1")
        assert res["recon_result"] is not None
        assert res["exploit_result"] is not None
        assert res["report_result"] is not None
        assert "Mock findings by ReconAgent" in res["recon_result"]["findings"]

@pytest.mark.asyncio
async def test_continuous_learning_get_embedding():
    mock_memory = MagicMock()
    cl = ContinuousLearning(memory=mock_memory)
    
    emb1 = await cl._get_embedding("test_text")
    assert len(emb1) in (32, 1536)
    
    emb2 = await cl._get_embedding("test_text")
    assert emb1 == emb2

@pytest.mark.asyncio
async def test_continuous_learning_record_experience():
    mock_memory = MagicMock()
    cl = ContinuousLearning(memory=mock_memory)
    
    exp = Experience(target="10.0.0.1", action="scan", result="success", success=True)
    await cl.record_experience(exp)
    
    assert mock_memory.store.call_count == 1
    args, kwargs = mock_memory.store.call_args
    stored_data = json.loads(kwargs["value"])
    assert stored_data["target"] == "10.0.0.1"

def test_cosine_similarity():
    mock_memory = MagicMock()
    cl = ContinuousLearning(memory=mock_memory)
    
    v1 = [1.0, 0.0]
    v2 = [1.0, 0.0]
    v3 = [0.0, 1.0]
    
    assert cl._cosine_similarity(v1, v2) == 1.0
    assert cl._cosine_similarity(v1, v3) == 0.0
    assert cl._cosine_similarity([], []) == 0.0
    assert cl._cosine_similarity([0.0], [0.0]) == 0.0

@pytest.mark.asyncio
async def test_continuous_learning_query():
    mock_memory = MagicMock()
    
    cl = ContinuousLearning(memory=mock_memory)
    emb = await cl._get_embedding("Target: 10.0.0.1 | Action: scan")
        
    mock_entry = MagicMock()
    mock_entry.value = json.dumps({
        "target": "10.0.0.1",
        "action": "scan",
        "result": "success",
        "success": True,
        "embedding": emb
    })
    
    mock_memory.search.return_value = [mock_entry]
    
    results = await cl.query_similar_experiences("scan", "10.0.0.1")
    
    assert len(results) == 1
    assert results[0].action == "scan"
