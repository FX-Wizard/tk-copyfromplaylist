import imp
import os
import time
import shutil
import ssl
from urllib.request import urlopen
import platform

import sgtk

# standard toolkit logger
logger = sgtk.platform.get_logger(__name__)

class PlaylistPacker():
    '''
    Parameters:
    shotgun : shotgun api instance
    projectName (str): name of project
    '''
    def __init__(self, shotgun, projectName, localStorage, msgCallback=None):
        
        self.sg = shotgun
        self.projectName = projectName
        self.localStorage = localStorage
        self.msgCallback = msgCallback

    def getProjectPath(self):
        tankName = self.sg.find_one('Project', [['name', 'is', self.projectName]], ['tank_name'])['tank_name']
        projectPath = os.path.join(self.localStorage, tankName)
        self.log('PROJECT PATH: {}'.format(projectPath))
        return projectPath


    def osName(self):
        # Returns name of OS
        if sgtk.util.is_windows():
            return 'windows'
        elif sgtk.util.is_macos():
            return 'mac'
        else:
            return 'linux'


    def copyVersionsFromPlaylist(self, playlistName):
        self.log('### Copying from playlist: %s' % playlistName)
        # Get playlist
        try:
            playlistId = self.sg.find_one('Playlist', [['code', 'is', playlistName]], ['id'])['id']
        except:
            self.log('CAN NOT FIND PLAYLIST', error=1)

        if not playlistId:
            raise Exception('Playlist not found')

        filters = [['playlist', 'is', {'type':'Playlist', 'id':playlistId}]]
        fields = ['version.Version.published_files', 'version.Version.sg_uploaded_movie']
        result = self.sg.find('PlaylistVersionConnection', filters, fields)

        fileList = []
        urlList = []

        for item in result:
            try:
                itemId = item['version.Version.published_files'][-1]['id']
                search = self.sg.find_one('PublishedFile', [['id', 'is', itemId]], ['path'])
                filePath = search['path']['local_path_%s' % self.osName()]
                fileList.append(filePath)
                self.log('Found: %s' % filePath)
            except:
                versionName = item['version.Version.sg_uploaded_movie']['name']
                self.log('Cannot get file: %s... trying URL' % versionName)

                image = item['version.Version.sg_uploaded_movie']
                urlList.append(image)
        
        today = time.strftime('%Y%m%d')
        projectDir = os.path.join(self.getProjectPath(), 'IO', 'Out')
        
        outDir = os.path.join(projectDir, today)
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        
        outDir = os.path.join(outDir, playlistName)
        if not os.path.exists(outDir):
            os.makedirs(outDir)

        success = True
        
        for path in fileList:
            fileName = os.path.basename(path)
            self.log('Copying: {}'.format(path))
            try:
                outPath = os.path.join(outDir, fileName)
                shutil.copyfile(path, outPath)
            except:
                self.log('cannot copy file {}'.format(fileName), error=1)
                success = False

        ssl._create_default_https_context = ssl._create_unverified_context # monkey patch to fix SSL errors
        for item in urlList:
            filePath = os.path.join(outDir, item['name'])
            self.log('Downloading: {}'.format(item['name']))
            try:
                # urllib.request.urlretrieve(item['url'], filePath) # python 3 way
                request = urlopen(item['url'])
                with open(filePath, 'wb') as output:
                    output.write(request.read())
            except Exception as error:
                success = False
                self.log('cannot download file {} URL: {}'.format(item['name'], item['url']), error=1)
                self.log('ERROR: {}'.format(error), error=1)
                
        return {'outputPath': outDir, 'success': success}


    def log(self, msg, error=0):
        if logger:
            if error:
                logger.warn(msg)
            else:
                logger.info(msg)
        if self.msgCallback:
            self.msgCallback({msg: msg, error: error})
        print(msg)


    def packagePlaylists(self, listOfPlaylists, compress):
        '''
        Parameters:
        listOfPlaylists (list): list of shotgun playlists
        compress (bool): compress in zip file
        '''
        for playlist in listOfPlaylists:
            run = self.copyVersionsFromPlaylist(playlist)

            if run['success']:
                if compress:
                    try:
                        shutil.make_archive(run['outputPath'], 'zip', run['outputPath'])
                    except:
                        self.log('FAILED TO CREATE ZIP FILE: %s' % run['outputPath'], error=1)
            else:
                self.log('FAILED TO GET ALL VERSIONS FOR PLAYLIST: %s' % playlist, error=1)