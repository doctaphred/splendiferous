# <level> <points> <discount> <price>
cards = """\
1 0 w 00021
1 0 b 10002
1 0 g 21000
1 0 r 02100
1 0 k 00210

1 0 w 02002
1 0 b 00202
1 0 g 02020
1 0 r 20020
1 0 k 20200

1 0 w 02201
1 0 b 10220
1 0 g 01022
1 0 r 20102
1 0 k 22010

1 0 w 31001
1 0 b 01310
1 0 g 13100
1 0 r 10013
1 0 k 00131

1 0 w 01111
1 0 b 10111
1 0 g 11011
1 0 r 11101
1 0 k 11110

1 0 w 01211
1 0 b 10121
1 0 g 11012
1 0 r 21101
1 0 k 12110

1 0 w 03000
1 0 b 00003
1 0 g 00030
1 0 r 30000
1 0 k 00300

1 1 w 00400
1 1 b 00040
1 1 g 00004
1 1 r 40000
1 1 k 04000

2 1 w 00322
2 1 b 02230
2 1 g 23002
2 1 r 20023
2 1 k 32200

2 1 w 23030
2 1 b 02303
2 1 g 30230
2 1 r 03023
2 1 k 30302

2 2 w 00050
2 2 b 05000
2 2 g 00500
2 2 r 00005
2 2 k 50000

2 3 w 60000
2 3 b 06000
2 3 g 00600
2 3 r 00060
2 3 k 00006

2 2 w 00142
2 2 b 20014
2 2 g 42001
2 2 r 14200
2 2 k 01420

2 2 w 00053
2 2 g 05300
2 2 b 53000
2 2 r 30005
2 2 k 00530

3 4 w 00007
3 4 b 70000
3 4 g 07000
3 4 r 00700
3 4 k 00070

3 3 w 03353
3 3 b 30335
3 3 g 53033
3 3 r 35303
3 3 k 33530

3 4 w 30036
3 4 b 63003
3 4 g 36300
3 4 r 03630
3 4 k 00363

3 5 w 30007
3 5 b 73000
3 5 g 07300
3 5 r 00730
3 5 k 00073

"""


# 3 points each, require either 4x 2 colors or 3x 3 colors
nobles = """\
bg
bw
kr
kw
rg
gbr
gbw
kbw
krg
krw
"""

# Alternatively:
# wb...
# .bg..
# ..gr.
# ...rk
# w...k
# wbg..
# .bgr.
# ..grk
# w..rk
# wb..k
