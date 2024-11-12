import pandas as pd
import sys
import collections
from apriori_algo import apriori, calculate_conf

'''Generate the k=1 frequent ditemset with their support rate'''
# input: df of transcations, min_supp
# return list of ([itemset], supp)
def init_l1(supp, data):
    length = len(data)
    supports = data.sum() / length
    filtered_col_names = supports[supports >= supp].index.tolist()
    return [[[item], supports[item]] for item in filtered_col_names]


'''Convert df into list'''
#input: df
#return: list(each row) of list(values in each row)
def get_basket(data):
    temp = data.values.tolist()
    basket = []
    for idxs in temp:
        basket.append([idx for idx, t in enumerate(idxs) if t])
    return basket

'''Generate testing data according to the project example to dummy df format. <For testing only.>'''
def test():
    data = [
        ["pen", "ink", "diary", "soap"],
        ["pen", "ink", "diary"],
        ["pen", "diary"],
        ["pen", "ink", "soap"],
    ]
    df = pd.DataFrame(data)

    def expand_row(row):
        return pd.Series({item: True for item in row if pd.notna(item)})

    one_hot_encoded_df = df.apply(expand_row, axis=1).fillna(False)
    # print(one_hot_encoded_df)
    
    return one_hot_encoded_df


def main():
    #take in user query
    if len(sys.argv) != 4:
        print("Usage: python3 main.py <dataset_file> <param1> <param2>")
        return
    dataset_file = sys.argv[1]
    supp = float(sys.argv[2])
    conf = float(sys.argv[3])
    
    # dataset_file = 'INTEGRATED-DATASET.csv'
    if dataset_file == "toy":
         # use toy test case
        df = test()
    else:
        df = pd.read_csv(dataset_file)
   
    headers = list(df.columns)
    # print("header length",len(headers), headers)
    
    #preprocess
    #change col name into index
    new_column_names = {old_name: int(index) for index, old_name in enumerate(df.columns)}
    df.rename(columns=new_column_names, inplace=True)
    #generate l1 basket and convert df into list
    l1 = init_l1(supp,df)
    baseket = get_basket(df)

    # apriori start.... res_idxs = [l1,l2,...]
    res_idxs = apriori(l1, baseket, supp)

    print(f'=====Frequent itemsets (min_sup={supp*100}%)')
    

    res = {}
    for li in res_idxs:
        for lj in li: 
            res[tuple(lj[0])] = lj[1]
    # print(res)
    ordered_res =list(res.items())
    ordered_res  = sorted(ordered_res, key=lambda x:x[1], reverse=True)
    for key in ordered_res:
        # print(key)
        s = ""
        for i in key[0]:
            s+= headers[i] + ","
        print(f'[{s[:-1]}], Supp: {key[1]*100:.2f}%')
    print("Total number of frequent itemsets: ", len(ordered_res))

    
    print(f'=====High-confidence association rules (min_conf{conf*100}%)')
    rules =calculate_conf(res_idxs, conf)

    ordered_rules =list(rules.items())
    ordered_rules  = sorted(ordered_rules, key=lambda x:x[1][0], reverse=True)
    for key in ordered_rules:
        # print(key)
        s = ""
        for i in key[0][:-1]:
            s+= headers[i] + ","
        print(f'[{s[:-1]}] => [{headers[key[0][-1]]}] :  (Conf: {key[1][0]*100:.2f}%, Supp: {key[1][1]*100:.2f}%)')
    print("Total number of associate rules: ", len(rules))


if __name__ == "__main__":
    main()
