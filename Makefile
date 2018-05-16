.PHONY: clean

FLAGS=-O3 -Wall -Wpedantic -march=native -std=c++11

ALL=demo1\
    demo2

DEPS=test.py lib/*.py

run: $(ALL)
	./demo1
	./demo2

demo1: demo1.cpp
	$(CXX) $(FLAGS) $< -o $@

demo2: demo2.cpp
	$(CXX) $(FLAGS) $< -o $@

demo1.cpp: $(DEPS)
	# all nibbles (lower & higer) are different
	python test.py 0x20 0x31 0x42 0x53 0x64 0x75 0x86 0x97 0xa8 0xb9 0xca > /tmp/$@
	mv /tmp/$@ $@

demo2.cpp: $(DEPS)
	# some nibbles are repeated
	python test.py 0x10 0x20 0x30 0x11 0x21 0x22 0x12 > /tmp/$@
	mv /tmp/$@ $@

clean:
	$(RM) demo*

