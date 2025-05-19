import os
import re
import whisper
from typing import List, Tuple
from pydub import AudioSegment
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips
)
from moviepy.video.fx.all import crop

# --- CONFIGURATION ---
IMG_LIST = [
    "horror_images_filtered/horror_images_restore/001_sunny_suburban_street_with_horror_atmosphere/image_8.jpg",
    "horror_images_filtered/horror_images_restore/004_old_countryside_house_with_eerie_shadows/image_4.jpg",
    "horror_images_filtered/horror_images_restore/020_hallway_with_flickering_light_horror_style/image_2.jpg",
    "horror_images_filtered/horror_images_restore/023_wooden_staircase_in_haunted_mansion/image_6.jpg",
    "horror_images_filtered/horror_images_restore/047_attic_with_cobwebs_and_single_lightbulb/image_13.jpg",
    "horror_images_filtered/horror_images_restore/049_creepy_painting_with_glowing_red_eyes/image_8.jpg",
    "horror_images_filtered/horror_images_restore/054_wall_mirror_in_haunted_horror_room/image_3.jpg",
    "horror_images_filtered/horror_images_restore/150_bloody_writing_on_mirror_horror/image_3.jpg"
]

AUDIO_FOLDER = "Audios"
BGM_PATH = "BG_MUSIC/BGM.mp3"
OUTPUT_FOLDER = "FinalShorts"
FINAL_VIDEO_PATH = os.path.join(OUTPUT_FOLDER, "combined_shorts.mp4")

# --- UTILITIES ---

def load_audio_files(folder: str) -> List[str]:
    return sorted([f for f in os.listdir(folder) if f.endswith(".wav")])

def mix_audio_with_bgm(main_audio: AudioSegment, bgm: AudioSegment) -> AudioSegment:
    bgm_loop = bgm * (len(main_audio) // len(bgm) + 1)
    return main_audio.overlay(bgm_loop[:len(main_audio)])

def combine_all_audio(audio_files: List[str], bgm: AudioSegment) -> Tuple[str, List[float]]:
    combined = AudioSegment.empty()
    durations = []

    for file in audio_files:
        main_audio = AudioSegment.from_file(os.path.join(AUDIO_FOLDER, file))
        mixed = mix_audio_with_bgm(main_audio, bgm)
        durations.append(len(mixed) / 1000)  # duration in seconds
        combined += mixed

    output_path = "temp_full_audio.wav"
    combined.export(output_path, format="wav")
    return output_path, durations

def transcribe_audio(path: str, model) -> List[dict]:
    result = model.transcribe(path, word_timestamps=False)
    return result["segments"]

def compute_image_switch_points(durations: List[float]) -> List[float]:
    switch_times = []
    cum_time = 0
    for dur in durations:
        cum_time += dur
        switch_times.append(cum_time)
    return switch_times

def get_image_for_time(t: float, switch_times: List[float], img_list: List[str]) -> str:
    for i, switch in enumerate(switch_times):
        if t < switch:
            return img_list[i % len(img_list)]
    return img_list[-1]

def create_video_and_subtitle_clips(segments: List[dict], switch_times: List[float]) -> Tuple[List[ImageClip], List[TextClip]]:
    video_clips = []
    subtitle_clips = []

    for seg in segments:
        text = seg['text'].strip()
        if not text:
            continue
        start, end = seg['start'], seg['end']
        image_path = get_image_for_time(start, switch_times, IMG_LIST)

        image_clip = (
            ImageClip(image_path)
            .set_start(start)
            .set_duration(end - start)
            .resize(height=1920)
        )
        image_clip = crop(image_clip, width=1080, height=1920, x_center=image_clip.w / 2)

        txt_clip = (
            TextClip(text, fontsize=50, color='white', font='Arial-Bold', method='caption', size=(1000, None))
            .set_position(("center", 1600))
            .set_start(start)
            .set_duration(end - start)
        )

        video_clips.append(image_clip)
        subtitle_clips.append(txt_clip)

    return video_clips, subtitle_clips

def create_final_video(video_clips: List[ImageClip], subtitle_clips: List[TextClip], audio_path: str, output_path: str):
    print("🎬 Combining video and subtitles...")
    composite = CompositeVideoClip(video_clips + subtitle_clips)
    final_audio = AudioFileClip(audio_path)
    final_video = composite.set_audio(final_audio)

    final_video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")
    print("✅ Final video saved to:", output_path)

# --- MAIN DRIVER ---

def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    print("📂 Loading audio files...")
    audio_files = load_audio_files(AUDIO_FOLDER)

    print("🎵 Loading background music...")
    bg_music = AudioSegment.from_file(BGM_PATH).apply_gain(-18)

    print("🔊 Combining and mixing all audio files...")
    combined_audio_path, durations = combine_all_audio(audio_files, bg_music)
    switch_times = compute_image_switch_points(durations)

    print("🧠 Loading Whisper model...")
    model = whisper.load_model("base")

    print("📝 Transcribing full audio...")
    segments = transcribe_audio(combined_audio_path, model)

    print("🎞️ Generating clips and subtitles...")
    video_clips, subtitle_clips = create_video_and_subtitle_clips(segments, switch_times)

    create_final_video(video_clips, subtitle_clips, combined_audio_path, FINAL_VIDEO_PATH)

    os.remove(combined_audio_path)
    print("🧹 Cleaned up temporary files.")

if __name__ == "__main__":
    main()
