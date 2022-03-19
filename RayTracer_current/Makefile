CXX=g++
CXXFLAGS=-g -std=c++11 -Wall

all: simpleRaycast
clean:
	rm -f *.o *.h.gch simpleRaycast raycast.ppm
test: simpleRaycast
	./simpleRaycast
.PHONY: all clean test

simpleRaycast: simpleRaycast.o
	$(CXX) $(LDFLAGS) -o $(@) $(^)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c -o $(@) $(<)