include Makefile.local

VERSION       := $(shell git describe --tags | sed -e 's/^v//' -e 's/RC[0-9]*//')
RPM_TOPDIR    := $(shell rpm --eval %_topdir)
RPM_SOURCEDIR := $(shell rpm --eval %_sourcedir)
RPM_RPMSDIR   := $(shell rpm --eval %_rpmdir)

rpm: $(RPM_RPMSDIR)/noarch/python2-iml-common-$(VERSION)-1.el7.centos.noarch.rpm

srpm: python-iml-common-$(VERSION)-1.el7.centos.src.rpm

python-iml-common-$(VERSION)-1.el7.centos.src.rpm: iml-common-$(VERSION).spec
	rpmbuild -bs --define %_srcrpmdir\ $$PWD --define %_sourcedir\ dist $<

spec: iml-common-$(VERSION).spec

dist: dist/iml-common-$(VERSION).tar.gz

version:
	@echo $(VERSION)

copr_rpm: python-iml-common-$(VERSION)-1.el7.centos.src.rpm
	set -e;                                                    \
	if [ -z "$(COPR_OWNER)" -o                                 \
	     -z "$(COPR_PROJECT)" ]; then                          \
	    echo "ERROR:";                                         \
	    echo "COPR_OWNER and COPR_PROJECT need to be defined"; \
	    echo "You can add them to a Makefile.local";           \
	    exit 1;                                                \
	fi
	copr-cli build $(COPR_OWNER)/$(COPR_PROJECT) $<

$(RPM_RPMSDIR)/noarch/python2-iml-common-$(VERSION)-1.el7.centos.noarch.rpm: iml-common-$(VERSION).spec
	rpmbuild -bb $<

iml-common-$(VERSION).spec: dist/iml-common-$(VERSION).tar.gz Makefile
	pyp2rpm -p 2 -d $(RPM_TOPDIR) $< | sed -e "s/^Source0:.*/Source0:        iml-common-$(VERSION).tar.gz/" -e 's/python-setuptools-scm/python2-setuptools_scm/g' > $@

dist/iml-common-$(VERSION).tar.gz:
	python setup.py sdist

clean:
	rm -rf dist iml-common-*.spec

tags:
	ctags -R .
