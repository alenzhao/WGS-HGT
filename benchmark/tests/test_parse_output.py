# ----------------------------------------------------------------------------
# Copyright (c) 2015, The WGS-HGT Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from unittest import TestCase, main
from shutil import rmtree
from tempfile import mkdtemp
from os import remove
from os.path import join

from benchmark.parse_output import (parse_hgts,
                                    parse_consel,
                                    parse_output,
                                    parse_darkhorse,
                                    parse_hgtector)


class ParseOutputTests(TestCase):
    """ Tests for parse_output.py """

    def setUp(self):
        """ Set up working directory and test files
        """
        self.working_dir = mkdtemp()
        # TREX output
        self.trex_output_hgt_fp = join(
            self.working_dir, "trex_output_hgt.txt")
        with open(self.trex_output_hgt_fp, 'w') as tmp:
            tmp.write(trex_output_hgt)
        # RANGER-DTL-U output
        self.rangerdtl_output_hgt_fp = join(
            self.working_dir, "rangerdtl_output_hgt.txt")
        with open(self.rangerdtl_output_hgt_fp, 'w') as tmp:
            tmp.write(rangerdtl_output_hgt)
        # RIATA-HGT output
        self.riatahgt_output_hgt_fp = join(
            self.working_dir, "riatahgt_output_hgt.txt")
        with open(self.riatahgt_output_hgt_fp, 'w') as tmp:
            tmp.write(riatahgt_output_hgt)
        # JANE 4 output
        self.jane4_output_hgt_fp = join(
            self.working_dir, "jane4_output_hgt.txt")
        with open(self.jane4_output_hgt_fp, 'w') as tmp:
            tmp.write(jane4_output_hgt)
        # Consel output
        self.consel_output_hgt_fp = join(
            self.working_dir, "consel_output_hgt.txt")
        with open(self.consel_output_hgt_fp, 'w') as tmp:
            tmp.write(consel_output_hgt)
        # HGTector output
        self.hgtector_output_hgt_fp = join(
            self.working_dir, "hgtector_output_hgt.txt")
        with open(self.hgtector_output_hgt_fp, 'w') as tmp:
            tmp.write(hgtector_output_hgt)
        # DarkHorse output
        self.darkhorse_output_hgt_fp = join(
            self.working_dir, "darkhorse_output_hgt.txt")
        with open(self.darkhorse_output_hgt_fp, 'w') as tmp:
            tmp.write(darkhorse_output_hgt)
        # empty output
        self.empty_output_hgt_fp = join(
            self.working_dir, "empty_output_hgt.txt")
        with open(self.empty_output_hgt_fp, 'w') as tmp:
            tmp.write(empty_output_hgt)
        # list of files to remove
        self.files_to_remove = [self.trex_output_hgt_fp,
                                self.rangerdtl_output_hgt_fp,
                                self.riatahgt_output_hgt_fp,
                                self.jane4_output_hgt_fp,
                                self.consel_output_hgt_fp,
                                self.hgtector_output_hgt_fp,
                                self.empty_output_hgt_fp]

    def tearDown(self):
        for file in self.files_to_remove:
            remove(file)
        rmtree(self.working_dir)

    def test_parse_hgts_trex(self):
        """ Test functionality of parse_hgts() for TREX
        """
        with open(self.trex_output_hgt_fp, 'r') as f:
            output = parse_hgts(f, 'trex')
        self.assertEqual(int(output), 1)

    def test_parse_hgts_rangerdtl(self):
        """ Test functionality of parse_hgts() for RANGER-DTL-U
        """
        with open(self.rangerdtl_output_hgt_fp, 'r') as f:
            output = parse_hgts(f, 'ranger-dtl')
        self.assertEqual(int(output), 1)

    def test_parse_hgts_riatahgt(self):
        """ Test functionality of parse_hgts() for RIATA-HGT in PhyloNet
        """
        with open(self.riatahgt_output_hgt_fp, 'r') as f:
            output = parse_hgts(f, 'riata-hgt')
        self.assertEqual(int(output), 1)

    def test_parse_hgts_jane4(self):
        """ Test functionality of parse_hgts() for Jane 4
        """
        with open(self.jane4_output_hgt_fp, 'r') as f:
            output = parse_hgts(f, 'jane4')
        self.assertEqual(int(output), 1)

    def test_parse_consel(self):
        """ Test functionality of parse_consel
        """
        output_exp = ['0.99', '0.01']
        with open(self.consel_output_hgt_fp, 'r') as f:
            output = parse_consel(input_f=f)
        self.assertListEqual(output, output_exp)

    def test_parse_output(self):
        """Test functionality of parse_output
        """
        output_exp = ["0.99", "0.01"]
        output = parse_output(hgt_results_fp=self.consel_output_hgt_fp,
                              method="consel")
        self.assertEqual(output_exp, output)
        output_exp = "1"
        output = parse_output(hgt_results_fp=self.riatahgt_output_hgt_fp,
                              method="riata-hgt")
        self.assertEqual(output_exp, output)
        output_exp = ("WP_011672248.1\t372461\tBuchnera aphidicola\tProteobac"
                      "teria;Gammaproteobacteria;Enterobacteriales;Enterobact"
                      "eriaceae;Buchnera;Buchnera aphidicola\t37.5\t99.14\nWP"
                      "_045117937.1\t580331\tThermoanaerobacter italicus\tFir"
                      "micutes;Clostridia;Thermoanaerobacterales;Thermoanaero"
                      "bacteraceae;Thermoanaerobacter;Thermoanaerobacter ital"
                      "icus\t42.6\t93.84")
        output = parse_output(hgt_results_fp=self.hgtector_output_hgt_fp,
                              method="hgtector")
        self.assertEqual(output_exp, output)
        output_exp = ("G2311_SE001,\tgi|557307555|ref|YP_008766893.1|\t140749"
                      "3\tShigella phage SfIV\tViruses;Caudovirales;Myovirida"
                      "e\t67.4\t100\t0.002\nG1250_SE001,\tgi|9630468|ref|NP_0"
                      "46899.1|\t40631\tEnterobacteria phage N15\tViruses;Cau"
                      "dovirales;Siphoviridae;N15likevirus\t79.4\t100\t0.002\n"
                      "G1252_SE001,\tgi|428782382|ref|YP_007112139.1|\t114714"
                      "4\tEnterobacteria phage HK225\tViruses;Caudovirales;Si"
                      "phoviridae;Lambdalikevirus\t88.2\t100\t0.002\nG1251_SE"
                      "001,\tgi|428782381|ref|YP_007112138.1|\t1147144\tEnter"
                      "obacteria phage HK225\tViruses;Caudovirales;Siphovirid"
                      "ae;Lambdalikevirus\t94.9\t100\t0.002")
        output = parse_output(hgt_results_fp=self.darkhorse_output_hgt_fp,
                              method="darkhorse")
        self.assertEqual(output_exp, output)

    def test_parse_output_empty(self):
        """Test functionality of parse_output with empty file
        """
        output_exp = 'NaN'
        output = parse_output(hgt_results_fp=self.empty_output_hgt_fp,
                              method="riata-hgt")
        self.assertEqual(output_exp, output)

    def test_parse_output_error(self):
        """Test functionality of parse_output passing unsupported method
        """
        self.assertRaises(ValueError,
                          parse_output,
                          hgt_results_fp=self.consel_output_hgt_fp,
                          method="Consel")

    def test_parse_hgtector(self):
        """ Test functionality of parse_hgtector
        """
        output_exp = ("WP_011672248.1\t372461\tBuchnera aphidicola\tProteobac"
                      "teria;Gammaproteobacteria;Enterobacteriales;Enterobact"
                      "eriaceae;Buchnera;Buchnera aphidicola\t37.5\t99.14\nWP"
                      "_045117937.1\t580331\tThermoanaerobacter italicus\tFir"
                      "micutes;Clostridia;Thermoanaerobacterales;Thermoanaero"
                      "bacteraceae;Thermoanaerobacter;Thermoanaerobacter ital"
                      "icus\t42.6\t93.84")
        with open(self.hgtector_output_hgt_fp, 'r') as f:
            output = parse_hgtector(input_f=f)
        self.assertEqual(output, output_exp)

    def test_parse_darkhorse(self):
        """Test functionality of parse_darkhorse
        """
        output_candidate_genomes_fp = join(
            self.working_dir, "output_candidate_genomes_fp")
        output_exp = ("G2311_SE001,\tgi|557307555|ref|YP_008766893.1|\t140749"
                      "3\tShigella phage SfIV\tViruses;Caudovirales;Myovirida"
                      "e\t67.4\t100\t0.002\nG1250_SE001,\tgi|9630468|ref|NP_0"
                      "46899.1|\t40631\tEnterobacteria phage N15\tViruses;Cau"
                      "dovirales;Siphoviridae;N15likevirus\t79.4\t100\t0.002\n"
                      "G1252_SE001,\tgi|428782382|ref|YP_007112139.1|\t114714"
                      "4\tEnterobacteria phage HK225\tViruses;Caudovirales;Si"
                      "phoviridae;Lambdalikevirus\t88.2\t100\t0.002\nG1251_SE"
                      "001,\tgi|428782381|ref|YP_007112138.1|\t1147144\tEnter"
                      "obacteria phage HK225\tViruses;Caudovirales;Siphovirid"
                      "ae;Lambdalikevirus\t94.9\t100\t0.002")
        with open(self.darkhorse_output_hgt_fp, 'r') as f:
            output = parse_darkhorse(input_f=f,
                                     output_fp=output_candidate_genomes_fp,
                                     low_lpi=0.0,
                                     high_lpi=0.6)
        self.assertEqual(output, output_exp)


