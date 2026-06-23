ARG PYTHON_VERSION=3.11
ARG SIYARIX_VERSION=3.0.0

FROM python:${PYTHON_VERSION}-slim AS base

WORKDIR /app

LABEL org.opencontainers.image.licenses="AGPL-3.0-or-later" \
      org.opencontainers.image.source="https://github.com/mufthakherul/siyarix" \
      org.opencontainers.image.title="siyarix" \
      org.opencontainers.image.description="AI Cybersecurity Orchestration Agent" \
      org.opencontainers.image.version="${SIYARIX_VERSION}" \
      org.opencontainers.image.vendor="MD MUFTHAKHERUL ISLAM MIRAZ"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive \
    SIYARIX_VERSION=${SIYARIX_VERSION}

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

FROM base AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md LICENSE ./
COPY src/ src/
RUN pip install --user ".[all]"

FROM base AS production

RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && update-ca-certificates

RUN groupadd -r siyarix && useradd -m -r -g siyarix siyarix

COPY --from=builder --chown=siyarix:siyarix /root/.local /home/siyarix/.local

USER siyarix
ENV PATH=/home/siyarix/.local/bin:$PATH \
    SIYARIX_HOME=/home/siyarix/.siyarix \
    SIYARIX_NO_TELEMETRY=1

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ["siyarix", "--help"]

ENTRYPOINT ["siyarix"]
CMD ["--help"]

FROM base AS development

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    git \
    make \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md LICENSE ./
COPY src/ src/
RUN pip install --user ".[all,dev]"
COPY tests/ tests/
COPY .pre-commit-config.yaml ./
ENV PATH=/root/.local/bin:$PATH \
    SIYARIX_DEBUG=1
ENTRYPOINT ["bash"]
