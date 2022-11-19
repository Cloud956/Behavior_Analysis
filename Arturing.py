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
    behavior = [0, 0, 0, 0, 0, 0,0,0,0,0,0]
    state = [0, 0, 0]
    known = df.dropna()
    jealousy_retarder_metric = 0
    guilt_retarder_metric = 0
    known.reset_index(inplace=True, drop=True)
    length=0
    for index, row in known.iterrows():
        tested_behavior = process_row(row, state)
        add(behavior, tested_behavior)
        length+=1
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
            behavior[i] = behavior[i] / length
    except Exception:
        b=2
    add(population_behavior, behavior)
def test_person(df: object) -> object:
    global prediction_rate, population_behavior,multiply_population,multiply_human,prediction_success_dictionary
    behavior = [0, 0,0,0,0,0,0,0,0,0,0]
    state = [0, 0, 0]
    known = df[5:]
    jealousy_retarder_metric=0
    guilt_retarder_metric = 0
    known.reset_index(inplace=True, drop=True)
    for index, row in known.iterrows():
        tested_behavior = process_row_comparing_to_pop(row, state)
        add(behavior,tested_behavior)
        if tested_behavior[3] ==0:
            jealousy_retarder_metric+=1
        if tested_behavior[4] ==0:
            guilt_retarder_metric+=1
    if not jealousy_retarder_metric ==5 and not guilt_retarder_metric==5:
        behavior[3] = behavior[3]*(5/(5-jealousy_retarder_metric))
        behavior[4] = behavior[4] * (5 / (5 - guilt_retarder_metric))
    results = known.choice.array
    #ADJUSTING WEIGHTS FOR PREDICTIONS HERE
    success_rate={
        0 : [],
        1 : [],
        2 : [],
        3 : [],
        4 : [],
        5 : []
    }
    for var1 in range(-10,10):
        for var2 in range(-10,10):
            multiply_population=var1/5
            multiply_human=var2/5
            u = []
            current_success=0
            for index, row in known.iterrows():
                result = predict_final_choice(row, behavior, state)
                u.append(choices_inv.get(result))
            for i in range(0, 5):
                if results[i] == u[i]:
                    current_success+=1
            success_rate.get(current_success).append(str(multiply_population)+"_"+str(multiply_human))
    u = []
    unknown = df[:5]
    unknown.reset_index(inplace=True,drop=True)
    results_prediction={
        0 : "",
        1 : "",
        2 : "",
        3 : "",
        4 : ""
    }
    for num in range(5,0,-1):
        list=success_rate.get(num)
        if len(list)>0:
            if num in prediction_success_dictionary:
                prediction_success_dictionary[num] = prediction_success_dictionary.get(num)+1
            else:
                prediction_success_dictionary[num] = 1
            #print(f" best results  of {num} for list {list} ")

            for vars in list:
                variables=vars.split(sep="_")
                var1=float(variables[0])
                var2=float(variables[1])
                multiply_population = var1
                multiply_human = var2
                for index,row in unknown.iterrows():
                    result=predict_final_choice(row,behavior,state)
                    results_prediction[index]=results_prediction.get(index) + choices_inv.get(result)# results_prediction.get(index)+choices_inv.get(result)
            if num>10:
                num_below=num-1
                list_below=success_rate.get(num_below)
                for vars in list_below:
                    variables = vars.split(sep="_")
                    var1 = float(variables[0])
                    var2 = float(variables[1])
                    multiply_population = var1
                    multiply_human = var2
                    for index, row in unknown.iterrows():
                        result = predict_final_choice(row, behavior, state)
                        results_prediction[index] = results_prediction.get(index) + choices_inv.get(result)
            break
    final_fucking_results=[]
    for i in range(0,5):
        string = results_prediction.get(i)
        a=string.count("a")
        b=string.count("b")
        c=string.count("c")
        if a >=b and a>=c:
            final_fucking_results.append("a")
            continue
        if b>=a and b>=c:
            final_fucking_results.append("b")
            continue
        if c>=a and c>=b:
            final_fucking_results.append("c")
            continue
    results_to_test = unknown.choice.array
    b=2
    for i in range(0,5):
        if final_fucking_results[i]==results_to_test[i]:
            prediction_rate+=1
