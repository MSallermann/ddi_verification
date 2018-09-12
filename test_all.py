# -->> Set path to spirit python pkg here <<--
path_to_spirit_pkg = "/path/to/spirit/python"
import sys
sys.path.append(path_to_spirit_pkg)

from test_cases import test_brute_force

number_of_tests = 0
number_of_passed = 0
passed = []
failed = []

print(">>> TEST: " + test_brute_force.name + "\n")

if test_brute_force.run():
    passed.append(test_brute_force.name)
else:
    failed.append(test_brute_force.name)

print("\n>--------------------------------<")
print(  "              SUMMARY             ")
print(  ">--------------------------------<")
print(">>> Passed {0} out of {1} tests".format(len(passed), len(passed) + len(failed)))
print("\n>>> Failed tests:")
for name in failed:
    print(" -- " + name)
print("\n>>> Passed tests:")
for name in passed:
    print(" -- " + name)
print(  ">--------------------------------<")





