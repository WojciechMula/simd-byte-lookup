
FLAGS=-O3 -Wall -Wpedantic -march=native -std=c++11

run: demo1
	./demo1

demo1: demo1.cpp
	$(CXX) $(FLAGS) $< -o $@

demo1.cpp: test.py lib/*.py
	# all nibbles (lower & higer) are different
	python test.py 0x20 0x31 0x42 0x53 0x64 0x75 0x86 0x97 0xa8 0xb9 0xca > $@