empty_output_hgt = """
"""

trex_output_hgt = """
hgt : reading options
hgt : reading the input file
Root_existance = -1
(1) - SE001
(2) - SE010
(3) - SE008
(4) - SE006
(5) - SE009
(6) - SE005
(7) - SE004
(8) - SE003
(9) - SE002
(10) - SE007

1-11 --> 2.149488
2-11 --> 1.086610
11-12 --> 3.776117
3-12 --> 0.863054
4-13 --> 0.567042
5-13 --> 0.501468
12-14 --> 0.210245
13-14 --> 0.902942
14-15 --> 0.205423
6-15 --> 3.099251
15-16 --> 0.371456
7-16 --> 1.812913
16-17 --> 0.729336
8-17 --> 1.737411
9-18 --> 1.660613
10-18 --> 0.700002
17-19 --> 0.244478

Root_existance = -1
(1) - SE006
(2) - SE009
(3) - SE008
(4) - SE001
(5) - SE010
(6) - SE005
(7) - SE004
(8) - SE003
(9) - SE002
(10) - SE007

1-11 --> 5.232907
2-11 --> 5.232907
3-12 --> 6.135849
11-12 --> 0.902942
4-13 --> 2.149488
5-13 --> 2.149488
6-14 --> 3.130818
13-14 --> 0.981330
12-15 --> 0.205423
14-15 --> 3.210454
15-16 --> 0.371456
7-16 --> 6.712729
16-17 --> 0.729336
8-17 --> 7.442065
9-18 --> 6.053406
10-18 --> 6.053406
17-19 --> 0.244478
4,3040.873033,2.000000
4,3040.873033,2.000000

hgt : adding the tree roots
hgt : pre-treatment process
===============================================
| CRITERIA VALUES BEFORE DETECTION
| RF distance  =  4
| LS criterion = 54.3
| BD criterion = 2.0
===============================================

hgt : scenario unique
hgt : start of detection

== NEW STEP OF DETECTION == [size of the trees (after reduction)=8]

[1 HGT]
HGT-DETECTION : cpt_hgt= 0
hgt_red : HGT #1 : [ 2--11] -> [ 5-- 9]
HGT-DETECTION : cpt_hgt= 0
RF = 0 | LS = 0.00 | BD = 0.00
rRF = 2 | rLS = 0.22 | rBD = 1.00
HGT-DETECTION : cpt_hgt= 0
hgt : HGT #1 : [ 6--16] -> [13--12]

Criteria values after this step :
RF = 0 | LS = 0.00 | BD = 0.00

hgt : Looking for idling hgt
HGT_INT : Procedure de suppression des transferts inutiles, il y a 1 transferts
HGT_INT : bestHGT[1].valide=1
HGT-DETECTION : on a termine le calcul RF=4(0)
hgt : multicheckTab[0].m=1 : (1) 1
hgt : formatting the results
hgt_valide=1
hgt : number of HGT(s) found = 1
hgt : end of computation, check the file results.txt for the program output
"""

