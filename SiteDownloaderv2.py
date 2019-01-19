from tkinter import *
import os
import io
import urllib.request
from html.parser import HTMLParser


class MyGui():
    
    def __init__(self,Root):
        print('Gui Imported...')
        Root.withdraw()
    
        self.Root = Root
    
    def MainForm(self):
        print('Gui Created...')
        guiMainWindow = Toplevel(self.Root)
        guiMainWindow.withdraw() 
        guiMainWindow.resizable(width=FALSE, height=FALSE)
        guiMainWindow.geometry("+500+250")
        guiMainWindow.title('EUU Site Downloader')
        guiMainWindow.wm_iconbitmap("hourglass")
        guiMainWindow.deiconify()
        
        Label(guiMainWindow, text="Download Folder Name : ").grid(row=0)
        Label(guiMainWindow, text="Site Url ( http://) ").grid(row=1)
        
        CopyFolderName = Entry(guiMainWindow)
        CopyFolderName.grid(row=0,column=1)
    
        SiteUrl = Entry(guiMainWindow)
        SiteUrl.grid(row=1,column=1)

        Button(guiMainWindow,text='Download Site',command=self.DownloadSite).grid(row=2,column=0,columnspan=2,sticky="ew")

        self.CopyFolderName = CopyFolderName
        self.SiteUrl = SiteUrl
        self.guiMainWindow = guiMainWindow
        
    def DownloadSite(self):
        Folder = self.CopyFolderName.get()
        Url = self.SiteUrl.get()
        print('Site Download Started!  :')
        print('Site Download Folder :',Folder)
        print('Site Download Url :',Url)
        print('Download WebSite --> command sent Waiting...\n')
        
        DownloadWeb(Folder,Url)
    