def predict_person(df: object) -> object:
    global prediction_rate, population_behavior, multiply_population, multiply_human, results_df, prediction_success_dictionary
    behavior = [0, 0, 0, 0, 0, 0, 0, 0]
    state = [0, 0, 0]
    unknown=df[df['choice'].isna()] ###
    if unknown.empty:###
        return False###
    known = df[df['choice'].notna()]####
    jealousy_retarder_metric = 0
    guilt_retarder_metric = 0
    known.reset_index(inplace=True, drop=True)
    for index, row in known.iterrows():
        tested_behavior = process_row_comparing_to_pop(row, state)
        add(behavior, tested_behavior)
        if tested_behavior[3] == 0:
            jealousy_retarder_metric += 1
        if tested_behavior[4] == 0:
            guilt_retarder_metric += 1
    if not jealousy_retarder_metric == 5 and not guilt_retarder_metric == 5:
        behavior[3] = behavior[3] * (5 / (5 - jealousy_retarder_metric))
        behavior[4] = behavior[4] * (5 / (5 - guilt_retarder_metric))
    results = known.choice.array
    # ADJUSTING WEIGHTS FOR PREDICTIONS HERE
    success_rate = {
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
        5: []
    }
    for var1 in range(-10, 10):
        for var2 in range(-10, 10):
            multiply_population = var1 / 5
            multiply_human = var2 / 5
            u = []
            current_success = 0
            for index, row in known.iterrows():
                result = predict_final_choice(row, behavior, state)
                u.append(choices_inv.get(result))
            for i in range(0, 5):
                if results[i] == u[i]:
                    current_success += 1
            success_rate.get(current_success).append(str(multiply_population) + "_" + str(multiply_human))
    u = []
    unknown.reset_index(inplace=True, drop=True)
    results_prediction = {
        0: "",
        1: "",
        2: "",
        3: "",
        4: ""
    }
    for num in range(5, 0, -1):
        list = success_rate.get(num)
        if len(list) > 0:
            if num in prediction_success_dictionary:
                prediction_success_dictionary[num] = prediction_success_dictionary.get(num)+1
            else:
                prediction_success_dictionary[num] = 1
            # print(f" best results  of {num} for list {list} ")
            for vars in list:
                variables = vars.split(sep="_")
                var1 = float(variables[0])
                var2 = float(variables[1])
                multiply_population = var1
                multiply_human = var2
                for index, row in unknown.iterrows():
                    result = predict_final_choice(row, behavior, state)
                    results_prediction[index] = results_prediction.get(index) + choices_inv.get(
                        result)  # results_prediction.get(index)+choices_inv.get(result)
            if num < 4:
                b = 2
            break
    final_fucking_results = []
    for i in range(0, 5):
        string = results_prediction.get(i)
        a = string.count("a")
        b = string.count("b")
        c = string.count("c")
        if a >= b and a >= c:
            final_fucking_results.append("a")
            continue
        if b >= a and b >= c:
            final_fucking_results.append("b")
            continue
        if c >= a and c >= b:
            final_fucking_results.append("c")
            continue
    qids=unknown.qid ###
    qpart=unknown.qpart###
    prediction=final_fucking_results###
    for i in range(len(prediction)):######
        new_row = pd.DataFrame([[qids[i], qpart[i],prediction[i]]], columns=['qid','qpart','prediction'])####
        results_df = pd.concat([results_df, new_row])###
    results_to_test = unknown.choice.array
    b = 2
    for i in range(0, 5):
        if final_fucking_results[i] == results_to_test[i]:
            prediction_rate += 1
def predict_choice(row,behavior,state):
    choices = give_choices(row)
    Ms,Self,Wholesome,Jealousy,Guilt,Third,First,Other,bs1,bs2,bs3=get_weights(choices,state)
    u=[]
    a=1
    b=1
    for i in range(0,3):
        u.append(Ms[i]*behavior[0] + b*Self[i]*behavior[1]+ Wholesome[i]*behavior[2]  + Jealousy[i]*behavior[3]+ Guilt[i]*behavior[4]+a*Third[i]*behavior[5]+First[i]*behavior[6]+Other[i]*behavior[7]+bs1[i]*behavior[8]+bs2[i]*behavior[9]+bs3[i]*behavior[10])
    max_value = max(u)
    index = u.index(max_value)
    return index
