import itertools
import collections

'''Run apriori algo'''
# input: l1=[[item_id:k-1, supp]...], basket=list of transcations, supp=float[0~1]
#return: res = [l1,l2,...]
def apriori(l1, baseket, supp):

    res = [l1]
    k = 1
    while len(res[-1]) > 0:
        ck = apriori_gen_with_prune(res[-1])
        print("Finding k = ", k , "itemset, ck length: ",len(ck))
        k +=1

        mp = collections.defaultdict(int)
        for t in baseket:
            # Use only subset that exist in transaction
            ct = subset(ck,t)
            for c in ct:
                mp[tuple(c)] += 1
        items = mp.items()
        lk = [[list(k),v/len(baseket)] for k,v in items if v >= len(baseket)*supp] #tuple list
        # print("lk length: ",len(lk))
        res.append(lk)
        # print("result length :", len(res))

    return res

'''Retain only cand in ck which occur in transaction t.'''
# Input: t is one transcation, ck is combined itemset condidates
# Return: res list of list(itemset) [[itemsets...],...]
def subset(ck, t:list):
    t = set(t)
    res = []
    for tp in ck:
        stp = set(tp)
        if stp.issubset(t):
            res.append(tp)
    return res

'''Extract list of each itemset from ([itemset], supp)'''
# input: list of ([itemset], supp)
# return: list of ([itemset])
def remove_supp(li):
    return [item[0] for item in li]

'''Take in L_k-1 and run apriori-gen to generate new cand itemsets, then do prune to check all the subset k-1 cand has support > min(which means exist in prev l_k-1), if does add cand into c_k.'''
'''Here we dont need to order, since we idx all the col, and it is place in itemset in order.'''
# Input: L_k_1 is a list of list [[item_id:k-1, supp], ...]
# Return: C_k as a list of list [[itemset:item_id, ...]...]
def apriori_gen_with_prune(L_k_1):
    # convert to [[itemset:item_id, ...]...]
    raw_l_k_1 = remove_supp(L_k_1)
    # print(raw_l_k_1)

    c_k = []
    
    for i in range(len(raw_l_k_1)):
        for j in range(i+1, len(raw_l_k_1)):
            if (raw_l_k_1[i][:-1] == raw_l_k_1[j][:-1] and raw_l_k_1[i][-1] < raw_l_k_1[j][-1]):
                cand  = raw_l_k_1[i]+ [raw_l_k_1[j][-1]]
                # Prune
                '''Iterate candidate in C_k Check if subset(size k-1) of candidate not in original raw_l_k_1, then remove the candidate. '''
                if not any(list(subset) not in raw_l_k_1 for subset in itertools.combinations(cand, len(cand)-1)):
                    c_k.append(cand)
    
    return c_k

'''We calculate the conf value and generate the associate rules'''
# input: res_idxs: [l1,l2,...], conf:float[0,1]
# return: rules:{[itemsets_LHS, RHS]: conf}
def calculate_conf(res_idxs, conf):
    #build cand dict{itemsets: support rate}
    cand_dict = collections.defaultdict(int)
    for lst in res_idxs:
        for ele in lst:
            cand_dict[tuple(ele[0])] = ele[1]
    # print(cand_dict)
    # for key in cand_dict.keys():
    #     print(key, cand_dict[key])

    #build rules dict{[itemsets_LHS, RHS]: conf}
    rules =collections.defaultdict(int)

    for l_n in res_idxs:
        # print(" =========")
        # print(l_n)

        #exclude null itemset(l_last =[]) or l contain only one item
        if len(l_n)==0 or len(l_n[0][0]) == 1:
            continue
        #for each cand, find all the subset(k-1) and cal conf
        for cand in l_n:
            for subset in itertools.combinations(cand[0], len(cand[0])-1):
                # find LHS and RHS
                s_cand = set(tuple(cand[0]))
                s_subset = set(subset)
                diff = s_cand - s_subset
                right = tuple(diff)

                #conf = prob(all)/ prob(LHS)
                comp_conf = cand[1] / cand_dict[subset]

                if comp_conf >= conf:
                    rule = subset + right
                    rules[rule] = [comp_conf, cand[1]]
    return rules

# Testing
# L_k_minus_1 = [['1', '2','3'], ['1','2','4'], ['1','3','4'], ['1','3','5'], ['2','3','4']] #['1', '2', '3', '4']
# # L_k_minus_1 = [['1'],['2'],['3']]
# C_k = apriori_gen_with_prune(L_k_minus_1)
# print(C_k)
# print(type(C_k))