rangerdtl_output_hgt = """

 ------------ Reconciliation for Gene Tree 1 (rooted) -------------
Species Tree:
(((((((SE001,SE010)n7,SE008)n6,(SE006,SE009)n8)n5,SE005)n4,SE004)n3,SE003)n2,\
(SE002,SE007)n9)n1;

Gene Tree:
(((((SE008_01000,(SE006_01000,SE009_01000)m7)m5,(SE005_01000,(SE001_04150,SE0\
10_04150)m12)m10)m4,SE004_01000)m3,SE003_01000)m2,(SE002_01000,SE007_01000)m1\
7)m1;

Reconciliation:
SE008_01000: Leaf Node
SE006_01000: Leaf Node
SE009_01000: Leaf Node
m7 = LCA[SE006_01000, SE009_01000]: Speciation, Mapping --> n8
m5 = LCA[SE008_01000, SE009_01000]: Speciation, Mapping --> n5
SE005_01000: Leaf Node
SE001_04150: Leaf Node
SE010_04150: Leaf Node
m12 = LCA[SE001_04150, SE010_04150]: Speciation, Mapping --> n7
m10 = LCA[SE005_01000, SE010_04150]: Transfer, Mapping --> SE005, Recipient \
--> n7
m4 = LCA[SE008_01000, SE010_04150]: Speciation, Mapping --> n4
SE004_01000: Leaf Node
m3 = LCA[SE008_01000, SE004_01000]: Speciation, Mapping --> n3
SE003_01000: Leaf Node
m2 = LCA[SE008_01000, SE003_01000]: Speciation, Mapping --> n2
SE002_01000: Leaf Node
SE007_01000: Leaf Node
m17 = LCA[SE002_01000, SE007_01000]: Speciation, Mapping --> n9
m1 = LCA[SE008_01000, SE007_01000]: Speciation, Mapping --> n1

The minimum reconciliation cost is: 4 (Duplications: 0, Transfers: 1, \
Losses: 1)
"""

