
import re
from deck_of_cards import deck_of_cards
import random

def findAttrPath(obj, nameOfAttr):
    attrList = []
    for attrName in dir(obj):
        if not attrName.startswith("_"):
            attrList.append(attrName)

    for attrName in attrList:
        attr = getattr(obj, attrName)
        if isinstance(attr, (type)):
            try:
               returnAttr = getattr(attr, nameOfAttr)
            except:
               returnAttr = findAttrPath(attr, nameOfAttr)
            if returnAttr is not None:
                return returnAttr
        else:
            return None
        




def buildNPC(NPC, characterStats, favoredTrait="random", favoredTraitType="Corporeal", favoredAptitudes=[]):

    characterStats.sort(key=lambda x: x.points)
    

    if hasattr(NPC.Corporeal, favoredTrait):
        attr = getattr(NPC.Corporeal, favoredTrait)
    elif hasattr(NPC.Incorporeal, favoredTrait):
        attr = getattr(NPC.Incorporeal, favoredTrait)
    else:
        attr = getattr(NPC, favoredTraitType)
        attrs = []
        for x in attr.list:
            attrs.append(getattr(attr, x))
        attr = random.choice(attrs)
        favoredTrait = attr.name

    thisTrait = characterStats.pop()
    attr.level = thisTrait.level
    attr.die = thisTrait.die

    corporealTraits = NPC.Corporeal.list.copy()
    incorporealTraits = NPC.Incorporeal.list.copy()

    if favoredTrait in corporealTraits:
        corporealTraits.remove(favoredTrait)
    elif favoredTrait in incorporealTraits:
        incorporealTraits.remove(favoredTrait)

    random.shuffle(corporealTraits)
    random.shuffle(incorporealTraits)

    if favoredTraitType == "Corporeal":
        allTraits = corporealTraits
        allTraits.extend(incorporealTraits)
    else:
        allTraits = incorporealTraits
        allTraits.extend(corporealTraits)

    for trait in allTraits:
        try:
            attr = getattr(NPC.Corporeal, trait)
        except:
            attr = getattr(NPC.Incorporeal, trait)
        thisTrait = characterStats.pop()
        attr.level = thisTrait.level
        attr.die = thisTrait.die


    NPC.wind = int(re.search(r'\d+', NPC.Incorporeal.Spirit.die).group()) + int(re.search(r'\d+', NPC.Corporeal.Vigor.die).group())
    aptitudePoints = int(re.search(r'\d+', NPC.Incorporeal.Knowledge.die).group()) + int(re.search(r'\d+', NPC.Incorporeal.Smarts.die).group()) + int(re.search(r'\d+', NPC.Incorporeal.Cognition.die).group())


    allAptitudes = NPC.Corporeal.Deftness.list + NPC.Corporeal.Nimbleness.list + NPC.Corporeal.Quickness.list + NPC.Corporeal.Strength.list + NPC.Corporeal.Vigor.list \
        + NPC.Incorporeal.Cognition.list + NPC.Incorporeal.Knowledge.list + NPC.Incorporeal.Mien.list + NPC.Incorporeal.Smarts.list + NPC.Incorporeal.Spirit.list

    random.shuffle(allAptitudes)
    favoredAptitudes.reverse()
    for aptitude in favoredAptitudes:
        allAptitudes.remove(aptitude)
        allAptitudes.insert(0, aptitude)

    i = 0
    while aptitudePoints > 0:
        if aptitudePoints > 35:
            pointsToSpend = 10
        elif aptitudePoints > 15:
            pointsToSpend = 6
        elif aptitudePoints > 5:
            pointsToSpend = 3
        else:
            pointsToSpend = 1
        aptitudePoints -= pointsToSpend
        aptitude = findAttrPath(NPC, allAptitudes[i])


        while pointsToSpend >= (aptitude.level+1):
            aptitude.level += 1
            pointsToSpend -= aptitude.level

        if len(aptitude.possibleConcentrations) > 0:
            aptitude.concentrations.append(random.choice(aptitude.possibleConcentrations))

        i += 1

    NPC.pace = int(re.search(r'\d+', NPC.Corporeal.Nimbleness.die).group())

    return NPC



class Trait:
    level = 1
    die = "d4"
class Aptitude:
    def __init__(self, name):
        self.level = 0
        self.concentrations = []
        self.possibleConcentrations = []
        self.name = name

class TraitType:
    list = []

