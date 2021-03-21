import requests
import os
import json
from twilio.rest import Client
import csv
import numpy as np
import requests


# To set your enviornment variables in your terminal run the following line:

account_sid = os.environ['account_sid']
auth_token = os.environ['auth_token']
bearer_token = os.environ['BEARER_TOKEN']
from_number_with_plus = os.environ['from_number_with_plus']
to_number = os.environ['to_number']



#with open('usernames.csv', newline='') as csvfile:
#    data = list(csv.reader(csvfile))


accounts_to_follow_all_tweets = ["GaetenD","Gandalf_of_PI"]
keywords = ["Miller","Meeks","Iowa","IA-02","IA02"]
#keywords = ["are","the"]

big_list_accounts = ["cnnbrk",
"BBCBreaking",
"BreakingNews",
"Reuters",
"CNBCnow",
"AP",
"bpolitics",
"playbookdc",
"PunchbowlNews",
"politicoelex",
"politico",
"reason",
"wef",
"TheEconomist",
"WSJ",
"BBCWorld",
"SCOTUSblog",
"nytimes",
"washingtonpost",
"plural_vote",
"DKElections",
"CookPolitical",
"MollyJongFast",
"JakeLahut",
"NateSilver538",
"Nate_Cohn",
"Redistrict",
"kdrum",
"Giambusso",
"annagronewold",
"arindube",
"sahilkapur",
"tarapalmeri",
"brettcannon",
"kasie",
"hugolowell",
"Phil_Mattingly",
"seungminkim",
"GregStohr",
"Zachary_Cohen",
"JaneMayerNYer",
"AmyEGardner",
"jdawsey1",
"DanielPFlatley",
"yeselson",
"lindsaywise",
"DanaBashCNN",
"jmartNYT",
"elwasson",
"sarahnferris",
"StevenTDennis",
"heatherscope",
"marianne_levine",
"MZanona",
"SeanPrevil",
"EmmaKinery",
"politicoalex",
"AndrewSolender",
"grace_panetta",
"AndrewFeinberg",
"Acosta",
"maggieNYT",
"PhilipRucker",
"pkcapitol",
"AshleyRParker",
"rachaelmbade",
"burgessev",
"JStein_WaPo",
"stevennelson10",
"JakeSherman",
"samjmintz",
"KatyODonnell_",
"hbottemiller",
"connorobrienNH",
"liz_crampton",
"GavinBade",
"sabrod123",
"theodoricmeyer",
"AlexThomp",
"AliceOllstein",
"mmcassella",
"TrackerVote",
"laraseligman",
"NatashaBertrand",
"tylerpager",
"kirk_bado",
"kaitlancollins",
"marceelias",
"ChadPergram",
"jaselzer",
"peterbakernyt",
"kkondik",
"mattyglesias",
"jbarro",
"gtconway3d",
"jaketapper",
"TedNesi",
"JustinGrayWSB",
"BrendanKeefe",
"Garrett_Archer",
"hjessy_",
"conorsen",
"WinWithJMC",
"RalstonReports",
"HouseDailyPress",
"SenatePPG",
"SenatePress",
"PleaseEv"]

big_list_accounts = accounts_to_follow_all_tweets + big_list_accounts


stringOfAccounts=""
stringOfAccountsRule1 = ""
stringOfAccountsRule2 = ""
stringOfAccountsRule3 = ""
stringOfAccountsRule4 = ""
stringOfAccountsRule5 = ""
stringOfKeywords = ""


for x in keywords:
    stringOfKeywords=stringOfKeywords+x+" OR "

stringOfKeywords=stringOfKeywords[:-4]
keywordsWithPars= '(' + stringOfKeywords + ')'




