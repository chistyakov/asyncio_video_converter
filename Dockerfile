FROM python:3.6

VOLUME /input

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

WORKDIR converter_to_hls

CMD python main.py