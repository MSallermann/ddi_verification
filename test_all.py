# -->> Set path to spirit python pkg here <<--
path_to_spirit_pkg = "/Users/sallermann/Coding/spirit/core/python"
import sys
sys.path.append(path_to_spirit_pkg)

from test_cases import *

tests = [   
            Test_Brute_Force(), 
            Test_Continuous_Nucleation(), 
            Test_Homogeneous_Sphere(),
            Test_mu_s_Scaling(),
            Test_Continuous_Nucleation()
        ]

number_of_tests = 0
number_of_passed = 0
passed = []
failed = []

for test in tests:
    print("--------------------------------")
    print("-->> BEGIN Test: " + test.name + " <<--\n")
    if test.run():
        passed.append(test.name)
    else:
        failed.append(test.name)
    print("\n-->> END Test:   " + test.name + " <<--")    
    print("--------------------------------")

print("\n>================================<")
print(  "              SUMMARY             ")
print(  ">================================<")
print(">>> Passed {0} out of {1} tests".format(len(passed), len(passed) + len(failed)))
print("\n>>> Failed tests:")
for name in failed:
    print(" -- " + name)
print("\n>>> Passed tests:")
for name in passed:
    print(" -- " + name)
print(  ">--------------------------------<")





