# Retrieval Event

## Requirements

```bash
Docker 
Docker Compose 
```

## Prepare data
Extract keyframe from video by

```bash
ffmpeg -skip_frame nokey -i test.mp4 -vsync vfr -frame_pts true out-%02d.jpeg
```

## Deploy

```bash
make up_services 
```