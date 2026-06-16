# SPDX-License-Identifier: AGPL-3.0-or-later
"""Continuous Learning and Semantic Memory for Siyarix.

This module provides vector memory and experience tracking so the agent
can learn from past engagements and avoid repeating mistakes.
"""

from __future__ import annotations

import json
import logging
import math
from dataclasses import dataclass

from siyarix.memory import MemoryManager, MemoryLayer
from siyarix.providers import ProviderManager

logger = logging.getLogger(__name__)


@dataclass
class Experience:
    target: str
    action: str
    result: str
    success: bool
    embedding: list[float] | None = None


class ContinuousLearning:
    """Manages long-term semantic memory and learning from past actions."""

    def __init__(self, memory: MemoryManager) -> None:
        self.memory = memory
        self.providers = ProviderManager.get_instance()
        self._embedding_cache: dict[str, list[float]] = {}

    async def _get_embedding(self, text: str) -> list[float]:
        """Get vector embedding for text. Uses OpenAI/Ollama via ProviderManager if available, else simulated."""
        if text in self._embedding_cache:
            return self._embedding_cache[text]

        try:
            # First try OpenAI via ProviderManager
            api_key = self.providers.get_api_key("openai")
            if api_key:
                from openai import AsyncOpenAI
                client = AsyncOpenAI(api_key=api_key)
                response = await client.embeddings.create(
                    input=[text],
                    model="text-embedding-3-small"
                )
                embedding = response.data[0].embedding
                self._embedding_cache[text] = embedding
                return embedding

            # Try local Ollama if configured
            ollama_base = self.providers.get_base_url("ollama")
            if ollama_base:
                import httpx
                async with httpx.AsyncClient() as client:
                    resp = await client.post(f"{ollama_base.rstrip('/')}/api/embeddings", json={"model": "nomic-embed-text", "prompt": text})
                    if resp.status_code == 200:
                        embedding = resp.json().get("embedding")
                        if embedding:
                            self._embedding_cache[text] = embedding
                            return embedding

        except Exception as e:
            logger.debug("Real embedding failed or not configured, using simulated: %s", e)
            
        try:
            # Better simulated embedding using hashing for local usage
            import hashlib
            h = hashlib.sha256(text.encode('utf-8')).digest()
            # Convert hash bytes to a 32-dimensional float vector between -1 and 1
            embedding = [(b / 127.5) - 1.0 for b in h]
            self._embedding_cache[text] = embedding
            return embedding
        except Exception as e:
            logger.warning("Embedding simulation failed: %s", e)
            return [0.0] * 32

    def _cosine_similarity(self, v1: list[float], v2: list[float]) -> float:
        if not v1 or not v2 or len(v1) != len(v2):
            return 0.0
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm_a = math.sqrt(sum(a * a for a in v1))
        norm_b = math.sqrt(sum(b * b for b in v2))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    async def record_experience(self, exp: Experience) -> None:
        """Save a new experience to vector memory."""
        text_rep = f"Target: {exp.target} | Action: {exp.action} | Success: {exp.success} | Result: {exp.result}"
        exp.embedding = await self._get_embedding(text_rep)

        # Store in persistent memory
        key = f"exp_{hash(text_rep)}"
        self.memory.store(
            key=key,
            value=json.dumps(
                {
                    "target": exp.target,
                    "action": exp.action,
                    "result": exp.result,
                    "success": exp.success,
                    "embedding": exp.embedding,
                }
            ),
            layer=MemoryLayer.PERSISTENT,
            tags=["experience", "learning"],
        )
        logger.info("Recorded learning experience for action: %s", exp.action)

    async def query_similar_experiences(
        self, current_action: str, target: str, limit: int = 3
    ) -> list[Experience]:
        """Find similar past experiences to guide current decisions."""
        query_text = f"Target: {target} | Action: {current_action}"
        query_emb = await self._get_embedding(query_text)

        # Retrieve all experiences
        # In a production environment with millions of rows, this would be an HNSW/Faiss index
        all_exps = self.memory.search("experience", layer=MemoryLayer.PERSISTENT, limit=1000)

        scored_exps = []
        for entry in all_exps:
            try:
                data = json.loads(entry.value)
                if "embedding" in data and data["embedding"]:
                    score = self._cosine_similarity(query_emb, data["embedding"])
                    if score > 0.5:  # Threshold
                        scored_exps.append(
                            (
                                score,
                                Experience(
                                    target=data["target"],
                                    action=data["action"],
                                    result=data["result"],
                                    success=data["success"],
                                    embedding=data["embedding"],
                                ),
                            )
                        )
            except Exception:
                continue

        scored_exps.sort(key=lambda x: x[0], reverse=True)
        return [exp for score, exp in scored_exps[:limit]]
