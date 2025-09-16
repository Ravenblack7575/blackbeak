# **blackbeak**
Sequence data extraction from pdf documents

A collection of python scripts and notebooks for extraction of sequence data from pdf documents. 

### Impetus
Researchers are often searching and curating sequence data from journal papers for assay development, genomic analysis and other study objectives. It takes a lot of time and careful effort to extract them manually (copy-paste) which are prone to error and mislabelling. It would be useful to have a collection of scripts or script templates that would enable researchers to easily pull out the information and data into neat csv tables. The downstream uses for such data include machine learning workflows, and generative AI workflows.


## **Python Scripts**

## 1. extract_sequences_from_pdf.py

This script will extract oligo sequences (15-40 nucleotides) from pdf documents. It is meant to extract primer and probe sequences (their names and nucleotide sequences, and any modifications) from the document and output a json file and a csv file. (Output csv will contain the following fields: name,sequence,source,dye,quencher)

extract_sequences_from_pdf_moduleversion.py : use this version if you prefer to use it in a jupyter notebook. Copy and paste the code into a notebook cell, edit path and parameters where required.

Limitiations: The script is able to more effective pull out the sequences from tables than from main text bodies.

### Dependencies
Python (>3.11) is the coding language used. Dependencies include:
- pandas
- re
- pypdf2
- json
- pathlib

### About the patterns it captures

It should capture most oligo patterns, although it is likely to miss those sequences that lie in paragraphs or those broken due to line or page breaks. 

The other pattern it might miss are those sequences that are broken into groups of three bases. (e.g. AAA TCG GGG CCA...) I think that most papers do not have oligos in this format unless they were manually typed. The primers can be captured nicely, but probe sequences could get messy. 

Always check the sequences with the papers just to make sure. 

### Usage

Download your pdf into a working folder. Use the script to extract primer and probe sequences from all the documents in the folder.

Run: <code> python extract_sequences_from_pdf.py [folder containing pdf documents] </code>

<BR>
<BR>
<BR>
<BR>
<BR>


#### Plans

This will take some time as I'm still very new at this.

- simple RAG for extraction of sequences
- updated and improved scripts from Chopshop archive (extraction of reference numbers)
- simple RAG for extraction of methods

