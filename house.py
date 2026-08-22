"""we are going to build a house using star pattern"""

# i thing if i am right with the name we need a tripaziam at top 
# let for row and 60 star at bottom and the decrease as we go up
# 60, 58, 56, 54, 52, 50
for i in range(5):
	print()

for i in range(5):
	print(" "*40, end = "")
	print("  "*(5-i), end = "")
	print("*"*i*5, end="")
	print("*"*(60 - i))


# we need 6 line full of star house space above door

# space above window
for i in range(2):
	print(" "*50 , end="")
	print("*"*60)

# carve window
for i in range(3):
	print(" "*50, end="")
	print("*"*41, end="")
	print(" "*8, end="")
	print("*"*11)

# space above window
for i in range(2):
        print(" "*50 , end="")
        print("*"*60)


# door part 
for i in range(7):
	print(" "*50, end="")
	print("*"*7, end="")
	print(" "*9, end="")
	print("*"*44)



# first need  a solid base 
"""better single two row with 159 star"""

print("*"*159)
print("*"*159)






