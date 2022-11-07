import pandas as pd
from os.path import dirname,abspath,join
import sys

choices_map= {
    "a": 0,
    "b": 1,
    "c": 2
}
choices_inv = {v: k for k, v in choices_map.items()}
def read_csv(file_path):
    try:
        data = pd.read_csv(file_path, sep=",", encoding='utf-8')
        return data
    except Exception:
        print("Something went wrong when trying to open the csv file!")
        sys.exit(2)
def drop_columns(data,columns):
    for i in range(len(columns)):
        try:
            data.pop(columns[i])
        except Exception:
            print(f"Column titled {columns[i]} does not exist in the file!")
    data.reset_index(inplace=True, drop=True)
def add(l1,l2):
    for i in range(len(l1)):
        l1[i]=l1[i]+l2[i]
def test_person(df):
    global prediction_rate
    behavior = [0, 0,0,0,0,0,0,0,0]
    state = [0, 0, 0]
    known = df[5:]
    known.reset_index(inplace=True, drop=True)
    for index, row in known.iterrows():
        tested_behavior = process_row(row, state)
        add(behavior,tested_behavior)
    summ = sum(behavior)

    try:
        for i in range(len(behavior)):
            behavior[i] = behavior[i] / summ
    except Exception:
        print(f"wyjebalo sie na {df}")
    u = []
   # print(behavior)
    unknown = df[:5]
    unknown.reset_index(inplace=True,drop=True)
    for index, row in unknown.iterrows():
        result = predict_choice(row, behavior,state)
        u.append(choices_inv.get(result))
    results = unknown.choice.array
    for i in range(0,5):
        if results[i] == u[i]:
            prediction_rate+=1
def predict_choice(row,behavior,state):
    global a,b,c,d,e,f,g,h,x
    choices = give_choices(row)
    Ms,Self,Wholesome,Jealousy,Guilt,Add01,Add02,Add12,Last=get_weights(choices,state)
    u=[]
    for i in range(0,3):
        u.append(Ms[i]*behavior[0]*a + Self[i]*behavior[1]*b+ Wholesome[i]*behavior[2]*c  + Jealousy[i]*behavior[3]*d+ Guilt[i]*behavior[4]*e + Add01[i]*behavior[5]*f + Add02[i]*behavior[6]*g + Add12[i]*behavior[7]*h + Last[i]*behavior[8]*x)
    max_value = max(u)
    index = u.index(max_value)
    return index
def give_choices(row):
    a1 = row.a1
    a2 = row.a2
    a3 = row.a3
    b1 = row.b1
    b2 = row.b2
    b3 = row.b3
    c1 = row.c1
    c2 = row.c2
    c3 = row.c3
    choice1 = [a1, a2, a3]
    choice2 = [b1, b2, b3]
    choice3 = [c1, c2, c3]
    choices = [choice1, choice2, choice3]
    return choices

"""

Metoda nauki

"""
def process_row(row,state):
    choice=row.choice

    choices=give_choices(row)

    ranks=get_rankings(choices,state)

    chosen=choices_map.get(choice)
    behavior_analysis=[]
    for i in range(len(ranks)):
        if ranks[i] == chosen:
            behavior_analysis.append(1)
        else:
            behavior_analysis.append(0)

    chosen_choice = choices[chosen]
    add(state,chosen_choice)
    return behavior_analysis
def give_methods_values(choices,state):
    Ms = []
    Self = []
    Wholesome = []
    Jealousy = []
    Guilt = []
    Add01=[]
    Add02=[]
    Add12=[]
    Last=[]
    for i in range(0, 3):
        c = choices[i]
        Ms.append(c[0]+c[2]+c[1])
        Self.append(c[1])
        Guilt.append(c[1] - c[2])
        Jealousy.append(c[0] - c[2])
        Add01.append(c[0]+c[1])
        Add02.append(c[0] + c[2])
        Add12.append(c[1] + c[2])
        Last.append(c[2])
        changes = []
        if 0 not in state:
            changes.append(c[0] / state[0])
            changes.append(c[1] / state[1])
            changes.append(c[2] / state[2])
            summm = sum(changes)
            Wholesome.append(summm / 3)
        else:
            Wholesome.append(0)
    return Ms,Self,Wholesome,Jealousy,Guilt,Add01,Add02,Add12,Last

