# Use the TensorFlow GPU image with Jupyter pre-installed
FROM tensorflow/tensorflow:2.2.2-gpu-py3-jupyter

# Set the working directory inside the container
WORKDIR /tf/notebooks

# Install any additional dependencies or libraries
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    matplotlib \
    scikit-learn \
    keras

# Expose the Jupyter Notebook port
EXPOSE 8888

# Default command to start Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
