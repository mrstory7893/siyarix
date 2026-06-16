from __future__ import annotations
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import os
from siyarix.core import AgentCore, AgentMode

@pytest.mark.asyncio
async def test_agent_start_shutdown():
    agent = AgentCore(mode=AgentMode.AUTONOMOUS)
    with patch("asyncio.get_running_loop") as mock_loop:
        mock_loop.return_value.add_signal_handler = MagicMock()
        with patch.object(agent, "initialize", new_callable=AsyncMock) as mock_init:
            with patch.object(agent.executor_registry, "close", new_callable=AsyncMock) as mock_er_close:
                with patch.object(agent.executor_autonomous, "close", new_callable=AsyncMock) as mock_ea_close:
                    await agent.start()
                    mock_init.assert_called_once()
                    
                    await agent.shutdown()
                    mock_er_close.assert_called_once()
                    mock_ea_close.assert_called_once()

@pytest.mark.asyncio
async def test_agent_initialize():
    agent = AgentCore(mode=AgentMode.AUTONOMOUS)
    with patch.object(agent.registry, "discover_from_path") as mock_discover:
        with patch.object(agent.registry, "scan_path") as mock_scan:
            with patch.object(agent.planner_registry, "build_index") as mock_build_index:
                with patch.object(agent._event_bus, "emit", new_callable=AsyncMock):
                    await agent.initialize()
                    mock_discover.assert_called_once()
                    mock_scan.assert_called_once()
                    mock_build_index.assert_called_once()
