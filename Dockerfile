FROM continuumio/miniconda3:latest

WORKDIR /app

# Install dependencies
COPY environment.yml .
RUN conda env create -f environment.yml
RUN /opt/conda/envs/mybackend/bin/pip install redis
# Copy app source code
COPY . .

# Make the startup script executable
RUN chmod +x run_all.sh

# Activate conda env and run app
CMD ["bash", "-c", "source activate mybackend && ./run_all.sh"]
