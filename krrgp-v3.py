# coding: utf-8

# In[4]:


import pandas as pd

df = pd.read_csv('data.csv')


# In[33]:


class Vehicle:
    def __init__(self, arr):
        self.is_new = arr[0]
        self.brand = arr[1]
        self.name = arr[2]
        self.vehicle_type = arr[3]
        self.variant = arr[4]
        self.transmition = arr[5]
        self.price = arr[6]
        self.monthly_payment = arr[7]
        self.for_work = arr[8] == 1
        self.for_long_travel = arr[9] == 1
        self.for_big_family = arr[10] == 1
        self.for_outdoor = arr[11] == 1
        self.for_high_speed = arr[12] == 1
        self.rating = arr[13]
        self.feedback1 = arr[14]
        self.feedback2 = arr[15]
        self.feedback3 = arr[16]


    
    def __str__(self):
        return """
        Rating: {0.rating} / 5
        Brand: {0.brand}
        Name: {0.name}
        Type: {0.vehicle_type}
        Transmition: {0.transmition}
        Price: RM {0.price}
        Monthly Payment: RM {0.monthly_payment}
        Suitable For Work: {0.for_work}
        Suitable For Long Travel: {0.for_long_travel}
        Suitable For Big Family: {0.for_big_family}
        Suitable For Outdoor : {0.for_outdoor}
        Suitable For High Speed : {0.for_high_speed}
        
        Feedback:
        ~ {0.feedback1}
        ~ {0.feedback2}
        ~ {0.feedback3}
        """.format(self)
    

class VehicleList:
    def __init__(self):
        self.list = []
    
    def add(self, vehicle):
        self.list.append(vehicle)
    
    def __str__(self):
        li = [str(x) for x in self.list]
        return "\n---\n".join(li)
    

def df_to_vlist(df_clean):
    vlist = VehicleList()
    for _, row in df_clean.iterrows():
        vlist.add(Vehicle(row))
    return vlist


def clean_data(df):
    df = df.drop([
        'USED',

    ])
    df = df.rename(columns={
        "NEW": "IS_NEW",
        "VEHICLE TYPE": "VEHICLE_TYPE",
        "BRANDS": "BRAND",
        "MONTHLY PAYMENT FOR 10% DOWNPAYMENT": "MONTHLY_PAYMENT",
        "LONG TRAVEL": "LONG_TRAVEL",
        "BIG FAMILY": "BIG_FAMILY",
        "WORK": "FOR_WORK",
        "LONG TRAVEL": "FOR_LONG_TRAVEL",
        "BIG FAMILY": "FOR_BIG_FAMILY",
        "OUTDOOR": "OUTDOOR",
        "OUTDOOR": "FOR_OUTDOOR",
        "HIGH SPEED": "HIGH SPEED",
        "HIGH SPEED": "FOR_HIGH_SPEED",
    })
    return df


def filter_numeric(vlist, attr, max_amt):
    new_vlist = VehicleList()
    for i in range(len(vlist.list)):
        if (vlist.list[i].__dict__[attr] <= max_amt):
            new_vlist.add(vlist.list[i])
    return new_vlist


def filter_binary(vlist, attr, criteria):
    new_vlist = VehicleList()
    for i in range(len(vlist.list)):
        if (vlist.list[i].__dict__[attr] == criteria):
            new_vlist.add(vlist.list[i])
    return new_vlist


def ask(question, choice_ary):
    print(question)
    for i, choice in enumerate(choice_ary):
        print("{}: {}".format(i, choice))
    ans = -1
    while True:
        try:
            ans = int(input("> "))
        except ValueError:
            print("Please enter only numbers".format(0, len(choice_ary) - 1))
            continue
        if ans in list(range(len(choice_ary))):
            break
        else:
            print("Please answer with numbers in range [{},{}]".format(0, len(choice_ary) - 1))
        
    return ans

def predict_future_no_car(vlist, attr, min_cars):
    return len(filter_binary(vlist, attr, True).list) <= min_cars or         len(filter_binary(vlist, attr, False).list) <= min_cars
    


# In[34]:



