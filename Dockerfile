FROM python:3.9
WORKDIR /gtkm
COPY requirements.txt /gtkm/
RUN pip3 install -r requirements.txt
COPY . /gtkm/
CMD ["uvicorn", "gtkm.main:app", "--reload", "--host", "0.0.0.0", "--env-file", ".env"]