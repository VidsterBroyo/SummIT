from flask import Flask, request
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
CORS(app)

maintainStyle = True

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}

@app.route("/getScrapedSite", methods=['POST'])
def getScrapedSite():
    link = request.get_json()["url"]
    print("\nLINK: ", link)

    maintainStyle = True

    try:
        response = requests.get(link, headers=HEADERS, timeout=10)
    except:
        return "Sorry, something went wrong :("
    
    websiteHTML = response.text

    soup = BeautifulSoup(websiteHTML, "html.parser")

    file = open("websiteInput.html", "w", encoding="utf-8")
    file.write(soup.prettify())
    file.close()


    # for ads in soup.select(".ad-container") + soup.select("[class*=headerAd]") + soup.select("[class*=ad-class]") + soup.select("[class^=adsbox]"):
    for ads in soup.select("[class^=ad i]") + soup.select("[class$=ad i]") + soup.select("[class*=-ad i]"):
        ads.decompose()


    # remove images
    for image in soup.find_all("img"):
        print("REMOVING IMAGE:", image)
        if image.attrs.get("alt"):
            imageParagraph = BeautifulSoup(f"<p style='line-height: 15px; background: rgba(255, 255, 255, 0.5);'><i>Image Removed. Alt text: {image.attrs.get("alt")}</i></p>", "html.parser")
        else:
            imageParagraph = BeautifulSoup("<p style='background: rgba(255, 255, 255, 0.5);'><i>Image Removed</i></p>", "html.parser")

        image.replace_with(imageParagraph)


    # remove icons (svg)
    for icon in soup.find_all("svg"):
        icon.decompose()


    # remove videos
    for video in soup.find_all("video"):
        video.replace_with(BeautifulSoup(f"<p style='background: rgba(255, 255, 255, 0.5);'><i>Video removed</i></p>", "html.parser"))


    # remove embed
    for iframe in soup.find_all("iframe") + soup.find_all("embed"):
        if title:=iframe.attrs.get("title"):
            iframeParagraph = BeautifulSoup(f"<p style='background: rgba(255, 255, 255, 0.5);'><i>Embed removed. Title: {title}</i></p>", "html.parser")
        else:
            iframeParagraph = BeautifulSoup("<p style='background: rgba(255, 255, 255, 0.5);'><i>Embed removed.</i></p>", "html.parser")

        iframe.replace_with(iframeParagraph)


    # remove references to files from links & removes scripts
    for reference in soup.find_all("script"):
        reference.decompose()



    if maintainStyle:
        # find domain name
        if (link.count("/") > 2):
            domainName = link[:link.find("/", 8)]
        else:
            domainName = link
    
        print("DOMAIN NAME: ", domainName)

        # disabling import links and keeping css files
        for i in soup.find_all("link", href=True):
            href = i["href"]

            # check if the link is for styling
            if href.endswith(".css") or href.endswith(".woff") or href.startswith("https://fonts"):
                print("\nKEEPING the following link:")
                print(href)

                # add the full link if it doesn't have it already
                if not href.startswith("http"):
                    i['href'] = domainName + href


            # if not,
            else:
                # if there are no children, delete it
                if len(i.contents) == 0:
                    print("\nDELETING the following link:")
                    print(href)
                    i.decompose()

                # if there are, just remove the href attribute
                else:
                    print("\nDISABLING the following link:")
                    print(href)
                    del i['href']
        

        # change links so that they use SummIT to render
        for link in soup.find_all("a", href=True):
            href = link["href"]

            # add the full link if it doesn't have it already
            if not href.startswith("http"):
                href = domainName + href
                # print("fixed link:", href)

            link["href"] = "javascript:void(0);"
            link["onclick"] = "generateSite('"+href+"')"
            # print(href)



    else:

        # turn navbar into hidden section
        compiledHeaders = "" # compile all headings/navbars
        for navBar in soup.find_all("header") + soup.find_all("nav") + soup.select(".l-navWrapper"):
            try:
                compiledHeaders += str(navBar)
                navBar.decompose()
            except:
                print("error happened")
                continue

        # put them all at the top
        hiddenNav = BeautifulSoup(f"<details id='hiddenNav' style='background-color:lightgrey'> <summary style='background-color:white'><b>Navigation Bar</b></summary> {compiledHeaders} </details>", "html.parser")
        soup.body.insert(1, hiddenNav)


        
        # remove buttons + input boxes
        for element in soup.find_all("button") + soup.find_all("input"):
            element.decompose()


        # turn footer into hidden section
        if soup.find("footer"):
            footers = soup.find_all("footer")
            hiddenFooter = BeautifulSoup(f"<details id='hiddenFooter' style='background-color:lightgrey'> <summary style='background-color:white'><b>Footer</b></summary> {''.join(str(footer) for footer in footers)} </details>", "html.parser")
            soup.footer.replace_with(hiddenFooter)

            for i in soup.find_all("footer"):
                if i.parent.name != "details":
                    i.decompose()


        for i in soup.find_all("link"):
            i.decompose()


    soup.head.append(BeautifulSoup('<script src="/static/script.js"></script>', features="html.parser"))
    soup.head.append(BeautifulSoup('<link rel="stylesheet" href="static/style.css" type="text/css">', features="html.parser"))

    
    file = open("websiteOutput.html", "w", encoding="utf-8")
    file.write(soup.prettify())
    file.close()
    return soup.prettify()


    
if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 81)