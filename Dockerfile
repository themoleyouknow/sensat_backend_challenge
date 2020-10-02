FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

# Image metadata
LABEL maintainer="Maurice Zard"
LABEL version="0.1"
LABEL description="Sensat Backend Challenge"

# This system supports the C.UTF-8 locale which is recommended,
# Tell Flask where to find the application instance,
# Append packages to the Python path
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV FLASK_APP=/usr/src/sensat_backend_challenge/server.py

# Define the working directory of the current Docker container
WORKDIR /usr/src/sensat_backend_challenge

# Copy the current folder to the working directory
COPY . .

# Make this current working directory
RUN cd /usr/src/sensat_backend_challenge

# Install dependencies:
RUN pip install -r requirements.txt

# Expose the container's port to the host OS
EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]