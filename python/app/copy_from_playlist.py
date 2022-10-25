import os
import time
import shutil
import ssl
import webbrowser
import subprocess
#from urllib.request import urlopen
import urllib
import platform

import sgtk

from .ui.dialog import Ui_Dialog
from tank.platform.qt import QtCore, QtGui
from tank.platform.qt5 import QtWidgets

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
        self.app = QtWidgets.QApplication.instance()
        self.app.processEvents()

        self.ui = Ui_Dialog()



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

    def copyVersionsFromPlaylist(self, playlistName, outputDir, openFolder):

        self.setVericalScroll()
        # Get playlist
        try:
            playlistId = self.sg.find_one('Playlist', [['code', 'is', playlistName]], ['id'])['id']
        except:
            self.log_status('CAN NOT FIND PLAYLIST', error=1)

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
                if os.path.exists(filePath):
                    fileList.append(filePath)
                    self.log_status('Found: %s' % filePath)
            except:
                #versionName = item['version.Version.sg_uploaded_movie']['name']
                #self.log_status('Cannot get file: %s... trying URL' % versionName)

                image = item['version.Version.sg_uploaded_movie']
                urlList.append(image)
        
        now = time.strftime('%Y%m%d-%H%M')
        #projectDir = os.path.join(self.getProjectPath(), 'IO', 'Out') if outputDir == "" else outputDir
        projectDir = os.path.join(self.getProjectPath(), 'MyPlaylists') if outputDir == "" else outputDir
        
        outDir = os.path.join(projectDir, now)
        if not os.path.exists(outDir):
            os.makedirs(outDir)

        folderName = playlistName.replace("/", "_")
        #folderName = folderName.replace(" ", "_")
        outDir = os.path.join(outDir, folderName)
        if not os.path.exists(outDir):
            os.makedirs(outDir)

        success = True
        folderName = outDir.replace("/", "\\")
        msg = f"\n\nCopying files from playlist: \"{playlistName}\" to folder: \n{folderName}"
        self.log_status(msg)

        if openFolder:
            webbrowser.open("{}".format(outDir))

        count = len(fileList)
        if count > 0:
            msg = f"\n\n Trying to copy {count} files...\n"
            self.log_status(msg)
        for i, path in enumerate(fileList):
            fileName = os.path.basename(path)
            self.log_status('({}/{})  Copying: {}'.format(i+1, count, path))
            try:
                outPath = os.path.join(outDir, fileName)
                shutil.copyfile(path, outPath)
            except:
                self.log_status('cannot copy file {}'.format(fileName), error=1)
                success = False

        ssl._create_default_https_context = ssl._create_unverified_context # monkey patch to fix SSL errors
        count = len(urlList)
        if count > 0:
            msg = f"\n\n Downloading {count} files...\n"
            self.log_status(msg)
        for i, item in enumerate(urlList):
            try:
                filePath = os.path.join(outDir, item['name'])
                success = True

                self.log_status('({}/{})  Downloading: {}'.format(i + 1, count, item['name']))
                urllib.request.urlretrieve(item['url'], filePath) # python 3 way

            except Exception as error:
                # success = False
                # self.log_status('cannot download file {} URL: {}'.format(item['name'], item['url']), error=0)
                # self.log_status('ERROR: {}'.format(error), error=0)
                self.log_status('({}/{})  Unable to download file'.format(i + 1, count))
            if success:
                if count > 0:
                    val = ((i +1)/ count) * 100
                self.updateFileProgress(val)
                
        return {'outputPath': outDir, 'success': success}


    def packagePlaylists(self, listOfPlaylists, openFolder, compress, outputDir):
        '''
        Parameters:
        listOfPlaylists (list): list of shotgun playlists
        compress (bool): compress in zip file
        '''
        self.setVericalScroll()
        msg = f"\nCopying playlists to destination folder {outputDir} ..."

        self.log_status(msg)
        for playlist in listOfPlaylists:

            run = self.copyVersionsFromPlaylist(playlist, outputDir, openFolder)

            if run['success']:
                self.log_status('\n\nFile downloading is complete')
                if compress:
                    try:
                        self.log_status('\n\nZipping files ...')
                        shutil.make_archive(run['outputPath'], 'zip', run['outputPath'])
                        folderName = run['outputPath'].replace("/", "\\")
                        self.log_status('\nZipping destination folder is complete at: \n%s\n\n' % folderName)
                    except:
                        self.log_status('\n\nFAILED TO CREATE ZIP FILE: %s' % run['outputPath'], error=1)
            else:
                self.log_status('\n\nFAILED TO GET ALL VERSIONS FOR PLAYLIST: %s' % playlist, error=1)

    def log(self, msg, error=0):
        if logger:
            if error:
                logger.warn(msg)
            else:
                logger.info(msg)
        if self.msgCallback:
            self.msgCallback({msg: msg, error: error})
        print(msg)

    def add_status(self, status):
        self.ui.status_dialog.append(status)
        self.app.processEvents()
        # self.ui.status_dialog.reload()

        #item = QtGui.QStandardItem(status)
        #self.ui.status_model.appendRow(item)


    def log_status(self, msg, error=0):
        if logger:
            if error:
                logger.warn(msg)
                txt = "Warning: " + msg
                self.add_status(txt)
            else:
                logger.info(msg)
                txt = msg
        if self.msgCallback:
            self.msgCallback({msg: msg, error: error})
        self.add_status(txt)
        print(msg)

    def updateFileProgress(self, val):
            self.ui.FilesProgressBar.setValue(val)
            self.app.processEvents()

    def setVericalScroll(self):
        self.ui.status_dialog.verticalScrollBar().setValue(self.ui.status_dialog.verticalScrollBar().maximum())


