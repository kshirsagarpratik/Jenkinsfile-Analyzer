from pypeg2 import *


class Agent(str):
    grammar = "agent", word

class Instruction(str):
    grammar = name(), restline, endl

# class Script()
class Steps(List):
    grammar = "steps", "{", attr('commands',maybe_some(Instruction)), "}"

class Stage_Item(Namespace):
    grammar = "stage", "('", name(), "')", "{", attr("steps", some(Steps)), "}"

class Stages(List):
    grammar = "stages", "{", some(Stage_Item), "}"

class Pipeline(Namespace):
    grammar = "pipeline", maybe_some(whitespace), "{", attr("agent", Agent), attr("stages", Stages), "}"

