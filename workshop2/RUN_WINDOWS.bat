@echo off
REM JOLLY PIRATE launcher script for MacOS/Linux
REM ============================================
REM Copyright(c) 2017 Jonas Sjöberg
REM https://github.com/jonasjberg
REM http://www.jonasjberg.com
REM University mail: js224eh[a]student.lnu.se

REM TODO: Verify that this is working!


SET self_path=%~dp0
pushd %self_path%
python3 jollypirate
popd
