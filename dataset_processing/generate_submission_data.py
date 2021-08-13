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
    180, 570, 4090, 6692, 7162, 9147, 11278, 13058, 13231, 179, 426, 481, 653, 980, 1065, 1164, 1393, 1435, 1800, 2378, 2572,
    # Non popular
    11, 27, 65, 70, 72, 73, 75, 79, 110, 111, 127, 147, 161, 171, 177, 208, 211, 234, 242, 243, 299, 343, 370, 401, 407, 410, 428, 440, 458, 460, 463, 467, 471, 475, 484, 497, 504, 551, 573, 591, 596, 598, 599, 612, 631, 638, 639, 661, 663, 685, 695, 699, 710, 739, 761, 762, 770, 773, 793, 794, 942, 990, 991, 994,1014,1024,1028,1038,1060,1072,1074,1122,1126,1131,1135,1136,1168,1171,1178,1208,1215,1218,1243,1267,1269,1284,
    13197, 13217, 13227, 13230, 13232, 13237, 13276, 13290, 13291, 13294, 13297, 13298, 13308, 13326, 13336, 13341, 13351, 13352, 13353, 13356, 13372, 13373, 13385

]
false_classifications = [
    # Apples
    10131, 208,
    # Non popular
    74, 78, 112, 163, 330, 365, 406, 434, 474, 632, 641, 677, 712, 714, 723, 850, 924, 981, 982, 999, 1130, 1214, 1260, 1295,
    13342, 13328, 13325, 13301, 13236, 13228, 13220, 13211, 13210, 13187
]

# select class_id, name, original_url from classification natural join image natural join label where name in (select label from imglabel group by label having COUNT(*) < 10) and class_id < 1295 order by class_id desc;
submissions = [

]

# (SELECT 10131, 208, 74, 78, 112, 163, 330, 365, 406, 434, 474, 632, 641, 677, 712, 714, 723, 850, 924, 981, 982, 999, 1130, 1214, 1260, 1295)
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


# select label from imglabel group by label having COUNT(*) < 10;


# select class_id, name, original_url from classification natural join image natural join label where name in (select label from imglabel group by label having COUNT(*) < 10);