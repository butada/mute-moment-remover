from moviepy.editor import VideoFileClip, concatenate_videoclips
import numpy as np

INPUT_VIDEO = 'input.mp4'
OUTPUT_VIDEO = 'output.mp4'
AUDIO_THREASHOLD = 0.15

def remove_silence_from_video(input_video, output_video, audio_threshold=0.01, min_silence_duration=1.0):
    # Load video
    video = VideoFileClip(input_video)
    audio = video.audio.to_soundarray(fps=22000)
    
    # Function to determine if a chunk is silent
    is_silent = lambda arr: np.max(np.abs(arr)) < audio_threshold
    
    # Split audio into chunks and identify silent chunks
    chunk_size = int(min_silence_duration * 22000)  # Assuming 22000 fps for audio
    silent_chunks = []
    for i in range(0, len(audio), chunk_size):
        chunk = audio[i:i+chunk_size]
        if is_silent(chunk):
            silent_chunks.append((i/22000, (i+len(chunk))/22000))
    
    # Identify the non-silent parts of the video
    non_silent_parts = []
    start = 0
    for silent_start, silent_end in silent_chunks:
        non_silent_parts.append((start, silent_start))
        start = silent_end
    non_silent_parts.append((start, video.duration))
    
    # Concatenate non-silent parts of the video
    final = concatenate_videoclips([video.subclip(start, end) for start, end in non_silent_parts])
    
    # Write the result to a file
    final.write_videofile(output_video, codec='libx264', audio_codec='aac')

# Example usage
remove_silence_from_video(INPUT_VIDEO, OUTPUT_VIDEO, audio_threshold=AUDIO_THREASHOLD)

