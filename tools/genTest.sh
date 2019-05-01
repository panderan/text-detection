#!/bin/bash
idx=$1
TEST_PATH="IDCards/Rear/Testing"
find $TEST_PATH/$idx  -maxdepth 1 -type f | grep jpg$ | sort > filenames.txt
find $TEST_PATH/$idx/mask  -maxdepth 1 -type f | grep jpg$ | sort > maskFilenames.txt