riatahgt_output_hgt = """
RIATAHGT speciesTree {geneTree}
species tree: (((((((SE001:2.1494877,SE010:1.08661)I2:3.7761166,SE008:0.86305\
436)I3:0.21024487,(SE006:0.56704221,SE009:0.5014676)I1:0.90294223)I4:0.205423\
23,SE005:3.0992506)I5:0.37145632,SE004:1.8129133)I6:0.72933621,SE003:1.737411\
)I7:0.24447835,(SE002:1.6606127,SE007:0.70000178)I0:1.6331374)I8:1.594016;
gene tree: (((((SE008:6.135849,(SE006:5.2329068,SE009:5.2329068)I1:0.9029422)\
:0.2054233,(SE005:3.1308178,(SE001:2.1494876,SE010:2.1494876)I2:0.9813302):3.\
2104545):0.3714563,SE004:6.7127286):0.7293362,SE003:7.4420648):0.2444784,(SE0\
02:6.0534057,SE007:6.0534057)I0:1.6331375):1.594016;
There are 1 component(s), which account(s) for 1 solution(s), each of size 1
-----------------------------------------------------------------------------\
------------------------
            Component I5:
            Subsolution1:
                SE005 -> I2

*****************************************************************************\
************************
Consensus network for this set of gene trees
(((((((SE001:2.1494877,SE010:1.08661)I2:3.7761166,SE008:0.86305436)I3:0.21024\
487,(SE006:0.56704221,SE009:0.5014676)I1:0.90294223)I4:0.20542323,SE005:3\
.0992506)I5:0.37145632,SE004:1.8129133)I6:0.72933621,SE003:1.737411)I7:0.2444\
7835,(SE002:1.6606127,SE007:0.70000178)I0:1.6331374)I8:1.594016;
SE005 -> I2

"""

