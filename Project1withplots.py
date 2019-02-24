import time # time package to track CPU time
import numpy as np # numpy package referred to as np
import matplotlib.pyplot as plt # matplotlib.pyplot package referred to as plt

with open("retail.txt") as file: # opens the file for reading

    totalBaskets = 0 # holds number of baskets

    # counts number of baskets by reading file
    for basket in file:
        totalBaskets += 1

    file.seek(0) # restart from beginning of file

    # Scalability Test
    # three support thresholds to test
    # twelve different chunk sizes to text
    supportThresholds = [0.01, 0.05, 0.1]
    sizeOfChunks = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    percentages = ['1%', '5%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']

    for q in supportThresholds: # loops through array of support thresholds

        aprioriPlots = [] # declares array for aprioriPlots

        pcyPlots = [] # declares array for pcyPlots

        plt.xlabel('Dataset Size') # x-axis label for graph

        plt.ylabel('Runtime (seconds)') # y-axis label for graph

        for size in sizeOfChunks: # loops through array of chunk sizes

            print("A-priori Algorithm")

            print("Support threshold = {}".format(q))
            print("Dataset size = {}".format(size))

            chunk = int(totalBaskets * size) # declares size of chunk

            s = int(chunk * q) # declares support threshold for size of chunk

            counts = [0] * chunk # declares array of counts

            aprioriStart = time.clock() # starts timer for a-priori algorithm

            inc = 0 # sets incrementor to 0

            # Pass 1 of A-priori Algorithm
            for basket in file: # reads each basket of items in file
                for number in basket.split(' '): # loops through each item in basket
                    if number != '\n': # avoids newline
                        inc += 1 # increments inc
                        counts[int(number)] += 1 # increments count of item in basket
                    if inc == chunk: # stops when incrementor is as large as chunk
                        break
                if inc == chunk: # stops when incrementor is as large as chunk
                    break

            file.seek(0) # restart from beginning of file

            # in-between passes
            # loops through array of counts
            # determines if item is frequent
            for i in range(chunk):
                if counts[i] < s: # set count to 0 if it is less than support threshold
                    counts[i] = 0

            inc = 0 # sets incrementor to 0

            countsOfPairs = [0] * chunk # declares array of pair counts

            # Pass 2 of A-priori Algorithm
            for basket in file: # reads each basket of items in file
                numbers = basket.split(' ') # turns basket into array
                numbers.remove('\n') # deletes newline from array
                numbers = list(map(int, numbers)) # converts strings to integers
                for i in range(len(numbers) - 1): # left number in pair
                    inc += 1 # increments inc
                    for j in range(i + 1, len(numbers)): # right number in pair
                        # if both counts of pairs are frequent
                        if inc < chunk and counts[numbers[i]] > 0 and counts[numbers[j]] > 0:
                            # one-dimensional triangular matrix approach
                            k = (numbers[i] - 1)*(int(numbers[i] / 2)) + numbers[j] - numbers[i]
                            countsOfPairs[k] += 1 # increments count of pair
                    if inc == chunk: # stops when incrementor is as large as chunk
                        break
                if inc == chunk: # stops when incrementor is as large as chunk
                    break

            file.seek(0) # restart from beginning of file

            inc = 0 # sets incrementor to 0

            # determines which pairs are frequent
            for basket in file: # reads each basket of items in file
                numbers = basket.split(' ') # turns basket into array
                numbers.remove('\n') # deletes newline from array
                numbers = list(map(int, numbers)) # converts strings to integers
                for i in range(len(numbers) - 1): # left number in pair
                    inc += 1 # increments inc
                    for j in range(i + 1, len(numbers)): # right number in pair
                        # if both counts of pair items are frequent
                        if inc < chunk and counts[numbers[i]] > 0 and counts[numbers[j]] > 0:
                            # one-dimensional triangular matrix approach
                            k = (numbers[i] - 1)*(int(numbers[i] / 2)) + numbers[j] - numbers[i]
                            if countsOfPairs[k] >= s: # if count of pair is greater than support threshold
                                print("Pair {" + str(numbers[i]) + ", " + str(numbers[j]) + "} is frequent.")
                            else:
                                print("Pair {" + str(numbers[i]) + ", " + str(numbers[j]) + "} is not frequent.")
                    if inc == chunk: # stops when incrementor is greater than chunk
                        break
                if inc == chunk: # stops when incrementor is greater than chunk
                    break

            aprioriEnd = time.clock() # stops timer for a-priori algorithm

            aprioriCPUTime = aprioriEnd - aprioriStart # calculates runtime for a-priori algorithm

            aprioriPlots.append(aprioriCPUTime) # saves runtime to array

            file.seek(0) # restart from beginning of file

            print("PCY Algorithm")

            hashBucketCounts = [0] * chunk # declares array of bucket counts

            counts = [0] * chunk # declares array of item counts

            inc = 0 # sets incrementor to 0

            pcyStart = time.clock() # start timer for pcy algorithm

            # Pass 1 of PCY Algorithm
            for basket in file: # reads each basket of items in file
                for number in basket.split(' '): # loops through each item in basket
                    if number != '\n': # avoids newline
                        inc += 1 # increments inc
                        counts[int(number)] += 1 # increments count of item in basket
                    if inc == chunk: # stops when incrementor is as large as chunk
                        break
                if inc == chunk: # stops when incrementor is as large as chunk
                    break
                numbers = basket.split(' ') # turns basket into array
                numbers.remove('\n') # deletes newline from array
                numbers = list(map(int, numbers)) # converts strings to integers
                for i in range(len(numbers) - 1): # left number in pair
                    for j in range(i + 1, len(numbers)): # right number in pair
                        h = (numbers[i] + numbers[j]) % chunk # hashes pair to bucket
                        hashBucketCounts[h] += 1 # increments count of bucket

            # in-between passes
            # loops through array of bucket counts
            # determines if bucket is frequent
            # converts array of bucket counts to bitmap
            for i in range(chunk):
                if hashBucketCounts[i] >= s: # frequent bucket is set to 1 else 0
                    hashBucketCounts[i] = 1
                else:
                    hashBucketCounts[i] = 0

            file.seek(0) # restart from beginning of file

            inc = 0 # sets incrementor to 0

            # Pass 2 of PCY Algorithm
            for basket in file: # reads each basket of items in file
                numbers = basket.split(' ') # loops through each item in basket
                numbers.remove('\n') # deletes newline from array
                numbers = list(map(int, numbers)) # converts strings to integers
                for i in range(len(numbers) - 1): # left number in pair
                    inc += 1 # increments inc
                    for j in range(i + 1, len(numbers)): # right number in pair
                        # if both counts of pair items are frequent
                        if inc < chunk and counts[numbers[i]] >= s and counts[numbers[j]] >= s:
                            h = (numbers[i] + numbers[j]) % chunk # hashes pair to bucket
                            if hashBucketCounts[h] == 1: # if bucket is frequent
                                print("Pair {" + str(numbers[i]) + ", " + str(numbers[j]) + "} is frequent.")
                            else:
                                print("Pair {" + str(numbers[i]) + ", " + str(numbers[j]) + "} is not frequent.")
                    if inc == chunk: # stops when incrementor is as large as chunk
                        break
                if inc == chunk: # stops when incrementor is as large as chunk
                    break

            pcyEnd = time.clock() # stops timer for pcy algorithm

            pcyCPUTime = pcyEnd - pcyStart # calculates runtime for pcy algorithm

            pcyPlots.append(pcyCPUTime) # saves runtime to array

            file.seek(0) # restart from beginning of file

        x = np.array(aprioriPlots) # copies a-priori runtimes to new array created using numpy package
        y = np.array(pcyPlots) # copies pcy runtimes to new array created using numpy package

        plt.xticks(np.arange(len(percentages)), percentages) # creates x-axis ticks for percentages
        plt.plot(x, color='blue', marker='o', linewidth=2, markersize=6) # plots a-priori runtimes on graph
        plt.plot(y, color='orange', marker='o', linewidth=2, markersize=6) # plots pcy runtimes on graph
        plt.legend(['A-priori', 'PCY'], loc='upper left') # creates legend to differentiate a-priori and pcy

        if q == 0.01: # if support threshold is 1%
            plt.title('support threshold: 1%') # creates graph title
            plt.savefig('1%.pdf') # outputs graph as .pdf file
        elif q == 0.05: # if support threshold is 5%
            plt.title('support threshold: 5%') # creates graph file
            plt.savefig('5%.pdf') # outputs graph as .pdf file
        else: # if support threshold is 10%
            plt.title('support threshold: 10%') # creates graph file
            plt.savefig('10%.pdf') # outputs graph as .pdf file

        plt.clf() # clears graph for next support threshold test
