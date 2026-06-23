# SPDX-License-Identifier: AGPL-3.0-or-later

from __future__ import annotations

from ..manager import ProviderManager
from .anthropic import register_profile as register_anthropic
from .azure import register_profile as register_azure
from .cerebras import register_profile as register_cerebras
from .deepseek import register_profile as register_deepseek
from .fireworks import register_profile as register_fireworks
from .gemini import register_profile as register_gemini
from .groq import register_profile as register_groq
from .huggingface import register_profile as register_huggingface
from .llamacpp import register_profile as register_llamacpp
from .lmstudio import register_profile as register_lmstudio
from .localai import register_profile as register_localai
from .minimax import register_profile as register_minimax
from .mistral import register_profile as register_mistral
from .moonshot import register_profile as register_moonshot
from .nvidia import register_profile as register_nvidia
from .ollama import register_profile as register_ollama
from .openai import register_profile as register_openai
from .opencode_zen import register_profile as register_opencode_zen
from .openrouter import register_profile as register_openrouter
from .perplexity import register_profile as register_perplexity
from .registry import register_profile as register_registry
from .together import register_profile as register_together
from .vllm import register_profile as register_vllm
from .xai import register_profile as register_xai
from .zai import register_profile as register_zai


def register_all_profiles(manager: ProviderManager) -> None:
    register_openai(manager)
    register_anthropic(manager)
    register_gemini(manager)
    register_groq(manager)
    register_together(manager)
    register_openrouter(manager)
    register_deepseek(manager)
    register_xai(manager)
    register_mistral(manager)
    register_perplexity(manager)
    register_cerebras(manager)
    register_fireworks(manager)
    register_zai(manager)
    register_minimax(manager)
    register_moonshot(manager)
    register_nvidia(manager)
    register_opencode_zen(manager)
    register_huggingface(manager)
    register_azure(manager)
    register_ollama(manager)
    register_lmstudio(manager)
    register_llamacpp(manager)
    register_vllm(manager)
    register_localai(manager)
    register_registry(manager)


__all__ = [
    "register_all_profiles",
]