jane4_output_hgt = """Best Timing:
Time: 0 Node: Dummy Root
Time: 1 Node: 18 Name: 18`
Time: 2 Node: 14 Name: 14`
Time: 3 Node: 12 Name: 12`
Time: 4 Node: 10 Name: 10`
Time: 5 Node: 8 Name: 8`
Time: 6 Node: 17 Name: 17`
Time: 7 Node: 4 Name: 4`
Time: 8 Node: 2 Name: 2`
Time: 9 Node: 7 Name: 7`
Time: 10 Node: SE001
Time: 10 Node: SE010
Time: 10 Node: SE008
Time: 10 Node: SE006
Time: 10 Node: SE009
Time: 10 Node: SE005
Time: 10 Node: SE004
Time: 10 Node: SE003
Time: 10 Node: SE002
Time: 10 Node: SE007
Host Tree:
Number of nodes: 19, Number of tips: 10
(2) -> 0; Name: SE001 --> (-1) (-1);
(2) -> 1; Name: SE010 --> (-1) (-1);
(4) -> 2; Name: 2` --> (0) (1);
(4) -> 3; Name: SE008 --> (-1) (-1);
(8) -> 4; Name: 4` --> (2) (3);
(7) -> 5; Name: SE006 --> (-1) (-1);
(7) -> 6; Name: SE009 --> (-1) (-1);
(8) -> 7; Name: 7` --> (5) (6);
(10) -> 8; Name: 8` --> (4) (7);
(10) -> 9; Name: SE005 --> (-1) (-1);
(12) -> 10; Name: 10` --> (8) (9);
(12) -> 11; Name: SE004 --> (-1) (-1);
(14) -> 12; Name: 12` --> (10) (11);
(14) -> 13; Name: SE003 --> (-1) (-1);
(18) -> 14; Name: 14` --> (12) (13);
(17) -> 15; Name: SE002 --> (-1) (-1);
(17) -> 16; Name: SE007 --> (-1) (-1);
(18) -> 17; Name: 17` --> (15) (16);
(-1) -> 18; Name: 18` --> (14) (17);
Parasite Tree:
Number of nodes: 19, Number of tips: 10
(4) -> 0; Name: SE008_01000 --> (-1) (-1);
(3) -> 1; Name: SE006_01000 --> (-1) (-1);
(3) -> 2; Name: SE009_01000 --> (-1) (-1);
(4) -> 3; Name: 3` --> (1) (2);
(10) -> 4; Name: 4` --> (0) (3);
(9) -> 5; Name: SE005_01000 --> (-1) (-1);
(8) -> 6; Name: SE001_04150 --> (-1) (-1);
(8) -> 7; Name: SE010_04150 --> (-1) (-1);
(9) -> 8; Name: 8` --> (6) (7);
(10) -> 9; Name: 9` --> (5) (8);
(12) -> 10; Name: 10` --> (4) (9);
(12) -> 11; Name: SE004_01000 --> (-1) (-1);
(14) -> 12; Name: 12` --> (10) (11);
(14) -> 13; Name: SE003_01000 --> (-1) (-1);
(18) -> 14; Name: 14` --> (12) (13);
(17) -> 15; Name: SE002_01000 --> (-1) (-1);
(17) -> 16; Name: SE007_01000 --> (-1) (-1);
(18) -> 17; Name: 17` --> (15) (16);
(-1) -> 18; Name: 18` --> (14) (17);

Best Solution:
==================================
Parasite Node: SE008_01000
Association type: Tip
Host: SE008
Event Time: 10
Subtree Cost: 0
--------------------------
Parasite Node: SE006_01000
Association type: Tip
Host: SE006
Event Time: 10
Subtree Cost: 0
--------------------------
Parasite Node: SE009_01000
Association type: Tip
Host: SE009
Event Time: 10
Subtree Cost: 0
--------------------------
Parasite Node: 3`
Association type: Cospeciation
Host: 7`
Event Time: 9
Subtree Cost: 0
--------------------------
Parasite Node: 4`
Association type: Cospeciation
Host: 8`
Event Time: 5
Subtree Cost: 2
--------------------------
Parasite Node: SE005_01000
Association type: Tip
Host: SE005
Event Time: 10
Subtree Cost: 0
--------------------------
Parasite Node: SE001_04150
Association type: Tip
Host: SE001
Event Time: 10
Subtree Cost: 0
--------------------------
Parasite Node: SE010_04150
Association type: Tip
Host: SE010
Event Time: 10
Subtree Cost: 0
--------------------------
Parasite Node: 8`
Association type: Cospeciation
Host: 2`
Event Time: 8
Subtree Cost: 0
--------------------------
Parasite Node: 9`
Association type: Host Switch
Host: (10`, SE005)
Switch Target: (4`, 2`)
Event Time: 8
Subtree Cost: 3
--------------------------
Parasite Node: 10`
Association type: Cospeciation
Host: 10`
Event Time: 4
Subtree Cost: 5
--------------------------
Parasite Node: SE004_01000
Association type: Tip
Host: SE004
Event Time: 10
Subtree Cost: 0
--------------------------
Parasite Node: 12`
Association type: Cospeciation
Host: 12`
Event Time: 3
Subtree Cost: 5
--------------------------
Parasite Node: SE003_01000
Association type: Tip
Host: SE003
Event Time: 10
Subtree Cost: 0
--------------------------
Parasite Node: 14`
Association type: Cospeciation
Host: 14`
Event Time: 2
Subtree Cost: 5
--------------------------
Parasite Node: SE002_01000
Association type: Tip
Host: SE002
Event Time: 10
Subtree Cost: 0
--------------------------
Parasite Node: SE007_01000
Association type: Tip
Host: SE007
Event Time: 10
Subtree Cost: 0
--------------------------
Parasite Node: 17`
Association type: Cospeciation
Host: 17`
Event Time: 6
Subtree Cost: 0
--------------------------
Parasite Node: 18`
Association type: Cospeciation
Host: 18`
Event Time: 1
Subtree Cost: 5
Cost Before Parasite Root: 0
--------------------------
Cospeciation: 8
Duplication: 0
Host Switch: 1
Loss: 1
Failure to Diverge: 0

"""

