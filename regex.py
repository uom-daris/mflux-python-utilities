import re

melID = "MELU A 123411.jpeg"
hello = 'Hello'
id = "123411"

pattern = re.compile("^MELU")
# pattern2 = re.compile("[]"+id+"as")

my_regex = r"[^0-9]" + re.escape(id) + r"[^0-9]"
my_reg = r"^MELU"
# my_regex = re.escape(id)

found = pattern.match(melID)
if found:
    print 'got it'

if re.search(my_regex, melID):
    print 'got it too'

if re.search(my_reg, melID) and re.search(my_regex,melID):
    print 'got it too too'