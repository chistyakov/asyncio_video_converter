import asyncio
import logging
import os

import async_timeout

from services.utils import makedirs, path_exists
from .exceptions import FailedToStartConvertation
from .tasks import Task, State

logger = logging.getLogger(__name__)

FFMPEG_BIN_PATH = 'ffmpeg'
CODEC_ARGS = ('-c:v', 'h264')
OUTPUT_ARGS = ('-f', 'hls', '-hls_list_size', '0', '-hls_playlist_type', 'vod')
PLAYLIST_NAME = 'playlist.m3u8'

STOP_FFMPEG_TIMEOUT_IN_SEC = 5


class ConvertTask(Task):
    def __init__(self, filename, config, loop, executor):
        super().__init__()
        self.filename = filename
        self.config = config
        self._loop = loop
        self._executor = executor

        self._ffmpeg_proc = None

    async def run(self):
        if not await path_exists(self.input_path, loop=self._loop, executor=self._executor):
            raise FileNotFoundError(f'The file {self.filename} does not exist')

        if await makedirs(self.output_path_dir, loop=self._loop, executor=self._executor):
            await self.start_ffmpeg()
        return self

    @property
    def input_path(self):
        return os.path.join(self.config['input_dir'], self.filename)

    async def start_ffmpeg(self):
        args = [
            FFMPEG_BIN_PATH,
            '-i', self.input_path,
            *CODEC_ARGS,
            *OUTPUT_ARGS, self.output_path,
        ]
        logger.info('run ffmpeg with args:\n%s', ' '.join(args))
        try:
            self._ffmpeg_proc = await asyncio.create_subprocess_exec(
                *args,
                loop=self._loop,
                stdout=asyncio.subprocess.PIPE,
            )
            return self._ffmpeg_proc
        except Exception as e:
            logger.exception(
                'Exception on starting ffmpeg for %s (task_id: %s)',
                self.filename, self.task_id
            )
            raise FailedToStartConvertation(task_id=self.task_id) from e

    @property
    def output_path(self):
        return os.path.join(self.config['output_dir'], self.relative_output_path)

    @property
    def relative_output_path(self):
        return os.path.join(self.task_id, PLAYLIST_NAME)

    @property
    def output_path_dir(self):
        return os.path.join(self.config['output_dir'], self.task_id)

    async def stop(self, timeout=STOP_FFMPEG_TIMEOUT_IN_SEC):
        if self.state != State.IN_PROGRESS:
            logger.warning('ffmpeg for the task %s is not running', self.task_id)
            return
        try:
            async with async_timeout.timeout(timeout, loop=self._loop):
                await self._ffmpeg_proc.communicate(input=b'q')

        except (asyncio.TimeoutError, ValueError):
            logger.warning('Timeout on closing ffmpeg for task %s.'
                           'The process will be killed', self.task_id)
            self._ffmpeg_proc.kill()

    @property
    def state(self):
        if self._ffmpeg_proc is None:
            return State.FAILED_TO_START
        if self._ffmpeg_proc.returncode is None:
            return State.IN_PROGRESS
        if self._ffmpeg_proc.returncode == 0:
            return State.FINISHED_SUCCESSFULLY
        else:
            return State.FINISHED_WITH_ERROR

    def __repr__(self):
        return f'Convert task for {self.filename} ({self.task_id}) {self.state}'

    @property
    def result(self):
        if self.state == State.FAILED_TO_START:
            return None
        else:
            return self.relative_output_path
