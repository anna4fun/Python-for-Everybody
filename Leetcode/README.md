For python 3:

## 1. Generate Number
1. range(): range(n) will give range(0,n), if you want to create a iterable list, use list(range(n))


## 2. Built-in functions for list and string
1. map(): list(map(function, list_of_input)) will be the same as [function(i) for i in list(range(i))], see lc771
2. count(): str.count(sub-str), count the occurance of sub-str in str

      for example :
      map(str.count, str1) : think of str1 as a list, where the map function pass in every character in str1 into str, and check the occurance of that particular character in str. Here we could use sum() to adds up the occurance of every character in str1. see leetcode 771.

3. find() and index(): 

	str.find('character'), see if a character lies inside a string, if exist, returns the index of the LEFT MOST 'character', if not, return -1.

	list.index('element') similarily, you can find whether an element exist in a list by calling index() function. If the element does not exist, it will return an ValueError message.

4. split() and join():

	str.split('character') : separate string by every occurance of 'character', return a list of the separated parts, could use list indexation to retrieve sub_strings.

	'character'.join(a_list_of_string) : in contrast to split(), use join() to merge a list of strings into one big string, connected by designated 'character', for example, join with @ will be '@'.join(list).

5. list.pop(index): pop() will remove the index'th element of the list and return it, useful for Stack data type where you need to take out the first or lastest element that put into the stack.

6. To check if a list is empty: **For sequences, (strings, lists, tuples), use the fact that empty sequences are false.** 

7. Unlike list, in string, you cannot assign value to an existing element in the string. If you want to change the ith element of the string, or swap 2 element in the string, this error will pop-up ‘TypeError: 'str' object does not support item assignment’, see lc345 reverse a string, which is basically a changed version of reverse string.

8. chr() and ord() : ord('a') = 97, chr(97) = 'a'. This pair of functions gives the Unicode code point of the character. see leetcode 709 & 804, upper and lower case letters.

9. `|` is bitwise OR, logical OR for putting multiple conditions together is `or`

10. floor division `//` vs `round()`: floor division will stabilize the output to the smaller side of the integer, while `round()` can goes to larger side(eg. round(7/2) = 4) and smaller side (eg. round(5/2) = 2). To stabilize and predictable the calculation in binary search problems, use floor division.

## 3. Binary Tree
1. By convention, use the `root` Node to represent the whole tree, and use Node.value to retrieve the value of each Node.

2. Whenever you want to travel a tree with DFS(first reach leaf, then goes right), use a **Stack** to save the nodes of the tree, upper and left nodes come in first, lower and right nodes come in last, this is the best way to save a tree into an array. <114 Flatten Binary Tree To Linked List>

**Notice** that DFS is always acompanied by recursive function.

3. In contrast, to travel a tree BFS(at each level, travel from left to right, and then goes to the next level), use a **Double-ended Queue**, because the node's childs cannot be created along with the node, use a Deque could temporarily save the node.

4. leetcode 100 Same Tree(DFS) and leetcode 101 Symmetric Tree(BFS) are the same kind of problem: they both want to assert sub-trees are the same or not.

## 4. Binary Search

1. Use two pointers to save which sub-section you are searching in. 







   
          