consel_output_hgt = """
# reading /home/evko1434/hgt-detection/datasets/simulated/alf_simulations/det\
ect_hgts/input_tree.nwk_puzzle.pv
# rank item    obs     au     np |     bp     pp     kh     sh    wkh    wsh |
#    1    2  -12.2  0.988  0.957 |  0.955  1.000  0.927  0.927  0.927  0.927 |
#    2    1   12.2  0.012  0.043 |  0.045  5e-06  0.073  0.073  0.073  0.073 |

"""

hgtector_output_hgt = """
HGTector result of id
Query	Length	Product	Hits	Self	Close	Distal	HGT	Hit	E-value	Ident\
ity	Coverage	TaxID	Organism	Lineage
WP_011672393.1	252		414	1.52	0.53	108.57		WP_011069951	7.7e-\
38	36.5	98.02	36870	Wigglesworthia glossinidia	Proteobacteria;Gammap\
roteobacteria;Enterobacteriales;Enterobacteriaceae;Wigglesworthia;Wiggleswort\
hia glossinidia
WP_011672274.1	530		502	1.87	34.33	316.29		WP_035473704	2.5e-\
208	67.7	99.81	1492922	Gammaproteobacteria bacterium MFB021	Proteobac\
teria;Gammaproteobacteria;Gammaproteobacteria bacterium MFB021
WP_011672320.1	97		1	1.00	0.00	0.00\t\t
WP_011672350.1	554		502	1.64	16.08	159.98		WP_028305369	6.7e-\
119	42.3	96.57	1122617	Oceanospirillum maris	Proteobacteria;Gammaprote\
obacteria;Oceanospirillales;Oceanospirillaceae;Oceanospirillum;Oceanospirillu\
m maris
WP_011672309.1	178		2	1.62	0.00	0.00\t\t
WP_011672248.1	700		487	1.50	0.00	118.70	1	WP_011672421	4.1e-\
113	37.5	99.14	372461	Buchnera aphidicola	Proteobacteria;Gammaproteobac\
teria;Enterobacteriales;Enterobacteriaceae;Buchnera;Buchnera aphidicola
WP_045117922.1	455		502	1.75	0.41	198.03		WP_025368665	1.4e-\
109	45.2	99.34	1009858	Buchnera aphidicola	Proteobacteria;Gammaproteobac\
teria;Enterobacteriales;Enterobacteriaceae;Buchnera;Buchnera aphidicola
WP_011672298.1	425		3	1.55	0.00	0.14		WP_011672587	1.5e-\
22	31.5	82.35	372461	Buchnera aphidicola	Proteobacteria;Gammaproteobac\
teria;Enterobacteriales;Enterobacteriaceae;Buchnera;Buchnera aphidicola
WP_045117937.1	146		247	1.63	0.00	91.28	1	WP_012995888	1.9e-\
25	42.6	93.84	580331	Thermoanaerobacter italicus	Firmicutes;Clostridia\
;Thermoanaerobacterales;Thermoanaerobacteraceae;Thermoanaerobacter;Thermoanae\
robacter italicus
WP_011672284.1	151		2	1.59	0.00	0.00\t\t
WP_011672324.1	332		2	1.40	0.00	0.00\t\t
WP_011672384.1	1292		502	1.60	10.70	141.55		WP_011672422	1\
.9e-233	37.4	98.84	372461	Buchnera aphidicola	Proteobacteria;Gammaprote\
obacteria;Enterobacteriales;Enterobacteriaceae;Buchnera;Buchnera aphidicola
WP_045117931.1	337		502	1.78	14.57	234.72		WP_012674255	2.3e-\
93	51.6	100.00	204536	Sulfurihydrogenibium azorense	Aquificae;Aquific\
ae;Aquificales;Hydrogenothermaceae;Sulfurihydrogenibium;Sulfurihydrogenibium \
azorense
WP_011672391.1	171		3	1.74	0.32	0.00\t\t
WP_011672351.1	204		11	1.55	0.26	2.12		WP_053469245	1.5e-\
23	36.4	95.59	1560217	Clostridium sp. L74	Firmicutes;Clostridia;Clostri\
diales;Clostridiaceae;Clostridium;Clostridium sp. L74
WP_011672228.1	151		2	1.39	0.00	0.00\t\t
WP_045117927.1	223		502	1.66	6.42	207.82		WP_041063045	7.0e-\
51	49.1	98.65	1410383	Candidatus Tachikawaea gelatinosa	Proteobacteri\
a;Gammaproteobacteria;Enterobacteriales;Enterobacteriaceae;Candidatus Tachika\
waea;Candidatus Tachikawaea gelatinosa
WP_011672400.1	398		266	1.61	0.27	66.29		WP_014953873	2.4e-\
65	40.7	97.99	859653	alpha proteobacterium HIMB5	Proteobacteria;Alphap\
roteobacteria;Pelagibacterales;Pelagibacteraceae;alpha proteobacterium HIMB5
WP_011672275.1	97		2	1.60	0.00	0.00\t\t
"""

