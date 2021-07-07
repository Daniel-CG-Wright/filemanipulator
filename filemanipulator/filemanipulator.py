#Programmed in Python 3.9.1
#Possible next additions - reading file tools, a file browser GUI, a file transfer feature
#Maybe search by contents of a file for (finddirfiles) also.
#Add chunking tools to limit memory usage, in case files are huge and could cause memory errors

from io import UnsupportedOperation
import os #Some of these may be superfluous but they were imported
#at the time of creation and I am unwilling to change them
from os import listdir
from os.path import isfile, join, isdir, splitext #File manipulation tools
import random
from random import randint
from time import sleep
from sys import getsizeof
from re import DOTALL, IGNORECASE, findall
from collections import deque

bannedfilecharacters = ["/", "\\", "<", ">", "\"", "?", "*", ":", "|"] #These cannot be used in file names.

def FileChunking(line, chunksize, casesensitive=True):
    """
    Internal function used in chunking lines to save memory usage.

    Generator function; it yields the chunk data per chunk in rapid succession,
    therefore it should be used as a generator, rather than attempting to store
    the data in a variable, which would result in only the data of the last chunk
    being stored.

    Args:
        line (obj): The current line/file being read.
        chunksize (str): The chunk size in bytes.
        casesensitive (bool): If False, converts the data to lowercase.
    
    Yields:
        str: The chunk of each line to be used for processing, as though it were a separate line.
        Repeated until the entire line is read.
    """
    #Repeats for each chunk of the line until all chunks have been read.
    #Splits the line into chunks


    
    while True:

        
        
        data = line.read(chunksize)
        if not data: break


        if casesensitive == False: data = data.lower()
        yield data
        
def FileNameSanitise(filename, bannedcharacters = bannedfilecharacters):

    """Sanitises a name from either a premade list of banned characters (the characters not allowed for Windows 10 file names) or a custom inputted one.
    
    Sanitises a string (typically a file name) from banned characters,
    specified in a parsed list.

    Args:
        filename (str): The name to sanitise.
        bannedcharacters (list): The characters to sanitise - each entry counts as a 'character', 
        and therefore will only be sanitised if the name contains the whole entry, 
        therefore characters should be entered individually as their own elements.
    
    Returns:
        str: The sanitised filename
    """
     #Needed as strings are immutable
    #Throwaway lambda used to circumvent the scoping of the while loop.

    while any(char in filename for char in bannedcharacters): filename = filename.replace((char for char in bannedcharacters if char in filename), "") #Replaces the banned characters with blanks

    return filename


    
