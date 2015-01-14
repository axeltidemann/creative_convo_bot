from pattern.web import URL, DOM

def popular_hashtags():

    url = URL("https://hashtags.org")
    src = url.download()
    dom = DOM(src)

    popular = {}

    for div in dom("div.box2 div.textwidget div"):
        category = div("strong")[0].content
        hashtags = [ a.content for a in div("a") ]
        popular[category] = hashtags

    return popular

if __name__ == '__main__':
    print popular_hashtags()
