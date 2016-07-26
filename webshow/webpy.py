#-*- coding: UTF-8 -*-
import web
render = web.template.render('templates/')
urls=(
	"/","index"
)

app = web.application(urls,globals())
class index:
    def __init__(self):
        pass
    def GET(self):
        data=web.input()
        if data:
            searchword=data.searchword
        else:
            searchword=''
        target_list=list()
        topic=list()
        if searchword:
            while True:
                name,price,url=0,0,0#main.search(searchword)
                data = dict()
                data['name'] =name
                data['price']=price
                data['url'] = url #url.decode("utf-8")
                target_list.append(data)
        return render.index(searchword,target_list)


if __name__ == "__main__":
	app = web.application(urls,globals())
	app.run()
