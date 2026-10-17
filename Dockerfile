# Use a lean official Python base image (CPU-only, ultra-fast)
FROM python:3.12-slim

# Prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies required for building packages, git, curl, and wget
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:$PATH"

# Install Julia
RUN wget https://julialang-s3.julialang.org/bin/linux/x64/1.10/julia-1.10.4-linux-x86_64.tar.gz \
    && tar zxvf julia-1.10.4-linux-x86_64.tar.gz \
    && cp -r julia-1.10.4 /opt/julia \
    && ln -s /opt/julia/bin/julia /usr/local/bin/julia \
    && rm julia-1.10.4-linux-x86_64.tar.gz

# Install uv using the official standalone installer
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory inside the container
WORKDIR /workspace

VOLUME ["/workspace", "/models"]

# Copy dependency definition files first to leverage Docker layer caching
COPY pyproject.toml uv.lock ./

# Install Python and project dependencies using uv
RUN uv sync --frozen --no-dev

# Ensure the virtual environment's binaries and Rust are in the path
ENV PATH="/workspace/.venv/bin:/root/.cargo/bin:$PATH"

# Expose default port for Jupyter Lab
EXPOSE 8888

# Default command to run when starting the container
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]