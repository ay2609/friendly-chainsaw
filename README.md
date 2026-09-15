# friendly-chainsaw

Shazam-style audio fingerprinting and song recognition, built for a BWSI/CogWorks capstone.

## What it is

A from-scratch implementation of audio fingerprinting and song recognition (in the style of
Shazam): record a short clip via microphone, extract spectrogram peaks, generate fingerprints, and
match against a local song database.

The included notebook, [`Audio_Capstone_Project_Scaffolding.ipynb`](Audio_Capstone_Project_Scaffolding.ipynb),
walks through the whole workflow — populating the database, recording a clip, getting a match, and
plotting the spectrogram/fingerprints — and is the best starting point for understanding how the
pieces fit together.

Uses the course-provided `Microphone` library and [`sturdy-garbanzo`](https://github.com/ay2609/sturdy-garbanzo)
(a small sample-song library) as git submodules.

## Stack

- Python, numpy/scipy (spectrogram + peak-finding), microphone I/O

## Credits

Built during a Beginning Workshop in Science and Innovation (BWSI) / CogWorks summer program, in
collaboration with teammate Hunter Baker.

## Getting started

See the walkthrough notebook, `Audio_Capstone_Project_Scaffolding.ipynb`, for the full workflow.
