baseBonii = [0.01, 0.02, 0.03, 0.04, 0.05] # 0.01 = 1%
setMulti = [1.15, 1.15, 1.15, 1.15, 1.15, 1.5] # 1.15x = 15% bonus, these should be per attribute (?)

# First, calculate total set multiplier by multiplying all set multipliers
setTotal = reduce(lambda x, y: x*y, setMulti)  # gets something to multply base bonus
print "bonus multipler from set: ", setTotal
# Then, apply that multiplier to each base bonus to get the effective bonus
effectiveBonii = map(lambda x: (x*setTotal)+1, baseBonii) # +1 to make these modifiers
print "effective bonii: ", effectiveBonii
# Lastly, reduce all the effective bonii to a single total bonus by multiplying them all together (per attribute)
total = reduce(lambda x, y: x*y, effectiveBonii)

print total