def CreateFile(filename, filetype = ".txt", 
information = "", overwrite = True, 
overwriteappend = "", wraplength = -1, 
directory = os.getcwd(), encoding = "utf-8", 
returns = True, bannedcharacters=bannedfilecharacters): #Writes a file, deciding whether or not to overwrite current information etc

    
#Documentation
    """ 
    Creates a file in a specified directory (defaults to the current directory).

    Creates a file in a specified directory, specified with the directory argument.
    Files can also be written with information, which can be managed by parsing textwrapping
    arguments.

    Args:
        filename (str): The name of the file. Sanitised for banned characters
                            in the bannedcharacters argument, and must be ASCII.
        filetype (str): The file extension (default .txt)
        information (str): The information to write to the file on creation. 
                            Can be a list of strings, or a standalone string. (default \"\")
        overwrite (bool): Whether other files with the same name should be
                            overwritten, or the new file have a character appended
                            to its name to make it unique (see overwriteappend) (default False)
        overwriteappend (str): The character to append to make the file unique.
                                If not specified, a random ASCII charactetr is generated.
                                Appends repeatedly until the file is unique.
                                Example: if the filename was foo.txt, and this file already
                                existed in the directory, and overwrite was False, and
                                the overwriteappend was set to "bar", the file would be saved
                                as foobar.txt. If foobar.txt also existed already, the file would
                                be saved as foobarbar.txt.
        wraplength (int): The number of characters each line of information should be, before\na line break is inserted.\n
                            Default is infinite, and should be left blank if custom line breaks are used.
        directory (str): The directory that the file should be created in. (default current directory).
        encoding (str): The type of encoding the file should be created with.
                        (default "utf-8")
        returns (bool): Whether 'True' should be returned if the file saved successfully.
                        (default True)
        bannedcharacters (list): A list of all the banned characters from file names that will
                                be sanitised. Each entry counts as a character and must be entirely
                                within the file name to be sanitised. Case sensitive.
                                Example: bannedcharacters = ["foo", "bar"]. "foo" will be removed from
                                foofile.txt, but not foba.txt or Foo.txt. "bar" will not be removed from
                                b_a_r.txt.
                                Defaults to the list of characters banned from Windows 10
                                file names.

        
    Returns:
        bool:  True if the file was created successfully and 'returns' was True.

    Raises:
        FileNotFoundError: If the directory was not found or the file could not save.
    """

    global bannedfilecharacters
    replaced = True
    totalfilename = filename + filetype
    totalfilename = FileNameSanitise(totalfilename)
    if totalfilename.isascii() == False: raise ValueError("Filenames must be ASCII!")

    completefilename = os.path.join(directory, totalfilename) #Incorporates the directory
    
    if isinstance(information, list) == False: 
        informationlist = [information] 
        
    else: informationlist = information #Sets a list for a writelines function to write information to the file

    if wraplength > 0 and isinstance(information, list) == False: 

        informationlist = [""] #Controls wrapping

        for index, element in enumerate(list(information)):
            
            informationlist[index] = "" 

            for x in range(wraplength):

                informationlist[index] += element #Adds a character from the information string to the correct index in the list until the wrapping limit is reached for that index

    overwritespec = False if overwriteappend == "" else True #Tracks whether to keep the user-specified overwriteappend or generate a random one


    if overwrite == False: 
        while True:
            if overwritespec == False:
                overwriteappend = overwriteappend.join(chr(randint(97, 122)))   

            try:
                with open(completefilename, mode = "r") as test: #Tries to open any files with the same name as the current, in the current directory, to see if they exist
                    pass

                filename += overwriteappend #Appends the overwrite appendage to the file name to save it as a new file. Repeated until there are no files with the same name
                totalfilename = filename + filetype #Ensures only the file name is changed, not the file type
                completefilename = os.path.join(directory, totalfilename)
                continue

            except FileNotFoundError:
                break #A unique file name has been found


        completefilename = os.path.join(directory, totalfilename) #Incorporates the directory again, in case changes were made to the first file name

    try:
        with open(completefilename, mode = "w+", encoding = encoding) as f:
            
            
            if information != "": f.writelines(informationlist)  #Writes information, if information for the file was inserted

            if returns: return True

    except FileNotFoundError:

        raise FileNotFoundError("The file could not save. Possible causes: Lacking permissions, no storage space, or other")

def FindDirFiles(directory = os.getcwd(), types = [], searchchars = [], totalmatch = False, allscentriespresent = False, casesensitive = True):

    """
    Find files within a specific directory, with different possible search criteria
    
    Args:

        directory (str): The directory to search in. Defaults to the current directory.

        types (list): The possible types of files to include, in strings within the list 
        (\"file\"/\"directory\" ONLY, NOT extensions!).
        A blank list will also return all items in the directory chosen
        
        searchchars (list): Only returns files with the characters in one or more entries 
        in their name.
        
        totalmatch (bool): Only returns files that have names completely matching one or more entries in searchchars.
        e.g. if the searchchars input is ["file.txt"], and this is true, only a file with the name "file.txt" will be returned.
        Otherwise, a file just including this string, such as "notafile.txt" would also be returned.
        
        allscentriespresent (bool): Only returns files that have all the strings entered into the searchchars list in their name.
        Effectively changes the above parameter functions from 'or' to 'and'. Takes precedence over totalmatch; as both cannot be True at once.
        
        casesensitive (bool): Whether or not file names must have characters of the same type AND case
            as specified in the searchchars list. Defaults to True
    
    Returns:
        list: Returns an unsorted list containing the names of all the matching files, or a blank list if no files were present.
    
    Raises: 
        FileNotFoundError: if the chosen directory could not be found.

    ValueError
        If a type(s) of file other than 'directory' or 'file' is specified.
    """

    dirfiles = [] #List of files in the directory matching the criteria - will be returned as a list later
    checkfiles = [] #List of files to check through

    if casesensitive == False: searchchars = [x.lower() for x in searchchars] #Used for case sensitivity overcoming

    if len(types) > 0: #If types were specified
        
        typefilters = []

        for x in types: 
            if x != "file" and x != "directory": raise ValueError("A file type other than \"file\" or \" directory\" was provided!") 
            
            elif x == "file" and "file" not in typefilters: typefilters.append(x)
            
            elif x == "directory" and "directory" not in typefilters: typefilters.append(x)
            
            else: break
            
            
            #Raises a value error if a value in 'types' is not 'file' or 'directory'.
            #Otherwise, if the value was 'file' and this has not been added to the filters, it is added - and the same for 'directory'

             #Leaves the loop once the maximum number of type filters has been reached, as there are only two possibilities - optimises code if longer lists are presented.
            
    
    

    
        

        if "file" in typefilters: checkfiles.append([file for file in listdir(directory) if isfile(os.path.join(directory, file))]) #Adds all files of type 'file' to the dirfiles list

        if "directory" in typefilters: checkfiles.append([file for file in listdir(directory) if isdir(os.path.join(directory, file))]) #Adds all directories to the dirfiles list

        

    else: checkfiles = listdir(directory) #Adds all things to dirfiles if no type was selected for filtering
    
    
    if len(searchchars) > 0: #Avoids unnecessary checking of non-existent criteria (slow)
        for file in checkfiles: #Removes files from dirfiles that do not match the 'searchchars' search criteria

           
            if casesensitive == True:
                #If any character to be searched for is in the file
                if totalmatch == False and allscentriespresent == False and any(string in file for string in searchchars): dirfiles.append(file)

                #Checks how many of the search criteria strings are in the file name, if all must be present. Only appends the file to the dirfiles to be returned if all characters are present
                elif allscentriespresent == True and len([string for string in searchchars if string in file]) == len(searchchars): dirfiles.append(file)

                #Checks if the entirety of at least 1 entire string in the searchchars string is in the file name
                elif totalmatch == True and allscentriespresent == False: 
                    for char in searchchars:
                        if char == file:
                            dirfiles.append(file)
                            break
                        else:
                            pass

                    

            elif casesensitive == False: #Re-does the above code, but with filecheck used instead, a case-lowered version of the file name. Ensures the original file name is kept (in terms of case), but with proper sorting

                filecheck = file.lower()

                #If any character to be searched for is in the file
                if totalmatch == False and allscentriespresent == False and any(string in filecheck for string in searchchars): dirfiles.append(file)

                #Checks how many of the search criteria strings are in the file name, if all must be present. Only appends the file to the dirfiles to be returned if all characters are present
                elif allscentriespresent == True and len([string for string in searchchars if string in filecheck]) == len(searchchars): dirfiles.append(file)

                #Checks if the entirety of at least 1 entire string in the searchchars string is in the file name
                elif totalmatch == True and allscentriespresent == False and any(string == filecheck for string in searchchars): dirfiles.append(file)

           

    else: dirfiles = checkfiles
    return dirfiles #Returns the list of suitable file names.



