from sqlalchemy import create_engine

def insertSample():
    engine = create_engine("postgresql://master:cs425!ProjectGroup3@cs425-ogs-group-3.cnjzlkxau3i8.us-east-1.rds.amazonaws.com/cs425")
    with engine.connect() as con:
        sampledata = open('/Users/kayinho/github/CS-425-Online-Grocery-Store-App-master/Application/sample.sql', 'r') #replace with the full path of 'sample.sql' in your local computer
        sqlFile = sampledata.read()
        sampledata.close()
        sqlCommands = sqlFile.replace('\n','').split('--break')
        for command in sqlCommands:
            if (command != ''):
                con.execute(command)

if __name__ == '__main__':
    insertSample()