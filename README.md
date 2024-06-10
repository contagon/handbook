# LDS Handbook Tracker

A simple scraper for tracking changes in the LDS General Handbook using git diff. 

All the versions are stored in the `editions` folder. Additionally, in the `diff` branch, each edition is stored with a tag and a seperate commit in the `handbook` folder. Links comparing different editions are as follows:

| Edition | Compare to Previous                                                    | Compare to Current                                                     |
|---------|------------------------------------------------------------------------|------------------------------------------------------------------------|
| 2024-05 | [Link](https://github.com/contagon/handbook/compare/2023-08...2024-05) | NA                                                                     |
| 2023-08 | [Link](https://github.com/contagon/handbook/compare/2022-08...2023-08) | [Link](https://github.com/contagon/handbook/compare/2023-08...2024-05) |
| 2022-08 | [Link](https://github.com/contagon/handbook/compare/2021-12...2022-08) | [Link](https://github.com/contagon/handbook/compare/2022-08...2024-05) |
| 2021-12 | [Link](https://github.com/contagon/handbook/compare/2021-07...2021-12) | [Link](https://github.com/contagon/handbook/compare/2021-12...2024-05) |
| 2021-07 | [Link](https://github.com/contagon/handbook/compare/2021-03...2021-07) | [Link](https://github.com/contagon/handbook/compare/2021-07...2024-05) |
| 2021-03 | [Link](https://github.com/contagon/handbook/compare/2020-12...2021-03) | [Link](https://github.com/contagon/handbook/compare/2021-03...2024-05) |
| 2020-12 | [Link](https://github.com/contagon/handbook/compare/2020-07...2020-12) | [Link](https://github.com/contagon/handbook/compare/2020-12...2024-05) |
| 2020-07 | [Link](https://github.com/contagon/handbook/compare/2020-03...2020-07) | [Link](https://github.com/contagon/handbook/compare/2020-07...2024-05) |
| 2020-03 | NA                                                                     | [Link](https://github.com/contagon/handbook/compare/2020-03...2024-05) |

Editions were found via [Church Newsroom](https://newsroom.churchofjesuschrist.org/) and checking the "Summary of Recent Changes" page on [the wayback machine](https://web.archive.org/).

I began this project when the 2024-05 edition came out - all previous editions are also from the wayback machine. Unfortunately, about 15% of edition chapters weren't saved - for these chapters I used the previous edition version, and if it didn't exist, the newer edition version. Missing pages can be found in [missing.txt](editions/missing.txt).

If you feel like running this yourself, requirements are found in `requirements.txt` - additionally I ran it all with python 3.10. Getting all the editions can be done via running `run.sh`, indiviual downloading/sanitizing/copying missing can be done via the cli interface in `run.py`. Making the diff branch is done via `branch.sh`.

I hope you enjoy! I've enjoyed having an easy visualization of changes to see how the church is continuing to focus on Christ, His work, and bringing others unto Him. 