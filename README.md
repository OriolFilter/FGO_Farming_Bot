# FGO_farming_bot


## Instalation:

To execute the bot, you must install [Python](https://www.python.org/downloads/) on your system, once [Python](https://www.python.org/downloads/) is installed, execute 'setup.bat', also it will create the folder 'tmp', so you don't have to add it manually, once it's done you are ready to go!


## Usage:

# From terminal

Use 'py main.py'.

# From desktop envoirment

If the file is not associated to Python automatically, left click 'main.py', 'open with', and click on 'Python'.

Remember, when running the bot, it will need the folder 'templates', and a folder called 'tmp', so the bot can store the screenshots. (create 'tmp' folder if it does not exist).

To use this bot you must need use Nox emulator with a resolution of 1280 x 720, without resizing the screen.


## How does the bot works:

It will be doing screenshots from your NoxApplication, then filtering the results and comparing them with some templates, then proceed to act.

When doing screenshots it will drag the application in front of your screen.

Even dragging it in front of your screen, in case you don't have it as 'active' window, the bot will avoid calling it, in case someone needs to use the PC while the bot still running.

Also this bot does not work at 'Android' level, it presses your screen, means that if you plan to leave it while you are doing somthing on the PC, it will result in the bot not farming.

## Combat System:

### Picking cards

The order is, effective cards first, then your card priority selection (ej. Buster, Arts, Quick).


## Supported emulators:

    - Nox

## Known versions of Python & emulators that work:

#### Nox:

    - v6 (checked 20/02/2020)

#### Python:

    - 3.8 (checked 20/02/2020)

#### ISOs:

    - Windows 10


## Future implementations

    - Noble Phantasm Usage

    - More Craft Essence support

    - Removing the need of storing a screenshot (this isn't a priority)

    - Working on background insted of foreground

## Versions

- 1.01 First Version

- 1.01b Added CE picker, improved performance & menu

### CE ADDED

        - ChaldeaLunchtime

        - MysticEyesOfDistortion (event)

- 1.02 Added NP behavior, improved code, fixed some buggs & added more elements to 'templates'

#### CE ADDED

        - Chorus (event)

        - Decapitating bunny 2018 (event)

        - Sprinter (event)

        - RepeatMagic (event)

        - MatureGentelman (event)

        - VividDanceOfFists (event)

        - SummersPrecognition (event)

        - TreefoldBarrier (event)

        - GrandPuppeteer (event)

#### About Updates

Remember to update 'templates' folder with each patch.

#### About CE Added

Since im using my own friends to get the files, if im not able to be friend with somone who has X CE, i won't be able to get the image, so there is a chane about some craft essences being without the 'Limitet Break' form
