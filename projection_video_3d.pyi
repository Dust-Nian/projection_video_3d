def verify_ffmpeg(ffmpeg_path: str) -> bool:
    """
    验证 ffmpeg 是否可用

    Args:
        ffmpeg_path: ffmpeg 可执行文件路径

    Returns:
        bool: ffmpeg 是否可用
    """
    ...

def extract_audio(ffmpeg_path: str, input_path: str, output_path: str) -> bool:
    """
    从视频中提取音频

    Args:
        ffmpeg_path: ffmpeg 可执行文件路径
        input_path: 输入视频路径
        output_path: 输出音频路径

    Returns:
        bool: 提取是否成功
    """
    ...

def merge_audio_video(
    ffmpeg_path: str, video_path: str, audio_path: str, output_path: str
) -> bool:
    """
    合并音频和视频

    Args:
        ffmpeg_path: ffmpeg 可执行文件路径
        video_path: 视频文件路径
        audio_path: 音频文件路径
        output_path: 输出文件路径

    Returns:
        bool: 合并是否成功
    """
    ...
