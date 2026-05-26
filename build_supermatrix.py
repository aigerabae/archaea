#!/usr/bin/env python3
"""
Concatenate multiple FASTA alignment files into a supermatrix.

Usage:
  python build_supermatrix.py            # run normally
  python build_supermatrix.py --check    # diagnostic only, no output written

Produces:
  supermatrix.fa       — concatenated alignment in FASTA format
  partitions.txt       — RAxML-style partition file
  partitions_nexus.txt — NEXUS charset block (IQ-TREE / PartitionFinder)
"""

import os
import glob
import sys
from collections import OrderedDict

# ── Configuration ─────────────────────────────────────────────────────────────
INPUT_PATTERN = "no_spaces_aln_OG*.fa.fas"   # glob pattern for your files
OUTPUT_FASTA  = "supermatrix.fa"
OUTPUT_PARTS  = "partitions.txt"
OUTPUT_NEXUS  = "partitions_nexus.txt"
MISSING_CHAR  = "-"                           # gap fill for absent taxa

# How taxon names are extracted from FASTA headers.
# "full"  → entire header string after ">"   e.g. "Sp1|WP_12345"
# "pipe"  → part before first "|"            e.g. "Sp1"
# "space" → part before first space          e.g. "Sp1"
TAXON_NAME_MODE = "pipe"
# ─────────────────────────────────────────────────────────────────────────────


def extract_taxon(header, mode):
    h = header.strip()
    if mode == "pipe":
        return h.split("|")[0]
    elif mode == "space":
        return h.split()[0]
    else:
        return h


def parse_fasta(filepath, mode):
    seqs = OrderedDict()
    current = None
    with open(filepath) as fh:
        for line in fh:
            line = line.rstrip()
            if not line:
                continue
            if line.startswith(">"):
                current = extract_taxon(line[1:], mode)
                if current in seqs:
                    raise ValueError(f"Duplicate taxon '{current}' in {filepath}")
                seqs[current] = []
            else:
                if current is None:
                    raise ValueError(f"Sequence data before header in {filepath}")
                seqs[current].append(line)
    return {k: "".join(v) for k, v in seqs.items()}


def main():
    check_only = "--check" in sys.argv

    files = sorted(glob.glob(INPUT_PATTERN))
    if not files:
        sys.exit(f"No files matched pattern '{INPUT_PATTERN}' in {os.getcwd()}")

    print(f"Found {len(files)} alignment files.")
    print(f"Taxon name mode: '{TAXON_NAME_MODE}'\n")

    # ── Pass 1: parse all files ───────────────────────────────────────────────
    all_taxa  = OrderedDict()
    file_data = []
    skipped   = []

    for i, fp in enumerate(files, 1):
        try:
            seqs = parse_fasta(fp, TAXON_NAME_MODE)
        except Exception as e:
            print(f"  ERROR parsing {fp}: {e} — skipping")
            skipped.append(fp)
            continue

        lengths = {len(s) for s in seqs.values()}
        if len(lengths) != 1:
            print(f"  WARNING: {fp} has unequal sequence lengths {lengths} — skipping")
            skipped.append(fp)
            continue

        aln_len = lengths.pop()
        locus = os.path.basename(fp)
        for ext in (".fa.fas", ".fas", ".fa", ".fasta"):
            locus = locus.replace(ext, "")

        file_data.append((locus, seqs, aln_len))
        for taxon in seqs:
            all_taxa[taxon] = None

        if i % 50 == 0:
            print(f"  Parsed {i}/{len(files)} files …")

    all_taxa   = list(all_taxa.keys())
    total_taxa = len(all_taxa)
    total_len  = sum(d[2] for d in file_data)

    print(f"\n{'─'*50}")
    print(f"Loci parsed successfully : {len(file_data)}")
    print(f"Loci skipped             : {len(skipped)}")
    print(f"Total unique taxa        : {total_taxa}")
    print(f"Total alignment length   : {total_len:,} bp")
    print(f"{'─'*50}")

    # ── Diagnostic: show first 10 taxon names ────────────────────────────────
    print("\nFirst 10 taxon names (after extraction):")
    for t in all_taxa[:10]:
        print(f"  '{t}'")

    # ── Diagnostic: taxa coverage ─────────────────────────────────────────────
    taxon_counts = {t: 0 for t in all_taxa}
    for _, seqs, _ in file_data:
        for t in seqs:
            taxon_counts[t] += 1

    min_cov = min(taxon_counts.values())
    max_cov = max(taxon_counts.values())
    print(f"\nTaxon coverage across loci: min={min_cov}, max={max_cov} (out of {len(file_data)} loci)")
    if min_cov < len(file_data):
        missing_taxa = [t for t, c in taxon_counts.items() if c < len(file_data)]
        print(f"  {len(missing_taxa)} taxa missing from at least one locus (will be gap-filled)")

    # ── Locus length stats ────────────────────────────────────────────────────
    locus_lens = [d[2] for d in file_data]
    print(f"\nLocus lengths: min={min(locus_lens)}, max={max(locus_lens)}, "
          f"mean={sum(locus_lens)//len(locus_lens)}")

    if check_only:
        print("\n[--check mode] No output files written. Re-run without --check to build supermatrix.")
        return

    # ── Pass 2: concatenate ───────────────────────────────────────────────────
    print("\nConcatenating …")
    concat = {t: [] for t in all_taxa}
    partitions = []
    pos = 1

    for locus, seqs, aln_len in file_data:
        for taxon in all_taxa:
            concat[taxon].append(seqs[taxon] if taxon in seqs else MISSING_CHAR * aln_len)
        partitions.append((locus, pos, pos + aln_len - 1))
        pos += aln_len

    # ── Write supermatrix.fa ──────────────────────────────────────────────────
    with open(OUTPUT_FASTA, "w") as out:
        for taxon in all_taxa:
            out.write(f">{taxon}\n")
            seq = "".join(concat[taxon])
            for i in range(0, len(seq), 80):
                out.write(seq[i:i+80] + "\n")

    size_mb = os.path.getsize(OUTPUT_FASTA) / 1e6
    print(f"Wrote {OUTPUT_FASTA}  ({size_mb:.1f} MB)")

    # ── Write partition files ─────────────────────────────────────────────────
    with open(OUTPUT_PARTS, "w") as out:
        for locus, start, end in partitions:
            out.write(f"DNA, {locus} = {start}-{end}\n")
    print(f"Wrote {OUTPUT_PARTS}  (RAxML format)")

    with open(OUTPUT_NEXUS, "w") as out:
        out.write("#nexus\nbegin sets;\n")
        for locus, start, end in partitions:
            out.write(f"  charset {locus} = {start}-{end};\n")
        out.write("end;\n")
    print(f"Wrote {OUTPUT_NEXUS}  (NEXUS format)")

    # ── Sanity check ──────────────────────────────────────────────────────────
    seq_lengths = {len("".join(concat[t])) for t in all_taxa}
    assert seq_lengths == {total_len}, f"BUG: length mismatch! {seq_lengths}"
    print(f"\nSanity check passed — all {total_taxa} sequences are {total_len:,} bp.")
    print("Done.")


if __name__ == "__main__":
    main()
