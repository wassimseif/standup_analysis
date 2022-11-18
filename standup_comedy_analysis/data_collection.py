from standup_comedy_analysis.Project import Project
import whisper
import yt_dlp
from typing import Iterator, TextIO
import os

with open(Project.data_dir / "input_data.txt") as fp:
    video_ids = fp.readlines()

video_ids = [v.strip().replace("\n", "") for v in video_ids]

model_name = "large"

model = whisper.load_model(model_name)


def srt_format_timestamp(seconds: float):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000
    return (f"{hours}:") + f"{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def get_audio(url):

    ydl = yt_dlp.YoutubeDL(
        {
            "quiet": True,
            "verbose": False,
            "format": "bestaudio",
            "outtmpl": str(Project.export_dir / "%(id)s.%(ext)s"),
            "postprocessors": [
                {
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                    "key": "FFmpegExtractAudio",
                }
            ],
        }
    )

    result = ydl.extract_info(url, download=True)
    print(f"Downloaded video \"{result['title']}\". Generating subtitles...")
    return result["title"], f"{result['id']}.mp3"


def write_srt(transcript: Iterator[dict], file: TextIO):
    count = 0
    for segment in transcript:
        count += 1
        print(
            f"{count}\n"
            f"{srt_format_timestamp(segment['start'])} --> {srt_format_timestamp(segment['end'])}\n"
            f"{segment['text'].replace('-->', '->').strip()}\n",
            file=file,
            flush=True,
        )


def proces_video(video_id: str):
    url = f"https://www.youtube.com/watch?v={video_id}"
    title, path = get_audio(url)
    result = model.transcribe(path)
    srt_path = Project.export_dir, f"{path}.srt"
    with open(srt_path, "w", encoding="utf-8") as srt:
        write_srt(result["segments"], file=srt)

    print("Saved SRT to", os.path.abspath(srt_path))


if __name__ == "__main__":
    proces_video(video_id=video_ids[0])
