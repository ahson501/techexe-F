# Use NVIDIA CUDA base image for GPU support
FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

# Set working directory
WORKDIR /dock6

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential cmake gfortran libopenmpi-dev \
    flex bison git wget curl \
    python3 python3-pip python3-venv \
    csh tcsh \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /miniconda.sh && \
    chmod +x /miniconda.sh && \
    /miniconda.sh -b -p /opt/conda && \
    rm /miniconda.sh

# Set Conda environment variables
ENV PATH="/opt/conda/bin:$PATH"
ENV CONDA_ENV_NAME="openmm-env"

# Create Conda environment with OpenMM, CUDA, and Jupyter
RUN conda create -n $CONDA_ENV_NAME -c conda-forge openmm cudatoolkit=11.8 openmmtools openmmforcefields jupyter -y

# Ensure Conda is initialized for all shells
RUN echo ". /opt/conda/etc/profile.d/conda.sh && conda activate $CONDA_ENV_NAME" >> /etc/profile
RUN echo ". /opt/conda/etc/profile.d/conda.sh && conda activate $CONDA_ENV_NAME" >> /root/.bashrc

# Verify Jupyter installation
RUN /opt/conda/bin/conda run -n $CONDA_ENV_NAME jupyter --version

# Set default shell to Bash for Conda activation
SHELL ["/bin/bash", "-c"]

# Copy DOCK6 source code into the container
COPY dock.6.12_linux.tar.gz /dock6/

# Extract and install DOCK6
RUN tar -xvzf dock.6.12_linux.tar.gz && rm dock.6.12_linux.tar.gz

# Move into the correct directory
WORKDIR /dock6/dock6/install

# Build DOCK6
RUN ls -l && ./configure gnu && make install -j$(nproc)

# Set environment variables for OpenMM & DOCK6
ENV OPENMM_PLATFORM=CUDA
ENV PATH="/dock6/dock6/bin:$PATH"
ENV LD_LIBRARY_PATH="/usr/local/cuda/lib64:/opt/conda/envs/$CONDA_ENV_NAME/lib:$LD_LIBRARY_PATH"
ENV DOCK6_HOME="/dock6/dock6"
ENV DOCK6_BIN="/dock6/dock6/bin"

# Verify CUDA installation
RUN nvcc --version

# Test OpenMM CUDA support
RUN bash -c "source /opt/conda/etc/profile.d/conda.sh && \
    conda activate $CONDA_ENV_NAME && \
    python -c \"import openmm as mm; print([mm.Platform.getPlatform(i).getName() for i in range(mm.Platform.getNumPlatforms())])\""

# Run Jupyter by default
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--notebook-dir=/tf/notebooks", "--allow-root"]
