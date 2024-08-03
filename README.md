# Docker Image Size at Different Stages

| Stage                                         |   Image Size      |
|-----------------------------------------------|-------------------|
| Base Python 3.11.9-slim-bookworm image        |         129.91 MB |
| Added FastAPI project with poetry             |         217.09 MB |
| Install packages via poetry                   |         268.28 MB |
| Added multi stage and copy venv with project  |         171.95 MB |
| Installed ffmpeg in runtime image             |         796.75 MB |
| Added openai-whisper v20231117                |           6.14 GB |