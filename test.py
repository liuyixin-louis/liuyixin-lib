s = ""
with open('a.out',mode="r+") as f:
    for fi in f.readlines():
        # print()
        # break
        s+=fi.split("\t")[1]+"\n"
        
with open("a.out",mode="w+") as f:
    f.write(s)
