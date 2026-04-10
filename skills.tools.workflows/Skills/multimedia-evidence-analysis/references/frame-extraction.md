# Frame extraction from video evidence

After Phase 2 identifies key moments in a video, grab those frames as stills for exhibit use. The firm ships an `extract_video_frames.py` helper that wraps `ffmpeg` and writes JPEGs at the requested timestamps.

## When to extract a frame

- Traffic violation visible (red light run, lane departure, stop-sign roll)
- Moment of impact
- Visible vehicle damage
- Visible injuries to the client
- Scene conditions: weather, lighting, road surface, signage
- Anything that proves or disproves a disputed fact

## Invocation

```bash
python <tools-path>/extract_video_frames.py \
  cases/<slug>/documents/<category>/<video>.mp4 \
  00:01:15 \
  00:02:30 \
  00:03:45
```

Pass the source video as the first argument and one or more `HH:MM:SS` timestamps after it. The tool writes JPEGs to the working directory by default; route outputs to:

```
cases/<slug>/documents/photos/<source>-<YYYY-MM-DD>/<HH-MM-SS>.jpg
```

Where `<source>` is a short stable identifier for the video (e.g. `dashcam`, `bodycam-kelly`, `surveillance-bp`). Create the per-day subfolder so multiple extractions from the same source don't collide.

## Logging

Add a row to the "Extracted Frames" table in the analysis memo for each frame, referencing the file path. Include a one-line description of what the frame shows and why it matters.