def ReadFile(filename, directory = os.getcwd(), actiontriggers = [], actions = [], casesensitivetriggers = True, totalmatch = "none", bannedcharacters = bannedfilecharacters, encoding = "utf-8", skipempties=True):
    """
    Reads a chosen file in a directory using readlines

    Reads a chosen file in a directory using readlines,
    and returns a list containing each line. Can execute 
    procedures stored in 'actions', when the correlating
    index actiontrigger is read. To have several procedures
    trigger in succession per action trigger, a nested list
    should be used (see below). Newlines are removed.
    Args:
        filename (str): The name of the file to be read. Sanitised automatically for banned characters. Must include the extension.
        directory (str): The directory to access.
                    (default current directory)

        actiontriggers (list): The strings that will cause the procedure in the
            correlating index for the 'actions' list to be called. Must be an exact match,
            although case sensitivity is controlled by the casesensitivetriggers arg.
            If 'totalmatch' is "word", the action trigger will only work if a word is only
            comprised of the action trigger. If 'totalmatch' is "line", the action trigger
            will only work if the entire line is composed of the action trigger.
            REPEAT HANDLING: If triggers are repeated, only the first instance of the
            trigger (and its actions) will be used, and further instances are ignored.

        actions (list): The procedures that should be called when action triggers
            are read. Example: actiontriggers = ["foo"], and actions = [myFunc1], where
            myFunc1 does: print("foobar"). Whenever "foo" is read in the file, "foobar"
            will print, as myFunc1 is called. Partials should be used to parse procedures
            requiring arguments - the functions are treated in the same way as tKinter button commands.
            If "stop" or "s" is inserted as a function at any point, the reading will stop and the
            current read information will be returned as is. Alternatively, the current data
            can be yielded as part of an iterator using "yield" or "y". These are the only string-based
            command available (for the time being).
        totalmatch (bool): Controls whether an action trigger only triggers its action(s) when an entire word is comprised of one of the action triggers ("word"), or an entire line ("line"). Defaults to "none", where any character sequence match
            will trigger an action. Example: "foo" in "foobar" will trigger for "none", 
            "foo" in "foo in a sentence." will trigger for "word", and "foo" will trigger for
            a "foo" on its own line (disregarding line breaks)
        bannedcharacters (list): The characters sanitised against in the file name
        encoding (str): The encoding to read the file with (default "utf-8")
        skipempties (bool): Whether empty lines should be returned
    Returns:
        list: A list containing a string per element for each line
    
    Raises:
        FileNotFoundError: If the file or directory was not found.
    
    """
    #Combines the filename (sanitised) and the directory          
    totalfilename = os.path.join(directory, FileNameSanitise(filename, bannedcharacters))
    
    if casesensitivetriggers == False:
        actiontriggers = [x.lower() for x in actiontriggers]

    #Trying to open the total file name, to handle a potential file not found error
    try:
        with open(totalfilename, "r", encoding=encoding) as file:
            
            #A list in which the file contents are stored, one element for each line
            
            returnedcontents = []
            #Examining each line at a time. Readlines is avoided, as this will
            #not allow functions to be executed as soon as their triggers are read
            for line in file:
                
                

                #Replaces new line characters to avoid character corruption when checking
                line = line.replace("\n", "")
                
                if skipempties == True:
                    while True:
                        try: returnedcontents.remove("")
                        except ValueError: break
                
                linecontents = ""
                

                if casesensitivetriggers == False:
                    line = line.lower()
                #Only executes the checks if they have been specified, to optimise
                if len(actiontriggers) > 0:
                    #Executes the right action for the trigger if the total match is "line"
                    if totalmatch == "line":
                        if line in actiontriggers:
                            if isinstance(actions[actiontriggers.index(line)], list):
                                for x in actions[actiontriggers.index(line)]:
                                    if callable(x): x()
                                    elif x == "s" or x == "stop": return line
                                    elif x == "y" or x == "yield": yield line
                            else:
                                x = actions[actiontriggers.index(line)]
                                if callable(x): x()
                                elif x == "s" or x == "stop": return returnedcontents
                                elif x == "y" or x == "yield": yield returnedcontents
                            #Compatibility with nested lists for multiple function support

                        else: returnedcontents.append(line)

                    #For word-based matching
                    elif totalmatch == "word":
                        for word in line.split():
                            if word in actiontriggers:
                                if isinstance(actions[actiontriggers.index(word)], list): 
                                    for x in actions[actiontriggers.index(word)]:
                                        if callable(x): x()
                                        elif x == "s" or x == "stop": returnedcontents.append(linecontents); return returnedcontents
                                        elif x == "y" or x == "yield": returnedcontents.append(linecontents); yield returnedcontents
                                else:
                                    x = actions[actiontriggers.index(word)]
                                    if callable(x): x()
                                    elif x == "s" or x == "stop": returnedcontents.append(linecontents); return returnedcontents
                                    elif x == "y" or x == "yield": returnedcontents.append(linecontents); yield returnedcontents
                            else: linecontents = linecontents+" "+word+" "

                    #For other matching (character based default)
                    else:
                        for index, element in enumerate(actiontriggers):
                             for word in line.split():
                                 
                                 if element in word:
                                     
                                     if isinstance(actions[index],list):
                                        for x in actions[index]:
                                            
                                            if callable(x): x()
                                            elif x == "s" or x == "stop": returnedcontents.append(linecontents); return returnedcontents
                                            elif x == "y" or x == "yield": returnedcontents.append(linecontents); yield returnedcontents
                                     else:
                                         x = actions[index]
                                         if callable(x): x()
                                         elif x == "s" or x == "stop": returnedcontents.append(linecontents); return returnedcontents
                                         elif x == "y" or x == "yield": returnedcontents.append(linecontents); yield returnedcontents
                                 else: linecontents = linecontents+" "+word+" "
                    returnedcontents.append(linecontents)
                else: returnedcontents.append(line)
        
        if skipempties == True:
            while True:
                try: returnedcontents.remove("")
                except ValueError: break
                
        return returnedcontents
        
    except FileNotFoundError:
        raise FileNotFoundError("The file or directory was not found!")

