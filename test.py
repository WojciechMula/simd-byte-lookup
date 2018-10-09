import sys
from lib.generate import generate

TEST_PROGRAM = """
// Program generated automatically
#include <immintrin.h>
#include <cstdint>
#include <cstdlib>
#include <cstdio>

// %(VALUES_LIST)s
static bool expected_value[256] = {%(EXPECTED_LIST)s};

%(FUNCTION_BODY)s

bool test() {
    for (int i=0; i < 256; i++) {
        const __m128i in  = _mm_set1_epi8(i);
        const __m128i ret = %(FUNCTION_NAME)s(in);
        const int ret0 = _mm_extract_epi8(ret, 0);

        if (bool(ret0) != expected_value[i]) {
            printf("Failed for #%%d\\n", i);
            return false;
        }
    }

    puts("All OK");
    return true;
}


int main() {
    return test() ? EXIT_SUCCESS : EXIT_FAILURE;
}

"""

def print_program(generator_name, values):
 
    function = generate(generator_name, values, 'in_set')
    if function is None:
        raise ValueError("Don't know how to build lookup for values %s" % values)


    expected_list = ['false'] * 256
    for x in values:
        expected_list[x] = 'true'

    params = {
        'VALUES_LIST'       : ', '.join(map(str, values)),
        'EXPECTED_LIST'     : ', '.join(expected_list),
        'FUNCTION_NAME'     : function.function_name,
        'FUNCTION_BODY'     : str(function),
    }

    print TEST_PROGRAM % params


def main():
    args = sys.argv[1:]
    generator_name = args[0]
    values = [int(arg, 16) for arg in args[1:]]
    print_program(generator_name, values)


if __name__ == '__main__':
    main()

