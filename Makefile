include Makefile.local

VERSION        := $(shell git describe --tags | sed -e 's/^v//' -e 's/RC[0-9]*//' -e 's/-g.*//')
VERSION_PARTS  := $(subst ., ,$(VERSION))
VERSION_MAJOR  := $(word 1, $(VERSION_PARTS))
VERSION_MINOR  := $(word 2, $(VERSION_PARTS))
VERSION_BUGFIX := $(word 3, $(VERSION_PARTS))
VERSION_LOCAL1 := $(word 4, $(VERSION_PARTS))
VERSION_LOCAL2 := $(word 5, $(VERSION_PARTS))
RPM_TOPDIR     := $(shell rpm --eval %_topdir)
RPM_SOURCEDIR  := $(shell rpm --eval %_sourcedir)
RPM_RPMSDIR    := $(shell rpm --eval %_rpmdir)

rpm: $(RPM_RPMSDIR)/noarch/python2-iml-common-$(VERSION)-1.el7.centos.noarch.rpm

srpm: python-iml-common$(VERSION_MAJOR).$(VERSION_MINOR)-$(VERSION)-1.el7.centos.src.rpm

python-iml-common$(VERSION_MAJOR).$(VERSION_MINOR)-$(VERSION)-1.el7.centos.src.rpm: iml-common-$(VERSION).spec
	rpmbuild -bs --define %_srcrpmdir\ $$PWD --define %_sourcedir\ dist $<

spec: iml-common-$(VERSION).spec

dist: dist/iml-common-$(VERSION).tar.gz

version:
	@echo $(VERSION)

copr_rpm: python-iml-common$(VERSION_MAJOR).$(VERSION_MINOR)-$(VERSION)-1.el7.centos.src.rpm
	set -e;                                                    \
	if [ -z "$(COPR_OWNER)" -o                                 \
	     -z "$(COPR_PROJECT)" ]; then                          \
	    echo "ERROR:";                                         \
	    echo "COPR_OWNER and COPR_PROJECT need to be defined"; \
	    echo "You can add them to a Makefile.local";           \
	    exit 1;                                                \
	fi
	copr-cli build $(COPR_OWNER)/$(COPR_PROJECT) $<

$(RPM_RPMSDIR)/noarch/python2-iml-common-$(VERSION)-1.el7.centos.noarch.rpm: iml-common-$(VERSION).spec dist/iml-common-$(VERSION).tar.gz
	rpmbuild -bb --define %_sourcedir\ $$PWD/dist $<

iml-common-$(VERSION).spec: Makefile
	curl 'https://raw.githubusercontent.com/intel-hpdd/manager-for-lustre-dependencies/python-iml-common$(VERSION_MAJOR).$(VERSION_MINOR)-$(VERSION_MAJOR).$(VERSION_MINOR).$(VERSION_BUGFIX)-1/python-iml-common/python-iml-common.spec' | sed -e '/^%global patch/s/$$/.$(VERSION_LOCAL1).$(VERSION_LOCAL2)/' -e '/Source0:/s/^\(.*  *\).*/\1iml-common-%{version}.tar.gz/' > $@

dist/iml-common-$(VERSION).tar.gz:
	python setup.py sdist

clean:
	rm -rf dist iml-common-*.spec

tags:
	ctags -R .