def get_rankings(choices,state):

    Ms,Self,Wholesome,Jealousy,Guilt,Add01,Add02,Add12,Last=give_methods_values(choices,state)
    max_self=max(Self)
    max_group=max(Ms)
    max_wholesome = max(Wholesome)

    min_guilt=min(Guilt)
    min_jealousy=min(Jealousy)

    max01=max(Add01)
    max02=max(Add02)
    max12=max(Add12)
    maxLast=max(Last)
    index_group = Ms.index(max_group)

    index_self=Self.index(max_self)

    index_wholesome=Wholesome.index(max_wholesome)

    index_guilt=Guilt.index(min_guilt)

    index_jealousy=Jealousy.index(min_jealousy)

    index_add01=Add01.index(max01)
    index_add02 = Add02.index(max02)
    index_add12 = Add12.index(max12)
    index_last = Last.index(maxLast)
    pointers_to_choices=[index_group,index_self,index_wholesome,index_guilt,index_jealousy,index_add01,index_add02,index_add12,index_last]
    return pointers_to_choices
def get_weights(choices,state):

    Ms, Self, Wholesome, Jealousy, Guilt,Add01,Add02,Add12,Last = give_methods_values(choices, state)
    min_guilt = min(Guilt)
    min_jealousy = min(Jealousy)
    for m in [Ms,Self,Wholesome,Add01,Add02,Add12,Last]:
        divide_by_biggest(m)
    for i in range(0,3):
        if Jealousy[i]<=0:
            Jealousy[i]=1
        else:
            Jealousy[i]=min_jealousy/Jealousy[i]
        if Guilt[i]==0:
            Guilt[i]=1
        else:
            Guilt[i]=min_guilt/Guilt[i]

    return Ms, Self, Wholesome,Jealousy,Guilt,Add01,Add02,Add12,Last
def divide_by_biggest(list):
    try:
        max_val=max(list)
        for i in range(len(list)):
            list[i]=list[i] / max_val
    except:
        print(list)
        print(max_val)

"""
na podstawie wyborow bierze rankingi metod,
bierze rankingi kazdej metody per choice picked
"""
def process_choice(choices,state,choice):
    Ms,Self,Wholesome=get_rankings(choices,state)
    selected=choices_map.get(choice)
    returner=[]
    returner.append(Ms[selected])
    returner.append(Self[selected])
    returner.append(Wholesome[selected])
    return returner


"""

GOING FOR MAX  ->1
GOING EQUAL ->2
GOING FOR MYSELF ->2

(0.3,0.5,0.2)

MAX*0.3
SUM*0.5
MYSELF*0.2



"""
global prediction_rate,a,b,c,d,e,f,g,h,x
a=4
b=10
c=4
d=1
e=7
prediction_rate=0
columns=["qid","qpart","odd","visible"]
path=dirname(abspath(__file__))
path = join(path, "data")
path = join(path,"data_social-preferences_extract-2-for-students.csv")
#print(path)
df=read_csv(path)
drop_columns(df,columns)
current=0
maxValue=0
max_results=[]



for a1 in range(1,3):
    for a2 in range(1,3):
        for a3 in range(1, 3):
            for a4 in range(1, 3):
                for a5 in range(1, 3):
                    for a6 in range(1,3):
                        for a7 in range(1,3):
                            for a8 in range(1,3):
                                for a9 in range(1,3):
                                    for i in range(0, 800):
                                        a=a1
                                        b=a2
                                        c=a3
                                        d=a4
                                        e=a5
                                        f=a6
                                        g=a7
                                        h=a8
                                        x=a9
                                        start = current * 10
                                        person = df[start:start + 10]
                                        current += 1
                                        person.reset_index(inplace=True, drop=True)
                                        # print(person)
                                        # print("-------------------")
                                        # process_person(person)
                                        if not i % 2 == 0:
                                            test_person(person)

                                    if prediction_rate > maxValue:
                                        maxValue = prediction_rate
                                        max_results = [a, b, c,d,e,f,g,h,x]
                                    print(prediction_rate)
                                    prediction_rate = 0
                                    start = 0
                                    current = 0

print(maxValue)
print(max_results)
