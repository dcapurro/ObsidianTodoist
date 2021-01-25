# load what we need
from datetime import datetime
import os
from todoist.api import TodoistAPI

#FOr the token, use string of your TodoIst account

token = ''

# create a TodoistAPI object with the token, which we store to the api variable
api = TodoistAPI(token)

# This step is not necessary, but I also created a To Do note inside obsidian
# to store my todos. In this case I , my file is called Todos.md
# you can call it whatever you want but you need to modify the name here.
# You need to add the path to the todo file

ToDoFile = 'path_toMy_file/ToDos.md'
count = 0

# directory is the path to the obsidian repository
directory = r'path_to_obsidian_repository'
for subdir, dirs, files in os.walk(directory):
    for filename in files:
        filepath = subdir + os.sep + filename

# This is where we read all files in the repository. If your
# file contains a line that starts with [x] then the script will create a todo
# item in Todoist and replace the [x] with a [ok] so it won't read it multiple times
# here I also add ech todo to the Todos.md file I mentioned before...
        if filepath.endswith(".md"):
            file1 = open(filepath, 'r')
            while True:
                count += 1
                line = file1.readline()
                if line[0:3] == '[x]':
                    f = open(ToDoFile, 'a+')  # open file in append mode
                    f.write("- " + line[3:] + ' ' + datetime.today().strftime('%d-%m-%Y') + '\n')
                    f.close()

                    # Fetches the latest updated data from the server.
                    api.sync()
                    task1 = api.items.add(line[3:])
                    api.commit()

                # if line is empty
                # end of file is reached
                if not line:
                    break

            #read input file
            fin = open(filepath, "rt")
            #read file contents to string
            data = fin.read()
            #replace all occurrences of the required string
            data = data.replace('[x]', '[ok]')
            #close the input file
            fin.close()
            #open the input file in write mode
            fin = open(filepath, "wt")
            #overrite the input file with the resulting data
            fin.write(data)
            #close the file
            fin.close()
            file1.close()
