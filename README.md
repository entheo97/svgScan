# svg-scan

A proof-of-concept Bash script that detects malware hidden in base64-encoded comments inside SVG files.

## Background

In July 2026, Elastic Security Labs documented a Contagious Interview campaign (REF9403) in which attackers sent developers a fake coding challenge. The project hid its payload as base64 fragments in the comments of SVG flag images. Each file looked like an ordinary image, and the malware only appeared once the comments were pulled out and decoded.

Write-up: https://www.elastic.co/security-labs/contagious-interview-malware-svg-steganography

This script demonstrates the core idea of catching that technique with standard Linux tools: extract SVG comments, decode them and check the result against known-bad strings.

## How it works

For each `.svg` file in a directory, the script:

1. Extracts every XML comment with `grep -Pzo`
2. Strips the comment delimiters with `sed`
3. Removes all whitespace with `tr -d`
4. Checks that what is left is valid base64 and decodes it with `base64 -d`
5. Writes the decoded text to `decoded_output.txt`
6. Compares the decoded text against `malicious.txt` with `grep -F -f` and reports matches per file

Each stage does one small job and the pipe passes the result to the next. Together they reproduce the attacker's extraction and decoding steps, with a comparison against known-bad strings at the end.

## The indicator list

`malicious.txt` comes from SecLists, an open-source collection of security-testing wordlists. It contains strings for finding backdoor shells, rootkits, botnets and exploitable functions. Matching is literal and case-sensitive, and blank lines in the list are ignored. The list also contains a few `#` comment lines and a stray line of backticks, which are read as patterns like any other line but rarely matter.

## Requirements

- Bash 4 or newer
