from downloader import no_cost
import zipfile
import os

def make_imagepack(PackName="image",RespFile="resp.txt"):
    PackName = str(PackName)
    zip_file = PackName + '.zip'
    zip = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)
    filelist = no_cost(RespFlie=str(RespFile))
    for filename in filelist:
        zip.write(filename)
    print('packed done,prepare delete temp file')
    for filename in filelist:
        print("deleting file:%s" % filename)
        os.remove(filename)
        print("delete file:%s done"%filename)
    print("finished")
