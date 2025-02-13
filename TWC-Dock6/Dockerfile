# Use NVIDIA CUDA base image
FROM nvidia/cuda:12.4.0-base-ubuntu22.04

# Set working directory
WORKDIR /dock6

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential cmake gfortran libopenmpi-dev \
    python3 python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Install Jupyter Notebook
RUN pip3 install notebook

# Install OpenMM for GPU-accelerated AMBER scoring
RUN pip3 install --no-cache-dir openmm

# Copy dock6.tar.gz from local machine into the container
COPY dock.6.12_source.tar.gz /dock6/

# Extract and install DOCK6
RUN tar -xvzf dock.6.12_source.tar.gz && rm dock.6.12_source.tar.gz

# Set environment variables for OpenMM
ENV OPENMM_PLATFORM CUDA

# Expose Jupyter Notebook port
EXPOSE 8888


# Start Jupyter Notebook with token
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=twc@211_huzaifa"]


