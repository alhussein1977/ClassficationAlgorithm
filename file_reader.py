import os
import pandas as pd
class FileReader:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.text_files = None
        self.pathFile = None
        self.examples = None
        self.attributes=None
        self.target_attribute = None
        self.new_record=None
    #Displays a list of txt files in the data folder, and the user selects the desired file and stores its path
    def read_Files(self):
        # Get all text files in the folder
        self.text_files = [f for f in os.listdir(self.folder_path) if f.endswith('.txt')]
        # Print a list of file names with their numbers
        print("Select the number of data to apply one of the classification algorithms to:")
        for i,file in enumerate(self.text_files):
            print(f"\t{i+1}: {file}")
        print(f'\t{len(self.text_files)+1}: Go to Back Menu')
        print(f'\t{len(self.text_files)+2}: Exit of Appliction')
        # Obtain the required file number from the user
        while True:
            try:
                selected_file = int(input("\t\t\t\t")) - 1
                if selected_file >= 0 and selected_file < len(self.text_files):
                    # Store the path of the seleced file in an pathFile variable
                    self.pathFile = os.path.join(self.folder_path, self.text_files[selected_file])
                    print(f"The selected data to be applied by the algorithm is: {self.text_files[selected_file]}")
                    print(f"Paht of the dataset: {self.pathFile}")
                    break
                elif selected_file==len(self.text_files):
                    return 'Back'
                elif selected_file==len(self.text_files)+1:
                    return 'Exit'
                else:
                    print(f"The number you selected is incorrect. The selected numbers must be between 1 and {len(self.text_files)}")
            except ValueError:
                print(f"Please enter an integer between 1 and {len(self. text_files)}")
        return self.pathFile
    # Read data from the selected dataset file
    def read_dataset(self):
         # Read the first line and store the column names in an array named attributes
        with open(self.pathFile) as file:
            self.attributes = file.readline().strip().split(' ')
        # Read more lines and store data in a pandas dataset
        self.examples = pd.read_csv(self.pathFile, delimiter=' ', header=None, skiprows=1, names=self.attributes)
        return self.examples,self.attributes
    #Choose the target adjective or class
    def chose_targetattribute(self):
       
        print("Select the target attribute number from the list of existing attributes:")
        for indx,attribute in enumerate(self.attributes):
            print(f"\t{indx+1}: {attribute}")
        while True:
            try:
                numAttribute=int(input('\t\t\t'))-1
                if numAttribute >= 0 and numAttribute < len(self.attributes):
                    self.target_attribute= self.attributes[numAttribute]
                    print('The target attribute selected is: ' + str(self.attributes[(numAttribute)]))
                    break
                else:
                    print(f"The selected number is incorrect, please choose a number between 1 and {len(self.attributes)}")
            except ValueError:
                print(f"Please enter an integer between 1 and {len(self.attributes)}")
        return self.target_attribute
    # A function to enter a new record or the new state
    def read_newState(self):
        print('Please enter the new status (record) values:')
        self.new_record = []
        # Display attribute names and their values
        for indx, attribute in enumerate(self.attributes):
            if attribute != self.target_attribute:
                print(f"Attribute ( {attribute} )")
                # Display all possible values for an attribute
                for indv, val in enumerate(self.examples[attribute].unique()):
                    print(f"\t {indv+1}:{val}")
                # Choose the desired value from the user
                while True:
                    try:
                        selected_value = int(input(f"Select the value number of the attribute ({attribute}) for the new record:")) - 1
                        if selected_value>=0 and selected_value<len(self.examples[attribute].unique()):
                           # Store the selected value in a new variable called new_attributes
                            self.new_record.append(self.examples[attribute].unique()[selected_value])
                            break
                        else:
                            print(f"The selected number is incorrect. Please choose a number between 1 and {len(self.examples[attribute]. unique())}")
                    except ValueError:
                        print(f"Please enter an integer between 1 and {len(self.examples[attribute]. unique())}")
        return self.new_record
     
