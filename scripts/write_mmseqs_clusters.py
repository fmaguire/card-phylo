#!/usr/bin/env python

import os
import argparse
from Bio import SeqIO

def run():
    parser = argparse.ArgumentParser(description='Write mmseq sequence cluster files and dump singeltons.')
    parser.add_argument('cluster_fasta', type=str,
                    help="Path to MMSEQS2 easy-cluster fasta")
    parser.add_argument('output_folder', type=str,
                    help="Folder to output family sequences")
    args = parser.parse_args()

    cluster_seqs = []
    out_fh = None
    cluster = 0
    num_seqs = 0

    singleton_record = open(os.path.join(args.output_folder, 'singleton.txt'), 'w')
    for record in SeqIO.parse(args.cluster_fasta, 'fasta'):
        if len(record.seq) == 0:
            if out_fh:
                if num_seqs > 1:
                    SeqIO.write(cluster_seqs, out_fh, 'fasta')
                    cluster += 1
                else:
                    SeqIO.write(cluster_seqs, singleton_record, "fasta")
                    print(f"MMSEQS2 singleton: {cluster_seqs[0].id}")
                cluster_seqs = []
                num_seqs = 0
                out_fh.close()
            out_fh = open(os.path.join(args.output_folder, str(cluster) + ".fasta"), 'w')
        else:
            cluster_seqs.append(record)
            num_seqs += 1
    singleton_record.close()

if __name__ == '__main__':
    run()