# deadlands-classic-npc-generator
A simple generator that can create a quick and dirty stat block for a mook or NPC.

## Requirements:
  deck-of-cards: https://pypi.org/project/deck-of-cards/
 
## How to Use:
  This script creates NPCs based on a few user specified values. Each of these values has defaults, so the script can be run alone.
  
  Usage is ```main.py favoredTrait favoredTraitType Aptitude1 Aptitude2 Aptitude3...```
  
  Ex: ```py main.py Vigor Incorporeal Shootin TaleTellin QuickDraw Search```
  
  The script will build an NPC by drawing cards like creating a player character. It will rank these cards and assign them to traits based on criteria entered. It will then          determine the number of aptitude points that character should have an divy them up based on criteria entered or randomly if no aptitudes are specified.
  
## Notes and Thoughts:
  First real python project. There are probably some conventions I've broken along the way. Feel free to note what I did wrong, but I may not get to it.
  
  I created this script mostly for personal use, so it isn't ultra customizable, but I hope someone can get some use out of it. My philosophy when designing this is I just needed   a template to work off of so I could tweak values after the fact. It is not meant to be a complete character builder. Just something to spit out a quick stat block for a mook     or give me something to work off of for a bigger NPC.
