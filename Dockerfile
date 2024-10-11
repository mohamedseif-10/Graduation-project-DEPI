# Use an official Python runtime as a parent image
FROM python:3.9.1-slim

# Set the working directory in the container
WORKDIR /app

# Copy all the .py and .ipynb files to the container
COPY *.py /app/
COPY *.ipynb /app/

# Install Jupyter and any other required dependencies from a requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Jupyter if it's not included in requirements.txt
RUN pip install jupyter

# Expose port 8888 for Jupyter Notebook
EXPOSE 8888

# Run Jupyter notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
