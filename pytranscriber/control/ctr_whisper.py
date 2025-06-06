'''
   (C) 2025 Raryel C. Souza
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMessageBox
import os
import sys
import whisper
import datetime
import shutil
from pytranscriber.control.ctr_engine import CtrEngine


class CtrWhisper(CtrEngine, QObject):
    errorSignal = pyqtSignal(str)  # Define the signal
    MODEL_DIR = None

    @classmethod
    def initialize(cls):
        """Initialize MODEL_DIR before using the class."""
        if cls.MODEL_DIR is None:
            cls.MODEL_DIR = cls.get_whisper_model_dir()

    def __init__(self):
        super().__init__()
        self.errorSignal.connect(self.show_error_message)  # Connect signal to slot

    @staticmethod
    def get_whisper_model_dir():
        base_path = os.path.expanduser("~/pytranscriber")  # User's home directory

        model_dir = os.path.join(base_path, "whisper_models")
        os.makedirs(model_dir, exist_ok=True)  # Ensure directory exists
        return model_dir

    @staticmethod
    def generate_subtitles(source_path, src_language, outputSRT=None, outputTXT=None, model='base'):
        CtrWhisper.patch_ffmpeg()  # Ensure FFmpeg is available

        model = whisper.load_model(model, download_root=CtrWhisper.MODEL_DIR)
        result = model.transcribe(source_path, verbose=True, language=src_language)

        if CtrEngine.is_operation_canceled():
            return -1

        content_srt = CtrWhisper.generate_srt_file_content(result["segments"])
        content_txt = CtrWhisper.generate_txt_file_content(result["segments"])

        CtrWhisper.save_output_file(outputSRT, content_srt)
        CtrWhisper.save_output_file(outputTXT, content_txt)

        return outputSRT

    @staticmethod
    def show_error_message(message):
        """Displays the error message in a PyQt5 QMessageBox."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec_()

    @staticmethod
    def generate_srt_file_content(transcribed_segments):
        content = ""

        def format_timestamp(seconds):
            """Convert seconds to SRT-compliant timestamp (HH:MM:SS,mmm)."""
            td = datetime.timedelta(seconds=seconds)
            total_seconds = int(td.total_seconds())
            millis = int(round((td.total_seconds() - total_seconds) * 1000))
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            secs = total_seconds % 60
            return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

        for i, s in enumerate(transcribed_segments, start=1):
            start_time = format_timestamp(s["start"])
            end_time = format_timestamp(s["end"])
            content += f"{i}\n{start_time} --> {end_time}\n{s['text'].strip()}\n\n"

        return content

    @staticmethod
    def generate_txt_file_content(transcribed_segments):
        content = ""
        for s in transcribed_segments:
            content = content + str(s["text"])
        return content

    #forces whisper to use the embedded ffmpeg in frozen app
    @staticmethod
    def patch_ffmpeg():
        """Ensure FFmpeg is correctly detected and patched for PyInstaller frozen apps."""
        if getattr(sys, "frozen", False):  # Running as a bundled executable
            ffmpeg_path = os.path.join(sys._MEIPASS, "ffmpeg")
        else:
            ffmpeg_path = shutil.which("ffmpeg")  # Use system-wide FFmpeg

        if not ffmpeg_path:
            raise FileNotFoundError("FFmpeg not found!")

        os.environ["FFMPEG_PATH"] = ffmpeg_path
        os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)

        # Monkey-patch shutil.which to always return the correct FFmpeg path
        original_which = shutil.which

        def patched_which(cmd, *args, **kwargs):
            if cmd == "ffmpeg":
                return ffmpeg_path
            return original_which(cmd, *args, **kwargs)

        shutil.which = patched_which  # Apply the patch