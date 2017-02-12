#DB assignment 1 Mini SQL
import csv
import re
import itertools
from prettytable import PrettyTable


#############Global Variables########

table_map = {}

##############Functions###############


def get_table_meta(filename):
    
    temp = []
    out = {}
    flag = 0
    cur = ""
    
    with open(filename) as x:
        temp = x.readlines()
    
    for x in temp:
        if x.strip() == "<end_table>":
            flag = 0
            cur = ""
        
        if flag == 1:
            cur = x.strip()
            out[cur] = []
            flag = 2
        elif flag == 2:
            out[cur].append(x.strip())

        if x.strip() == "<begin_table>":
            flag = 1

    return out

def populate_table(metadata):
    
    data = {}

    for i in metadata:
        
        mp = {}
        
        data[i] = []
        name = i+""+".csv"
        k = 0
        for j in metadata[i]:
            mp[j] = k
            mp[i+'.'+j] = k
            col = []
            data[i].append(col)
            #data[i][k] = []
            k = k+1

        table_map[i] = mp
        
        with open(name, 'rb') as mycsvfile:
            thedata = csv.reader(mycsvfile)
            for row in thedata:
                k = 0
                for x in row:
                    data[i][k].append(x)
                    k = k+1
    
    return data

def extended_query(string, data, ids, out):
   
    table_data = data[0]
    meta_data = data[1]
    tables = data[2]
    cols = data[3]

    prod = out[0]
    table_id = out[1]
    
    temp = cols[0].split('(')[0].lower()
    bloody = 0
    hell = []
    col_name = "default"
    if temp == "sum" or temp == "avg" or temp == "min" or temp == "max" or temp == "distinct":
        bloody = 1
        col_name = cols[0].split('(')[1].split(')')[0]
        cols = []
        cols.append(col_name)

    #if where is not present then we print the cartesian product. Right?
    if ids[1] == -1:
        if cols[0] == '*':
            head = []
            for i in tables:
                for j in meta_data[i]:
                    head.append(i+'.'+j)
            t = PrettyTable(head)
            
            for i in prod:
                row = []
                for j in i:
                    for k in j:
                        row.append(k)
                t.add_row(row)
            print t
        else:
            t = PrettyTable(cols)
            c = 0
            while c<len(prod):
                row = []
                for i in cols:
                    for j in tables:
                        if i in table_map[j]:
                            row.append(prod[c][table_id[j]][table_map[j][i]])
                            hell.append(prod[c][table_id[j]][table_map[j][i]])
                t.add_row(row)
                c = c+1
            if bloody == 0: 
                print t

    # now we have 3 cases only "where" , "where" with "and", "where" with "or"
    
    # case1
    cond = []
    if ids[2] == -1 and ids[3] == -1 and ids[1] > -1:
        flag = 0
        i = ids[1]+1
        while i < len(string):
            add = string[i].strip()
            add = add.split('=')
            for j in add:
                if j!='':
                    cond.append(j)
            i = i+1
        cond[1] = cond[1].split(';')[0]

        for i in tables:
            if cond[1] in table_map[i]:
                flag = 1
                break
        
        if cols[0] == '*':
            head = []
            for i in tables:
                for j in meta_data[i]:
                    head.append(i+'.'+j)
            t = PrettyTable(head)
            
            row_ids = []
            c = 0
            while c<len(prod):
                check = []
                if flag == 1:
                    for i in cond:
                        for j in tables:
                            if i in table_map[j]:
                                check.append(prod[c][table_id[j]][table_map[j][i]])
                    if check[0] == check[1]:
                        row_ids.append(c)
                    c = c+1
                else:
                    i = cond[0]
                    for j in tables:
                        if i in table_map[j]:
                                check.append(prod[c][table_id[j]][table_map[j][i]])
                    if check[0] == cond[1]:
                        row_ids.append(c)
                    c = c+1
                            

            for c in row_ids:
                row = []
                for i in prod[c]:
                    for j in i:
                        hell.append(j)
                        row.append(j)
                t.add_row(row)
            if bloody == 0:
                print t
        else:
            t = PrettyTable(cols)
            row_ids = []
            c = 0
            while c<len(prod):
                check = []
                if flag == 1:
                    for i in cond:
                        for j in tables:
                            if i in table_map[j]:
                                check.append(prod[c][table_id[j]][table_map[j][i]])
                    if check[0] == check[1]:
                        row_ids.append(c)
                    c = c+1
                else:
                    i = cond[0]
                    for j in tables:
                        if i in table_map[j]:
                                check.append(prod[c][table_id[j]][table_map[j][i]])
                    if check[0] == cond[1]:
                        row_ids.append(c)
                    c = c+1


            for c in row_ids:
                row = []
                for i in cols:
                    for j in tables:
                        if i in table_map[j]:
                            row.append(prod[c][table_id[j]][table_map[j][i]])
                            hell.append(prod[c][table_id[j]][table_map[j][i]])
                t.add_row(row)
            if bloody == 0:
                print t

    if ids[1] > -1 and (ids[2] > -1 or ids[3] > -1):
        cond = []
        i = ids[1]+1
        to = max(ids[2],ids[3])
        while i < to:
            add = string[i].strip()
            add = add.split('=')
            for j in add:
                if j!='':
                    cond.append(j)
            i = i+1
        cond[1] = cond[1].split(';')[0]

        cond2 = []
        i = to+1
        while i < len(string):
            add = string[i].strip()
            add = add.split('=')
            for j in add:
                if j!='':
                    cond2.append(j)
            i = i+1
        cond2[1] = cond2[1].split(';')[0]

        flag1 = 0
        flag2 = 0
        for i in tables:
            if cond[1] in table_map[i]:
                flag1 = 1
                break
        for i in tables:
            if cond2[1] in table_map[i]:
                flag2 = 1
                break
        t = []
        if cols[0] == '*':
            head = []
            for i in tables:
                for j in meta_data[i]:
                    head.append(i+'.'+j)
            t = PrettyTable(head)
        else:
            t = PrettyTable(cols)
        
        row_ids = []
        c = 0
        while c<len(prod):
            check = []
            if flag1 == 1:
                for i in cond:
                    for j in tables:
                        if i in table_map[j]:
                            check.append(prod[c][table_id[j]][table_map[j][i]])
                if check[0] == check[1]:
                    row_ids.append(c)
                c = c+1
            else:
                i = cond[0]
                for j in tables:
                    if i in table_map[j]:
                            check.append(prod[c][table_id[j]][table_map[j][i]])
                if check[0] == cond[1]:
                    row_ids.append(c)
                c = c+1


        row_ids2 = []
        c = 0
        while c<len(prod):
            check = []
            if flag2 == 1:
                for i in cond2:
                    for j in tables:
                        if i in table_map[j]:
                            check.append(prod[c][table_id[j]][table_map[j][i]])
                if check[0] == check[1]:
                    row_ids2.append(c)
                c = c+1
            else:
                i = cond2[0]
                for j in tables:
                    if i in table_map[j]:
                            check.append(prod[c][table_id[j]][table_map[j][i]])
                if check[0] == cond2[1]:
                    row_ids2.append(c)
                c = c+1

        row_idss = []

        if ids[2] > -1:
            row_idss = list(set(row_ids) & set(row_ids2))
        else:
            row_idss = list(set(row_ids) | set(row_ids2))

        if cols[0] == '*':
            for c in row_idss:
                row = []
                for i in prod[c]:
                    for j in i:
                        row.append(j)
                t.add_row(row)
        else:
            for c in row_idss:
                row = []
                for i in cols:
                    for j in tables:
                        if i in table_map[j]:
                            row.append(prod[c][table_id[j]][table_map[j][i]])
                            hell.append(prod[c][table_id[j]][table_map[j][i]])
                t.add_row(row)
        if bloody == 0:
            print t

    if bloody == 0:
        return


    for i in range(len(hell)):
        j = int(hell[i])
        hell[i] = j

    if temp == "sum":
        ans = sum(hell)
        print ans
        return
    elif temp == 'avg':
        ans = sum(hell)
        n = len(hell)
        ans = float(ans/n)
        print ans
        return
    elif temp == 'max':
        print max(hell)
        return
    elif temp == 'min':
        print min(hell)
        return
    elif temp == 'distinct':
        ans = set(hell)
        for i in ans:
            print i
    
    return

