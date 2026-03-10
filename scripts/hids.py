#!/usr/bin/python3

import json
import argparse
import enum
import os
import stat
import hashlib


# database dictionary structure:
# {
#    "/path/to/file/file1.txt" :
#    {
#        "type": "f",
#        "uid": 1234,
#        "gid": 1234,
#        "mode": "0o644",
#        "size": 1440000,
#        "hash": "0123456789ABCDEF"
#    },
#    "/path/to/dir1" :
#    {
#        "type": "d",
#        "uid": 1234,
#        "gid": 1234,
#        "mode": "0o755"
#    },
#    ...
# }


Actions = ['count', 'add', 'hash', 'check', 'verify', 'update']


# --- Action 1: count ---

# print the number of files and directories in the specified path and/or database
def count(data, files, directories):
    # count files in database, skip if no database given
    if data != None:
        f=0
        d=0
        for entry in data:
            if data[entry]['type'] == 'f':
                f+=1
            elif data[entry]['type'] == 'd':
                d+=1
        print(f'database contains {f} files and {d} directories')
    # count files and dirs, skip if no files and no directories given (empty list = boolean False)
    if files or directories:
        # get the number of items in the list of files
        f=len(files)
        d=len(directories)
        print(f'path contains {f} files and {d} directories')
    # success
    return True


# --- Action 2: add ---

# add files and directories that are not in the database yet to the database
def add(data, files, directories):
    # handle list of files
    for fpath in files:
        # check whether file is already in the database
        if not fpath in data:
            # add the properties of the file to the database
            data[fpath] = filedata(fpath)
        # if a file path is already in the database, you should use check or update
        else:
            print(f'file already in database: {fpath}')
            print('use check or update action')
            return False
    # handle list of directories
    for dpath in directories:
        # check whether directory is already in the database
        if not dpath in data:
            # add the properties of the directory to the database
            data[dpath] = dirdata(dpath)
        # if a directory path is already in the database, you should use check or update
        else:
            print(f'directory already in database: {dpath}')
            print('use check or update action')
            return False
    print('add: success')
    # output file count in database
    count(data, None, None)
    return True

# return a dictionary with information about a directory
def dirdata(dpath):
    assert os.path.isdir(dpath)

    # initialize new empty dictionary for the directory's properties.
    dir_properties = {}

    # type for directory is 'd'
    dir_properties['type'] = 'd'

    # get file system statistics
    st = os.stat(dpath)

    # owner user id
    dir_properties['uid'] = st.st_uid

    # owner group id
    dir_properties['gid'] = st.st_gid

    # permission bits only (e.g. 0o755)
    dir_properties['mode'] = oct(stat.S_IMODE(st.st_mode))

    # finally, return the dictionary
    return dir_properties

# return a dictionary with information about a file
def filedata(fpath):
    assert os.path.isfile(fpath)

    # initialize new empty dictionary for the file's properties.
    file_properties = {}

    # type for file is 'f'
    file_properties['type'] = 'f'

    # get file system statistics
    st = os.stat(fpath)

    # owner user id
    file_properties['uid'] = st.st_uid

    # owner group id
    file_properties['gid'] = st.st_gid

    # permission bits only (e.g. 0o644)
    file_properties['mode'] = oct(stat.S_IMODE(st.st_mode))

    # file size
    file_properties['size'] = st.st_size

    # finally, return the dictionary
    return file_properties


# --- Action 3: hash ---

# add checksum for files (not directories) to database entries
# this function is not called "hash" because python has a built-in function with that name
def cksum(data, files, directories):
    # go through all files found in the path
    for fpath in files:

        # check if file exists in database
        if fpath not in data:
            print(f'file not in database: {fpath}')
            return False

        # skip if entry is not a file
        if data[fpath]['type'] != 'f':
            continue

        # check if hash already exists
        if 'hash' in data[fpath]:
            print(f'hash already exists for file: {fpath}')
            return False

        # calculate sha256 hash
        h = sha256file(fpath)

        # store hash in database
        data[fpath]['hash'] = h

        print(f'hash added for {fpath}')

    print('hash: success')
    return True


# --- Action 4: update ---

# update database entries that have changed
def update(data, files, directories):

    # collect current paths from filesystem
    current_paths = set(files + directories)

    # remove entries that no longer exist
    for path in list(data.keys()):
        if path not in current_paths:
            print(f'removed: {path}')
            del data[path]

    # update or add current entries
    for fpath in files:
        data[fpath] = filedata(fpath)

    for dpath in directories:
        data[dpath] = dirdata(dpath)

    print('update: success')
    count(data, None, None)

    return True


# --- Action 5: verify ---

