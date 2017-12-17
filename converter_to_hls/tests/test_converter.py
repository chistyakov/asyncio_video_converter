# TODO: add more unittests for the ConvertManager and ConvertTask
import asyncio
from unittest.mock import patch

from asynctest.mock import patch as async_patch

from services.transcoding import ConvertTask


async def test_run_converter_task_runs_ffmpeg_subprocess(loop):
    with async_patch('asyncio.create_subprocess_exec') as mock_subprocess_exec, (
         patch('os.path.exists', return_value=True)), (
         patch('os.makedirs', return_value=True)), (
         patch('services.transcoding.manager.ConvertTask.build_task_id', return_value='uuid')):
        task = ConvertTask(filename='foo', config={
                               'input_dir': '/input',
                               'output_dir': '/output',
                               'tasks_limit': 2
                           }, loop=loop, executor=None)
        await task.run()
        mock_subprocess_exec.assert_called_once_with(
            'ffmpeg', '-i', '/input/foo', '-c:v', 'h264',
            '-f', 'hls', '-hls_list_size', '0', '-hls_playlist_type', 'vod',
            '/output/uuid/playlist.m3u8',
            loop=loop,
            stdout=asyncio.subprocess.PIPE,
        )