def run_ES():
    min_cars = 0
    
    df_clean = clean_data(df)
    print(df_clean.dtypes)
    vlist = df_to_vlist(df_clean)
    print("Welcome to the Car ES")
    
    amt = ask(
        "What is ur expected budget for a car?", 
            [
                "RM 40,000", 
                "RM 50,000", 
                "more than RM 50,000", 
                "I don't know"
            ]
        )
    
    if amt == 0:
        vlist = filter_numeric(vlist, 'price', 40000)
    elif amt == 1:
        vlist = filter_numeric(vlist, 'price', 50000)
    elif amt == 2:
        vlist = filter_numeric(vlist, 'price', float('inf'))
    elif amt == 3:
        monthly_amt = ask(
        "How much can you pay for a car per month?",
            [
                "RM 600",
                "RM 800",
                "RM 1,000",
                "RM 2,000",
                "RM 4,000",
                "RM 6,000",
                "RM 8,000",
                "RM 10,000",
            ]
        )
        
        if monthly_amt == 0:
            vlist = filter_numeric(vlist, 'monthly_payment', 600)
        elif monthly_amt == 1:
            vlist = filter_numeric(vlist, 'monthly_payment', 800)
        elif monthly_amt == 2:
            vlist = filter_numeric(vlist, 'monthly_payment', 1000)
        elif monthly_amt == 3:
            vlist = filter_numeric(vlist, 'monthly_payment', 2000)
        elif monthly_amt == 4:
            vlist = filter_numeric(vlist, 'monthly_payment', 4000)
        elif monthly_amt == 5:
            vlist = filter_numeric(vlist, 'monthly_payment', 6000)
        elif monthly_amt == 6:
            vlist = filter_numeric(vlist, 'monthly_payment', 8000)
        elif monthly_amt == 7:
            vlist = filter_numeric(vlist, 'monthly_payment', 10000)
        
        
    print("We have {} cars that match your budget preference".format(len(vlist.list)))
    
    
    want_new = ask(
        "Do you want new car?",
        [
            "Yes",
            "Doesn't matter if new or old (More choices)"
        ]
    ) == 0
    
    
    if want_new:
        vlist = filter_binary(vlist, 'is_new', True)
        print("Good, we have {} new cars".format(len(vlist.list)))
    else:
        print("Great, we still have {} cars for you".format(len(vlist.list)))
    
    if predict_future_no_car(vlist, 'for_work', min_cars):
        print(vlist)
        return

    is_for_work = ask(
        "Do you wish to use the car for work(executive car)?",
        [
            "Yes",
            "No"
        ]
    ) == 0
    
    vlist = filter_binary(vlist, 'for_work', is_for_work)
    print("Ok, We have {} cars that match your preferences.".format(len(vlist.list)))

    if predict_future_no_car(vlist, 'for_long_travel', min_cars):
        print(vlist)
        return

    is_for_long_travel = ask(
        "Do you always travel long distances?",
        [
            "Yes",
            "No"
        ]
    ) == 0
    
    vlist = filter_binary(vlist, 'for_long_travel', is_for_long_travel)
    print("Ok, We have {} cars that match your preferences.".format(len(vlist.list)))

    if predict_future_no_car(vlist, 'for_big_family', min_cars):
        print(vlist)
        return

    is_for_big_family = ask(
        "Do you have a big family?",
        [
            "Yes",
            "No"
        ]
    ) == 0

    vlist = filter_binary(vlist, 'for_big_family', is_for_big_family)
    print("Ok, We have {} cars that match your preferences.".format(len(vlist.list)))

    if predict_future_no_car(vlist, 'for_outdoor', min_cars):
        print(vlist)
        return

    is_for_outdoor = ask(
        "Do you like to do outdoor activities?",
        [
            "Yes",
            "No"
        ]
    ) == 0

    vlist = filter_binary(vlist, 'for_outdoor', is_for_outdoor)
    print("Ok, We have {} cars that match your preferences.".format(len(vlist.list)))

    if predict_future_no_car(vlist, 'for_high_speed', min_cars):
        print(vlist)
        return

    is_for_high_speed = ask(
        "Do want high speed car?",
        [
            "Yes",
            "No"
        ]
    ) == 0

    vlist = filter_binary(vlist, 'for_high_speed', is_for_high_speed)
    print("Ok, We have {} cars that match your preferences.".format(len(vlist.list)))

    print(vlist)
        
if __name__ == '__main__':
    while True:
        run_ES()
        want_retry = input("Thank you for using the Car ES!\nDo you want to try again? (y/n)").upper() == "Y"
        if not want_retry:
            break
    print("See you again! :D")
    

