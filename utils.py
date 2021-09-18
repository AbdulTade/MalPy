delimiter = "\x12"
delimLower = "\x05"

toMoorse = {
    "A" : "*_",
    "B" : "_***",
    "C" : "_*_*",
    "D" : "_**",
    "E" : "*",
    "F" : "**_*",
    "G" : "__*",
    "H" : "****",
    "I" : "**",
    "J" : "*___",
    "K" : "_*_",
    "L" : "*_**",
    "M" : "__",
    "N" : "_*",
    "O" : "___",
    "P" : "*__*",
    "Q" : "__*_",
    "R" : "*_*",
    "S" : "***",
    "T" : "_",
    "U" : "**_",
    "V" : "***_",
    "W" : "*__",
    "X" : "_**_",
    "Y" : "_*__",
    "Z" : "__**",
    "1" : "*____",
    "2" : "**___",
    "3" : "***__",
    "4" : "****_",
    "5" : "*****",
    "6" : "_****",
    "7" : "__***",
    "8" : "___**",
    "9" : "____*",
    "0" : "_____",
    "a" : f"{delimLower}*_",
    "b" : f"{delimLower}_***",
    "c" : f"{delimLower}_*_*",
    "d" : f"{delimLower}_**",
    "e" : f"{delimLower}*",
    "f" : f"{delimLower}**_*",
    "g" : f"{delimLower}__*",
    "h" : f"{delimLower}****",
    "i" : f"{delimLower}**",
    "j" : f"{delimLower}*___",
    "k" : f"{delimLower}_*_",
    "l" : f"{delimLower}*_**",
    "m" : f"{delimLower}__",
    "n" : f"{delimLower}_*",
    "o" : f"{delimLower}___",
    "p" : f"{delimLower}*__*",
    "q" : f"{delimLower}__*_",
    "r" : f"{delimLower}*_*",
    "s" : f"{delimLower}***",
    "t" : f"{delimLower}_",
    "u" : f"{delimLower}**_",
    "v" : f"{delimLower}***_",
    "w" : f"{delimLower}*__",
    "x" : f"{delimLower}_**_",
    "y" : f"{delimLower}_*__",
    "z" : f"{delimLower}__**",
}
 
#toMoorse dictionary is reversed, so that values become keys and keys become values
fromMoorse = {value : key for key,value in toMoorse.items()}
fromMoorse = dict(reversed(list(fromMoorse.items())))

print(fromMoorse)

class Utils:

    def __init__(self) -> None:
        pass
        
    def toMoorseCode(self,path):
        contentToWrite = ""
        with open(path,'r') as f:
            contents = f.read()
            for i in range(len(contents)):
                code = ord(contents[i])
                if((code <= 122 and code >= 97) or (code <= 90 and code >= 65)):
                    contentToWrite = contentToWrite + delimiter + toMoorse[contents[i]]
                else:
                    contentToWrite = contentToWrite + contents[i]
            f.close()
        return contentToWrite

    def fromMoorseCode(self,path):
        contents = ''
        codes = []
        with open(path,'r') as f:
            contents = f.read()
            f.close()
        codes = contents.split(delimiter)
        for i in range(len(codes)):
            try:
                codes[i] = codes[i].replace(codes[i],fromMoorse[codes[i]])
            except KeyError as e:
                continue
        contents = ''.join(codes)
        return contents


if __name__ == '__main__':
    out = Utils().toMoorseCode('C:\\Users\\anonymous-legion\\Documents\\Projects\\pyMalware\\Malware-Attack-Strategy.sh')
    print("Moorse Encoded file: ", out,end="\n")
    f = open('C:\\Users\\anonymous-legion\\Documents\\Projects\\pyMalware\\Malware-Attack-Strategy.out','w')
    f.write(out)
    f.close()
    print(Utils().fromMoorseCode('C:\\Users\\anonymous-legion\\Documents\\Projects\\pyMalware\\Malware-Attack-Strategy.out'))
