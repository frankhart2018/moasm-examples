import os
import unittest
from typing import List
import glob

from moasm.pretokenizer.pretokenizer import PreTokenizer
from moasm.pretokenizer.pretoken import PreToken
from moasm.grouper.grouper import Grouper
from moasm.tokenizer.token import Token
from moasm.tokenizer.tokenizer import Tokenizer
from moasm.parser.node.node import Node
from moasm.parser.parser import Parser
from moasm.compiler.opcode import OpCode
from moasm.compiler.compiler import Compiler
from moasm.vm.vm import VM


class CodeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__OUT_FILE_NAME = "out"

    def __get_moasm_output(self, file_name):
        tokens: List[PreToken] = PreTokenizer(source_file_path=file_name).tokenize()
        groups: List[List[str]] = Grouper(tokens=tokens).group()
        tokens: List[Token] = Tokenizer(groups=groups).tokenize(dump_late_groups=False, file_name="")
        ast_root: Node = Parser(tokens=tokens).parse()
        bytecode: List[OpCode] = Compiler(ast_root=ast_root).compile()
        vm: VM = VM(opcodes=bytecode)
        vm.run(out_file=self.__OUT_FILE_NAME)

    def __read_file_contents(self, file_path) -> str:
        with open(file_path, "r") as f:
            return f.read()

    def __compare_outputs(self, output_file_path) -> bool:
        return self.__read_file_contents(output_file_path) == self.__read_file_contents(self.__OUT_FILE_NAME)

    def __get_moasm_example_paths(self) -> List[str]:
        return glob.glob(os.path.join("examples", "*.moasm"))

    def test_moasm(self):
        file_paths: List[str] = self.__get_moasm_example_paths()
        print()
        test_failed = 0
        for i, file_name in enumerate(file_paths):
            print(f"\u231B Running {file_name}!")
            output_file_name = ".".join(os.path.basename(file_name).split(".")[:-1])
            output_file_path = os.path.join("outputs", output_file_name)
            self.__get_moasm_output(file_name)
            is_output_same: bool = self.__compare_outputs(output_file_path=output_file_path)

            if is_output_same:
                print(f"\u2705 [{i+1}/{len(file_paths)}] - {file_name}")
            else:
                test_failed += 1
                print(f"\u274C [{i+1}/{len(file_paths)}] - {file_name}")

        if os.path.exists(self.__OUT_FILE_NAME):
            os.remove(self.__OUT_FILE_NAME)

        if test_failed > 0:
            self.fail()


if __name__ == "__main__":
    unittest.main()