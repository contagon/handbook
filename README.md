# General Handbook Tracker

A simple scraper for tracking changes of the General Handbook of the Church of Jesus Christ of Latter-Day Saints using git diff. 

For those not familiar with the Church of Jesus Christ, I recommend you check out [the church's website](https://www.churchofjesuschrist.org/welcome/what-do-latter-day-saints-believe?lang=eng) for more information about our beliefs. It is a worldwide church, with volunteer-based clergy that follow the instructions put out by the General Handbook.

The easiest way to visualize changes is via the links below. Removed text from previous editions will be shown in red on the left, and the new version with changes in green on the right.

| Edition | Compare to Previous                                                    | Compare to Current                                                     |
| ------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| 2024-08 | [Link](https://github.com/contagon/handbook/compare/2024-05...2024-08) | NA                                                                     |
| 2024-05 | [Link](https://github.com/contagon/handbook/compare/2023-08...2024-05) | [Link](https://github.com/contagon/handbook/compare/2024-05...2024-08) |
| 2023-08 | [Link](https://github.com/contagon/handbook/compare/2022-08...2023-08) | [Link](https://github.com/contagon/handbook/compare/2023-08...2024-08) |
| 2022-08 | [Link](https://github.com/contagon/handbook/compare/2021-12...2022-08) | [Link](https://github.com/contagon/handbook/compare/2022-08...2024-08) |
| 2021-12 | [Link](https://github.com/contagon/handbook/compare/2021-07...2021-12) | [Link](https://github.com/contagon/handbook/compare/2021-12...2024-08) |
| 2021-07 | [Link](https://github.com/contagon/handbook/compare/2021-03...2021-07) | [Link](https://github.com/contagon/handbook/compare/2021-07...2024-08) |
| 2021-03 | [Link](https://github.com/contagon/handbook/compare/2020-12...2021-03) | [Link](https://github.com/contagon/handbook/compare/2021-03...2024-08) |
| 2020-12 | [Link](https://github.com/contagon/handbook/compare/2020-07...2020-12) | [Link](https://github.com/contagon/handbook/compare/2020-12...2024-08) |
| 2020-07 | [Link](https://github.com/contagon/handbook/compare/2020-03...2020-07) | [Link](https://github.com/contagon/handbook/compare/2020-07...2024-08) |
| 2020-03 | NA                                                                     | [Link](https://github.com/contagon/handbook/compare/2020-03...2024-08) |

I hope you enjoy! I've enjoyed having an easy visualization of changes to see how the church is continuing to focus on Christ, His work, and bringing others unto Him. 

Note, I am not doing this in any official capacity with the church, just on my own accord.

## Technical Info

All the versions are stored in the `editions` folder, with working hyperlinks both to [churchofjesuschrist.org](https://www.churchofjesuschrist.org/?lang=eng) and relative links to other chapters. Additionally, in the `diff` branch, each edition is stored with a tag and a separate commit in the `handbook` folder. Links comparing different editions are found in the table above.

Editions were found via [Church Newsroom](https://newsroom.churchofjesuschrist.org/) and checking the "Summary of Recent Changes" page on [the wayback machine](https://web.archive.org/).

I began this project when the 2024-05 edition came out - all previous editions are also from the wayback machine. Unfortunately, about 15% of edition chapters weren't saved - for these chapters I used the previous edition version, and if it didn't exist, the newer edition version. Missing pages can be found in [missing.txt](editions/missing.txt).

Please feel free to open an issue/pull request/etc if you have any questions or find some inconsistencies.

## Running the Scraper

If you feel like running this yourself, python package requirements are found in the `pyproject.toml` and ran using an activated `uv` python venv. Getting all the editions can be done via running `run.sh`, individual downloading/sanitizing/copying missing can be done via the cli interface in `run.py`. Making the diff branch is done via `branch.sh`.

To add a new version, simply add the new date to the `src/handbook/const.py` file and run!