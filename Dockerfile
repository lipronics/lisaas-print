FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y cups libcups2-dev && \
    pip install pycups

# Optional: Expose CUPS web interface
EXPOSE 631

COPY requirements.txt /
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r /requirements.txt

COPY print.py /app/print.py
WORKDIR /app

CMD ["python", "print.py"]