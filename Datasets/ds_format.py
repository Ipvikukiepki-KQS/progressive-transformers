import click
from nlu_datacreator import DataCustomization
from nlg_datacreator import NLGDataCustomization
from dm_datacreator import DMDataCustomization

@click.group()
def cli1():
    pass

@cli1.command()

#In default 'Relative Path' of the Testsuit and Testcase has provided(from os module '../' represents one level up to the current Working directory)
@click.option('--infile', default = 'Multiwoz_annotated.json', help = 'Loading JSON file in the specified path')
@click.option('--outnlu', default = 'NLU_traindata.json', help = 'output customized JSON file in the specified path')
@click.option('--outdm', default = 'DM_traindata.md', help = 'output customized conversation as md file in the specified path')
@click.option('--outnlg', default = 'NLG_traindata.md', help = 'output customized NLG as JSON file in the specified path')


def format(infile, outnlu, outdm, outnlg):
    print("The annotated data for training will be loaded from: ", infile)
    DC = DataCustomization(infile,outnlu)
    NLGDC = NLGDataCustomization(infile,outnlg)
    DMDC = DMDataCustomization(infile,outdm)
    #DC.trainData(infile,outnlu, C = 0)
    #NLGDC.trainData(infile,outnlg,C = 0)
    DMDC.trainData(infile,outdm, C = 0) 
    
if __name__ == '__main__':
     cli1()
