import os.path

class SKRIPS_rc:

    def __init__(self, filename):

        self.filename = filename
        self.lineinfo = []
        self.data = []
        self.keys = []
        self.key_linenumbers = {}


    def read(self):

        with open(self.filename, "r") as f:

            i = 0
            for line in f:
                line_lstrip = line.strip()

                if len(line_lstrip) == 0:
                    self.lineinfo.append("comment")
                    self.data.append(line)
                    self.keys.append('')

                elif line_lstrip[0] == "#":

                    self.lineinfo.append("comment")
                    self.data.append(line)
                    self.keys.append('')

                else:
                    
                    if line_lstrip.find(":") == -1:
                        raise Exception("Syntax error: cannot find separator `:` in line %d" % (i+1, ))

                    key, data = line_lstrip.split(":")

                    key = key.strip()
                    data = data.strip()

                    self.lineinfo.append("data")
                    self.keys.append(key)
                    self.data.append(data)

                    self.key_linenumbers[key] = i

                i += 1

        return self
            
    def write(self, filename = "", overwrite = False):

        if filename == "":
            filename = self.filename

        if os.path.isfile(filename) and overwrite is False:
            raise Exception("Output file %s exists and `overwrite` is False. " % (filename,))

        with open(filename, "w") as f:

            for i, lineinfo in enumerate(self.lineinfo):
                
                if lineinfo == "comment":
                   
                    # The trailing newline should be already contained in the stored data 
                    f.write("%s" % (self.data[i],))

                elif lineinfo == "data":
                    
                    keystr = "%s:" % (self.keys[i],)
                    if len(keystr) < 16:
                        keystr = "%s%s" % (keystr, "".join([" " for _ in range(16 - len(keystr))]))

                    f.write("%s%s\n" % (keystr, self.data[i]))

                else:
                    raise Exception("Unknown lineinfo: `%s`" % (lineinfo,))
    
        return self

    def setValue(self, key, val):

        
        key_linenumber = self.key_linenumbers[key]
        self.data[key_linenumber] = val

        return self 