class NPC:
    wind = 0
    pace = 0
    size = 6

    def print(self):
        print("Corporeal Stats:")
        self.printTraits(self.Corporeal, self.Corporeal.list)
        print("Incorporeal Stats:")
        self.printTraits(self.Incorporeal, self.Incorporeal.list)
        print("Wind: " + str(self.wind))
        print("Pace: " + str(self.pace))
        print("Size: " + str(self.size))
        
        
        
        



    def printAptitudes(self, trait, list):
        for aptName in list:
            apt = getattr(trait, aptName)
            if apt.level > 0:
                print("\t\t" + apt.name + " " + str(apt.level) + trait.die, end='')
                if len(apt.concentrations) > 0:
                    for concentration in apt.concentrations:
                        print(" " + concentration, end='')
                print("")

    def printTraits(self, traitType, list):
        for traitName in list:
            trait = getattr(traitType, traitName)
            print("\t" + trait.name + " " + str(trait.level) + trait.die)
            self.printAptitudes(trait, trait.list)    

    class Corporeal(TraitType):
        list = ['Deftness', 'Nimbleness', 'Quickness', 'Strength', 'Vigor']
        class Deftness(Trait):
            name = "Deftness"
            list = ['Bow', 'Filchin', 'Lockpickin', 'Shootin', 'SleightOfHand', 'SpeedLoad', 'Throwin']
            Bow = Aptitude('Bow')
            Filchin = Aptitude('Filchin\'')
            Lockpickin = Aptitude('Lockpickin\'')
            Shootin = Aptitude('Shootin\'')
            Shootin.possibleConcentrations.extend(['Automatics', 'Flamethrower', 'Pistol', 'Rifle', 'Shotgun'])
            SleightOfHand = Aptitude('Sleight of Hand')
            SpeedLoad = Aptitude('SpeedLoad')
            SpeedLoad.possibleConcentrations.extend(['Pistol', 'Rifle', 'Shotgun'])
            Throwin = Aptitude('Throwin\'')
            Throwin.possibleConcentrations.extend(['Balanced', 'Unbalanced'])

        class Nimbleness(Trait):
            name = "Nimbleness"
            list = ['Climbin', 'Dodge', 'Drivin', 'Fightin', 'HorseRidin', 'Sneak', 'Swimmin', 'Teamster']
            Climbin = Aptitude('Climbin\'')
            Climbin.level = 1
            Dodge = Aptitude('Dodge')
            Drivin = Aptitude('Drivin\'')
            Drivin.possibleConcentrations.extend(['Steam Boat', 'Ornithopter', 'Steam Wagon'])
            Fightin = Aptitude('Fightin\'')
            Fightin.possibleConcentrations.extend(['Brawlin', 'Knife', 'Lariat', 'Sword', 'Whip', 'Wrasslin'])
            HorseRidin = Aptitude('Horse Ridin\'')
            Sneak = Aptitude('Sneak')
            Sneak.level = 1
            Swimmin  = Aptitude('Swimmin\'')
            Teamster = Aptitude('Teamster')

        class Quickness(Trait):
            name = "Quickness"
            list = ['QuickDraw']
            QuickDraw = Aptitude('QuickDraw')
            QuickDraw.possibleConcentrations.extend(['Knife', 'Rifle', 'Shotgun', 'Sword'])

        class Strength(Trait):
            name = "Strength"
            list = []

        class Vigor(Trait):
            name = "Vigor"
            list = []

    class Incorporeal(TraitType):
        list = ['Cognition', 'Knowledge', 'Mien', 'Smarts', 'Spirit']
        class Cognition(Trait):
            name = "Cognition"
            list = ['Artillery', 'Arts', 'Scrutinize', 'Search', 'Trackin']
            Artillery = Aptitude('Artillery')
            Artillery.possibleConcentrations.extend(['Cannons', 'Gatling Guns', 'Rockets'])
            Arts = Aptitude('Arts')
            Arts.possibleConcentrations.extend(['Painting', 'Sculpting', 'Sketching'])
            Scrutinize = Aptitude('Scrutinize')
            Search = Aptitude('Search')
            Search.level = 1
            Trackin = Aptitude('Trackin\'')
        
        class Knowledge(Trait):
            name = "Knowledge"
            list = ['Academia', 'AreaKnowledge', 'Demolition', 'Disguise', 'Language', 'MadScience', 'Medicine', 'Professional', 'Science', 'Trade']
            Academia = Aptitude('Academia')
            AreaKnowledge = Aptitude('Area Knowledge')
            AreaKnowledge.level = 1
            AreaKnowledge.concentrations.append('Home County')
            AreaKnowledge.possibleConcentrations.extend(['Town', 'State', 'Region'])
            Demolition = Aptitude('Demolition')
            Disguise = Aptitude('Disguise')
            Language = Aptitude('Language')
            Language.possibleConcentrations.extend(['Apache', 'French', 'Gaelic', 'German', 'Latin', 'Indian Sign Language', 'Sioux', 'Spanish'])
            MadScience = Aptitude('Mad Science')
            Medicine = Aptitude('Medicine')
            Professional = Aptitude('Professional')
            Professional.possibleConcentrations.extend(['Journalism', 'Law', 'Military', 'Photography', 'Politics', 'Theology'])
            Science = Aptitude('Science')
            Science.possibleConcentrations.extend(['Biology', 'Chemistry', 'Engineering', 'Physics'])
            Trade = Aptitude('Trade')
            Trade.possibleConcentrations.extend(['Blacksmithing', 'Carpentry', 'Seamanship', 'Mining', 'Telegraphy', 'Undertaking'])

        class Mien(Trait):
            name = "Mien"
            list = ['AnimalWranglin', 'Leadership', 'Overawe', 'Performin', 'Persuasion', 'TaleTellin']
            AnimalWranglin = Aptitude('Animal Wranglin\'')
            Leadership = Aptitude('Leadership')
            Overawe = Aptitude('Overawe')
            Performin = Aptitude('Performin\'')
            Performin.possibleConcentrations.extend(['Acting', 'Singing'])
            Persuasion = Aptitude('Persuasion')
            TaleTellin = Aptitude('Tale Tellin\'')

        class Smarts(Trait):
            name = "Smarts"
            list = ['Bluff', 'Gamblin', 'Ridicule', 'Scroungin', 'Streetwise', 'Survival', 'Tinkerin']
            Bluff = Aptitude('Bluff')
            Gamblin = Aptitude('Gamblin\'')
            Ridicule = Aptitude('Ridicule')
            Scroungin = Aptitude('Scroungin\'')
            Streetwise = Aptitude('Streetwise')
            Survival = Aptitude('Surival')
            Survival.possibleConcentrations.extend(['Desert', 'Mountain'])
            Tinkerin = Aptitude('Tinkerin\'')
        
        class Spirit(Trait):
            name = "Spirit"
            list = ['Faith', 'Guts']
            Faith = Aptitude('Faith')
            Guts = Aptitude('Guts')

    
    
