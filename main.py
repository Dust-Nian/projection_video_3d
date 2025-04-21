import argparse
import os
import sys
import time
from enum import Enum
from pathlib import Path

import cv2
import numpy as np
from projection_video_3d import extract_audio, merge_audio_video, verify_ffmpeg


class ProjDir(Enum):
    """投影方向"""

    UP = 1
    DOWN = 2


def ensure_dir(path):
    """确保目录存在"""
    dir_path = Path(path).parent
    if not dir_path.exists():
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"创建目录: {dir_path}")


def get_ffmpeg_path(ffmpeg_path):
    """获取ffmpeg可执行文件路径"""
    if getattr(sys, "frozen", False):
        # 如果是打包后的exe
        return os.path.join(sys._MEIPASS, "ffmpeg.exe")
    # 开发环境使用参数传入的路径
    return ffmpeg_path


def create_3d_proj_video(in_path, out_path, ffmpeg_path="ffmpeg", direction=ProjDir.UP):
    """
    创建3D投影视频

    参数:
        in_path: 输入视频路径
        out_path: 输出视频路径
        ffmpeg_path: ffmpeg路径
        direction: 投影方向
    """
    # 获取正确的ffmpeg路径
    ffmpeg_path = get_ffmpeg_path(ffmpeg_path)

    # 验证ffmpeg
    if not verify_ffmpeg(ffmpeg_path):
        print("FFmpeg验证失败")
        return False

    # 临时文件
    temp_dir = Path("temp_proj")
    temp_dir.mkdir(exist_ok=True)
    temp_audio = temp_dir / "audio.aac"
    temp_video = temp_dir / "video_no_audio.mp4"

    # 提取音频
    try:
        if not extract_audio(ffmpeg_path, str(in_path), str(temp_audio)):
            temp_audio.unlink(missing_ok=True)
    except Exception:
        temp_audio.unlink(missing_ok=True)

    # 处理视频
    cap = cv2.VideoCapture(in_path)
    if not cap.isOpened():
        return False

    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out_w = w + 2 * h
    out_h = w + 2 * h

    writer = cv2.VideoWriter(
        str(temp_video), cv2.VideoWriter.fourcc(*"mp4v"), fps, (out_w, out_h)
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 生成投影帧
        if direction == ProjDir.UP:
            top = cv2.flip(frame, 1)
            right = cv2.flip(cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE), 1)
            bottom = cv2.flip(cv2.rotate(frame, cv2.ROTATE_180), 1)
            left = cv2.flip(cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE), 1)
        else:
            top = cv2.flip(cv2.rotate(frame, cv2.ROTATE_180), 1)
            right = cv2.flip(cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE), 1)
            bottom = cv2.flip(frame, 1)
            left = cv2.flip(cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE), 1)

        # 组合投影
        proj_frame = np.zeros((out_h, out_w, 3), dtype=np.uint8)
        proj_frame[0:h, h : h + w] = top
        proj_frame[h : h + w, 0:h] = left
        proj_frame[h : h + w, w + h : w + 2 * h] = right
        proj_frame[h + w : h + w + h, h : h + w] = bottom

        writer.write(proj_frame)

    cap.release()
    writer.release()

    ensure_dir(out_path)

    # 合并音视频
    if temp_audio.exists():
        try:
            if not merge_audio_video(
                ffmpeg_path, str(temp_video), str(temp_audio), out_path
            ):
                os.replace(temp_video, out_path)
        except Exception as e:
            print(f"合并音频和视频时出错: {e}")
            os.replace(temp_video, out_path)
    else:
        os.replace(temp_video, out_path)

    # 清理
    for f in temp_dir.glob("*"):
        f.unlink()
    temp_dir.rmdir()

    return True


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="创建3D投影视频",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="输入视频路径",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output.mp4",
        help="输出视频路径",
    )
    parser.add_argument(
        "-f",
        "--ffmpeg",
        default="ffmpeg",
        help="ffmpeg可执行文件路径",
    )
    parser.add_argument(
        "-d",
        "--direction",
        choices=["up", "down"],
        default="up",
        help="投影方向 (up/down)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    start_time = time.time()

    direction = ProjDir.UP if args.direction.lower() == "up" else ProjDir.DOWN

    if create_3d_proj_video(args.input, args.output, args.ffmpeg, direction):
        print("成功")

    else:
        print("失败")

    print(f"用时: {time.time() - start_time:.2f}秒")
