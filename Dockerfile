FROM python

RUN pip3 install boto3

COPY bucket_actions.py .
COPY copyscript.py .

ENTRYPOINT ["python3", "copyscript.py"]
