import sys
import os
def choseReadDataset():
    from file_reader import FileReader 
    reader = FileReader("\datasetTest")
    pathFile=reader.read_Files()
    examples,attributes= reader.read_dataset()
def choseMainMenue():
    print('Please enter the number of the required option:')
    print('\t 1.Choose the dataset')
    print('\t 2.Exit the Appliction')
    while True:
        try:
            numChoseMain=int(input('\t\t\t\t'))
            if numChoseMain>0 and numChoseMain<3:
                break
            else:
                print('The option number is incorrect, please enter the option number between 1 and 2')
        except ValueError:
            print("Please enter a valid number between 1 and 2")
    return numChoseMain
def choseOptionsMenu():
    print('Please choose one of the following options:')
    print('\t 1.Print Dataset')
    print('\t 2.Set Traget Attribute')
    print('\t 3.Add New State')
    print('\t 4.Set Other Dataset')
    print('\t 5.Exit Appliction')
    while True:
        try:
            numChoseOpt=int(input('\t\t\t\t'))
            if numChoseOpt>0 and numChoseOpt<6:
                break
            else:
                print('The option number is incorrect, please enter the option number between 1 and 5')
        except ValueError:
            print('Please enter a valid number between 1 and 5')
    return numChoseOpt
def choseAlgorithmMenu():
    #print('An algorithm has chosen a classification to apply to the data and a class selection for the new record (state)')
    #print('One of the algorithms chose the classification to apply to the dataset and test the class for the new record (state)')
    print('*' * 8,'Menu of classification algorithms','*' * 8)
    print(f'\t 1. ID3 Algorithm')
    print(f'\t 2. Bayesian Algorithm')
    print(f'\t 3. Go to Back Menu')
    print(f'\t 4. Exit Appliction')
    while True:
        try:
            numChoseAlgorithm = int(input('Enter the number of the algorithm you want to apply or go back to the previous menu:'))
            if numChoseAlgorithm > 0 and numChoseAlgorithm < 5:
                break
            else:
                print('The option number is incorrect, please enter the option number between 1 and 4')
        except ValueError:
            print('Please enter a valid number between 1 and 4')
    return numChoseAlgorithm

#Main
def main():
    print('-' * 30,'Welcome to the Application of Classification Algorithms','-' * 30)
    examples=None
    attributes=None
    target_attribute=None
    record_dict=None
    numChoseMain=choseMainMenue()
    while True:
        if numChoseMain==1:
            from file_reader import FileReader
            reader = FileReader("datasetTest")
            pathFile=reader.read_Files()
            target_attribute=None
            if pathFile=='Back':
                numChoseMain=choseMainMenue()
            elif pathFile=='Exit':
                numChoseMain=2
            else:
                examples,attributes= reader.read_dataset()
                numChoseOpt=choseOptionsMenu()
                while True:
                    if numChoseOpt==1:
                        # print of dataset
                        print(f'Total records (states) in the dataset ():{len(examples)}')
                        print(examples)
                        numChoseOpt=choseOptionsMenu()
                    elif numChoseOpt==2:
                        #chose of traget attribute
                        target_attribute=reader.chose_targetattribute()
                        numChoseOpt=choseOptionsMenu()
                    elif numChoseOpt==3:
                        if target_attribute==None:
                            print('Please select the target attribute first before entering the new record (state)')
                            target_attribute=reader.chose_targetattribute()
                        #record_dict=setNewstate()
                        new_record =reader.read_newState()
                        # Convert the record from a list to a directory
                        record_dict = dict(zip(attributes, new_record))
                        print('The new record:\n\t' + str(record_dict) + ' ' + target_attribute + '=?' )
                        numChoseAlgorithm=choseAlgorithmMenu()
                        while True:
                            if numChoseAlgorithm==1:
                                print('Run of ID3 Alrotihm')
                                from runID3 import minID3
                                id3algorithm=minID3(examples,attributes,target_attribute,record_dict)
                                id3algorithm.minID3()
                                numChoseAlgorithm=choseAlgorithmMenu()
                            elif numChoseAlgorithm==2:
                                print('Run of Baysean Alrotihm')
                                from runBaysaen import Baysaen
                                baysaen=Baysaen(examples,attributes,target_attribute,record_dict)
                                baysaen.predict_class()
                                numChoseAlgorithm=choseAlgorithmMenu()
                            elif numChoseAlgorithm==3:
                                numChoseOpt=choseOptionsMenu()
                                break
                            elif numChoseAlgorithm==4:
                                numChoseOpt=5
                                break
                    elif numChoseOpt==4:
                        numChoseMain=1
                        break
                    elif numChoseOpt==5:
                        numChoseMain=2
                        break               
        elif numChoseMain==2:
            break
    print('Thank you, for using the Classification Algorithms application program')
    sys.exit()  
main()
