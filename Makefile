.PHONY: clean

FLAGS=-O3 -Wall -Wpedantic -march=native -std=c++11

ALL=demo1\
    demo2\
    demo3\
    demo4\
    demo5\
    demo6\
    demo7\
    demo8

DEPS=lib/*.py
DEPS_TEST=test.py $(DEPS)

run: $(ALL)
	./demo1
	./demo2
	./demo3
	./demo4
	./demo5
	./demo6
	./demo7
	./demo8

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

demo6: demo6.cpp
	$(CXX) $(FLAGS) $< -o $@

demo7: demo7.cpp
	$(CXX) $(FLAGS) $< -o $@

demo8: demo8.cpp
	$(CXX) $(FLAGS) $< -o $@

demo1.cpp: $(DEPS_TEST)
	python test.py AllNibblesDifferent 0x20 0x31 0x42 0x53 0x64 0x75 0x86 0x97 0xa8 0xb9 0xca > /tmp/$@
	mv /tmp/$@ $@

demo2.cpp: $(DEPS_TEST)
	python test.py SomeNibblesRepeated 0x10 0x20 0x30 0x11 0x21 0x22 0x12 > /tmp/$@
	mv /tmp/$@ $@

demo3.cpp: $(DEPS_TEST)
	python test.py Naive 0x10 0x20 0x30 0x40 0x50 0x60 0x70 0x80 0x90 0x11 0x22 0x33 0x44 0x55 0x66 > /tmp/$@
	mv /tmp/$@ $@

demo4.cpp: $(DEPS_TEST)
	python test.py LowerNibbleConst 0x1c 0x2c 0x3c 0x4c 0x5c 0x6c 0x7c 0x8c 0x9c 0xac 0xbc 0xdc > /tmp/$@
	mv /tmp/$@ $@

demo5.cpp: $(DEPS_TEST)
	python test.py HigherNibbleConst 0x31 0x32 0x33 0x34 0x35 0x36 0x37 0x38 0x39 0x3a 0x3b 0x3d 0x3f > /tmp/$@
	mv /tmp/$@ $@

demo6.cpp: $(DEPS_TEST)
	python test.py Range 0x30 0x31 0x32 0x33 0x34 0x35 0x36 0x37 0x38 0x39 0x3a 0x3b 0x3c 0x3d 0x3e > /tmp/$@
	mv /tmp/$@ $@

demo7.cpp: $(DEPS_TEST)
	python test.py Universal 0x30 0x31 0x32 0x33 0x34 0x35 0x36 0x37 0x38 0x39 0x3a 0x3b 0x3c 0x3d 0x3e 0xff 0x14 0x7a 0x45 0x00 0x9d > /tmp/$@
	mv /tmp/$@ $@

demo8.cpp: $(DEPS_TEST)
	python test.py Universal2 0x30 0x31 0x32 0x33 0x34 0x35 0x36 0x37 0x38 0x39 0x3a 0x3b 0x3c 0x3d 0x3e 0xff 0x14 0x7a 0x45 0x00 0x9d > /tmp/$@
	mv /tmp/$@ $@

clean:
	$(RM) demo*

