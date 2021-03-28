FROM python:3.8.5

# Install JDK
RUN apt update -y && apt install -y default-jdk
RUN java --version

# Upgrade pip
RUN python -m pip install --upgrade pip

# work dir
WORKDIR /ApkColluding

# Copy requirements.txt and install all dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy all files in server directory
COPY . .

CMD [ "python", "./main.py" ]