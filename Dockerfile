FROM python:3.11

# Clone the repository
RUN git clone https://github.com/NupaZzz/joyreactor

# Install dependencies
WORKDIR /joyreactor
RUN pip install -r requirements.txt

# Create config directory
RUN mkdir /joyreactor/config

# Create token.py file with token value
ARG TOKEN
RUN echo "TOKEN = '${TOKEN}'" > /joyreactor/config/token.py

# Set entrypoint
WORKDIR /joyreactor
ENTRYPOINT [ "python3", "main.py" ]