import itertools
import json
import time
import argparse
import os
import numpy as np
import random
methodchoices = ["lsdcount", "lsdpigeonhole", "msdcount", "msdpigeonhole"]
datasizechoices = ["tiny", "small", "med", "large" ]
datachoices = ["Nearly Sorted", "Random", "Few Unique", "Sorted", "Reverse Sorted"]

def gen_list(cols, data_size, type='random'):
    max_value = {'large':9223372036854775807, 'med':4294967296, 'small': 1048576, 'tiny': 65536}[data_size]
    #---Random List---
    if type=='Random':
        lis = np.random.randint(-max_value, max_value, cols, dtype=np.int64).tolist()
        return [int(c) for c in lis]
    #---Few Unique---
    if type=='Few Unique':
        lis = np.random.randint(-max_value, max_value, cols, dtype=np.int64).tolist()
        few_unique = (np.random.choice(lis[0:len(lis) // 10], cols)).tolist()
        return [int(c) for c in few_unique]
    #---Reverse Sorted
    if type=='Reverse Sorted':
        lis = [-max_value]
        for i in range(1, cols):
            lis.append(lis[i-1]+(2*i*(max_value//cols)))
        return [int(c) for c in lis]
    #---Sorted List---
    if type=='Sorted':
        lis = [max_value]
        for i in range(1, cols):
            lis.append(lis[i-1]-(2*i*(max_value//cols)))
        return [int(c) for c in lis]
    #---Nearly Sorted
    if type=='Nearly Sorted':
        lis = [-max_value]
        for i in range(1, cols):
            lis.append(lis[i-1]+(2*i*(max_value//cols)))
        for idx1 in range(len(lis) - 2):
            if random.random() < 0.1:
                lis[idx1], lis[idx1 + 1] = lis[idx1 + 1], lis[idx1]
        return [int(c) for c in lis]
        
def myp(input):
    print(input, end='')
class Sorter:
    def __init__(self, config):
        self.t = time.time()
        self.outputpath = self.create_output_dictionary(config["output"])
        self.time_start = time.time()
        self.max_list_count = config["list_count"][0]
        self.max_list_length = config["list_length"]
        self.total_count = 0
        self.method = config["method"][0]
        self.datasizes = [item for item in datasizechoices if item not in config["exclude_data_sizes"]]
        self.datatypes = [item for item in datachoices if item not in config["exclude_data_types"]]
        self.begin_sorting()

    def create_output_dictionary(self, output):
        if output:
            path = output[0]
        else:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            path = "%s/sort_times.json" % (dir_path)
            uniq = 1
            while os.path.exists(path):
                path = "%s/sort_times_%d.json" % (dir_path, uniq)
                uniq += 1
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write("{\"radix_sort\":[]}")
        return path

    def set_data(self, data, list_length, data_size, data_type, time):
        dict = data['radix_sort']
        for idx, i in enumerate(dict):
            if i['data_type'] == data_type and i['data_size'] == data_size and i['rows'] == self.max_list_count and i['cols'] == list_length:
                data['radix_sort'][idx]['times'].setdefault(self.method,[])
                data['radix_sort'][idx]['times'][self.method].append(time)
                return data
        newData = {}
        newData.setdefault("data_type", data_type)
        newData.setdefault("data_size", data_size)
        newData.setdefault("rows", self.max_list_count)
        newData.setdefault("cols", list_length)
        newData.setdefault("times", {})
        newData['times'].setdefault(self.method,[])
        newData['times'][self.method].append(time)
        data['radix_sort'].append(newData)
        return data
            
  
        
    def begin_sorting(self):
        for i in range(1000):
            myp('\033[1;36m\rWarming up: %d/1000'%(i+1,))
            curr_list = gen_list(10000, 'large', 'Random')
            curr_list.sort()
        print(myp('\033[1;36m\r\033[KWarmup complete\n'))
        with open(self.outputpath, "r+") as f:
            data = json.load(f)
            data.setdefault("radix_sort", [])

        items = list(itertools.product(self.max_list_length, self.datasizes, self.datatypes, list(range(self.max_list_count))))
        interval = time.time()
        total_time = 0
        cum_total_time = 0
        sortd = True
        for list_length, data_size, data_type, count in items:
            self.print_sortmethod_count(data_size, data_type, count, len(items),interval)           
            curr_list = gen_list(list_length, data_size, data_type)
            t = time.time()
            curr_list.sort()
            newtime = time.time() - t
            currsortd = (all(curr_list[i] <= curr_list[i+1] for i in range(len(curr_list) - 1)))
            sortd &= currsortd
            data = self.set_data(data, list_length, data_size, data_type, newtime)
            total_time+=newtime
            if count+1 == self.max_list_count:
                self.print_sortmethod_evaluation(total_time, data_type, data_size, list_length, sortd)
                sortd = True
                interval = time.time( )
                cum_total_time+=total_time
                total_time = 0
            self.total_count+=1
        with open(self.outputpath, "r+") as f:
            f.seek(0)
            json.dump(data, f)
            f.truncate()
        self.print_conclusion(cum_total_time)

    


    def print_sortmethod_count(self, data_size, data_type, count, total_items, interval, ):
        datatabs = "\t" *  (4 - (len(data_type + str(data_size)) // 15))
        counttabs = "\t" * (2 - len(str(count)+"/"+str(self.max_list_count)) //7)
        myp( "\033[K")
        myp(
            "\033[1;31m\r%s %s%s   Current: %d/%d%s%d/%d\r\t\t\t"%(data_type,data_size,datatabs,(count),(self.max_list_count),counttabs,(self.total_count),(total_items))

        )
        myp("time: %f s"%(time.time()-interval))

    def print_sortmethod_evaluation(self, tdelta, data_type, data_size, list_length, sortd):
        name = "%s-%s" % (data_type, data_size)
        tabs = "\t\t" if len(name) < 16 else "\t"
        myp(
            "\033[1;32m\r\033[K%s%stime: %f s  data size: %d  Sorted = %s"%(name, tabs, tdelta, list_length, str(sortd))
            
        )
        myp( "\n")

    def print_conclusion(self, total_time):
        myp( "\r\033[K\033[1;35mTotal \t\t\ttime: %f s  tElapsed: %f\n" % (total_time, time.time() - self.time_start))
        myp(("\033[1;34mSaved to: %s\n"%self.outputpath ))
        myp( "\033[?25h")


def integer_range(minimum, maximum):
    def integer_range_checker(arg):
        try:
            i = int(arg)
        except ValueError:
            raise argparse.ArgumentTypeError("Must be an integer")
        if i < minimum or i > maximum:
            raise argparse.ArgumentTypeError(
                "Must be in range [%d .. %d]" % str(minimum), str(maximum)
            )
        return i

    return integer_range_checker

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Employs sorting algorithms from the pypy executable this script was run by to sort lists and store the time results",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="pypy handler.py",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        default="binaryDictionary.json",
        nargs=1,
        help="input json file generated by gendata.py",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        nargs=1,
        help="output json file to write times to. If none specified, one will be created",
    )
    parser.add_argument(
        "-l",
        "--list-length",
        type=int,
        default=[10000,100000,1000000],
        nargs="*",
        help="Maximum number of ints to be read into each list",
    )
    parser.add_argument(
        "-n",
        "--list-count",
        type=integer_range(1, 1000000),
        default=[100],
        nargs=1,
        help="Maximum number of lists to be read and sorted",
    )
    parser.add_argument(
        "-m",
        "--method",
        type=str,
        nargs = 1,
        help="Name of method used for sorting",
    )

    parser.add_argument(
        "-es",
        "--exclude-data-sizes",
        default=[],
        nargs="*",
        choices=datasizechoices,
        help="Exclude Data sizes while sorting, choose from: "
        + ", ".join(datasizechoices),
        metavar=" ",
    )
    
    parser.add_argument(
        "-et",
        "--exclude-data-types",
        nargs="*",
        default=[],
        choices=datachoices,
        help="Exclude Data types while sorting, choose from: " + ", ".join(datachoices),
        metavar=" ",
    )
    args = parser.parse_args()
    sorter = Sorter(vars(args))
