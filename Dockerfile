FROM python:3.6
RUN echo 'deb http://deb.debian.org/debian jessie-backports main contrib non-free' >> /etc/apt/sources.list.d/backports.list
RUN echo 'deb http://deb.debian.org/debian jessie-backports-sloppy main contrib non-free' >> /etc/apt/sources.list.d/backports.list
RUN apt-get update && apt-get install -y ffmpeg

ENV HOST=0.0.0.0
ENV PORT=8080
ENV TASKS_LIMIT=5
ENV OUTPUT_DIR=/output
ENV INPUT_DIR=/input

VOLUME /input

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

WORKDIR converter_to_hls

CMD python main.py