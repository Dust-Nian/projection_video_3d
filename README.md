# 3D 投影视频生成工具

一个用于创建 3D 投影视频的 Python 工具，可以将普通视频转换为适用于全息投影设备的格式。

## 功能特点

- 支持向上和向下两种投影方向
- 自动处理视频和音频
- 保持原视频音轨
- 支持命令行参数配置

## 环境要求

本项目使用 uv 包管理器进行依赖管理。主要依赖：

- Python 3.8+
- Rust
- OpenCV
- NumPy
- FFmpeg

## 安装依赖

```bash
uv venv
uv pip install -r requirements.txt
```

## 使用方法

```bash
python main.py -i 输入视频路径 -o 输出视频路径 [-d up/down] [-f ffmpeg路径]
```

参数说明：

- `-i/--input`: 输入视频文件路径（必需）
- `-o/--output`: 输出视频文件路径（默认：output.mp4）
- `-d/--direction`: 投影方向，可选 up 或 down（默认：up）
- `-f/--ffmpeg`: FFmpeg 可执行文件路径（默认：ffmpeg）

## 打包说明

使用 PyInstaller 打包为独立可执行文件：

```bash
pyinstaller -F --clean -i .\assets\logo.ico -n projection-video-3d --add-binary ".\assets\ffmpeg.exe;." .\main.py
```

打包后的文件将包含：

- 独立的可执行文件
- 内置的 FFmpeg
- 自定义图标
