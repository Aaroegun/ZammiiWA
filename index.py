import mysql.connector as sqlator
import json
import time
import requests

con= sqlator.connect(host="localhost",user="root", passwd="1234")


url = "https://graph.facebook.com/v14.0/107342252155803/messages"
headers = {
  'Authorization': 'Bearer EAAG4TjOkvoYBAD3XmcvcuPYOZCnAzqkBe9Gaz6vVcxHjaZBvt1rV6Vor4JDQWoM6kMZARAZBPsvw82XaPohzweAwaLYk1840TxJWpt3ykKxq5q19JMrZA2KVoA6N2TMDwxYuO26SGqoSZBWAZBJHCLYc8XHm6rRRd3rd02l2ZANZBZBGfpdo8I1URBeo8TBaE4ftydseOPazolgwZDZD',
  'Content-Type': 'application/json'
  }




def waButton(pnum, bodyText, buttons):
    msgFormat= {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": pnum,
        "type": "interactive",
        "interactive": {
        "type": "button",
        "body": {
        "text": bodyText
        },
        "action": {
            "buttons": []}}}
    for button in buttons:
        msgFormat["interactive"]["action"]["buttons"].append({"type":"reply","reply":{"id": button,"title":buttons[button]}})
    
    return msgFormat


def waList(pnum, bodyText, buttonName, sectionName, listItems):
    msgFormat={
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": pnum,
        "type": "interactive",
        "interactive": {
        "type": "list",
            "body": {
        "text": bodyText
        },
        "footer": {
            "text": "In Development"
            },
            "action": {
                "button": buttonName,
                "sections": [
                    {
                        "title": sectionName,
                        "rows": []}
                                ]
                                }
                                }
                                }

    for items in listItems:
        
        msgFormat["interactive"]["action"]["sections"][0]["rows"].append({"id": items, "title": listItems[items]})
    
    return msgFormat



crs=con.cursor(buffered=True)
crs.execute("use zammii")

userList = {}
userCList ={}

while True:
    message= input()

    if message.lower() =="home":
        data =  waButton(13182876695, "Welcome to bid helps \n Please select a option to continue", {"mainMenu": "Main menu", "support": "Call Us" })


    

    elif message.lower() == "mainmenu":

        statesList = {}
        crs.execute("select * from states where id>0 and id<9 ")
        sdata = crs.fetchall()
        for state in sdata:
            statesList[f"s{state[0]}"] = state[1]
        statesList["ns1"] = "Next"
        data = waList(13182876695, "Please Select a State\n Page 1", "States", "Available States", statesList)
    
    elif message.startswith("ns"):
        page = int(message[2:])
        lowerRange = (page-1) * 8
        upperRange = (page*8) + 1
        crs.execute(f"select * from states where id>{lowerRange} and id<{upperRange}")
        statesList = {}
        sdata = crs.fetchall()
        for state in sdata:
            statesList[f"s{state[0]}"] = state[1]
        statesList[f"ns{page+1}"] = "Next"
        statesList[f"ns{page-1}"] = "Previous"
        data = waList(13182876695, f"Please Select a State\n Page {page}", "States", "Available States", statesList)
    elif message.startswith("s"):
        stateId = int(message[1:])
        crs.execute(f"select id, name from cities where state_id = {stateId} ORDER BY name" )
        cityList = {}
        citydata =  crs.fetchmany(8)
        for city in citydata:
            cityList[f"c{city[0]}"] = city[1]
        cityList["nc1"] = "Next"
        data = waList(13182876695, "Please Select a District\n Page 1", "Districts", "Available Districts", cityList)
        userList["13182876695"] = stateId


    elif message.startswith("nc"):
        page = int(message[2:])
        stateId  = userList["13182876695"]
        crs.execute(f"select id, name from cities where state_id = {stateId} ORDER BY name" )
        cityList = {}
        citydata =  crs.fetchall()
        for elementId in range((page-1)*8, (page*8)-1):
            cityList[f"c{citydata[elementId][0]}"] = citydata[elementId][1]
        cityList[f"nc{page+1}"] = "Next"
        cityList[f"nc{page-1}"] = "Previous"
        data = waList(13182876695, f"Please Select a District\n Page {page}", "Districts", "Available Districts", cityList)
    
    elif message.startswith("c"):
        cityId = int(message[1:])
        crs.execute(f"select * from tenders")
        tenderList = {}
        tenderData = crs.fetchmany(8)
        for tender in tenderData:
            try:
                tenderList[f"t{tenderData[0]}"] = tenderData[1]
            except:
                pass
        data = waList(13182876695, "Please Select a Tender\n Page 1", "Tenders", "Available Tenders", tenderList)




        cityList[f"nc{page+1}"] = "Next"
        cityList[f"nc{page-1}"] = "Previous"
        print(cityList)
        data= waList(13182876695, f"Please Select a District\n Page {page}", "Districts", "Available Districts", cityList)
    

        
        





        

    elif message.lower() =="district":
        crs.execute("select*from states")
        states = crs.fetchall()
        lists = {}
        for i in states:
            lists[i[0]] = i[1]
        data = waList(13182876695, "Please Select Distrcts" , "Districts", "Available Districts", data)
         




    response = requests.request("POST", url, headers=headers, data=json.dumps(data))
    print(response.text)