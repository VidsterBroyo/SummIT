
function generateSite(url) {
    if (url == "form") {
        url = document.getElementById("url").value
        if (!url.startsWith("https://")){
            alert("URL must begin with 'https://'")
            return
        }
    }
    // let maintainStyle = document.getElementById("maintainStyle").checked

    var request = new XMLHttpRequest()
    // request.open('POST', 'http://localhost:81/getScrapedSite', false)
    request.open('POST', 'http://35.183.18.174:81/getScrapedSite', false)
    request.setRequestHeader("Content-Type", "application/json");
    body = {
        "url": url,
        // "styling": maintainStyle
    }
    request.send(JSON.stringify(body))

    console.log(request.responseText)
    document.write(request.responseText)
    document.close()
    window.scrollTo(0, 0);
}