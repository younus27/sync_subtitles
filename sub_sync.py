from tkinter import *
from tkinter import filedialog
from datetime import datetime
from datetime import timedelta


def browseFiles():
	
	global file_name, extenstion

	label_warning.configure(text="")
	label_warning.place_forget()

	complete_filename = filedialog.askopenfilename(	initialdir = "/",	title = "Select a File",
											filetypes = (("Srt files","*.srt*"),("All files","*.*")))

	file_name = ".".join(complete_filename.split(".")[:-1])
	extenstion = complete_filename.split(".")[-1]

	if extenstion != "srt":
		label_warning.place(x = 0, y = 60, width=400, height=25)
		label_warning.configure(text="Please select .srt file")
		sec_label.place_forget()
		sec.place_forget()
		label_file_explorer2.place_forget()	
		button_convert.place_forget()

	else:
		label_warning.place_forget()
		label_file_explorer2.configure(text="File Opened: "+file_name.split("/")[-1]+".srt" , fg = "blue")

		sec_label.place(x = 200, y = 60, width=60, height=25)
		sec.place(x = 280, y = 60, width=100, height=25)
		label_file_explorer2.place(x = 20, y = 100, width=240, height=25)

		button_convert.place(x = 280, y = 100, width=100, height=25)


def sync_time(time,shift):
	if time.split(",")[-1] == "000":
		time = time.split(",")[0]+",001"
	fulldate = datetime.strptime("2022-01-01" + ' ' + time, "%Y-%m-%d %H:%M:%S,%f")
	fulldate = fulldate + timedelta(milliseconds=shift)
	return str(fulldate).split(" ")[-1][:-3].replace(".",",")


def convert():
	
	global file_name, extenstion
	
	shift = int(sec.get())*1000
	synced_subtitles=[]	

	try:
		with open(file_name+"."+extenstion,"r") as f:
			subtitles = f.read().split("\n\n")[:-1]

		for line in subtitles:

			l = line.split("\n")

			index = l[0]
			dutation = l[1]
			sub = l[2:]

			if len(sub)>1:
				sub = "\n".join(sub)
			else:
				sub = sub[0]

			start_time, end_time =  dutation.split(" --> ")

			synced_start_time = sync_time(start_time,shift)
			synced_end_time = sync_time(end_time,shift)

			synced_duration = synced_start_time+" --> "+synced_end_time
			synced_line = index+"\n"+synced_duration+"\n"+sub

			synced_subtitles.append(synced_line)

		with open(file_name+"_synced."+extenstion,"w") as f:
			for line in synced_subtitles:
				f.write(line)
				f.write("\n\n")

		label_file_explorer2.configure(text="Completed : "+file_name.split("/")[-1]+"_synced.srt" , fg = "green")

	except Exception:
		label_warning.configure(text="Please select .srt file")     
	

if __name__ == "__main__":
	window = Tk()
	window.title('Sync Subtitles')
	window.geometry("400x140")
	window.config(background = "white")

	var = StringVar(window)
	var.set("0")

	label_file_explorer = Label(window, text = "Select .srt File", width = 70, height = 2, fg = "blue")
	label_file_explorer.place(x = 20, y = 20, width=240, height=25)

	button_explore = Button(window, text = "Browse Files", width = 30, height = 2, command = browseFiles)
	button_explore.place(x = 280, y = 20, width=100, height=25)


	label_warning = Label(window, text = "", width =80, height = 3, fg = "red", bg="white")


	sec_label = Label(window, text = "+/- sec", width = 70, height = 2, fg = "black")
	sec = Spinbox(window, from_= -1800, to = 1800 , textvariable=var)
	label_file_explorer2 = Label(window, text = "", width = 70, height = 2, fg = "blue")

	button_convert = Button(window, text = "Convert", width = 30, height = 2, command = convert)

	window.mainloop()
