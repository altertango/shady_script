import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep

find_rows=['PHE7','PHE9','PHE10','PHE11', 'PHE13']

output=[]
f="Numbers.csv"
count=0
with open(f, "rt", encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for line in reader:
        TheNumber = line[0]
        print("searching for number " + str(TheNumber))


        url="https://gradecard.ignou.ac.in/gradecardB/Result.asp?eno="+str(TheNumber)+"&program=BSC&hidden_submit=OK"

        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'dnt': '1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'none',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            }
        )

        f = urllib.request.urlopen(req)
        soup = BeautifulSoup(f.read(), 'html.parser')
        
        rows = soup.find_all('tr')
        table=[row.find_all('td') for row in rows]
        
        for r in table:
            aux=[TheNumber]
            isPH=False
            for c in r:
                ct=c.get_text()
                if isPH:
                    aux.append(ct)
                    isPH=False
                elif ct in find_rows:
                    aux.append(ct)
                    isPH=True
            if len(aux)>1:
                if int(aux[-1])>80 and int(aux[-1])<90:
                    print(aux)
                    output.append(aux)
        count+=1
        if count>30: break
with open('output.csv', 'wt', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for o in output:
        spamwriter.writerow(o)
input("Press Enter to continue...")
