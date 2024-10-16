FROM python:3.10-slim-bullseye

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy requirements.txt for package installation
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Install Streamlit if it's not included in requirements.txt
RUN pip install streamlit

# Expose port 8501 for Streamlit (not 80, since Streamlit runs on 8501)
EXPOSE 8501

# Command to run the Streamlit app
CMD ["sh", "-c", "cd web_app && streamlit run 🏠_Home.py --server.enableCORS=false --server.address=0.0.0.0"]
