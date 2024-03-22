import requests
import json
from tkinter import *
from PIL import ImageTk, Image
import os
import atexit

url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
key = "{app key}"
id = "{app id}"

headers = {'Content-Type': 'application/json', 'x-app-id': id, 'x-app-key': key}

gui1 = Tk()

food1 = StringVar()

w = Label(gui1, text="Calorie Search")
c = Entry(gui1, textvariable=food1)
b = Button(gui1, text="Search", command=gui1.destroy)
w.grid()
c.grid()
b.grid()
gui1.mainloop()

query = json.dumps({
  "query": food1.get()
})

api = requests.post(url, headers=headers, data=query)

food = json.loads(api.text)

nutval = food.get("foods")[0]

photos = nutval.get("photo")

highres = photos.get("highres")

print(nutval)

url = highres
filename = url.split('/')[-1]
r = requests.get(url, allow_redirects=True)
open(filename, 'wb').write(r.content)

gui2 = Tk()
i1 = Image.open(filename)
print(int(i1.size[0] * 0.25),int(i1.size[1] * 0.25))
i1 = i1.resize((int(i1.size[0] * 0.25),int(i1.size[1] * 0.25)))
ph = ImageTk.PhotoImage(i1)
gui2.title(food1.get())
i = Label(gui2, image=ph)
w = Label(gui2, text=food1.get())
c = Label(gui2, text=str(nutval.get("nf_calories")) + "kcals!")
p = Label(gui2, text=str(nutval.get("nf_protein")) + "g of protein!")
i.grid()
w.grid()
c.grid()
p.grid()
gui2.mainloop()

def exit_handler():
    os.remove(filename)

atexit.register(exit_handler)