def FindInFile(term, inputstring, instances=0, iterations=1):
    """Finds the index of a term in a string; for internal use.
    
    Args:
        term (str): The term being searched for.
        inputstring (str): The string to search in.
        instances (int): The number of instances of the term before the first is given.
        iterations(int): The number of results that should be searched for.
    Returns:
        list: The index of the term in a list, or [-1] if it was not found.
            A list is returned as there was once a functionality to return multiple
            points, but this has been revoked unless used directly with 'iterations'

    """

    index = 0
    indices = []

    if not isinstance(term, str) or term == "":
        raise ValueError("Null string provided!")

    if len(term) > len(inputstring):
        raise ValueError("The chunk size is smaller than the size of the search term ({0})".format(term))
        """char = term[0]
        for index, character in enumerate(inputstring):

            if character == char:
                
                    
                if inputstring[index:] in term:
                    
                    if instances <= 0:
                        selection.append(inputstring[index:])
                        return selection #For chunking ONLY
                    
                    elif instances > 0:
                        instances -= 1
                        continue

                
                else: continue
                """
    #If the character is actually in the input string to begin with; saves time
    if term in inputstring:
        #For finding the first character of the string.
        char = term[0]
        

        for index, character in enumerate(inputstring):

            if character == char:
                
                    
                if inputstring[index:index+len(term)] == term:

                    if instances <= 0:
                        
                        indices.append(index)
                        if len(indices) == iterations:
                            return indices
                        else: continue
                    
                    elif instances > 0:
                        instances -= 1
                        continue

                
                else: continue

    else: return [-1]

