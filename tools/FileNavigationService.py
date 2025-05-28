import os

class FileNavService:

    def __init__(self, projectPath):
        self.startPath = projectPath

    def __init__(self):
        self.startPath = "C:/Users/brandon.nesiba/source/repos/AIStreamingAgent/"


    def generate_dir_structure(self):
        print("getting directory structure...")
        dirListString = ''

        for root, dirs, files, in os.walk(self.startPath):

            if FileNavService.IsIgnorablePath(root):
                    continue
            level = root.replace(self.startPath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            dirListString = dirListString + '\n{}{}/'.format(indent, os.path.basename(root))
            for file in files:
                dirListString = dirListString + '\n{}{}'.format(indent + '    ', file)
        self.dirStructureString = dirListString
        return dirListString
    
    def get_file_text(self, subPath):
        filePath = os.path.join(self.startPath, subPath)
        print(f"Getting file text for: {filePath}")
        if not os.path.exists(filePath):
            print(f"File does not exist: {filePath}")
            return None
        with open(filePath, 'r', encoding='utf-8') as file:
            return file.read()
        
    def get_full_path(self, subPath):
        return os.path.join(self.startPath, subPath)
    
    def update_file_text(self, subPath, newText):
        filePath = os.path.join(self.startPath, subPath)
        print(f"Updating file text for: {filePath}")
        if not os.path.exists(filePath):
            print(f"File does not exist: {filePath}")
            return None
        with open(filePath, 'w', encoding='utf-8') as file:
            file.write(newText)

    @staticmethod
    def load_data_from_file(file):
        with open(file, 'r') as f:
            id = f.readline().strip()
            startPath = f.readline().strip()
            dirStructureString = f.readline().strip()
            dirStructureSummary = f.readline().strip()
            fileSummaryDict = eval(f.readline().strip())
            folderSummaryDict = eval(f.readline().strip())
            fileNav = FileNavService(startPath)
            fileNav.load_summaries(id, startPath, dirStructureString, dirStructureSummary, fileSummaryDict, folderSummaryDict)
            return fileNav

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
        if "appsettings" in string:
            return True
        if ".langgraph" in string:
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