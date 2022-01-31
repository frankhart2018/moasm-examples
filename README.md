# MoASM Examples

This repository has a two important uses:

1. It provides valid code examples of programs that MoASM assembler can run successfully.
2. It provides a test suite which tests the MoASM assembler for correctness, by checking the output of the examples with their expected outputs.

## Running testcases

1. Using pytest:

```bash
user@programmer~:$ pytest tests/* -s
```

2. Using unittest module:

```bash
user@programmer~:$ python tests/code_tests.py
```