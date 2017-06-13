__author__ = 'Guilherme Matsumoto'

from skmultiflow.data.FileStream import FileStream, FileOption
from skmultiflow.data.generators.RandomTreeGenerator import RandomTreeGenerator
from skmultiflow.data.generators.RandomRBFGeneratorDrift import RandomRBFGeneratorDrift
from skmultiflow.data.generators.RandomRBFGenerator import RandomRBFGenerator
from skmultiflow.data.generators.SEAGenerator import SEAGenerator
from skmultiflow.data.generators.WaveformGenerator import WaveformGenerator
from skmultiflow.evaluation.EvaluateStreamGenerationSpeed import EvaluateStreamGenerationSpeed


def demo():
    # Test with FileStream
    opt = FileOption("FILE", "OPT_NAME", "skmultiflow/datasets/covtype.csv", "CSV", False)
    stream = FileStream(opt, 7)
    stream.prepare_for_use()

    # Test with RandomTreeGenerator
    #opt_list = [['-c', '2'], ['-o', '0'], ['-u', '5'], ['-v', '4']]
    #stream = RandomTreeGenerator(opt_list)
    #stream.prepare_for_use()

    eval = EvaluateStreamGenerationSpeed(100000, float("inf"), None, 5)
    eval.eval(stream)