class DownloadWeb():
    def __init__(self,CopyFolder,Url):
        self.CopyFolder = CopyFolder
        self.SiteUrl = Url

        self.FolderControl(CopyFolder)
        IndexPageContent = self.SavePageFile('index.html')
        self.HtmlParse(IndexPageContent)

        while(True):
            FirstFileCount = self.GetFilesCount()
            for root, dirs, files in os.walk(CopyFolder):
                for file in files:
                    if file.endswith(".html") and file != 'index.html':
                        FilePath = os.path.join(root, file)
                        print('Page Work Started ----> ' + file)
                        PageContent = self.GetPageContent(FilePath)
                        self.HtmlParse(PageContent)
                        
            LastFileCount = self.GetFilesCount()
            
            if(FirstFileCount == LastFileCount):
                break
            else:
                LastFileCount = FirstFileCount
                continue
            

        print('Site Download Completed --- by emreuyguc')

    def GetFilesCount(self):
        return(len([name for name in os.listdir(self.CopyFolder) if os.path.isfile(os.path.join(self.CopyFolder, name))]))
    
    def FolderControl(self,FolderName):
        try:
            if not os.path.exists(FolderName):
                os.makedirs(FolderName)
                print('Folder Created: ',FolderName)
            else:
                print('Folder Have Already!. Not created: ',FolderName)
        except:
            print('! Error : class DownloadWeb --> Function FolderControl')


    def GetPageContent(self,FilePath):
        Page = open(FilePath,"r")
        PageContent = Page.read()
        Page.close()
        return(PageContent)
        
    def CheckFile(self,FilePath):
        if os.path.isfile(self.CopyFolder + "/" + FilePath):
            return(1)
        else:
            return(0)

    def SaveAssetFile(self,AssetUrl):
        try:
            print(self.SiteUrl + "/" + AssetUrl)
            Req = urllib.request.Request(self.SiteUrl + "/" + AssetUrl)
            Asset = urllib.request.urlopen(Req)
            print('Connect Succesful : ',AssetUrl)
            AssetContent = Asset.read()
            print('Resource Received: ',AssetUrl)
            Asset.close()
            print('Connection Closed: ',AssetUrl,'\n')
            
            UrlFolderPath = AssetUrl.split('/')
            if len(UrlFolderPath)>1:
                AssetFolder = '/'.join(UrlFolderPath[:-1])
                if not os.path.exists(self.CopyFolder + "/" + AssetFolder):
                    os.makedirs(self.CopyFolder + "/" + AssetFolder)
                
            AssetFile = open(self.CopyFolder + "/" + AssetUrl,"wb")
            AssetFile.write(AssetContent)
            print('Asset File Saved: ',AssetUrl,'\n')
            AssetFile.close()
            
        except urllib.error.HTTPError as e:
            print('! Error : class DownloadWeb --> Function SaveAssetFile')


    def SavePageFile(self,PageUrl):
        try:
            print(self.SiteUrl + "/" + PageUrl)
            Req = urllib.request.Request(self.SiteUrl + "/" +PageUrl)
            Page = urllib.request.urlopen(Req)
            print('Connect Succesful : ',PageUrl)
            PageContent = Page.read()
            print('Resource Received: ',PageUrl)
            PageContent = PageContent.decode('utf8')
            Page.close()
            print('Connection Closed: ',PageUrl,'\n')
            
            UrlFolderPath = PageUrl.split('/')
            if len(UrlFolderPath)>1:
                PageFolder = '/'.join(UrlFolderPath[:-1])
                if not os.path.exists(self.CopyFolder + "/" + PageFolder):
                    os.makedirs(self.CopyFolder + "/" + PageFolder)
                
            PageFile = open(self.CopyFolder + "/" + PageUrl,"w")
            PageFile.write(PageContent)
            PageFile.close()
            print('Page Saved: ',PageUrl,'\n')
            return(PageContent)
        except urllib.error.HTTPError as e:
            print('! Error : class DownloadWeb --> Function SavePageFile')
      
    def HtmlParse(self,Data):
        HtmlParser = MyHtmlParser()
        HtmlParser.feed(Data)
        self.Tags = HtmlParser.Tags
        self.Attrs = HtmlParser.Attrs
        self.HtmlData = HtmlParser.HtmlData
        for i in range(0,len(self.Tags)):
            for r in self.Attrs[i]:
                if len(r)>0:
                    if r[0] == 'src':
                        FileCheck = self.CheckFile(r[1])
                        if FileCheck == 0:
                            if(r[1][0] != '#' and r[1][:4] != 'http'):
                                try:
                                    self.SaveAssetFile(r[1])
                                except:
                                    print('Error Link :',r[1])
                        else:
                            print('File Already Exists',r[1])
                    elif r[0] == 'href':
                        FileCheck = self.CheckFile(r[1])
                        if FileCheck == 0:
                            try:
                                if(r[1][0] != '#' and r[1][:4] != 'http'):
                                    if(r[1][-4:] == 'html'):
                                        try:
                                            self.SavePageFile(r[1])
                                        except:
                                            print('Error Link :',r[1])
                                    else:
                                        try:
                                            self.SaveAssetFile(r[1])
                                        except:
                                            print('Error Link :',r[1])
                                else:
                                    print('File Already Exists: ',r[1])
                            except:
                                print('HATAAAA ->>',r)
                                
                            
        HtmlParser.Clean()
        print('Html Data Parsed Succesfull. \n')
        
class MyHtmlParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.reset()
        
        self.Tags = []
        self.Attrs = []
        self.HtmlData = []
        
    def handle_starttag(self, tag, attrs):
        self.Tags.append(tag)
        self.Attrs.append(attrs)
        
    def handle_data(self, data):
        self.HtmlData.append(data)
        
    def Clean(self):
        self.Tags = []
        self.Attrs = []
        self.HtmlData = []
        
if(__name__ == '__main__'):
    Root = Tk()
    
    gui = MyGui(Root)
    gui.MainForm()
    
    Root.mainloop()
