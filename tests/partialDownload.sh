#!/usr/bin/env bash

PROJECT_PATH="/home/v4d3r/Projects/dragonload/tests"
testFileURL="https://fgig.ir/movie/2019/Aladdin-2019_480.mp4"

# Get the file size
fileSize=$(\
    curl -I $testFileURL |\
    grep -i content-length |\
    cut -d ' ' -f2 |\
    tr -d '\r'
) #| awk '{print $2}')

# Initiate Download for the first 1/100
firstSegment=`bc <<< $fileSize/100`
curl -# --range 0-$firstSegment https://fgig.ir/movie/2019/Aladdin-2019_480.mp4 --output Aladdin.mp4.part1
