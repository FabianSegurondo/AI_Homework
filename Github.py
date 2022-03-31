#Hello World in python 
print('hello world')

#Binary search python 

def binarySearch (array, start, end , index):
    
    if (end >=start ):

        mid = (start + end) // 2

        if array [mid] == index:
            
            return mid
        elif array[mid] > index:

            return binarySearch (array, start, mid -1, index)
        else:
            return binarySearch (array, mid +1, end, index)
    else:
         return -1
 #example

array = [1,1,3,9,8,2,5,9,50] 
index = 9

result = binarySearch (array, 0 , len(array)-1, index)
if result != -1:
    print ("index of the element", result )
else:
    print ("element nonexist")