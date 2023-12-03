from urllib.request import urlopen
from urllib.error import HTTPError
import mysql.connector
import csv

conn = mysql.connector.connect (
    host = "localhost",
    user = "root",
    passwd = "",
    database = "python"
)

cursor = conn.cursor()
#cursor.execute("CREATE TABLE accounts (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, username VARCHAR(13), rank INT, level INT, xp VARCHAR(255))")

skills = ["attack","defence","strength","hitpoints","ranged","prayer","magic","cooking","woodcutting","fletching","fishing","firemaking","crafting","smithing","mining","herblore","agility","thieving","slayer","farming","runecrafting","hunter","construction"];

#usernameInput = input("OSRS username: ")
usernameInput = "Zlimon"
#len(usernameInput) <= 13 &

#def createSkillTables(skillName):
    #cursor.execute("CREATE TABLE " + skillName + " (id INT AUTO_INCREMENT PRIMARY KEY, account_id INT, rank INT, level INT, xp VARCHAR(255))")

#for skill in skills:
    #createSkillTables(skill)

if len(usernameInput) >= 1:
    accountUrl = "https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player=" + usernameInput

    try:
        getAccount = urlopen(accountUrl)
    except HTTPError as err:
        if err.code == 404:
            print (err.code)
            print ("This user does not exist!")
        else:
            print ("An error occured!")
    except:
        print ("An unknown error occured!")
    else:
        accountBytes = getAccount.read()
        accountStats = accountBytes.decode("utf-8")

        readAccountStats = csv.reader(accountStats.split('\n'), delimiter = ',')

        checkIfAccountExist = "SELECT * FROM accounts WHERE username = '%s'" % (usernameInput)
        cursor.execute(checkIfAccountExist)
        checkIfAccountExist = cursor.fetchone()

        if checkIfAccountExist:
            print ("Updating user!")

            accountHiscores = next(readAccountStats)

            accountHiscoresStats = []

            for accountHiscoresStat in accountHiscores:
                accountHiscoresStats.append(accountHiscoresStat)

            updateAccount = "UPDATE accounts SET rank = %s, level = %s, xp = %s WHERE username = %s"
            cursor.execute(updateAccount, (accountHiscoresStats[0], accountHiscoresStats[1], accountHiscoresStats[2], usernameInput))

            skillCount = 0

            for accountStat in readAccountStats:
                if skillCount == (len(skills)) : break

                updateSkill = "UPDATE " + skills[skillCount] + " SET rank = %s, level = %s, xp = %s WHERE account_id = %s"
                skillValue = (accountStat[0], accountStat[1], accountStat[2], 1)
                cursor.execute(updateSkill, skillValue)

                skillCount += 1

            conn.commit()

            print ("Done!")
        else:
            print ("User is not registered!")

            insertAccount = "INSERT INTO accounts (user_id, username, rank, level, xp) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insertAccount, (1, usernameInput, 0, 0, "0"))

            next(readAccountStats, None)

            skillCount = 0

            for accountStat in readAccountStats:
                if skillCount == (len(skills)) : break
                    
                insertSkill = "INSERT INTO " + skills[skillCount] + " (account_id, rank, level, xp) VALUES (%s, %s, %s, %s)"
                skillValue = (1, accountStat[0], accountStat[1], accountStat[2])
                cursor.execute(insertSkill, skillValue)

                skillCount += 1

            conn.commit()

            print ("Done!")
    finally:
        getAccount.close()
else:
    print ("Too long or short")