def cart_prod(table_data, tables):

    rows = []
    table_id = {}
    j = 0
    for i in tables:
        table_id[i] = j
        rows.append(zip(*table_data[i]))
        j = j+1
    if len(tables) > 1:
        prod= list(itertools.product(*rows))  
    else:
        rows.append([(0)])
        prod= list(itertools.product(*rows))  

    return (prod,table_id)

def query(string, table_data, meta_data):
   
    try:
        l = string.split()
        # here only Select,select,SELECT is valid
        cols = []

        id_from = -1
        id_where = -1
        id_and = -1
        id_or = -1
        id_eq = -1
        id_eq2 = -1
        j = 0

        for i in l:
            x = i.lower()
            if x == 'from':
                id_from = j
            if x == 'where':
                id_where = j
            if x == "and":
                id_and = j
            if x == "or":
                id_or = j
            if x == '=' and id_eq == -1:
                id_eq = j
            elif x == '=' and id_eq > -1:
                id_eq2 = j
            j = j+1

        
        if l[0].lower() != "select":
            print "There is an error in your query. Please check syntax"
            return
    
        if id_from == -1:
            print "No from statement in your query. Please check."
            return
    
        #Storing columns in cols
        i = 1
        while i < id_from:
            add = l[i].split(',')
            for j in add:
                if j != '':
                    cols.append(j)
            i = i+1

        tables = []
        i = id_from+1;
        to = id_where
        
        if id_where == -1:
            to = len(l)

        while i < to:
            add = l[i].split(',')
            for j in add:
                if j!='':
                    tables.append(j)
            i = i+1
        
        tables[len(tables)-1] = tables[len(tables)-1].split(';')[0]

        # for more than 1 tables
        if len(tables) > 1 or id_where > -1:
            out = cart_prod(table_data, tables)
            extended_query(l, (table_data,meta_data,tables,cols),(id_from, id_where, id_and, id_or, id_eq, id_eq2),out)
            return
        
        #checking for the sum,avg, max and min functions

        temp = cols[0].split('(')[0].lower()
        table = tables[0]
        
        if temp == "sum":
            col_name = cols[0].split('(')[1].split(')')[0]
            temp2 = table_data[table][table_map[table][col_name]]
            temp2 = map(int,temp2)
            print sum(temp2)
            return
        elif temp == 'avg':
            col_name = cols[0].split('(')[1].split(')')[0]
            temp2 = table_data[table][table_map[table][col_name]]
            temp2 = map(int,temp2)
            print float(sum(temp2))/len(temp2)
            return
        elif temp == 'max':
            col_name = cols[0].split('(')[1].split(')')[0]
            temp2 = table_data[table][table_map[table][col_name]]
            temp2 = map(int,temp2)
            print max(temp2)
            return
        elif temp == 'min':
            col_name = cols[0].split('(')[1].split(')')[0]
            temp2 = table_data[table][table_map[table][col_name]]
            temp2 = map(int,temp2)
            print min(temp2)
            return
        elif temp == 'distinct':
            col_name = cols[0].split('(')[1].split(')')[0]
            temp2 = table_data[table][table_map[table][col_name]]
            temp2 = set(temp2)
            print table
            print col_name
            for i in temp2:
                print i
            return

        #calling function for cases with "where" statement

        #Queries without any "where" statement

        if len(cols) == 1 and cols[0] == '*':
            #display_table(table_data,l[id_from+1], meta_data, meta_data[l[id_from+1]])
            display_table(table_data,tables[0], meta_data, meta_data[tables[0]])
        else:
            display_table(table_data,tables[0], meta_data, cols)
        
    except Exception as e:
        print type(e), e
        print "There is some error in your syntax"

    return

def display_table(data, table, meta, cols):
    
    t = PrettyTable(cols)
    c = 0
    for i in range(len(data[table][0])):
        l = []
        for j in cols:
            l.append(data[table][table_map[table][j]][c])
        c = c+1
        t.add_row(l)

    print t
    return

###############The SQL Engine####################

if __name__ == "__main__":

    filename = "metadata.txt"
    meta_data = get_table_meta(filename)
    table_data = populate_table(meta_data)
    
    cart_prod(table_data, ['table1'])

    while True:
        in_stream = raw_input("MiniSql>>")
        query(in_stream,table_data,meta_data)
