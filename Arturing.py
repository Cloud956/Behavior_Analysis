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
        data = pd.read_csv(file_path, sep=";", encoding='utf-8')
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

def learn_from_person(df):
    global prediction_rate, population_behavior
    behavior = [0, 0, 0, 0, 0, 0]
    state = [0, 0, 0]
    known = df.dropna()
    jealousy_retarder_metric = 0
    guilt_retarder_metric = 0
    known.reset_index(inplace=True, drop=True)
    for index, row in known.iterrows():
        tested_behavior = process_row(row, state)
        add(behavior, tested_behavior)
        if tested_behavior[3] == 0:
            jealousy_retarder_metric += 1
        if tested_behavior[4] == 0:
            guilt_retarder_metric += 1
    if not jealousy_retarder_metric ==5 and not guilt_retarder_metric ==5:
        behavior[3] = behavior[3] * (5 / (5 - jealousy_retarder_metric))
        behavior[4] = behavior[4] * (5 / (5 - guilt_retarder_metric))
    summ = sum(behavior)

    try:
        for i in range(len(behavior)):
            behavior[i] = behavior[i] / summ

    except Exception:
        print(f"wyjebalo sie na {df}")
    #add(population_behavior, behavior)
    u = []
def test_person(df: object) -> object:
    global prediction_rate, population_behavior
    behavior = [0, 0,0,0,0,0]
    state = [0, 0, 0]
    known = df[:5]
    jealousy_retarder_metric=0
    guilt_retarder_metric = 0
    known.reset_index(inplace=True, drop=True)
    for index, row in known.iterrows():
        tested_behavior = process_row(row, state)
        add(behavior,tested_behavior)
        if tested_behavior[3] ==0:
            jealousy_retarder_metric+=1
        if tested_behavior[4] ==0:
            guilt_retarder_metric+=1
    if not jealousy_retarder_metric ==5 and not guilt_retarder_metric==5:
        behavior[3] = behavior[3]*(5/(5-jealousy_retarder_metric))
        behavior[4] = behavior[4] * (5 / (5 - guilt_retarder_metric))

    #add(population_behavior, behavior)
    u = []
   # print(behavior)
    unknown = df[5:]
    unknown.reset_index(inplace=True,drop=True)
    for index, row in unknown.iterrows():
        result = predict_final_choice(row, behavior,state)
        u.append(choices_inv.get(result))
    results = unknown.choice.array
    for i in range(0,5):
        if results[i] == u[i]:
            prediction_rate+=1
def predict_person(df: object) -> object:
    global prediction_rate, population_behavior
    behavior = [0, 0,0,0,0,0]
    state = [0, 0, 0]
    known = df[:5]
    jealousy_retarder_metric=0
    guilt_retarder_metric = 0
    known.reset_index(inplace=True, drop=True)
    for index, row in known.iterrows():
        tested_behavior = process_row(row, state)
        add(behavior,tested_behavior)
        if tested_behavior[3] ==0:
            jealousy_retarder_metric+=1
        if tested_behavior[4] ==0:
            guilt_retarder_metric+=1
    behavior[3] = behavior[3]*(5/(5-jealousy_retarder_metric))
    behavior[4] = behavior[4] * (5 / (5 - guilt_retarder_metric))
    summ = sum(behavior)

    try:
        for i in range(len(behavior)):
            behavior[i] = behavior[i] / summ

    except Exception:
        print(f"wyjebalo sie na {df}")
    #add(population_behavior, behavior)
    u = []
   # print(behavior)
    unknown = df[5:]
    unknown.reset_index(inplace=True,drop=True)
    for index, row in unknown.iterrows():
        result = predict_choice(row, behavior,state)
        u.append(choices_inv.get(result))
    results = unknown.choice.array
    for i in range(0,5):
        if results[i] == u[i]:
            prediction_rate+=1
def predict_choice(row,behavior,state):
    choices = give_choices(row)
    Ms,Self,Wholesome,Jealousy,Guilt,Third=get_weights(choices,state)
    u=[]
    a=1
    b=1
    for i in range(0,3):
        u.append(Ms[i]*behavior[0] + b*Self[i]*behavior[1]+ Wholesome[i]*behavior[2]  + Jealousy[i]*behavior[3]+ Guilt[i]*behavior[4]+a*Third[i]*behavior[5])
    max_value = max(u)
    index = u.index(max_value)
    return index
def multiply_values(list,v):
    for i in range(len(list)):
        list[i]=list[i]*v
    return list
def predict_final_choice(row,behavior,state):
    global population_behavior, pop_success,x2
    choices = give_choices(row)
    first=pop_success/5
    human_behavior=behavior.copy()
    multiply_values(human_behavior,x2)
    second=(5-pop_success)/5
    final_behavior=[0,0,0,0,0,0]
    add(final_behavior,multiply_values(population_behavior,first))
    add(final_behavior,multiply_values(human_behavior,second))
    Ms,Self,Wholesome,Jealousy,Guilt,Third=get_weights(choices,state)
    u=[]
    a=1
    b=1
    for i in range(0,3):
        u.append(Ms[i]*final_behavior[0] + b*Self[i]*final_behavior[1]+ Wholesome[i]*final_behavior[2]  + Jealousy[i]*final_behavior[3]+ Guilt[i]*final_behavior[4]+a*Third[i]*final_behavior[5])
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
    global population_behavior,pop_success
    choice=row.choice

    choices=give_choices(row)

    Ms, Self, Wholesome, Jealousy, Guilt, Third = get_weights(choices,state)
    Methods=[Ms,Self,Wholesome,Jealousy,Guilt,Third]
    chosen=choices_map.get(choice)
    behavior_analysis=[]
    chosen_pop=predict_choice(row,population_behavior,state)
    chosen_choice = choices[chosen]
    add(state, chosen_choice)
    if chosen_pop == chosen:
       pop_success+=1
       return([0,0,0,0,0,0])
    else:
        for i in range(len(Methods)):
            m=Methods[i]
            behavior_analysis.append(m[chosen]-m[chosen_pop])
        return behavior_analysis
