#!/bin/sh
echo start installing
git lfs clone --progress https://huggingface.co/KiRiLLBEl/MovieDescriptionGen
echo end installing
python3 server.py