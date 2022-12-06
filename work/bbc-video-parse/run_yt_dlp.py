import sys
import yt_dlp
sys.argv.extend(["-F","bbc.com/news/av/world-middle-east-61404666"])

yt_dlp.main()