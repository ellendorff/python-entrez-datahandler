#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Class for handling entrez python download data files for pubmed abstracts.
Author: Tilia Ellendorff
Version: March 2015

"""
#from __future__ import division
#from __future__ import unicode_literals
from optparse import OptionParser
import xml.etree.cElementTree as ET
import codecs
import sys
import cPickle as pickle
import os
from Bio import Entrez
import codecs
#import shutil
#import random
#import nltk
#import collections
#import nltk.metrics
#from nltk import word_tokenize, wordpunct_tokenize

# Prevent Encoding exceptions in Python 2.x
sys.stdout = codecs.getwriter('utf-8')(sys.__stdout__)
sys.stderr = codecs.getwriter('utf-8')(sys.__stderr__)
sys.stdin = codecs.getreader('utf-8')(sys.__stdin__)


class Pubmed_dump_file(object):
    '''Pubmed_dump_file is a file loaded as pickle file from a pubmed dump in biopython format. The functions can be used to get specific information out like abstract text, title or mesh terms out of the Pubmed_dump_file.'''

    def __init__(self, pmid, dump_dir, entrez_email = None, options=None, args=None):
        self.pmid = pmid
        self.path = dump_dir + pmid
        self.dump_dir = dump_dir

        #print os.listdir(self.dump_dir)

        if not self.pmid in os.listdir(self.dump_dir):
            print 'ATTEMPT TO DOWNLOAD DATA FOR', self.pmid
            self.download_pmid_data(entrez_email, options=options, args=args)

        try:
            self.file = open(self.path, 'rb')
            self.text = pickle.load(self.file)

        except (IOError, EOFError, AttributeError):
            print 'ERROR, NO DATA FOR', self.pmid
            return None


    def download_pmid_data(self, entrez_email, options=None, args=None):

        if entrez_email == None:
            print 'DOWNLOAD OF NEW DATA CANNOT BE COMPLETED, PLEASE GIVE YOUR EMAIL.'
            return None

        Entrez.email = entrez_email
        print 'THE DATA FOR PUBMED-ID', self.pmid, 'WILL BE DOWNLOADED'

        handle = Entrez.efetch(db="pubmed", id=self.pmid, retmode="xml")
        record = Entrez.read(handle)

        download_file = open(self.path, 'w')
        pickle.dump(record, download_file)
        download_file.close()



    def get_data(self, options=None, args=None):
        try:
            return self.text[0]
        except (IndexError, KeyError):
            print pmid, 'no text_dict found', self.text

    def get_abstract(self, options=None, args=None):
        try:
            text_dict = self.text[0]
            abstract = text_dict[u'MedlineCitation'][u'Article'][u'Abstract'][u'AbstractText']
            if len(abstract) == 1:
                return ' '.join(abstract)

            else:
                abstract_list = []
                for i in range(len(abstract)):
                    one_abstract_section = abstract[i]
                    one_abstract_section_string = unicode(abstract[i])
                    print one_abstract_section_string
                    one_abstract_section_attr = one_abstract_section.attributes
                    print one_abstract_section_attr
                    
                    try:
                        # Add abstract headings, such as BACKGROUND; make this optional?
                        
                        abstract_label = one_abstract_section_attr[u'Label']
                        new_abstract_section_string = abstract_label + ': ' + one_abstract_section_string
                        
                        # if not new_abstract_section_string.endswith(u'.'):
#                             new_abstract_section_string = new_abstract_section_string + u'.'
                            
                        print new_abstract_section_string
                        print '\n'
                        abstract_list.append(new_abstract_section_string)
                    except KeyError:
                        abstract_list.append(one_abstract_section_string)
                    
                #abstract_list = [unicode(abstract[i]) for i in range(len(abstract))]
           
                abstract_string = ' '.join(abstract_list)
                return abstract_string

        except (IndexError, KeyError, AttributeError):
            return None

    def get_title(self, options=None, args=None):
        try:
            text_dict = self.text[0]
            return unicode(text_dict[u'MedlineCitation'][u'Article'][u'ArticleTitle'])

        except (IndexError, KeyError, AttributeError):
            return None

    def get_mesh(self, options=None, args=None):
        try:
            text_dict = self.text[0]
            mesh_list = text_dict[u'MedlineCitation'][u'MeshHeadingList']
            descriptor_list = [unicode(mesh_list[i][u'DescriptorName']) for i in range(len(mesh_list))]
            #print descriptor_list
            descriptor_dict = dict((n, descriptor_list[n]) for n in range(len(descriptor_list)))
            #for k, v in sorted(descriptor_dict.items()):
            #    print k,v
            qualifier_list = dict((i, [unicode(item) for item in mesh_list[i][u'QualifierName']]) for i in range(len(mesh_list)))
            #print self.pmid
            #for number, qualifier in qualifier_list.items():
            #    print number,  qualifier
        except (IndexError, KeyError):
            return None

    def get_mesh_descriptors(self, options=None, args=None):
        try:
            text_dict = self.text[0]
            mesh_list = text_dict[u'MedlineCitation'][u'MeshHeadingList']
            descriptor_list = [unicode(mesh_list[i][u'DescriptorName']) for i in range(len(mesh_list))]
            return '; '.join(descriptor_list)
        except (IndexError, KeyError):
            return None


    def get_mesh_qualifiers(self, options=None, args=None):
        try:
            text_dict = self.text[0]
            mesh_list = text_dict[u'MedlineCitation'][u'MeshHeadingList']
            #qualifier_list = list(set(sum([one_value for one_value in dict((i, [unicode(item) for item in mesh_list[i][u'QualifierName']]) for i in range(len(mesh_list))).values()], [])))
            qualifier_list = list(set(sum([[unicode(item) for item in mesh_list[i][u'QualifierName']] for i in range(len(mesh_list))], [])))
            return '; '.join(qualifier_list)
        except (IndexError, KeyError):
            return None


    def get_whole_abstract(self, options=None, args=None):
        try:
            whole_abstract_list = []
            whole_abstract_list.append(self.pmid + '. ')
            whole_abstract_list.append(self.get_title())
            whole_abstract_list.append(self.get_abstract())

            if not self.get_mesh_descriptors() == None:
                whole_abstract_list.append(self.get_mesh_descriptors())

            return ' '.join(whole_abstract_list)

        except (IndexError, KeyError, TypeError):
            return None

    def get_abstract_minus_mesh(self, options=None, args=None):
        try:
            whole_abstract_list = []
            whole_abstract_list.append(self.pmid + '. ')
            whole_abstract_list.append(self.get_title())
            whole_abstract_list.append(self.get_abstract())

            return ' '.join(whole_abstract_list)

        except (IndexError, KeyError, TypeError):
            return None