def FileTransfer(sourcefile, targetfile, 
                startpoint=-1, endpoint=-1, 
                startchar="", endchar="", 
                numberofchars=-1,
                charinstance1=0, charinstance2 = 0,
                casesensitive=True,
                chunking=False, chunksize=1000000,
                encoding="utf-8", createsecondfile=True,
                overwrite=True, overwritechars = "", readbinary = False,
                writebinary = False):
    """
    Transcribes text from one file to another.

    Transcribes text from one file to another, with specified start and
    end points, either numerical (number of characters), or from a given
    instance of a specific character/word/line. Out of startpoint, endpoint
    and numberofchars, if they are used, only 2 must be supplied, and the third
    can be automatically calculated. If the startchar naturally exceeds the endchar
    due to instance variables being set, they will automatically be swapped.
    
    Args:
        sourcefile (str): The file (including directory) from which data is transcribed.
        targetfile (str): The file (including directory) to which data is transcribed.
        startpoint (int): The start point of transcription, as the number of characters
                    from the file start point. If this is supplied, only one of endpoint or
                    numberofchars must be supplied for the transcription to work (if an end
                    point is desired)
        endpoint (int): The end point - number of characters from the file start point.
        startchar (str): The string to start reading from (inclusive)
        endchar (str): The string to stop reading from (inclusive)
        numberofchars (int): The number of chars that should be read from the start point.
        charinstance1 (int): The instance of a startchar that should be obeyed first - defuaults to the first
                        instance. Zero-indexed. For example, if charinstance1 = 3, the reading will only start
                        from the 4th instance of the startchar (the 4th "foo" if startchar = "foo")
        charinstance2 (int): The instance of an endchar that should be obeyed first - defuaults to the first
                        instance. Zero-indexed. For example, if charinstance2 = 3, the reading will only start
                        from the 4th instance of the endchar (the 4th "foo" if endchar = "foo")
        casesensitive (bool): Whether the matches to start/end chars and the file contents must be case sensitive (default True)
        chunking (bool): Whether file lines should be chunked to avoid memory errors on large files with long lines.
                    Takes more time but reduces memory usage. Cannot be used with charinstances, and takes priority over them.
        chunksize (int): The number of bytes each line chunk should be, if chunking is used. Defaults to 1000000 (1 MB)
        encoding (str): The file encoding to use. (default utf-8)
        createsecondfile (bool): Whether the second, target file should be created (even if it exists already - see overwrite args).
        overwrite (bool): Whether currently existing files akin in name to the target file being created should be overwritten.
        overwritechars (str): The string to append to the name of the new file if it cannot overwrite other files, so that it has a unique name.
        readbinary (bool): Whether the information read should be binary.
        writebinary (bool): Whether the information written should be binary.

    Returns:
        bool: True if the writing was successful.
    
    Raises:
        ValueError: If the endpoint is greater than the start point, or the number of chars is less than 1.
    """
    pointflag = False
    pointflagstart = False
    pointflagend = False
    contentsbuffer = []
    charcountread = None


    if endpoint > 0 and startpoint > 0:
        charcountread = endpoint - startpoint
        if charcountread <= 0:
            raise ValueError("The endpoint must be greater than the startpoint!")
    
    elif numberofchars > 0:
        charcountread = numberofchars
        print(charcountread)
        if endpoint < 1 and startpoint > -1:
            endpoint = startpoint + numberofchars
        
        elif startpoint < 0 and endpoint > 0:
            startpoint = endpoint - numberofchars

    elif endpoint > 0 and startpoint < 0:
        pointflagend = True
        pointflag = True
    
    elif startpoint >= 0 and endpoint < 1:
        pointflagstart = True
        pointflag = True

    if charcountread and startchar == "" and endchar == "":
        if charcountread <= 0:
            raise ValueError("The endpoint must be greater than the startpoint!")
        
        elif startpoint < 0 or endpoint < 1:
            raise ValueError("The startpoint or endpoint is invalid (startpoint < 0 | endpoint < 1)")


    if createsecondfile == True: mode = "w"
    else: mode = "a"
    readmode = "r"
    writemode = mode
    if readbinary: readmode = readmode + "b"
    if writebinary: writemode = writemode + "b"

    if createsecondfile == True: writemode = writemode + "+"
    #For the filter we will be using to get the string between the start and end chars, 
    #we use contentstuff = findall(startchar + '(.+)', string, DOTALL). We then go;
    #findall('(.+)' + endchar, contentstuff, DOTALL). This only works for the first and
    #last instances of the start and end chars respectively, but it is the most efficent
    #way when charinstances is 0. Otherwise, we use typical loop/gen stuff.
    #Update: This was scrapped as it was about the same efficiency as the below code,
    #but much harder to maintain and debug.

    #If startchar and numberofchars are provided.
    

    #If endchar and numberofchars are provided
    

    #Charcountread will count down the number of characters from the start character, until it reaches 0.
    #This can then be iterated as many times as 'iterations' is provided.

    #Opens the source file as f1, and the target file as f2

    overwritespec = False if overwritechars == "" else True #Tracks whether to keep the user-specified overwriteappend or generate a random one

    
    if overwrite == False and createsecondfile == True: 
        while True:
            if overwritespec == False:
                overwriteappend = "".join(chr(randint(97, 122)))   

            try:
                with open(targetfile, mode = "r") as test: #Tries to open any files with the same name as the current, in the current directory, to see if they exist
                    pass

                targetfile = splitext(os.path.basename(targetfile))[0] + overwriteappend #Appends the overwrite appendage to the file name to save it as a new file. Repeated until there are no files with the same name
                 #Ensures only the file name is changed, not the file type
                
                continue

            except FileNotFoundError:
                break #A unique file name has been found
    
    trailing = False
    with open(sourcefile, mode=readmode, encoding=encoding) as f1, open(targetfile, mode=writemode, encoding=encoding) as f2:

        if casesensitive == False: startchar = startchar.lower(); endchar = endchar.lower()
        
        if startchar != "" or endchar != "" or numberofchars > 0 or charcountread or pointflag:
        #For management when chunking is not necessary
            if chunking == False: 
                f1contents = f1.read()
                #Turning everything lowercase if casesensitivity is disabled to get everything to match casewise, although the contents
                #are still kept in their proper case.
                
                f1contents2 = f1contents
                if casesensitive == False: f1contents2 = f1contents.lower()

                if pointflag:
                    if pointflagend:
                        f2.write(f1contents[:endpoint])
                    elif pointflagstart:
                        f2.write(f1contents[startpoint:])

                if charcountread and endchar == "" and startchar == "":
                    f2.write(f1contents[startpoint:endpoint])
                
                if startchar != "" and endchar == "" and numberofchars < 1: f2.write(f1contents2[(x for x in FindInFile(startchar, f1contents, charinstance1)):])
                elif startchar == "" and endchar != "" and numberofchars < 1: f2.write(f1contents2[:(x for x in FindInFile(endchar, f1contents, charinstance2))])
                elif startchar != "" and endchar != "" and FindInFile(startchar, f1contents2, charinstance1) != -1 and FindInFile(endchar, f1contents2, charinstance2) != -1:
                    
                    #Adds the sections, splitting between every point where startchar and endchar is found, as long as they are satisfying provided instance and iterations criteria

                    

                    print(str(len(FindInFile(endchar, f1contents2, charinstance2))))
                    for x in range(len(FindInFile(endchar, f1contents2, charinstance2))):
                        swapped = False
                        startchar = startchar
                        endchar = endchar
                        
                        if FindInFile(endchar, f1contents2, charinstance2)[x] < FindInFile(startchar, f1contents2, charinstance1)[x]:
                            startchar2 = startchar
                            startchar = endchar
                            endchar = startchar2
                            swapped = True
                            print("swap")
                            
                        print(endchar)
                        print(startchar)
                        if swapped == True: contentsbuffer.append(f1contents[FindInFile(startchar, f1contents2, charinstance2)[x]:FindInFile(endchar, f1contents2, charinstance1)[x]])
                        else: contentsbuffer.append(f1contents[FindInFile(startchar, f1contents2, charinstance1)[x]:FindInFile(endchar, f1contents2, charinstance2)[x]])
                            

                            
                elif startchar != "" and numberofchars > 0 and FindInFile(startchar, f1contents2, charinstance1) != -1:

                    for x in FindInFile(startchar, f1contents2, charinstance1):
                        
                        contentsbuffer.append(f1contents[x:(x + numberofchars)])

                elif endchar != "" and numberofchars > 0 and FindInFile(endchar, f1contents2, charinstance2) != -1:
                    for x in FindInFile(endchar, f1contents2, charinstance2):

                        contentsbuffer.append(f1contents[(x-numberofchars)+1:x+1])
                
                else: pass

                #Transcribes the info to the destination file.
                
                f2.write("".join(str(x) for x in contentsbuffer))

            
            elif chunking == True:

                #Will be used for storing data from the start to the end points if it lies across several chunks. Uses First
                #in First out principle to ensure data remains in the correct order.
                selection = deque()
                selection2 = deque()
                #Repeating the code to check each chunk in sequence
                charcountinfile = 0
                
                if pointflag:
                    for chunk in FileChunking(f1, chunksize):
                        charcountinfile += len(chunk)



                trailing = False
                starttrailing = False
                writerest = False 
                
                
                charcountread2 = charcountread
                
                numberofchars2 = numberofchars
                for chunk in FileChunking(f1, chunksize):

                    chunk2 = chunk
                    if casesensitive == False: chunk2 = chunk.lower()

                    if endchar != "" and startchar == "" and numberofchars < 1:
                        if endchar in chunk2:
                            f2.write(chunk[FindInFile(endchar,chunk)])
                            writerest = False
                            return
                        else: f2.write(chunk); writerest = True

                    if starttrailing == True:
                        f2.write(chunk)

                    if trailing == True:
                        

                        if len(chunk) < charcountread2:
                            charcountread2 -= len(chunk)
                            selection.append(chunk)
                            print("appension")
                            continue
                        else:
                            print("no")
                            selection.append(chunk[:charcountread2])
                            charcountread2 -= len(chunk[:charcountread2])
                            print(charcountread2)
                            trailing = False
                            
                            print(len("".join(x for x in selection)))
                            print(numberofchars)
                                
                            f2.write("".join(x for x in selection))
                            return True
                            
                            

                    
                    
                    if startchar != "" and endchar == "" and numberofchars < 1 and startchar in chunk2:
                        f2.write(chunk[FindInFile(startchar, chunk, charinstance1):])
                        print("hnn")
                        writerest = True
                    
                    print(chunk)

                    if pointflag:

                        if pointflagend:
                            if endpoint > charcountread:
                                raise ValueError("The provided endpoint is outside the file size!")


                            else: break
                        
                        elif pointflagstart:
                            
                            if startpoint > charcountinfile: raise ValueError("The provided startpoint is outside the file size!")

                    if startpoint > 0 and numberofchars > 0:
                        if startpoint - len(chunk) == 0:
                            startpoint = 0
                            continue
                        
                        for x in range(len(chunk)):
                            if startpoint != 0:
                                startpoint -= 1

                            else: chunk = chunk[x:]; break
                        
                    if startpoint == 0 and numberofchars > 0:
                        
                        for x in range(len(chunk)):
                            if numberofchars > 0: f2.write(chunk[x]); numberofchars -= 1; print(chunk[x])
                            else: return True

                        continue




                            

                    """if endchar != "" and numberofchars > 0 and startchar == "":
                        if FindInFile(endchar, chunk2, charinstance2)[0] != -1 and FindInFile(endchar, chunk2, charinstance2)[0] - numberofchars2 >= 0:
                            f2.write(chunk[FindInFile(endchar, chunk2, charinstance2)[0] - numberofchars2:FindInFile(endchar, chunk2, charinstance2)[0]])
                        elif FindInFile(endchar, chunk2, charinstance2)[0] != -1 and FindInFile(endchar, chunk2, charinstance2)[0] - numberofchars2 < 0:
                            f2.write(chunk[:FindInFile(endchar, chunk2, charinstance2)[0]])
                            numberofchars2 -= len(chunk[:FindInFile(endchar, chunk2, charinstance2)[0]])
                            continue
                        elif FindInFile(endchar, chunk2, charinstance2)[0] == -1:
                            if len(chunk) <= numberofchars2:
                                f2.write(chunk)
                                numberofchars2 -= len(chunk)
                            else:
                                f2.write(chunk[len(chunk) - numberofchars2:])"""

                    

                    """ if charcountread and startpoint != -1 and endpoint != -1:
                        
                        if len(chunk[startpoint:]) <= charcountread2:
                            f2.write(chunk[startpoint:endpoint])
                        else:
                            f2.write(chunk[startpoint:])
                            charcountread2 -= len(chunk[startpoint:])
                            trailing = True
                            continue """
                    
                    

                    if startchar != "" and charcountread2 > 0 and endchar == "" and not trailing:
                        if FindInFile(startchar, chunk2)[0] != -1:
                            if FindInFile(startchar, chunk2)[0] + charcountread2 <= len(chunk):
                                print("gog")
                                f2.write(chunk[FindInFile(startchar, chunk2)[0]:FindInFile(startchar, chunk2)[0] + numberofchars])
                                return True
                            elif FindInFile(startchar, chunk2)[0] + charcountread2 > len(chunk):
                                selection.append((chunk[FindInFile(startchar, chunk2)[0]:]))
                                charcountread2 -= len(chunk[FindInFile(startchar, chunk2)[0]:])
                                trailing = True
                                print("trailing")
                                continue
                        else: continue
                    
                    if startchar != "" and FindInFile(startchar, chunk2) != -1 and charcountread2 < 1:

                        if endchar != "":
                            if FindInFile(endchar, chunk2, charinstance2) != -1:
                                #For matching if the endchar is in the chunk
                                f2.write(chunk[(x for x in FindInFile(startchar, chunk)):(y for y in FindInFile(endchar, chunk))])


                            else: selection.append(chunk[(FindInFile(startchar, chunk))])

                        elif numberofchars2 > 0:

                            for index in FindInFile(startchar, chunk2, charinstance1):
                                
                                if numberofchars2 > len(chunk[index:]):

                                    numberofchars2 -= len(chunk[index:])

                                    selection.append(chunk[index:])

                                else:

                                    f2.write(chunk[index:index + numberofchars2])
                                
                    elif endchar != "" and numberofchars2 > 0 and startchar == "":
                        raise UnsupportedOperation("The parameters given failed to operate (cannot supply an endchar and numberofchars2 alone whilst chunking!)")


                        """ print("ue9f")
                        if FindInFile(endchar, chunk2)[0] == -1:
                            selection.append(chunk)
                            selection2.append(chunk2)
                            print("fef")
                        elif FindInFile(endchar, chunk2)[0] != -1:
                            # if FindInFile(endchar, chunk2)[0] == 0 and chunksize > 1:
                            #     selection.append(chunk[0])
                            # else: 
                            print("f")
                            selection.append(chunk[:FindInFile(endchar, chunk2)[0] + 1])
                            charcountread2 += chunksize - 1
                            writelist = []
                            print(selection)
                            for x in range(len(selection)):
                                
                                for y in range(len(selection[-(x+1)])):
                                    
                                    
                                    if charcountread2 >= len(selection[-(x+1)][-y]):
                                        writelist.append(selection[-(x+1)][-y])
                                        charcountread2 -= len(selection[-(x+1)][-y])
                                        print(charcountread2)

                                    else:
                                        print(writelist)
                                        if chunksize > 1:
                                            writelist = writelist[:1-chunksize]
                                        lastset = False
                                        for x in writelist:
                                            for y in range(chunksize):
                                                f2.write(x)
                                            try:
                                                for chunk in FileChunking(f2, chunksize): #This is supposed to be f2
                                                    charcountinfile += len(chunk)
                                            except UnsupportedOperation:
                                                pass

                                            if charcountinfile < chunksize:
                                                f2.seek(0)
                                            
                                            else: f2.seek(charcountinfile-chunksize) """
                                            
                                            
                    
                        
                                       
                                        
                                        
                                        
                                        


                

                    elif startchar != "" and endchar != "" and FindInFile(endchar, chunk2) != -1 and FindInFile(startchar, chunk2) == -1:

                        for x in selection:

                            if startchar in x:

                                f2.write(x[(FindInFile(startchar, x)):] + chunk[:FindInFile(endchar, chunk)])
        

        elif chunking == False: f2.write(f1.read()) #If no search parameters have been specified

        elif chunking == True: f2.write("".join(str(x) for x in FileChunking(f1, chunksize)))
        
        
    return True

""" from functools import partial

def printhello():
    print("Hello World")

def Params(param):
    print(str(param))

paramchoice = partial(Params, "blubblubquail")
files = ReadFile("blub.txt", directory="C:/Users/Daniel/Documents/Python_projects", actiontriggers=["the"], actions=[printhello])
print(files) """



#Information in case a user tries to execute this file directly.
if __name__ == "__main__": print("This script is designed as a module to be integrated within\na primary, host module, not as a script on its own. It therefore has no functions standalone.\nThe program will shut down in 5 seconds."); print("To update the program or gain information on it, please see the README.txt file in the package directory."); sleep(5); exit()



""" from functools import partial

def printhello():
    print("Hello World")

def Params(param):
    print(str(param))

paramchoice = partial(Params, "blubblubquail")
files = ReadFile("blub.txt", directory="C:/Users/Daniel/Documents/Python_projects", actiontriggers=["the"], actions=[printhello])
print(files) """



#Information in case a user tries to execute this file directly.
if __name__ == "__main__": print("This script is designed as a module to be integrated within\na primary, host module, not as a script on its own. It therefore has no functions standalone.\nThe program will shut down in 5 seconds."); print("To update the program or gain information on it, please see the README.txt file in the package directory."); sleep(5); exit()









