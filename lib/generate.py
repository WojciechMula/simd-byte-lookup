from AllNibblesDifferent import *
from SomeNibblesRepeated import *
from LowerNibbleConst import *
from HigherNibbleConst import *
from Naive import *
from Range import *
from Universal import *
from builder import make_builder
from sse_writer import SSEWriter

all_classes = {
    'LowerNibbleConst'      : LowerNibbleConst,
    'HigherNibbleConst'     : HigherNibbleConst,
    'AllNibblesDifferent'   : AllNibblesDifferent,
    'SomeNibblesRepeated'   : SomeNibblesRepeated,
    'Naive'                 : Naive,
    'Range'                 : Range,
    'Universal'             : Universal,
    'Universal2'            : Universal2,
}

class FunctionListing(object):
    def __init__(self, generator_name, function_name, writer):
        self.generator_name = generator_name
        self.function_name  = function_name
        self.type_name      = writer.get_type_name()
        self.code           = writer.write()
        self.__render()

    def __str__(self):
        return self.image

    
    def __render(self):
        indent = ' ' * 4
        l = []
        l.append('// %s' % self.generator_name)
        l.append('%s %s(const %s input) {' % (self.type_name, self.function_name, self.type_name))
        for line in self.code:
            l.append(indent + line + ';')
        l.append('}')

        self.image = '\n'.join(l)


def get_generator(generator_name, values):
    try:
        class_name = all_classes[generator_name]
    except KeyError:
        names = ', '.join(sorted(list(all_classes.iterkeys())))
        raise ValueError("Invalid generator name, valid names are: %s" % (names))

    generator = class_name(values)
    if not generator.can_generate():
        raise ValueError("Selected generator can't handle given values")
    
    return generator


def generate(generator_name, values, function_name):

    builder = make_builder()
    generator = get_generator(generator_name, values)
    generator.generate(builder)
    writer = SSEWriter(builder)
    return FunctionListing(generator.name, function_name, writer)

