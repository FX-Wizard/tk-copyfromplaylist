import urllib
#from urllib.request import urlopen
import sys


def downloadFile(url, filePath):
    try:
        urllib.request.urlretrieve(url, filePath)
        """
        filePath = filePath.replace('\\', '/')
        request = urlopen(url)
        with open(filePath, 'wb') as output:
            output.write(request.read())
        """
    except :
        print('cannot download file {} URL: {}'.format(filePath, url))


if __name__ == '__main__':
    filePath = sys.argv[1]
    url = sys.argv[2]
    #print(filePath)
    #print(url)
    downloadFile(url, filePath)


