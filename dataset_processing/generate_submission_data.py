import random
import pandas as pd
import math

random.seed(1)

MIN_TRUST = 1
MAX_TRUST = 20

MIN_SUBS = 50
MAX_SUBS = 200


usernames = [
    "dadcountry", "videolabel", "hibiscussurvival", "demoniccarpus", "gotslothful", "exactingwitch", "burninspector", "withdrawscientific", "makeshiftblaring", "transportexhibition", "incisiveoutrigger", "covertfarflung", "guacamolearmed", "canoeingpistachio", "hippiehabit", "glaringpremium", "liberalboyscouts", "sundresspeony", "nurseliterate", "overripealready", "sweetshistorian", "walrusfritter", "enterpriseamphora", "bloodkitchen", "barelyjeer", "disordergothic", "pumpkinslagan", "progressdivision", "polopartial", "cooingdealer", "impartialgeneral", "talentprime", "plophover", "managehushed", "crystalsirritate", "bakedwomens", "mincedher", "outplacid", "whinegigantic", "extensiverusk", "insistentnative", "scuttlescultivated", "snowunbreaking", "breechesfewer", "retinaoccasion", "planehop", "celebrityradiant", "coamingvacation", "blightermoment", "growingblackneck", "toucaneggs", "onionsweekly", "oxeyeassistance", "ringedsavings", "nebulouswheelhouse", "pillrout", "childhoodmocha", "cameshrill", "duckdecision", "quiettaiga", "somewherelook", "fiberinclude", "suckasian", "preachflaxseed", "humburgergrateful", "gravykippers", "dropletcoffee", "gymtold", "dweebhill", "fantasywheel", "craftmeathead", "yeomancranberries", "observantverb", "feelingtroupe", "externalquart", "jukeboxgateway", "archivistdroplet", "backgroundrecall", "slimeballpinto", "buncartography", "unaffectedbarren", "ughdining", "don’tattached", "truedisorder", "uncommonplague", "pinksinglet", "rectumvroom", "archesraccoon", "humpsteak", "twistingprivacy", "observevessels", "assignstinker", "cajolescuttles", "oracleadmission", "fairleadefficiency", "preacherlinkage", "herselfstability", "laganfuturistic", "givengaze", "yeastbrilliant", "boneheadprickly", "ossifiedbronze", "changeablecarrots", "joystickunable", "creeplectern", "observancedam", "thudpanties", "grapnelboozer", "confidecauliflower", "transhipsuccessful", "buildmeaning", "joblessonions", "lilyarchitect", "helmplonker", "gnawcuckoo", "butchercarved", "transireleaf", "cancelpilchard", "amazonwatch", "prankfussy", "wastefulgush", "gradetoyota", "dreadfulabhorrent", "onlinegray", "favorburger", "woofgallery", "bongofully", "clientchemical", "everybodysledding", "loweryogurt", "competingjay", "learncorn", "gratefulsurvey", "garbagepunctual", "hormonesstreak", "confronthandball", "wrongmedulla", "merchantdata", "bobcatcarrot", "nidedifficult", "rearendexalted", "bathingsuitclove", "agilesteal", "probablysnowy", "boyscoutslighten", "thesecavities", "cherriesexcuse", "sugarviolet", "guiltlesslazuli", "gerbilbehave", "pepperpowered", "ebayquack", "shockhurdle", "multiplycardinal", "democracyundress", "lardfacemare", "borngullible", "sneakanywhere", "literateexpert", "insanethreat", "grainswitch", "yelljust", "majorityshoal", "mourningbazaar", "friendshipfoamy", "introduceswim", "sleuthcool", "dressskeleton", "tipimminent", "pigmanhorror", "breakdownemerald", "eggplantspectral", "ravenopulent", "umpirefit", "heritagereading", "endermitescarlet", "affectpalpita", "oddtrice", "outcomeoffice", "polecatstake", "receptivekiller", "rebuffhorseman", "boredcrackle", "dragplot", "notablesoil", "bangbanggive", "mouthguardathletic", "transformgaseous", "crewfrequently", "respirationticktock", "exhibitinvest", "chimpanzeefossil", "relaysurfeit", "increasingnowhere", "ailscene", "equipmentoccipital", "firststash", "nutsvacuum", "sneakershead", "gleamingthe"
]

NUM_USERS = len(usernames)
USER_ID_RANGE = range(1, NUM_USERS+1)

passwords = ["password123"]*NUM_USERS

trusts = []
for _ in usernames:
    trusts.append(random.uniform(MIN_TRUST, MAX_TRUST))

users = pd.DataFrame(
    zip(usernames, passwords, trusts, usernames),
    index=USER_ID_RANGE,
    columns=["Username", "Password", "Trust", "Name"])

users.to_csv('./dataset_processing/prod_dataset/member.csv')

true_classifications = [
    # Apples
    10539, 9227, 1122,
    # Birds
    180,570,4090,6692,7162,9147,11278,13058,13231,179,426,481,653,980,1065,1164,1393,1435,1800,2378,2572
]

false_classifications = [
    # Apples
    10131, 208
]

submissions = [

]

# select class_id, original_url from classification NATURAL JOIN Image NATURAL JOIN Label WHERE name = 'Apple';
# select class_id, confidence, original_url from classificationview natural join label natural join image where name = 'Apple';

for class_id in true_classifications:
    for user_id in random.sample(USER_ID_RANGE, random.randrange(MIN_SUBS, MAX_SUBS)):
        rank = 1.6*math.sqrt(random.uniform(MIN_TRUST, MAX_TRUST)) < trusts[user_id-1]
        submissions.append((class_id, user_id, rank))

for class_id in false_classifications:
    for user_id in random.sample(USER_ID_RANGE, random.randrange(MIN_SUBS, MAX_SUBS)):
        rank = 1.6*math.sqrt(random.uniform(MIN_TRUST, MAX_TRUST)) >= trusts[user_id-1]
        submissions.append((class_id, user_id, rank))

print(submissions)

pd.DataFrame(
    submissions,
    columns=["ClassID", "UserID", "TrueOrFalse"]
).to_csv('./dataset_processing/prod_dataset/submission.csv', index=False)
