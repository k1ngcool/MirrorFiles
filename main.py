import requests
import tkinter as tk
import easygui
from concurrent.futures import ThreadPoolExecutor
import gofile
import fileioapi

file_path = ""


def filepath():
    global file_path
    file_path = easygui.fileopenbox()


def upload_fileio():
    resp = fileioapi.upload(file_path)
    download_link = resp['link']
    print(download_link)
    textbox.insert(tk.END, download_link + "\n")


def upload_gofile():
    response = gofile.uploadFile(file_path)
    download_link = response['downloadPage']
    print(download_link)
    textbox.insert(tk.END, download_link + "\n")


def button2_clicked():
    with open("mirrors.txt", 'r') as file:
        with ThreadPoolExecutor() as executor:
            futures = []
            for line in file:
                line = line.strip()
                if line:
                    url, name = line.split('|')
                    future = executor.submit(upload_file, url, file_path, name)
                    futures.append(future)
            for future in futures:
                try:
                    result = future.result()
                    if result:
                        textbox.insert(tk.END, result + "\n")
                except Exception as e:
                    print(f'Error: {e}')


def upload_file(upload_url, file_path, name):
    with open(file_path, 'rb') as file:
        response = requests.post(upload_url, files={'file': file})

    if response.status_code == 200:
        json_response = response.json()
        print(f'{name}: Success!')
        full_link = json_response['data']['file']['url']['full']
        return full_link
    else:
        print(f'{name}: Error! errorcode:', response.status_code)
        raise Exception(f'{name}: Error! errorcode:', response.status_code)


# tkinter stuff
window = tk.Tk()
window.title("MirrorFiles - v0.2")
window.geometry("800x430")

button1 = tk.Button(window, text="File", command=filepath)
button1.pack(fill="x")

textbox = tk.Text(window, width=90, height=20)
textbox.pack()

button2 = tk.Button(window, text="18 Anonfiles Mirrors", command=button2_clicked)
button2.pack(fill="x")

button3 = tk.Button(window, text="Gofile", command=upload_gofile)
button3.pack(fill="x")

button4 = tk.Button(window, text="File.io", command=upload_fileio)
button4.pack(fill="x")

window.mainloop()