darkhorse_output_hgt = """query_id\tnonself_matches\tcandidate_matches\tbesth\
it_id\traw_LPI\tnorm_LPI\tpct_id\tquery_len\talign_len\tpct_coverage\tev\
alue\tbitscore\ttax_id\tspecies\tlineage\tquery_annotation\tbesthit_annotat\
ion
G2311_SE001,\t8\t6\tgi|557307555|ref|YP_008766893.1|\t0.002\t0.002\t67.4\t46\
\t46\t100\t9.3e-10\t70\t1407493\tShigella phage SfIV\tViruses;Caudovir\
ales;Myoviridae\tsequence type: type1, locus: 2310\texcisionase [Shigella pha\
ge SfIV]
G1250_SE001,\t501\t32\tgi|9630468|ref|NP_046899.1|\t0.002\t0.002\t79.4\t530\
\t530\t100\t4.5e-249\t868\t40631\tEnterobacteria phage N15\tViruses;Caudov\
irales;Siphoviridae;N15likevirus\tsequence type: type1, locus: 1249\tgp4 [En\
terobacteria phage N15]
G1252_SE001,\t494\t10\tgi|428782382|ref|YP_007112139.1|\t0.002\t0.003\t88.2\
\t110\t110\t100\t1.0e-46\t194\t1147144\tEnterobacteria phage HK225\tViruse\
s;Caudovirales;Siphoviridae;Lambdalikevirus\tsequence type: type1, locus: 125\
1\thead decoration protein D [Enterobacteria phage HK225]
G1251_SE001,\t499\t12\tgi|428782381|ref|YP_007112138.1|\t0.002\t0.003\t94.9\t\
447\t447\t100\t8.5e-233\t814\t1147144\tEnterobacteria phage HK225\tViruses;Ca\
udovirales;Siphoviridae;Lambdalikevirus\tsequence type: type1, locus: 1250\t\
head maturation protease C [Enterobacteria phage HK225]
G3193_SE001,\t483\t304\tgi|696545845|ref|WP_033078695.1|\t0.745\t0.775\t80.6\
\t124\t124\t100\t1.4e-52\t213\t1535422\tThalassotalea sp. ND16A\tBacteria;\
Proteobacteria;Gammaproteobacteria;Alteromonadales;Colwelliaceae;Thalassotale\
a\tsequence type: type1, locus: 3192\t30S ribosomal protein S12 [Thalassotale\
a sp. ND16A]gi|694336737|gb|KGJ89822.1|
G2940_SE001,\t486\t94\tgi|696545934|ref|WP_033078779.1|\t0.745\t0.775\t84.5\
\t71\t71\t100\t3.8e-26\t125\t1535422\tThalassotalea sp. ND16A\tBacteria;Pr\
oteobacteria;Gammaproteobacteria;Alteromonadales;Colwelliaceae;Thalassotalea\t\
sequence type: type1, locus: 2939\t30S ribosomal protein S21 [Thalassotalea s\
p. ND16A]gi|694336159|gb|KGJ89275.1|
G1709_SE001,\t497\t208\tgi|696543685|ref|WP_033076612.1|\t0.745\t0.775\t86.3\
\t118\t117\t99\t8.1e-50\t204\t1535422\tThalassotalea sp. ND16A\tBacteria;P\
roteobacteria;Gammaproteobacteria;Alteromonadales;Colwelliaceae;Thalassotale\
a\tsequence type: type1, locus: 1708\t50S ribosomal protein L20 [Thalassotale\
a sp. ND16A]gi|694347050|gb|KGJ99640.1|
G3168_SE001,\t489\t101\tgi|696545255|ref|WP_033078130.1|\t0.745\t0.775\t68.5\
\t92\t92\t100\t4.3e-30\t138\t1535422\tThalassotalea sp. ND16A\tBacteria;Pr\
oteobacteria;Gammaproteobacteria;Alteromonadales;Colwelliaceae;Thalassotale\
a\tsequence type: type1, locus: 3167\t30S ribosomal protein S19 [Thalassotale\
a sp. ND16A]gi|694340362|gb|KGJ93291.1|
"""

if __name__ == '__main__':
    main()