def multiply_values(list,v):
    returner=[]
    for i in range(len(list)):
        returner.append(list[i]*v)
    return returner
def predict_final_choice(row,behavior,state):
    global population_behavior, pop_success,multiply_population,multiply_human,human_sway
    choices = give_choices(row)
    first=pop_success/5
    human_behavior=behavior.copy()
    second=(5-pop_success)/5
    for i in range(len(human_behavior)):
        var=human_behavior[i]
        if var<=(-1*human_sway):
            human_behavior[i]=-1*human_sway
        elif var>=human_sway:
            human_behavior[i]=human_sway
    final_behavior=[0,0,0,0,0,0,0,0,0,0,0]
    human_behavior=multiply_values(human_behavior,multiply_human)
    pop_behavior=multiply_values(population_behavior,multiply_population)
    add(final_behavior,multiply_values(pop_behavior,first))
    add(final_behavior,multiply_values(human_behavior,second))
    Ms,Self,Wholesome,Jealousy,Guilt,Third,First,Other,bs1,bs2,bs3=get_weights(choices,state)
    u=[]
    for i in range(0,3):
        u.append(0*Ms[i]*final_behavior[0] + 0.8*Self[i]*final_behavior[1]+ 0*Wholesome[i]*final_behavior[2] + 0*Jealousy[i]*final_behavior[3]+ 0*Guilt[i]*final_behavior[4]+1.3*Third[i]*final_behavior[5]+0.4*First[i]*final_behavior[6]+0*Other[i]*final_behavior[7]+0*bs1[i]*final_behavior[8]+0*bs2[i]*final_behavior[9]+0*bs3[i]*final_behavior[10])
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

    Ms, Self, Wholesome, Jealousy, Guilt, Third,First,Other,bs1,bs2,bs3 = get_weights(choices,state)
    Methods=[Ms,Self,Wholesome,Jealousy,Guilt,Third,First,Other,bs1,bs2,bs3]
    chosen=choices_map.get(choice)
    behavior_analysis=[]
    chosen_choice = choices[chosen]
    add(state, chosen_choice)
    for i in range(len(Methods)):
        m=Methods[i]
        behavior_analysis.append(m[chosen])
    return behavior_analysis
def process_row_comparing_to_pop(row,state):
    global population_behavior,pop_success
    choice=row.choice

    choices=give_choices(row)

    Ms, Self, Wholesome, Jealousy, Guilt, Third,First,Other,bs1,bs2,bs3 = get_weights(choices,state)
    Methods=[Ms,Self,Wholesome,Jealousy,Guilt,Third,First,Other,bs1,bs2,bs3]
    chosen=choices_map.get(choice)
    behavior_analysis=[]
    chosen_pop=predict_choice(row,population_behavior,state)
    chosen_choice = choices[chosen]
    add(state, chosen_choice)
    if chosen_pop == chosen:
       pop_success+=1
       return([0,0,0,0,0,0,0,0,0,0,0])
    else:
        for i in range(len(Methods)):
            m=Methods[i]
            behavior_analysis.append(m[chosen_pop]-m[chosen])
        return behavior_analysis
def give_methods_values(choices,state):
    Ms = []
    Self = []
    Wholesome = []
    Jealousy = []
    Guilt = []
    Third = []
    First = []
    Other = []
    Bs1=[]
    bs2=[]
    bs3=[]
    for i in range(0, 3):
        c = choices[i]
        First.append(c[0])
        Other.append(c[0]+c[2])
        Ms.append(c[0]+c[2]+c[1])
        Self.append(c[1])
        Third.append(c[2])
        Bs1.append(c[1]/(c[0]+c[2]))
        if c[2]==0:
            bs2.append(1)
        else:
            bs2.append(c[1] / c[2])
        bs3.append(c[1]/c[0])
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

    return Ms,Self,Wholesome,Jealousy,Guilt, Third,First,Other,Bs1,bs2,bs3
