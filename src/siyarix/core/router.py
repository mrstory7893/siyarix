# SPDX-License-Identifier: AGPL-3.0-or-later
"""Semantic routing for pre-filtering intents."""

from __future__ import annotations

import logging
import re
from typing import Any
from ..registry import RiskLevel

logger = logging.getLogger(__name__)

RiskTier = RiskLevel

class IntentRoute:
    def __init__(
        self, mode: str = "general", risk_tier: Any = None, requires_confirmation: bool = False
    ) -> None:
        self.mode = mode
        self.risk_tier = risk_tier or RiskTier("low")
        self.requires_confirmation = requires_confirmation

class IntentRouter:
    """Routes natural language queries to specialized contexts."""
    
    INTENTS = {
        "recon": re.compile(r"\b(scan|discover|recon|nmap|find|search|enumerate)\b", re.I),
        "exploit": re.compile(r"\b(exploit|attack|bypass|inject|crack|pwn|metasploit)\b", re.I),
        "report": re.compile(r"\b(report|summarize|export|document|generate)\b", re.I),
        "brute": re.compile(r"\b(brute|crack|password)\b", re.I),
        "web": re.compile(r"\b(web|http|nikto|nuclei)\b", re.I)
    }

    @classmethod
    def route(cls, command: str, **kwargs: Any) -> IntentRoute:
        """Return the identified intent or 'general'."""
        text_lower = command.lower()
        
        if cls.INTENTS["exploit"].search(text_lower):
            return IntentRoute(mode="exploit", risk_tier=RiskTier("high"), requires_confirmation=True)
        if cls.INTENTS["brute"].search(text_lower):
            return IntentRoute(mode="brute", risk_tier=RiskTier("high"), requires_confirmation=True)
        if cls.INTENTS["web"].search(text_lower):
            return IntentRoute(mode="web", risk_tier=RiskTier("medium"))
        if cls.INTENTS["recon"].search(text_lower):
            return IntentRoute(mode="recon", risk_tier=RiskTier("low"))
        if cls.INTENTS["report"].search(text_lower):
            return IntentRoute(mode="report", risk_tier=RiskTier("low"))
            
        return IntentRoute(mode="general", risk_tier=RiskTier("low"))
