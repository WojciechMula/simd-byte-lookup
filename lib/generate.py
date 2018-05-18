from AllNibblesDifferent import *
from SomeNibblesRepeated import *
from LowerNibbleConst import *
from HigherNibbleConst import *
from Naive import *
from builder import make_builder
from sse_writer import SSEWriter

all_classes = [
    LowerNibbleConst,
    HigherNibbleConst,
    AllNibblesDifferent,
    SomeNibblesRepeated,
    Naive
]

class FunctionListing(object):
    def __init__(self, generator_name, function_name, code):
        self.generator_name = generator_name
        self.function_name  = function_name
        self.code = code
        self.__render()

    def __str__(self):
        return self.image

    
    def __render(self):
        indent = ' ' * 4
        l = []
        l.append('// %s' % self.generator_name)
        l.append('__m128i %s(const __m128i input) {' % self.function_name)
        for line in self.code:
            l.append(indent + line + ';')
        l.append('}')

        self.image = '\n'.join(l)


def get_generator(values, builder):
    for class_name in all_classes:
        generator = class_name(values, builder)
        if generator.can_generate():
            return generator


def generate(function_name, values):
 
    builder = make_builder()
    generator = get_generator(values, builder)
    generator.generate()
    writer = SSEWriter(builder)
    return FunctionListing(generator.name, function_name, writer.write())

