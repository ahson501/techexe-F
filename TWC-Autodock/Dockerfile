# Use a CUDA base image with a newer Ubuntu version
FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

# Set environment variables for non-interactive installations
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory inside the container
WORKDIR /data

# Expose the container's data directory as a volume
VOLUME /data

# Install necessary dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    gzip \
    git \
    build-essential \
    make \
    gcc \
    g++ && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set CUDA environment variables
ENV GPU_LIBRARY_PATH="/usr/local/cuda/lib64"  
ENV GPU_INCLUDE_PATH="/usr/local/cuda/include"  
ENV PATH="/usr/local/cuda/bin:${PATH}"
ENV CUDADIR="/usr/local/cuda"
ENV CUDA_HOME="/usr/local/cuda"
ENV LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH}"


# Download the AutoDock-GPU repository as a .zip file and unzip it
RUN wget https://github.com/ccsb-scripps/AutoDock-GPU/archive/refs/heads/develop.zip -O /data/develop.zip && ls -al /data
         
# Set the working directory to /data/AD-GPU_set_of_42/AutoDock-GPU-develop
WORKDIR /data/AD-GPU_set_of_42/AutoDock-GPU-develop

# Set entrypoint (replace with correct command to run AutoDock-GPU once it is built)
CMD ["sh", "-c", "echo 'AutoDock-GPU build complete. Please run appropriate commands to start the service.'"]
