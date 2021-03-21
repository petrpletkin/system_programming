FROM debian:bullseye-slim
RUN apt-get update -y && apt-get install python3-pip -y
COPY ./ .
CMD ["python3",  "trigram_in_text.py"]
