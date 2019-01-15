#!/bin/bash

python test_scan.py && docker build --rm -t scan:py .