class Stats:
    def getCardLevel(self, card):
        if card.suit == 0:
            return 4
        elif card.suit == 1:
            return 3
        elif card.suit == 2:
            return 2
        else:
            return 1
        
    def getCardDie(self, card):
        if card.rank == 2:
            return "d4"
        elif card.rank >= 3 and card.rank <= 8:
            return "d6"
        elif card.rank >= 9 and card.rank <= 11:
            return "d8"
        elif card.rank >= 12 and card.rank <= 13:
            return "d10"
        else:
            return "d12"
    def getCardPoints(self, level, die, levelMultiplier):
        if level == 4:
            points = (18*levelMultiplier)
        elif level == 3:
            points = (10*levelMultiplier)
        elif level == 2:
            points = (4*levelMultiplier)
        else:
            points = (0*levelMultiplier)

        if die == "d12":
            points += 108
        elif die == "d10":
            points += 72
        elif die == "d8":
            points += 42
        elif die == "d6":
            points += 18
        else:
            points += 0 #yea yea

        return points    

    def __init__(self, card, levelMultiplier=1):
            self.level = self.getCardLevel(card)
            self.die = self.getCardDie(card)
            self.card = card
            self.points = self.getCardPoints(self.level, self.die, levelMultiplier)

    def toString(self):
        return str(self.level) + self.die



if __name__ == "__main__":

    myDeck = deck_of_cards.DeckOfCards()
    #myDeck.add_jokers()
    myDeck.shuffle_deck()

    rawCharacterStats = []

    for x in range(12):
        rawCharacterStats.append(Stats(myDeck.give_random_card(), 2))


    rawCharacterStats.sort(key=lambda x: x.points)

    i = 0
    while len(rawCharacterStats) > 10:
        if rawCharacterStats[i].die != "d4":
            del rawCharacterStats[i]
        else:
            i += 1

    bob = buildNPC(NPC(), rawCharacterStats[:], 'Spirit', 'Corporeal', ['Shootin', 'Fightin'])
    bob.print()