# check files in path against database entries
# check correct hash for files that have a hash in the database
def verify(data, files, directories):

    # collect current paths from filesystem
    current_paths = set(files + directories)

    # collect paths stored in database
    db_paths = set(data.keys())

    # check for missing files/directories
    for path in db_paths:
        if path not in current_paths:
            print(f'missing: {path}')

    # check for new files/directories
    for path in current_paths:
        if path not in db_paths:
            print(f'new: {path}')

    # check existing entries
    for path in current_paths.intersection(db_paths):

        # get current properties
        if os.path.isfile(path):
            current = filedata(path)
        elif os.path.isdir(path):
            current = dirdata(path)
        else:
            continue

        stored = data[path]

        # check type change
        if current['type'] != stored['type']:
            print(f'type changed: {path}')
            continue

        # check uid
        if current['uid'] != stored['uid']:
            print(f'uid changed: {path}')

        # check gid
        if current['gid'] != stored['gid']:
            print(f'gid changed: {path}')

        # check mode
        if current['mode'] != stored['mode']:
            print(f'mode changed: {path}')

        # check size for files
        if current['type'] == 'f' and 'size' in stored:
            if current['size'] != stored['size']:
                print(f'size changed: {path}')

        # check hash if it exists
        if current['type'] == 'f' and 'hash' in stored:
            new_hash = sha256file(path)
            if new_hash != stored['hash']:
                print(f'hash changed: {path}')

    print('verify: done')
    return True

# --- helper functions ---

# return the SHA256 hash of a file
def sha256file(fpath):
    # only works with files, not directories
    assert os.path.isfile(fpath)
    # read file in 16k blocks
    BUFSIZE = 16384
    # initialize sha256 hash object
    s256 = hashlib.sha256()
    # open file for reading and read first block
    f = open(fpath, 'rb')
    buffer = f.read(BUFSIZE)
    # read block and update hash
    while len(buffer) > 0:
        s256.update(buffer)
        buffer = f.read(BUFSIZE)
    f.close()
    # return string containing hexdigit representation of hash
    return s256.hexdigest()


# --- database functions ---

# save database from dictionary to file
def save_db(dbfile, dict):
    jsondata = json.dumps(dict, indent=4)
    f = open(dbfile,"w")
    f.write(jsondata)
    f.close()

# read database from file into dictionary
def read_db(dbfile):
    f = open(dbfile,"r")
    dict = json.loads(f.read())
    f.close()
    return dict


# --- main function ---

def main():
    # parse commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database')
    parser.add_argument('-p', '--path')
    parser.add_argument('action', choices=Actions)
    args = parser.parse_args()

    # --- database directory setup ---

    # database is needed for add,hash,check/verify,update
    if args.action in ['add','hash','check','verify','update'] and args.database == None:
        print(f'action {args.action} needs database argument')
        return 1

    # load existing contents from database file
    data = None
    # if database is given but not a file, it's created later when writing back
    if args.database != None and os.path.isfile(args.database):
        data = read_db(args.database)

    # initialize empty dictionary if database is given
    if data == None and args.database != None:
        data = {}


    # --- file and directories list setup ---

    path = None
    file_list = []
    directory_list = []

    if args.path == None:
        # path is needed for add,hash,check/verify,update
        if args.action in ['add','hash','check','verify','update']:
            print(f'action {args.action} needs path argument')
            return 1
    else:
        # verify path is a file or directory
        if not os.path.isdir(args.path) and not os.path.isfile(args.path):
            raise argparse.ArgumentTypeError(f'{args.path} is not a valid file or directory')
        # normalize path
        path = os.path.abspath(args.path)

        # single file => add to file list
        if os.path.isfile(path):
            file_list.append(path)
        else:
            # add root directory
            directory_list.append(path)
            # get list of subdirectories and files
            for root,dirs,files in os.walk(path):
                for item in dirs:
                    # get full path
                    dpath = os.path.join(root,item)
                    directory_list.append(dpath)
                for item in files:
                    # get full path
                    fpath = os.path.join(root,item)
                    # could be link or special device instead of file, we ignore those
                    if os.path.isfile(fpath):
                        file_list.append(fpath)

    # --- run desired action ---

    r = False
    if args.action == 'count':
        r = count(data, file_list, directory_list)
    elif args.action == 'add':
        r = add(data, file_list, directory_list)
    elif args.action == 'hash':
        r = cksum(data, file_list, directory_list)
    elif args.action == 'verify' or args.action == 'check':
        r = verify(data, file_list, directory_list)
    elif args.action == 'update':
        r = update(data, file_list, directory_list)

    if not r:
        print(f'there was a problem running action {args.action}')
        return 1

    # save (possibly changed) database again
    if data != None and args.database != None:
        save_db(args.database, data)
    
    return 0

if __name__ == "__main__":
    main()
