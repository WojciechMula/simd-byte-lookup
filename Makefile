.PHONY: clean

FLAGS=-O3 -Wall -Wpedantic -march=native -std=c++11

ALL=demo1\
    demo2\
    demo3\
    demo4\
    demo5\
    test_compiler

DEPS=lib/*.py
DEPS_TEST=test.py $(DEPS)
DEPS_COMPILER=compiler.py $(DEPS)

run: $(ALL)
	./demo1
	./demo2
	./demo3
	./demo4
	./demo5

demo1: demo1.cpp
	$(CXX) $(FLAGS) $< -o $@

demo2: demo2.cpp
	$(CXX) $(FLAGS) $< -o $@

demo3: demo3.cpp
	$(CXX) $(FLAGS) $< -o $@

demo4: demo4.cpp
	$(CXX) $(FLAGS) $< -o $@

demo5: demo5.cpp
	$(CXX) $(FLAGS) $< -o $@

demo1.cpp: $(DEPS_TEST)
	# all nibbles (lower & higer) are different
	python test.py 0x20 0x31 0x42 0x53 0x64 0x75 0x86 0x97 0xa8 0xb9 0xca > /tmp/$@
	mv /tmp/$@ $@

demo2.cpp: $(DEPS_TEST)
	# some nibbles are repeated
	python test.py 0x10 0x20 0x30 0x11 0x21 0x22 0x12 > /tmp/$@
	mv /tmp/$@ $@

demo3.cpp: $(DEPS_TEST)
	# huge list
	python test.py 0x10 0x20 0x30 0x40 0x50 0x60 0x70 0x80 0x90 0x11 0x22 0x33 0x44 0x55 0x66 > /tmp/$@
	mv /tmp/$@ $@

demo4.cpp: $(DEPS_TEST)
	# lower nibbles const
	python test.py 0x1c 0x2c 0x3c 0x4c 0x5c 0x6c 0x7c 0x8c 0x9c 0xac 0xbc 0xdc > /tmp/$@
	mv /tmp/$@ $@

demo5.cpp: $(DEPS_TEST)
	# higher nibbles const
	python test.py 0x31 0x32 0x33 0x34 0x35 0x36 0x37 0x38 0x39 0x3a 0x3b 0x3d 0x3f > /tmp/$@
	mv /tmp/$@ $@

test_compiler: $(DEPS_COMPILER)
	python compiler.py --string=abcdeghijlmnop012346789/+-

clean:
	$(RM) demo*

