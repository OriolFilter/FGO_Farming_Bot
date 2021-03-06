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

The order is, effective cards first, then your card priority selection (ej. Buster, Arts, Quick), after effective cards come the neutral ones, and the last ones will be the cards affected by resist.


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

    - More Craft Essence support (atleast the event-and usual supportfarming)

    - Removing the need of storing a screenshot (this isn't a priority)

    - Working on background insted of foreground

    - Add support for more emulators

    - Storing, loading and autoloading config (autolading will search a file with X name inside his folder)

    - Limit the number times the bot regenerates energy (done)

    - Noble Phantasm Usage (done)

    - Allow color-chains (done)

    - Improve Noble Phantasm Usage (soon)


## Versions

- 1.01 First Version

- 1.01b Added CE picker, improved performance & added a menu

#### CE ADDED

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

- 1.02b Added a vertical scrollbar for the menu, added 'Select Emulator Software', and 'Introduce Emulator Window name', updated some CE to fix some issues related with them.

- 1.02c Now you can limit the times to get the energy refilled and added a 'update config' button, removing the need to pause->start the bot again, keep in mind that will restart the apples to use! Now support color-chains, also fixed some issues and updated.

- 1.03 Added 'revert card order' option, reverting the order of the cards selected, ending with the card with higher value, removed 'Quit' button.

- 1.04 Added 'MonaLisa' to the CE list, disabled CE from shiki event

- 1.04b Added support for 'Stuns' cards, which will avoid, improved code, fixed some errors about picking the CE from the support list

- 1.05 No longer sends a friend request in case you used somone who is not in your friend list.

- 1.06 Fixed minor bugs, fixed a bug where the bot ends when restoring the last apple, added the "Asisted mode/Card picker".
#### About Updates

Remember to update 'templates' folder with each patch.


#### CE

Since im using my own friends to get the files, if im not able to be friend with somone who has X CE, i won't be able to get the image, so there is a chane about some craft essences being without the 'Limitet Break' form

## CE list

### Active CE

        - ChaldeaLunchtime

        - MonaLisa


### Disabled CE

        - MysticEyesOfDistortion (event)

        - Chorus (event)

        - Decapitating bunny 2018 (event)

        - Sprinter (event)

        - RepeatMagic (event)

        - MatureGentelman (event)

        - VividDanceOfFists (event)

        - SummersPrecognition (event)

        - TreefoldBarrier (event)

        - GrandPuppeteer (event)
