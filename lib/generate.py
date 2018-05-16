from AllNibblesDifferent import *
from SomeNibblesRepeated import *
from Naive import *

all_classes = [
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
        l.append('__m128i %s(const __m128i in) {' % self.function_name)
        for line in self.code:
            l.append(indent + line + ';')
        l.append('}')

        self.image = '\n'.join(l)
    

def generate(function_name, values):
    
    for class_name in all_classes:
        generator = class_name(values)
        if not generator.can_generate():
            continue

        return FunctionListing(generator.name, function_name, generator.generate())

