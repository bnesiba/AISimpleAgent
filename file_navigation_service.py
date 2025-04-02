import json
import os
import uuid

class FileNavService:

    def __init__(self, projectPath):
        self.id = uuid.uuid4().hex
        self.startPath = projectPath
        self.dirStructureString = ""
        self.dirStructureSummary = ""
        self.fileSummaryDict: dict[str,str] = {}
        self.folderSummaryDict: dict[str,str] = {}
        self.projectSummary = ""


    def get_file_summaries(self, dirPath:str):
        keysToGet: list[str] = []
        fileSummaries: list[str] = []
        for summaryKey in self.fileSummaryDict.keys():
            if os.path.dirname(summaryKey).replace("\\", "/").rstrip("/") == dirPath.rstrip("/"):
                keysToGet.append(summaryKey)
        
        for key in keysToGet:
            fileSummaries.append(key + ": " +self.fileSummaryDict[key])
        
        return fileSummaries
    
    def get_folder_summaries(self, dirPath:str):
        keysToGet: list[str] = []
        folderSummaries: list[str] = []
        for summaryKey in self.folderSummaryDict.keys():
            if os.path.dirname(summaryKey).replace("\\", "/").rstrip("/") == dirPath.rstrip("/"):
                keysToGet.append(summaryKey)
        
        for key in keysToGet:
            folderSummaries.append(key + ": " +self.folderSummaryDict[key])
        
        return folderSummaries

    def get_top_5_folder_summaries(self):
        top5 = []
        keysList = sorted(self.folderSummaryDict)
        for i in range(5):
            if(i >= len(keysList)):
                break
            top5.append(keysList[i].replace("\\", "/") + ": " +self.folderSummaryDict[keysList[i]].replace("\\", "/"))
        return top5

    def load_summaries(self, id, projectPath, dirStructureString, dirStructureSummary, fileSummaryDict, folderSummaryDict, projectSummary):
        self.id = id
        self.startPath = projectPath
        self.dirStructureString = dirStructureString
        self.dirStructureSummary = dirStructureSummary
        self.fileSummaryDict = fileSummaryDict
        self.folderSummaryDict = folderSummaryDict
        self.projectSummary = projectSummary
    

    # @staticmethod
    # def load_data_from_file(file):
    #     with open(file, 'r') as f:
    #         id = f.readline().strip()
    #         startPath = f.readline().strip()
    #         dirStructureString = f.readline().strip()
    #         dirStructureSummary = f.readline().strip()
    #         fileSummaryDict = eval(f.readline().strip())
    #         folderSummaryDict = eval(f.readline().strip())
    #         fileNav = FileNavService(startPath)
    #         fileNav.load_summaries(id, startPath, dirStructureString, dirStructureSummary, fileSummaryDict, folderSummaryDict)
    #         return fileNav

    @staticmethod
    def IsIgnorablePath(string):
        if ".DS_Store" in string:
            return True
        if ".gitingore" in string:
            return True
        if ".git" in string:
            return True
        if ".vscode" in string:
            return True
        if ".idea" in string:
            return True
        if ".venv" in string:
            return True
        if "__pycache__" in string:
            return True
        if "node_modules" in string:
            return True
        if ".vs" in string:
            return True
        if "\\bin" in string:
            return True
        if "/bin" in string:
            return True
        if "\\obj" in string:
            return True
        if "/obj" in string:
            return True
        if ".editorconfig" in string:
            return True
        if ".eslintignore" in string:
            return True
        if "stylelintrc.json" in string:
            return True
        if ".yarnrc" in string:
            return True
        if ".prettierignore" in string:
            return True
        if ".prettierrc" in string:
            return True
        if ".nxignore" in string:
            return True
        if "yarn.lock" in string:
            return True
        if "package-lock.json" in string:
            return True
        if "package.json" in string:
            return True
        if "tsconfig.base.json" in string:
            return True
        if ".gz" in string:
            return True
        if "migrations.json" in string:
            return True
        if "all.css" in string:
            return True
        if "all.min.css" in string:
            return True
        if "duotone." in string:
            return True
        
        return False
    
    @staticmethod
    def IsReadableFileExtension(string):
        if ".cs" in string:
            return True
        if ".json" in string:
            return True
        if ".md" in string:
            return True
        if "js" in string:
            return True
        if ".py" in string:
            return True
        if ".html" in string:
            return True
        if ".css" in string:
            return True
        if ".scss" in string:
            return True
        if ".ts" in string:
            return True
        if ".txt" in string:
            return True
        if ".bat" in string:
            return True
        if ".sh" in string:
            return True
        if ".yaml" in string:
            return True
        if ".csproj" in string:
            return True
        if ".sln" in string:
            return True
        if ".xml" in string:
            return True
        if ".config" in string:
            return True
        
        return False