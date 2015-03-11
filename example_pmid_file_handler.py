#!/usr/bin/env python

"""
The following python libraries are needed:
OptionParser
codecs
cPickle
os
Bio
sys

"""


from pmid_file_handler import Pubmed_dump_file

pmid_file = Pubmed_dump_file('19', '../pmid_dump_data_storage/', entrez_email='xxxx@xxxx.xx')
# arguments: the PubmedID as a string, the directory of the data storage, an email necessary to download new data from Pubmed
# (E-mail is optional, but without it it is not possible to download new data but only previously downloaded data can be loaded)



text = pmid_file.text
# gives the (raw) download xml

abstract = pmid_file.get_abstract()
# gives the text of the abstract in unicode format

title = pmid_file.get_title()
# gives the title of the abstract in unicode format



mesh = pmid_file.get_mesh()
# gives the mesh descriptors and qualifiers for a pubmed article

mesh_qualifiers = pmid_file.get_mesh_qualifiers()
# only the mesh qualifiers

mesh_descriptors = pmid_file.get_mesh_descriptors()
# only the mesh descriptors



whole_abstract = get_whole_abstract()
# gives the whole abstract of the pubmed article



# COMMENT: IF ANY PART OF THE ABSTRACT IS MISSING, THESE FUNCTIONS RETURN None INSTEAD!


