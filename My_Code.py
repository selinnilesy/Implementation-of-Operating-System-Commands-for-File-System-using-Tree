def check_commands(FS,C):
    wd=[FS[0]]
    path=[]
    a=wd[:]

    def datum(tree):
        return tree[0]
    def children(tree):
        return tree[2:]
    def isleaf(tree):
        return len(children(tree)) == 0

    def edit_wd(wd):
        edit="/".join(wd)
        if len(wd)>1:
            wd=edit[1:]
            return wd
        return edit
    def findpath(wd,FS):
        if len(wd)==1:
            if isleaf(FS):
                return "a"
            else:
                for x in children(FS):
                    if (x[1]=="D" or x[1]=="d") and cmd[1]==datum(x):
                        return "b"
                    else: continue
                else: return "a"
        else:
            for x in children(FS):
                l=children(FS)
                if datum(x)==wd[1] and (x[1]=="d" or x[1]=="D"):
                    i=l.index(x)
                    return findpath(wd[1:],FS[i+2])
                else: continue
            else: return "a"

    def findpath2(wd, FS):
                    if len(wd) == 1:
                        return "b"
                    else:
                        for x in children(FS):
                            if datum(x) == wd[1] and (x[1] == "d" or x[1] == "D"):
                                l = children(FS)
                                i = l.index(x)
                                return findpath2(wd[1:], FS[i + 2])
                            else: continue
                        else:
                                return "a"

    def dirchanger(p):
        path=[]
        path.append("/")
        if len(cmd[1])==1: return "root"
        else:
            for x in p:
                if x=="": continue
                if x == ".": continue
                if x=="..":
                    if len(path)==1: return "error"
                    else:
                        del path[-1]
                        continue
                else:
                    path.append(x)
                    continue
            return path
    def validpath(path,FS):
        if len(path)==1: return "valid"
        else:
            for x in children(FS):
                if datum(x)==path[1] and (x[1]=="d" or x[1]=="D"):
                    l = children(FS)
                    i=l.index(x)
                    return validpath(path[1:],FS[i+2])
                else: continue
            else: return "invalid"
    def relpath(p):
        a=wd[:]
        for x in p:
            if x=="": continue
            elif x == ".": continue
            elif x=="..":
                if len(a)==1:
                    return "error"
                else:
                    del a[-1]
                    continue
            else:
                a.append(x)
                t=validpath(a,FS)
                if t=="valid": continue
                else:
                    del a[-1]
                    return "error"
        return a

    def controlpath(a, FS):
        if len(a) == 1:
            return "yes"
        else:
            for x in children(FS):
                if datum(x) == a[1] and (x[1] == "d" or x[1] == "D"):
                    l = children(FS)
                    i = l.index(x)
                    return controlpath(a[1:], FS[i + 2])
                else:
                    continue
            return FS

    def relfile(p):
            a = wd[:]
            for x in p:
                if x == "" or x == ".":
                    continue
                elif x == "..":
                    if len(a) == 1:
                        return "error"
                    else:
                        del a[-1]
                        continue
                else:
                    a.append(x)
                    continue
            return a

    for x in C:

        if x.startswith("cd"):
            if " " in x:
                cmd=x.split(" ")
                if len(cmd)>2:
                    z=edit_wd(wd)
                    return "ERROR",x,z
                if "/" not in cmd[1]:
                    if cmd[1]==".":
                        continue
                    if cmd[1]=="..":
                        if len(wd)==1:
                            z=edit_wd(wd)
                            return "ERROR",x,z
                        else:
                            del wd[-1]
                            continue
                    else:
                        t=wd[:]
                        t.append(cmd[1])
                        r=findpath2(t,FS)
                        if r=="a":
                            z=edit_wd(wd)
                            return "ERROR",x,z
                        if r=="b":
                            wd.append(cmd[1])
                            continue
                else:
                     p=cmd[1].split("/")
                     if cmd[1].startswith("/"):
                         a=dirchanger(p)
                         if a=="error":
                             z=edit_wd(wd)
                             return "ERROR",x,z
                         elif a=="root":
                             wd=[FS[0]]
                             continue
                         else:
                             c = validpath(a, FS)
                             if c == "valid":
                                 wd = a
                                 continue
                             if c == "invalid":
                                 z = edit_wd(wd)
                                 return "ERROR", x, z
                     else:
                         g=relpath(p)
                         if g=="error":
                             z=edit_wd(wd)
                             return "ERROR",x,z
                         else:
                             wd=g
                             continue
            else:
                wd=[FS[0]]
                continue

        if x.startswith("mkdir"):
            def makenode(l,t=[]):
                if len(l) == 0:
                    return t
                if len(t) == 0:
                    t.append(l[0])
                    t.append("d")
                    return makenode(l[1:],t)
                if len(t) == 2:
                    t.append([l[0], "d"])
                    return makenode(l[1:],t)
                else:
                    t[-1].append([l[0], "d"])
                    return makenode(l[1:],t)

            def validpath2(path,FS):
                if len(path)==1:
                    return "error"
                else:
                    a=0
                    i=2
                    while i<len(FS):
                      if path[1]==datum(FS[i]):
                          if (FS[i][1]=="d" or FS[i][1]=="D"):
                            a+=1
                            return validpath2(path[1:],FS[i])
                      else:
                          i+=1
                    else:
                            l=path[(a+1):]
                            g=cleaner(l)
                            for x in children(FS):
                                if g[0]==datum(x) and (x[1]=="f" or x[1]=="F"):
                                    return "samefileexists"
                                else: continue
                            b=makenode(g)
                            FS.append(b)
                            return "success"
            def reldirwalker(wd,arg):
                a=wd[:]
                i=0
                while i<len(arg):
                    if arg[i]=="..":
                        if len(a)==1:
                            return "error"
                        else:
                            del a[-1]
                            i+=1
                    elif (arg[i]=="." or arg[i]=="") :
                        i+=1
                    else:
                        a.append(arg[i])
                        t=controlpath(a,FS)
                        if t=="yes": i+=1
                        else:
                            l=arg[i:]
                            g=cleaner(l)
                            for x in children(t):
                                if g[0]==datum(x) and (x[1]=="f" or x[1]=="F"):
                                    return "samefileexists"
                                else: continue
                            z=makenode(g)
                            t.append(z)
                            return "success"
                return "allexists"
            def cleaner(l):
                a=[]
                for x in l:
                    if x=="" or x=="." or x=="..":
                        continue
                    else: a.append(x)
                return a

            if " " not in x:
                z = edit_wd(wd)
                return "ERROR",x,z
            else:
             cmd=x.split(" ")
             if  "/" in cmd[1]:
               arg = cmd[1].split("/")
               if cmd[1].startswith("/"):
                 r=dirchanger(arg)
                 if r=="error":
                     z = edit_wd(wd)
                     return "ERROR", x, z
                 if r=="root":
                     z = edit_wd(wd)
                     return "ERROR", x, z
                 else:
                     if len(r)==1:
                         z = edit_wd(wd)
                         return "ERROR", x, z
                     else:
                         c=validpath2(r,FS)
                         if c=="success":
                             continue
                         else:
                             z = edit_wd(wd)
                             return "ERROR",x,z
               else:
                   j=reldirwalker(wd,arg)
                   if j!="success":
                       z = edit_wd(wd)
                       return "ERROR", x, z
                   else:
                       continue
             else:
                 a=wd[:]
                 a.append(cmd[1])
                 j=validpath2(a,FS)
                 if j!="success":
                     z = edit_wd(wd)
                     return "ERROR", x, z
                 else: continue

        if x.startswith("rmdir"):
            def leafdeleter(path,FS):
                if len(path)==1:

                        del FS
                        return "success"

                i=2
                while i < len(FS):
                        if path[1] == datum(FS[i]) and (FS[i][1] == "d" or FS[i][1] == "D"):
                              return leafdeleter(path[1:], FS[i])
                        else: i+=1
                else:
                    return "error"
            def rmdir(wd,FS):
                if len(wd)==1:
                    if isleaf(FS):
                        print 4
                        del FS
                        return "success"
                    else:
                        print 5
                        return "error"
                else:
                    for x in children(FS):
                        print 2
                        if datum(x)==wd[1] and (x[1]=="d" or x[1]=="D"):
                          l = children(FS)
                          i = l.index(x)
                          return rmdir(wd[1:], FS[i+2])
                        else: continue

                    else:
                        print 55
                        return "error"

            if " " not in x:
                z = edit_wd(wd)
                return "ERROR", x, z
            else:
              cmd=x.split(" ")
              if len(cmd)>2:
                  z = edit_wd(wd)
                  return "ERROR", x, z

              else:

                if "/" in cmd[1]:
                    p=cmd[1].split("/")
                    if cmd[1].startswith("/"):
                      print 2
                      t=dirchanger(p)
                      s = "/".join(wd)
                      y = "/".join(t)
                      if s.startswith(y):
                          z = edit_wd(wd)
                          print 11
                          return "ERROR", x, z
                      elif  wd==t :
                            z = edit_wd(wd)
                            return "ERROR", x, z

                      else:
                        if t=="root":
                            z = edit_wd(wd)
                            return "ERROR", x, z
                        elif t=="error":
                            print 77
                            z = edit_wd(wd)
                            return "ERROR", x, z
                        else:
                            print 7
                            z=controlpath(t,FS)
                            if type(z)==list:
                                print 5555
                                z = edit_wd(wd)
                                return "ERROR", x, z
                            else:
                                s=leafdeleter(t,FS)
                                print 44
                                if s=="success":
                                    print 3
                                    continue
                                else:
                                    print 5555555
                                    z = edit_wd(wd)
                                    return "ERROR", x, z
                    else:
                        z=relpath(p)
                        if z!="error":
                          s = "/".join(wd)
                          y = "/".join(z)
                          if wd == z:
                                a = edit_wd(wd)
                                return "ERROR", x, a

                          elif s.startswith(y):
                              g = edit_wd(wd)
                              return "ERROR", x, g
                          else:
                            t=leafdeleter(z,FS)
                            if t=="success":
                                continue
                            else:
                                y = edit_wd(wd)
                                return "ERROR", x, y
                        else:
                            m = edit_wd(wd)
                            return "ERROR", x, m
                else:
                 if cmd[1]==".." or cmd[1]=="." or cmd[1]=="/":
                        z = edit_wd(wd)
                        return "ERROR", x, z
                 else:
                    a=wd[:]
                    a.append(cmd[1])
                    r=rmdir(a,FS)
                    if r=="error":
                        z = edit_wd(wd)
                        return "ERROR", x, z

                    else: continue
        elif x.startswith("rm"):
            def controlfile(path,FS):
                if len(path)==1:
                    return "nofileprovided"
                i=2
                while i<len(FS):
                    if datum(FS[i])==path[1]:
                        if FS[i][1]=="d" or FS[i][1]=="D":
                            return controlfile(path[1:],FS[i])
                        else:
                            if len(path)>2:
                                return "invalidpath2"
                            else:
                                del FS[i]
                                return "removed"
                    else: i+=1

            if " " not in x:
                z = edit_wd(wd)
                return "ERROR", x, z
            else:
              cmd=x.split(" ")
              if len(cmd) > 2:
                    z = edit_wd(wd)
                    return "ERROR", x, z

              else:
                if "/" in cmd[1]:
                    p=cmd[1].split("/")
                    if cmd[1].startswith("/"):
                        t=dirchanger(p)
                        if t=="root":
                            z = edit_wd(wd)
                            return "ERROR", x, z
                        elif t=="error":
                            z = edit_wd(wd)
                            return "ERROR", x, z
                        else:
                            z=controlfile(t,FS)
                            if z!="removed":
                                z = edit_wd(wd)
                                return "ERROR", x, z
                            else: continue
                    else:
                        z=relfile(p)
                        if z!="error":
                            g=controlfile(z,FS)
                            if g!="removed":
                                z = edit_wd(wd)
                                return "ERROR", x, z
                            else: continue
                else:
                  if cmd[1] == ".." or cmd[1]=="." or cmd[1]=="/":
                        z = edit_wd(wd)
                        return "ERROR", x, z
                  else:
                    a=wd[:]
                    a.append(cmd[1])
                    t=controlfile(a,FS)
                    if t=="removed": continue
                    else:
                        z = edit_wd(wd)
                        return "ERROR", x, z

        elif x.startswith("exec"):
            def existsfile(path,FS):
                if len(path)==2:
                    if isleaf(FS): return "invalid"
                    else:
                        for x in children(FS):
                            if path[1]==datum(x) and (x[1]=="f" or x[1]=="F"):
                                return "valid"
                            else: continue
                for x in children(FS):
                    if datum(x)==path[1] and (x[1]=="d" or x[1]=="D"):
                        l = children(FS)
                        i = l.index(x)
                        return existsfile(path[1:],FS[i+2])
                    else: continue

            if " " not in x:
                z = edit_wd(wd)
                return "ERROR", x, z
            else:
             cmd = x.split(" ")
             if len(cmd) > 2:
                  z = edit_wd(wd)
                  return "ERROR", x, z

             else:
              if "/" in cmd[1]:
                 p = cmd[1].split("/")
                 if cmd[1].startswith("/"):
                     t = dirchanger(p)
                     if t == "root":
                        z = edit_wd(wd)
                        return "ERROR", x, z
                     elif t == "error":
                        z = edit_wd(wd)
                        return "ERROR", x, z
                     else:
                         a=existsfile(t,FS)
                         if a=="valid": continue
                         else:
                             z = edit_wd(wd)
                             return "ERROR", x, z
                 else:
                       c=relfile(p)
                       if c!="error":
                            h=existsfile(c,FS)
                            if h=="valid": continue
                            else:
                               z = edit_wd(wd)
                               return "ERROR", x, z
                       z = edit_wd(wd)
                       return "ERROR", x, z
              a=wd[:]
              a.append(cmd[1])
              s=existsfile(a,FS)
              if s=="valid": continue
              else:
                  z = edit_wd(wd)
                  return "ERROR", x, z

        elif x.startswith("cp"):
            def pathtoabs(path):
                if "/" in path:
                    p=path.split("/")
                    if path.startswith("/"):
                        a=["/"]
                        for x in p:
                            if x=="" or x==".": continue
                            elif x=="..":
                                if len(a)!=1:
                                    del a[-1]
                                    continue
                                else: return "invalid"
                            else:
                                a.append(x)
                                continue
                        return a
                    else:
                        a=wd[:]
                        for x in p:
                            if x=="" or x==".": continue
                            elif x=="..":
                                if len(a)!=1:
                                    del a[-1]
                                    continue
                                else: return "invalid"
                            else:
                                a.append(x)
                                continue
                        return a

                else:
                     if path!="." and path!=".." and path!="/":
                        a=wd[:]
                        a.append(path)
                        return a
                     else: return "invalid"
            def targetsearcher(path,FS):
                if len(path)==2:
                    for x in children(FS):
                        if path[1]==datum(x):
                            if x[1]=="d" or x[1]=="D": return "yes"
                            else: return "error"
                        else: continue
                    return "no"
                i = 2
                while i < len(FS):
                    if datum(FS[i]) == path[1] and (FS[i][1]=="d" or FS[i][1]=="D"):
                        return targetsearcher(path[1:],FS[i])
                    else: i+=1
                else: return "error"

            def targetfetcher(path,FS):
                if len(path)==2:
                    for x in children(FS):
                        if path[1]==datum(x) and (x[1]=="d" or x[1]=="D"):
                            l=children(FS)
                            i=l.index(x)
                            return FS[i+2]
                        else: continue
                    else: return FS
                i = 2
                while i < len(FS):
                    if datum(FS[i]) == path[1] and (FS[i][1] == "d" or FS[i][1] == "D"):
                        return targetfetcher(path[1:], FS[i])
                    else: i += 1

            def sourcefetcher(path,FS):
                if len(path)==2:
                    i = 2
                    while i < len(FS):
                        if datum(FS[i]) == path[1]:
                            if FS[i][1]=="d" or FS[i][1]=="D": return FS[i]
                            else: return path[1]
                        else: i+=1
                    else: return False
                i = 2
                while i < len(FS):
                    if datum(FS[i]) == path[1] and (FS[i][1] == "d" or FS[i][1] == "D"):
                        return sourcefetcher(path[1:], FS[i])
                    else: i += 1
                else: return False

            if " " not in x:
                z = edit_wd(wd)
                return "ERROR", x, z
            else:
                cmd=x.split(" ")
                if len(cmd)!=3:
                    z = edit_wd(wd)
                    return "ERROR", x, z
                else:
                    a=pathtoabs(cmd[1])
                    if a!="invalid":
                        sourcepath=a
                    else:
                        z = edit_wd(wd)
                        return "ERROR", x, z
                    b=pathtoabs(cmd[2])
                    if b!="invalid":
                        targetpath=b
                    else:
                        z = edit_wd(wd)
                        return "ERROR", x, z
                    c=targetsearcher(targetpath,FS)
                    if c=="error":
                        z = edit_wd(wd)
                        return "ERROR", x, z
                    elif c=="yes":
                        target=targetfetcher(targetpath,FS)
                        k=sourcefetcher(sourcepath,FS)

                        if type(k)==list:
                            i=2
                            while i<len(target):
                                if datum(target[i])==datum(k):
                                    z = edit_wd(wd)
                                    return "ERROR", x, z
                                else: i+=1
                            target.append(k)
                        elif type(k)==str:
                            i = 2
                            while i < len(target):
                                if datum(target[i]) == k:
                                    z = edit_wd(wd)
                                    return "ERROR", x, z
                                else:
                                    i += 1
                            target.append([k,"f"])
                        else:
                            z = edit_wd(wd)
                            return "ERROR", x, z
                    elif c=="no":
                        target=targetfetcher(targetpath,FS)
                        k=sourcefetcher(sourcepath,FS)
                        if type(k)==str:
                            target.append([targetpath[-1],"f"])
                        elif type(k)==list:
                            l=[targetpath[-1],"d"]+target[2:]
                            target.append(l)
                        else:
                            z = edit_wd(wd)
                            return "ERROR", x, z
        else:
            z = edit_wd(wd)
            return "ERROR", x, z
    z=edit_wd(wd)
    return "SUCCESS",FS,z


print check_commands(['/', 'd', ['home', 'd', ['Desktop', 'D', ['the2', 'd', ['the2.pdf', 'f'], ['the2.py', 'F']], ['the3', 'D', ['the3.pdf', 'F'], ['the3.py', 'f']]], ['Documents', 'd', ['form.doc', 'f']]], ['etc', 'D']], ['cd /home/Desktop/the2', 'rmdir /etc'])
