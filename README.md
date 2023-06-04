# On-Least-Privilege-Persistent-Storage-Access-in-Web-Browsers

This repository contains the code used for our paper "On-Least-Privilege-Persistent-Storage-Access-in-Web-Browsers"

## Set-up
For our work, we instrumented the firefox codebase in order to integrate fine grained access control for third-party scripts, which otherwise have full control over first-party storage. 

To replicate our work, you can setup to build firefox on your machine by following the instructions from this tutorial: https://firefox-source-docs.mozilla.org/setup/index.html . We used "Nightly Firefox version 98.0a1" for our work. 

For crawling the 10,000 websites, we used marionette testing environment which visited the websites and collected the logs required for assessing the third-party accesses to the first-party storage. This script can be found in the `scripts` folder.   

## Usage

To replicate our work, you would need to integrate the code changes in the following folders:

In case of `strict restrictive browser`:
- In the netwerk folder, replace the files provided in this repository under the `netwerk` folder in  `restrictive_browser` folder. 
- In the ipc folder, replace the file provided in the folder `ipc` with the original file. 
- In the `toolkit/components/cookiebanners`, you'd have to change the following files in-order to avoid compatibility issues. 

In case of `relaxed browser`:
- In the netwerk folder, replace the files provided in this repository under the `netwerk\cookie` folder in  `relaxed_browser` folder. 
- In the ipc folder, replace the file provided in the folder `ipc` with the original file. 
- - In the `toolkit/components/cookiebanners`, you'd have to change the following files in-order to avoid compatibility issues. 

In case of discrepencies, we have mentioned( refer to the readme files in the particular folders) which lines are modified, or added, so that the changes can be done manually on a fresh firefox build. 

Once these changes are added, you can build the firefox code with the following command:
```bash
./mach build
```
Once the source code builds, you can run the browser with the command:
```bash
./mach run
```

You can find our firefox build [here](https://iitgnacin-my.sharepoint.com/:u:/g/personal/gayatripriyadarsini_iitgn_ac_in/EWRuSB0IIZFKpuS_VbJPd9YBwbhliRXj-HvntzSDLv2LbQ?e=QFiYdY). This can then be used to run the firefox browser by `./mach run`

