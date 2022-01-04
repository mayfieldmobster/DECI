import os
import magic
import zipfile
import math
import shutil

magic

def split_dir(path, num_nodes,AM_I = False, paired = False):
    files = os.listdir(path)
    if path[-1] == "/":
        path_name = path.split("/")[-2]

    else:
        path_name = path.split("/")[-1]

    if not path[-1] == "/":
        path = path + "/"

    dirs = []

    for file in files:
        if os.path.isdir(path +file):
            dirs.append(path + file)

    if AM_I:
        num_nodes += 1


    if len(dirs) == 0:
        group_size = math.ceil(len(files)/num_nodes)

        if not paired:
            files = [files[x:x+group_size] for x in range(0, len(files), group_size)]
            print(files)
            index = 0
            for group in files:
                filename = path + path_name +str(index) + ".zip"
                index += 1
                zip_obj = zipfile.ZipFile(filename, "w")
                for file in group:
                    zip_obj.write(path + file)

                zip_obj.close()


        elif paired:
            group_size = math.ceil(len(files) / num_nodes)

            files = [files[x:x + 2] for x in range(0, len(files), 2)]
            files = [files[x:x + group_size] for x in range(0, len(files), group_size)]
            index = 0
            for group in files:
                filename = path + path_name + str(index) + ".zip"
                index += 1
                zip_obj = zipfile.ZipFile(filename, "w")
                for file in group:
                    zip_obj.write(path + file[0])
                    zip_obj.write(path + file[1])

                zip_obj.close()




    if len(dirs) > 0:

        dir_names = []
        dir_index = 0
        for dir in dirs:
            dir_names.append(dir.replace(path,""))

        for dir in dirs:
            files = os.listdir(dir)
            group_size = math.ceil(len(files)/num_nodes)
            print(group_size)

            if not paired:
                files = [files[x:x + group_size] for x in range(0, len(files), group_size)]
                print(files)
                index = 0
                for group in files:
                    for file in group:

                        try:
                            os.mkdir(path + path_name + str(index))
                        except:
                            "directroy already exists"

                        try:
                            os.mkdir(path + path_name + str(index) + "/" + dirs[dir_index].replace(path, ""))
                        except:
                            "directroy already exists"
                        shutil.copyfile(dirs[dir_index] + "/" + file,
                                        path + path_name + str(index) + "/" + dirs[dir_index].replace(path, "") + "/" + file
                                        )

                    index += 1



            elif paired:
                files = [files[x:x + 2] for x in range(0, len(files), 2)]
                files = [files[x:x + group_size] for x in range(0, len(files), group_size)]
                print(files)
                index = 0
                for group in files:
                    for file in group:

                        try:
                            os.mkdir(path + path_name + str(index))
                        except:
                            "directory already exists"

                        try:
                            os.mkdir(path + path_name + str(index) + "/" + dirs[dir_index].replace(path, ""))
                        except:
                            "directory already exists"

                        shutil.copyfile(dirs[dir_index] + "/" + file,
                                        path + path_name + str(index) + "/" + dirs[dir_index].replace(path,"") + "/" + file[0]
                                        )
                        shutil.copyfile(dirs[dir_index] + "/" + file,
                                        path + path_name + str(index) + "/" + dirs[dir_index].replace(path, "") + "/" +
                                        file[1]
                                        )
                    index += 1

            dir_index += 1

        for i in range(num_nodes):
            shutil.make_archive(path + path_name + str(i), "zip", path + path_name + str(i))
            shutil.rmtree(path + path_name + str(i))



if __name__ == "__main__":
    split_dir("./data/", 3)
