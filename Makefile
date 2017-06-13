include ../include/Makefile.version

ARCH := $(shell echo $$(uname -m))

all: rpms

cleandist:
	rm -rf dist
	mkdir dist

version:
	echo 'VERSION = "$(VERSION)"' > iml_common/scm_version.py
	echo 'PACKAGE_VERSION = "$(PACKAGE_VERSION)"' >> iml_common/scm_version.py
	echo 'BUILD = "$(BUILD_NUMBER)"' >> iml_common/scm_version.py
	echo 'IS_RELEASE = $(IS_RELEASE)' >> iml_common/scm_version.py

develop: version
	python setup.py develop

tarball: version
	rm -f MANIFEST
	python setup.py sdist

rpms: cleandist tarball
	rm -rf _topdir
	mkdir -p _topdir/{BUILD,S{PEC,OURCE,RPM}S,RPMS/$(ARCH)}
	cp dist/iml-common-$(PACKAGE_VERSION).tar.gz _topdir/SOURCES
	cp iml-common.spec _topdir/SPECS
	dist=$$(rpm --eval %dist);                             \
	dist=$${dist/.centos/};                                \
	rpmbuild --define "_topdir $$(pwd)/_topdir" 		   \
		--define "version $(PACKAGE_VERSION)" 		  \
		--define "package_release $(PACKAGE_RELEASE)" \
		--define "%dist $$dist"                       \
		-bb _topdir/SPECS/iml-common.spec
	mv _topdir/RPMS/$(ARCH)/iml-common-*$(PACKAGE_VERSION)-$(PACKAGE_RELEASE)$$(rpm --eval %{dist} | sed -e 's/\(\.el[0-9][0-9]*\)\.centos/\1/').$(ARCH).rpm dist/
	rm -rf _topdir

docs download:
	@echo "Nothing to do here"
