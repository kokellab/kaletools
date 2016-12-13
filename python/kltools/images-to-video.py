# Douglas Myers-Turnbull wrote this for the Kokel Lab, which has released it under the Apache Software License, Version 2.0
# See the license file here: https://gist.github.com/dmyersturnbull/bfa1c3371e7449db553aaa1e7cd3cac1
# The list of copyright owners is unknown

# This was originally copied from https://gist.github.com/dmyersturnbull/f0ae8a871ba2a164eb81c5ba0ae438ba

import subprocess
import sys
import argparse
import os

def make_video_from_frames(input_dir: str, video_path: str, framerate: str='10/1', ffmpeg_path: str='ffmpeg', input_image_extension: str='.jpg') -> None:
	"""Runs ffmpeg on all selected files in a directory to generates an x264-encoded video in an MP4 container.
	Warnings:
		- Make sure that the frames are sorted in the correct order.
		- Overwrites the output video file without warning.
	video_path: the full path of the video file, which MUST end in .mp4
	framerate: a rational number in the format a/b (ex: 4/5 is 4 frames per every 5 seconds)
	input_image_extension: The extension of the images in the directory to use as input; must start with a dot (.)
	"""
	assert input_image_extension.startswith('.')
	assert video_path.endswith('.mp4')
	subprocess.Popen([ffmpeg_path,
			'-r', framerate,
			'-y',                                                        # overwrites
			'-pattern_type', 'glob',
			'-i', os.path.join(input_dir, '*' + input_image_extension),
			'-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',                  # needed because: https://stackoverflow.com/questions/24961127/ffmpeg-create-video-from-images
			'-c:v', 'libx264',
			'-pix_fmt', 'yuv420p',                                       # needed because most video players can only use the 264 pixel format, but it's not default
			video_path])


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="""
Runs ffmpeg on all selected files in a directory to generates an x264-encoded video in an MP4 container.
Uses options such that almost every video player can play the video.
	Warnings:
		- Make sure that the frames are sorted in the correct order.
		- Overwrites the output video file without warning.
""")
	parser.add_argument('--dir', required=True, type=str, help='The directory containing images')
	parser.add_argument('--video', required=True, type=str, help='The full path of the video file, which MUST end in .mp4')
	parser.add_argument('--framerate', default='10/1', type=str, help='A rational number in the format a/b (ex: 4/5 is 4 frames per every 5 seconds)')
	parser.add_argument('--ffmpeg', default='ffmpeg', type=str, help='The path to ffmpeg')
	parser.add_argument('--ext', default='.jpg', type=str, help='The extension of the images in the directory to use as input; must start with a dot (.)')
	opts = parser.parse_args()
	make_video_from_frames(opts.dir, opts.video, opts.framerate, opts.ffmpeg, opts.ext)
