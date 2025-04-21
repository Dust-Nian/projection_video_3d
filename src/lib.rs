use pyo3::prelude::*;
use std::process::Command;

#[pyfunction]
fn verify_ffmpeg(ffmpeg_path: &str) -> PyResult<bool> {
    let output = Command::new(ffmpeg_path).arg("-version").output();

    Ok(output.is_ok())
}

#[pyfunction]
fn extract_audio(ffmpeg_path: &str, input_path: &str, output_path: &str) -> PyResult<bool> {
    let status = Command::new(ffmpeg_path)
        .args(&[
            "-y",
            "-i",
            input_path,
            "-vn",
            "-acodec",
            "copy",
            output_path,
        ])
        .status()?;

    Ok(status.success())
}

#[pyfunction]
fn merge_audio_video(
    ffmpeg_path: &str,
    video_path: &str,
    audio_path: &str,
    output_path: &str,
) -> PyResult<bool> {
    let status = Command::new(ffmpeg_path)
        .args(&[
            "-y",
            "-i",
            video_path,
            "-i",
            audio_path,
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            output_path,
        ])
        .status()?;

    Ok(status.success())
}

#[pymodule]
fn projection_video_3d(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(verify_ffmpeg, m)?)?;
    m.add_function(wrap_pyfunction!(extract_audio, m)?)?;
    m.add_function(wrap_pyfunction!(merge_audio_video, m)?)?;
    Ok(())
}
