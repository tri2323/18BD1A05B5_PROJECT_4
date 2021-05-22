import requests
from flask import Flask, render_template, request
from twilio.rest import Client
import requests_cache

account_sid = "ACd71a76d251951cc432c9a0bd38565c95"
auth = "7358f41982969f31712c58bc931f46ac"
client = Client(account_sid,auth)
app = Flask(__name__)
@app.route('/')
def registration_form():
    print(1)
    return render_template('home.html')
@app.route('/login_page',methods=["POST","GET"])
def login_registration_form():
    d = {"Andaman and Nicobar Islands" : "AN", "Andhra Pradesh" : "AP","Arunachal Pradesh":"AR","Assam":"AS","Bihar":"BR","Chandigarh":"CH","Chhattisgarh":"CT","Daman and Diu":"DN","Delhi":"DL","Goa":"GA","Gujarat":"GJ","Himachal Pradesh":"HP","Haryana":"HR","Jharkhand":"JH","Jammu and Kashmir":"JK","Karnataka":"KA","Lakshadweep":"LD","Kerala":"KL","Maharashtra":"MH","Meghalaya":"ML","Madhya Pradesh":"MP","Manipur":"MN","Mizoram":"MZ","Nagaland":"NL","Odisha":"OR","Punjab":"PB","Puducherry":"PY","Rajasthan":"RJ","Sikkim":"SK","Telangana":"TG","Tamil Nadu":"TN","Tripura":"TR","Uttar Pradesh":"UP","Uttarakhand":"UT","West Bengal":"WB"}
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    source_st = d[request.form['state']]
    source_ct = request.form['source']
    destination_st = d[request.form['dstate']]
    destination_ct = request.form['dcity']
    phNo = request.form['tele']
    date = request.form['date']
    aadhar = request.form['ano']
    full_name = fname + " " + lname
    r = requests.get("https://api.covid19india.org/v4/data.json")
    json_data = r.json()
    cnt = json_data[destination_st]["total"]["confirmed"] - json_data[destination_st]["total"]["recovered"]
    pop = json_data[destination_st]["meta"]["population"]
    limit = (cnt/pop)*100
    print(limit)
    if limit<30 and request.method=='POST':
        status = "CONFIRMED"
    else:
        status = "NOT CONFIRMED"
    client.messages.create(to="whatsapp:+918985176686", from_= "whatsapp:+14155238886",body="Hello "+ full_name +", your travel from"+" "+ source_ct +", "+source_st+" to "+ destination_ct +", "+destination_st+ " has "+status+" "+"on "+date)
    return render_template('display.html',var1=full_name, var2=email,var3=aadhar,var4=source_st,var5=source_ct,var6=destination_st,var7=destination_ct,var8=phNo,var9=date,var10=status)
if __name__=="__main__":
    app.run(port=3001,debug=True)