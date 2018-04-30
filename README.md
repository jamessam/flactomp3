These are scripts for converting a directory of FLAC or WAV files to MP3. They can be extended to accept any audio format, should you choose to extend it.

The scripts require FFMPEG to be installed. The Python script automatically checks for FFMPEG on Macs, but assumes FFMPEG is installed and added to the system path on other OS's. The JavaScript and BASH do not currently check for FFMPEG.

For Python, it can be called as simply ```python tomp3.py```. The JS and BASH scripts need to be called as ```node /path/to/hi/res/files /path/to/mp3s wav```.
