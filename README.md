# MOS-test

This repository serves as a simple interface for  MOS (Mean Opinion Score) quality testing. The MOS is expressed as a single rational number, typically in the range 1–5, where 1 is lowest perceived quality, and 5 is the highest perceived quality. 

5 = Excellent
4 = Good
3 = Fair
2 = Poor
1 = Bad

If you are a participant:
- Your only task is to run the script and rate the audio quality from 1 to 5, based on how you percieve the quality of it, completely subjectively (not content, loudness preference, or personal taste :))
- Using headphones is recommended
- Please listen to each sample fully before submitting a score. You can stop the script entirely and continue whenever you are ready again, the previous results will be saved!!!
- Try not replaying audio more than once, try not comparing it with other audios from this test, or from real life, since this aims to reflect real listening scenarios


## Prerequisites
- Python 3.11+
- pygame, version 2.6.1, that can be installed with: pip install pygame

## Usage

You should unzip the audios folder I've sent you to this repository folder (or copy/paste all samples to the audios folder that you are supposed to make)

Run the MOS test script:

```bash
python mos_test.py
```
All results are being saved to the mos_scores.json file, please send me that file after you finish. Thank you and happy listening !!!