for x in big_list_accounts:

 if (len(stringOfAccountsRule1)+len(x)+5)<=512:
     stringOfAccountsRule1=stringOfAccountsRule1+"from:"+x+" OR "
     
 else:

     if (len(stringOfAccountsRule2)+len(x)+5)<=512:
         stringOfAccountsRule2=stringOfAccountsRule2+"from:"+x+" OR "

     else:

         if (len(stringOfAccountsRule3)+len(x)+5)<=512:
             stringOfAccountsRule3=stringOfAccountsRule3+"from:"+x+" OR "

         else:

             if (len(stringOfAccountsRule4)+len(x)+5)<=512:
                 stringOfAccountsRule4=stringOfAccountsRule4+"from:"+x+" OR "

             else:

                 if (len(stringOfAccountsRule5)+len(x)+5+len(keywordsWithPars)+3)<=512:
                     stringOfAccountsRule5=stringOfAccountsRule5+"from:"+x+" OR "
                 else:
                     print("string too long! Here's what you miss " + x)
                 
    




stringOfAccountsRule1=stringOfAccountsRule1[:-4]
stringOfAccountsRule2=stringOfAccountsRule2[:-4]
stringOfAccountsRule3=stringOfAccountsRule3[:-4]
stringOfAccountsRule4=stringOfAccountsRule4[:-4]
stringOfAccountsRule5=stringOfAccountsRule5[:-4]

rule5WithPars= '(' + stringOfAccountsRule5 + ')'

#keywordsPlusRule5 = rule5WithPars + " " + keywordsWithPars
keywordsPlusRule5 = rule5WithPars




client = Client(account_sid, auth_token)


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def get_rules(headers, bearer_token):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(headers, bearer_token, rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload
        )

    

    
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(headers, delete, bearer_token):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": stringOfAccountsRule1},
        {"value": stringOfAccountsRule2},
        {"value": stringOfAccountsRule3},
        {"value": stringOfAccountsRule4},
        {"value": keywordsPlusRule5}
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(headers, set, bearer_token):
    ticker = 0
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream?expansions=author_id&user.fields=created_at", headers=headers, stream=True,
    )
    
    print(response.status_code)
    print("Currently Streaming")
    
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            print(json.dumps(json_response, indent=4, sort_keys=True))
            
            success = 0
            text_sent=0

            for account_x in accounts_to_follow_all_tweets:
                if json_response['includes']['users'][0]['name'] ==account_x:
                    print("success")
                    success = 1

                    keyword = ""
                    send_text(headers, set, bearer_token, json_response, keyword)

                    text_sent = 1
                    break
                    

            if text_sent != 1:
                for word in keywords:
                    if word in json_response['data']['text']:
                        print("success")
                        success = 1

                        keyword = "Keyword: " + word
                        send_text(headers, set, bearer_token, json_response, keyword)
                        break


            if success ==0:
                print("failure")
                



def send_text(headers, set, bearer_token, json_response, keyword):
    linebreak = '\n'
    space = ' '

    # time_now = json_response['includes']['users'][0]['created_at']
    # time_now=time_now[:-5]
    # time_now = time_now[11:]

    message = client.messages \
        .create(

            body= '.' + linebreak
            + linebreak
            + json_response['includes']['users'][0]['name'] + linebreak 
            + "(@" + json_response['includes']['users'][0]['username'] + ")" + linebreak 
            + linebreak 
            + "- - - - - - - - - - - - - - - - - - - - - - -"+ linebreak 
            + json_response['data']['text'] + linebreak 
            + "- - - - - - - - - - - - - - - - - - - - - - -"+ linebreak 
            + keyword
            ,

            from_=from_number_with_plus,
            to=to_number
                     
        )

                



def main():
    bearer_token = os.environ.get("BEARER_TOKEN")
    headers = create_headers(bearer_token)
    rules = get_rules(headers, bearer_token)
    delete = delete_all_rules(headers, bearer_token, rules)
    set = set_rules(headers, delete, bearer_token)
    print()
    print()
    print(stringOfAccountsRule1)
    print()
    print()
    print(stringOfAccountsRule2)
    print()
    print()
    print(stringOfAccountsRule3)
    print()
    print()
    print(stringOfAccountsRule4)
    print()
    print()
    print(keywordsPlusRule5)
    print()
    print()
    print(keywords)
    print()
    get_stream(headers, set, bearer_token)



if __name__ == "__main__":
    main()
