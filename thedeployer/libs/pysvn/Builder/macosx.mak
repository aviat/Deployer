build: all test kit

all:	../Source/Makefile
	cd ../Source && $(MAKE)

clean:	../Source/Makefile
	cd ../Source && $(MAKE) clean && rm Makefile
	cd ../Tests && $(MAKE)  clean

../Source/Makefile: ../Source/setup.py
	cd ../Source && $(PYTHON) setup.py configure $(CONFIG_ARGS)

kit:
	cd ../Kit/MacOSX && $(PYTHON) make_pkg.py

test:
	cd ../Tests && $(MAKE)  all