# nie uzywamy
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
    Ms, Self, Wholesome, Jealousy, Guilt, Third,First,Other,bs1,bs2,bs3 = give_methods_values(choices, state)
    min_guilt = min(Guilt)
    min_jealousy = min(Jealousy)
    for m in [Ms,Self,Wholesome,Third,First,Other,bs1,bs2,bs3]:
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
            Self[i]=pow(Self[i],2)
        if min_jealousy != 0:
            Jealousy[i]=pow(min_jealousy/Jealousy[i],1)
        if min_guilt !=0:
            Guilt[i]=pow(min_guilt/Guilt[i],2)

#A LOT OF RANDOM SHIT FOR POWERS (LOOK INTO THOSE ARBITRARY POWERS). THOSE WILL NOT BE THE BEST ONCE FURTHER
#SHIT WILL BE IMPLEMENTED, NONETHELESS WITH TRIAL AND ERROR OPTIMISATION 1450 PEAK

    return Ms, Self, Wholesome,Jealousy,Guilt, Third,First,Other,bs1,bs2,bs3
def divide_by_biggest(list):
    global power_variable
    try:
        max_val=max(list)
        for i in range(len(list)):
            list[i]=list[i] / max_val
            list[i] =pow(list[i],power_variable)
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
global prediction_rate, population_behavior,a,pop_success,x2,human_sway,multiply_population,multiply_human,power_variable
power_variable = 1
multiply_population=1
multiply_human=1
human_sway=0.35
a=0.07
pop_success=0
population_behavior = [0.1772207237314289, 0.18370875674705725, 0.15108387005834809, 0.1617440080517915, 0.16873165681854402, 0.15751098459283025]
prediction_rate=0

population_behavior_from_6_without_division_by_sum = \
[0.9305816844027031, 0.9653641752873164, 0.7986340562775573, 0.873068453933686, 0.8965808412833038, 0.837040822279493]
population_behavior_from_8 = [0.9305816844027031, 0.9653641752873164, 0.7986340562775573, 0.873068453933686,\
                              0.8965808412833038, 0.837040822279493, 0.8333665756592636, 0.8936137803977628]
population_behavior=population_behavior_from_8
population_behavior=[0,0,0,0,0,0,0,0,0,0,0]
popul_b_11=[0.9305816844027031, 0.9789695940519627, 0.7986340562775573, 0.873068453933686, 0.8965808412833038, 0.837040822279493, 0.8333665756592636, 0.8936137803977628, 0.7541663436749159, 0.43501331836783985, 0.8001036804219313]
population_behavior=popul_b_11
multiply_values(population_behavior,10)
columns=["odd","visible"]
path=dirname(abspath(__file__))
path_data = join(path, "data")
pathfile = join(path_data,"data_social-preferences_extract-2-for-students.csv")

df=read_csv(pathfile)
drop_columns(df,columns)
current=0
maxValue=0
max_results=[]

path_to_results=join(path_data,"results.csv")
global results_df,prediction_success_dictionary
prediction_success_dictionary=dict()
results_df=pd.DataFrame(columns=['qid','qpart','prediction'])
"""

df=read_csv(filepath)
        new_row=pd.DataFrame([[title,amount]],columns=["Title","Amount"])
        df=pd.concat([df,new_row])
return pd.DataFrame(columns=["Title","Amount"])

"""

for i in range(0, 800):
    start = current * 10
    person = df[start:start + 10]
    current += 1
    person.reset_index(inplace=True, drop=True)
        # print(person)
        # print("-------------------")
        # process_person(person)
        #learn_from_person(person)
        #predict_person(person)
    if not i % 2 == 0:
        test_person(person)
        pop_success=0

print(prediction_rate)
#print(maxValue)
#print(max_results)
#for i in range(len(population_behavior)):
    #population_behavior[i]=population_behavior[i]/800
#print(population_behavior)
#results_df.to_csv(path_to_results,index=False)
#print(prediction_success_dictionary)