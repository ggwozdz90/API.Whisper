<div align="center">

![Build Status](https://github.com/ggwozdz90/API.Whisper/actions/workflows/ci.yml/badge.svg)

[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=ggwozdz90_API.Whisper&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=ggwozdz90_API.Whisper)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=ggwozdz90_API.Whisper&metric=bugs)](https://sonarcloud.io/summary/new_code?id=ggwozdz90_API.Whisper)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=ggwozdz90_API.Whisper&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=ggwozdz90_API.Whisper)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=ggwozdz90_API.Whisper&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=ggwozdz90_API.Whisper)
![Coverage](https://sonarcloud.io/api/project_badges/measure?project=ggwozdz90_API.Whisper&metric=coverage)

[![Known Vulnerabilities](https://snyk.io/test/github/ggwozdz90/API.Whisper/badge.svg)](https://snyk.io/test/github/ggwozdz90/API.Whisper)

</div>

# API Usage

## Authentication

To interact with the API, you must first authenticate and obtain a token. This is done by making a POST request to the `/login` endpoint.

### Request

- **Endpoint**: `/login`
- **Method**: POST
- **Payload**: Refer to `login_router.py` for the request payload structure.

### Response

- **Payload**: Refer to `login_router.py` for the response payload structure.

The response will include a token that you will use for subsequent requests.

## Transcription

Once you have obtained the token, you can use it to make requests to the `/transcribe` endpoint. The token should be included in the `X-Token` header.

### Request

- **Endpoint**: `/transcribe`
- **Method**: POST
- **Headers**:
  - `x-token`: The token received from the `/login` endpoint.
- **Payload**: Refer to `transcribe_router.py` for the request payload structure.

### Response

- **Payload**: Refer to `transcribe_router.py` for the response payload structure.


## Example Usage
```bash
# Step 1: Obtain the token
curl -X POST "http://your-api-url/login" -H "Content-Type: application/json" -d '{"email": "your-email@example.com"}'

# Step 2: Use the token to transcribe an audio file
curl -X POST "http://your-api-url/transcribe" -H "x-token: your-token" -F "file=@path-to-your-audio-file"
```


# Docker Image Size at Different Stages

| Stage                                         |   Image Size      |
|-----------------------------------------------|-------------------|
| Base Python 3.11.9-slim-bookworm image        |         129.91 MB |
| Added FastAPI project with poetry             |         217.09 MB |
| Install packages via poetry                   |         268.28 MB |
| Added multi stage and copy venv with project  |         171.95 MB |
| Installed ffmpeg in runtime image             |         796.75 MB |
| Added openai-whisper v20231117                |           6.14 GB |
| Updated Python image to 3.12.4-slim-bookworm  |           6.14 GB |
| Installed ffmpeg --no-install-recommends      |           5.98 GB |