def give_methods_values(choices,state):
    Ms = []
    Self = []
    Wholesome = []
    Jealousy = []
    Guilt = []
    Third = []
    for i in range(0, 3):
        c = choices[i]
        Ms.append(c[0]+c[2]+c[1])
        Self.append(c[1])
        Third.append(c[2])
        if c[1]<=c[2]:
            Guilt.append(-2)
        else:
            Guilt.append(c[1] - c[2])
        if c[1] >=c[0]:
            Jealousy.append(-2)
        else:
            Jealousy.append(c[0] - c[1])
        changes = []
        if 0 not in state:
            changes.append(c[0] / state[0])
            changes.append(c[1] / state[1])
            changes.append(c[2] / state[2])
            summm = sum(changes)
            Wholesome.append(summm / 3)
        else:
            Wholesome.append(0)
    Jeal_sum=0
    broken_jeal=[]
    for i in range(0,3):
        if Jealousy[i]>=0:
            Jeal_sum+=Jealousy[i]
        else:
            broken_jeal.append(i)
    if len(broken_jeal) == 3:
        Jealousy = [0,0,0]
    else:
        for num in broken_jeal:
            Jealousy[num] = Jeal_sum/(3-len(broken_jeal))
    Guilt_sum=0
    broken_guilt=[]
    for i in range(0,3):
            if Guilt[i]>=0:
                Guilt_sum+=Guilt[i]
            else:
                broken_guilt.append(i)
    if len(broken_guilt)==3:
        Guilt = [0,0,0]
    else:
        for num in broken_guilt:
            Guilt[num]=Guilt_sum/(3-len(broken_guilt))

    return Ms,Self,Wholesome,Jealousy,Guilt, Third

def get_rankings(choices,state):

    Ms,Self,Wholesome,Jealousy,Guilt,Third =give_methods_values(choices,state)
    max_self=max(Self)
    max_group=max(Ms)
    max_wholesome = max(Wholesome)

    min_guilt=min(Guilt)
    min_jealousy=min(Jealousy)


    index_group = Ms.index(max_group)

    index_self=Self.index(max_self)

    index_wholesome=Wholesome.index(max_wholesome)

    index_guilt=Guilt.index(min_guilt)

    index_jealousy=Jealousy.index(min_jealousy)


    pointers_to_choices=[index_group,index_self,index_wholesome,index_guilt,index_jealousy]
    return pointers_to_choices
def get_weights(choices,state):
    global a
    Ms, Self, Wholesome, Jealousy, Guilt, Third = give_methods_values(choices, state)
    min_guilt = min(Guilt)
    min_jealousy = min(Jealousy)
    for m in [Ms,Self,Wholesome,Third]:
        divide_by_biggest(m)
    for i in range(0,3):
        if Third[i]<=1:
            Third[i]=pow(Third[i],1)
        if Ms[i]<=1:
            Ms[i]=pow(Ms[i],1)
        if Wholesome[i]<=1:
            Wholesome[i]=pow(Wholesome[i],1)
        if Self[i] +a >=1:
            Self[i] = 1
        else:
            Self[i]=pow(Self[i],1)
        if min_jealousy != 0:
            Jealousy[i]=pow(min_jealousy/Jealousy[i],1)
        if min_guilt !=0:
            Guilt[i]=pow(min_guilt/Guilt[i],1)

#A LOT OF RANDOM SHIT FOR POWERS (LOOK INTO THOSE ARBITRARY POWERS). THOSE WILL NOT BE THE BEST ONCE FURTHER
#SHIT WILL BE IMPLEMENTED, NONETHELESS WITH TRIAL AND ERROR OPTIMISATION 1450 PEAK

    return Ms, Self, Wholesome,Jealousy,Guilt, Third
def divide_by_biggest(list):
    try:
        max_val=max(list)
        for i in range(len(list)):
            list[i]=list[i] / max_val
    except:
        #print(list)
       # print(max_val)
       b=2




"""

GOING FOR MAX  ->1
GOING EQUAL ->2
GOING FOR MYSELF ->2

(0.3,0.5,0.2)

MAX*0.3
SUM*0.5
MYSELF*0.2



"""
global prediction_rate, population_behavior,a,pop_success,x2
a=0.06
pop_success=0
population_behavior = [0.1772207237314289, 0.18370875674705725, 0.15108387005834809, 0.1617440080517915, 0.16873165681854402, 0.15751098459283025]
prediction_rate=0
multiply_values(population_behavior,10)
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
for j in range(1,101):
    x2=j
    for i in range(0, 800):
        start = current * 10
        person = df[start:start + 10]
        current += 1
        person.reset_index(inplace=True, drop=True)
    # print(person)
    # print("-------------------")
    # process_person(person)
        #learn_from_person(person)
        if not i % 2 == 0:
            test_person(person)
            pop_success=0
    if prediction_rate>maxValue:
        maxValue=prediction_rate
        max_results=[x2]
print(maxValue)
print(max_results)
