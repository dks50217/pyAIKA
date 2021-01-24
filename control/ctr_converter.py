import subprocess
import os

class WAVConverter(object):
    """
    Class for converting a region of an input audio or video file into a FLAC audio file
    """
    def __init__(self, source_file, out_file):
        self.source_file = source_file
        self.out_file = out_file

    def __call__(self):
        try:
            program_ffmpeg = r"C:\Users\User\Desktop\Mic\pyAIKA\ffmpeg.exe"
            print(program_ffmpeg)
            command = [program_ffmpeg,"-i",self.source_file,self.out_file]
            use_shell = True if os.name == "nt" else False
            subprocess.check_output(command, stdin=open(os.devnull), shell=use_shell)
            return None

        except KeyboardInterrupt:
            print("FLACConverter KeyboardInterrupt")
            return None