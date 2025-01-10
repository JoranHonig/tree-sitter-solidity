VERSION := 1.2.10

LANGUAGE_NAME := tree-sitter-solidity

# repository
SRC_DIR := src

PARSER_REPO_URL := $(shell git -C $(SRC_DIR) remote get-url origin 2>/dev/null)

ifeq ($(PARSER_URL),)
	PARSER_URL := $(subst .git,,$(PARSER_REPO_URL))
ifeq ($(shell echo $(PARSER_URL) | grep '^[a-z][-+.0-9a-z]*://'),)
	PARSER_URL := $(subst :,/,$(PARSER_URL))
	PARSER_URL := $(subst git@,https://,$(PARSER_URL))
endif
endif

TS ?= tree-sitter

# ABI versioning
SONAME_MAJOR := $(word 1,$(subst ., ,$(VERSION)))
SONAME_MINOR := $(word 2,$(subst ., ,$(VERSION)))

# Detect OS and Architecture for HOMEBREW_PREFIX
ifeq ($(shell uname -s),Darwin)
  ifeq ($(shell uname -m),arm64)
    # Apple Silicon
    HOMEBREW_PREFIX ?= /opt/homebrew
  else
    # Intel
    HOMEBREW_PREFIX ?= /usr/local
  endif
else
  HOMEBREW_PREFIX ?= /usr/local
endif

# install directory layout
PREFIX ?= $(HOMEBREW_PREFIX)
INCLUDEDIR ?= $(PREFIX)/include
LIBDIR ?= $(PREFIX)/lib
PCLIBDIR ?= $(LIBDIR)/pkgconfig

# object files
OBJS := $(patsubst %.c,%.o,$(wildcard $(SRC_DIR)/*.c))

# flags
ARFLAGS := rcs
override CFLAGS += -I$(SRC_DIR) -std=c11 -fPIC
LDFLAGS += -L$(LIBDIR)

# OS-specific bits
ifeq ($(OS),Windows_NT)
  $(error "Windows is not supported")
else ifeq ($(shell uname),Darwin)
  SOEXT = dylib
  SOEXTVER_MAJOR = $(SONAME_MAJOR).dylib
  SOEXTVER = $(SONAME_MAJOR).$(SONAME_MINOR).dylib
  LINKSHARED := $(LINKSHARED)-dynamiclib -Wl,
  ifneq ($(ADDITIONAL_LIBS),)
    LINKSHARED := $(LINKSHARED)$(ADDITIONAL_LIBS),
  endif
  LINKSHARED := $(LINKSHARED)-install_name,$(LIBDIR)/lib$(LANGUAGE_NAME).$(SONAME_MAJOR).dylib,-rpath,@executable_path/../Frameworks
else
  SOEXT = so
  SOEXTVER_MAJOR = so.$(SONAME_MAJOR)
  SOEXTVER = so.$(SONAME_MAJOR).$(SONAME_MINOR)
  LINKSHARED := $(LINKSHARED)-shared -Wl,
  ifneq ($(ADDITIONAL_LIBS),)
    LINKSHARED := $(LINKSHARED)$(ADDITIONAL_LIBS)
  endif
  LINKSHARED := $(LINKSHARED)-soname,lib$(LANGUAGE_NAME).so.$(SONAME_MAJOR)
endif

all: lib$(LANGUAGE_NAME).a lib$(LANGUAGE_NAME).$(SOEXT) $(LANGUAGE_NAME).pc

lib$(LANGUAGE_NAME).a: $(OBJS)
	$(AR) $(ARFLAGS) $@ $^

lib$(LANGUAGE_NAME).$(SOEXT): $(OBJS)
	$(CC) $(LDFLAGS) $(LINKSHARED) $^ $(LDLIBS) -o $@
ifneq ($(STRIP),)
	$(STRIP) $@
endif

$(LANGUAGE_NAME).pc: bindings/c/$(LANGUAGE_NAME).pc.in
	sed  -e 's|@URL@|$(PARSER_URL)|' \
		-e 's|@VERSION@|$(VERSION)|' \
		-e 's|@LIBDIR@|$(LIBDIR)|' \
		-e 's|@INCLUDEDIR@|$(INCLUDEDIR)|' \
		-e 's|@REQUIRES@|$(REQUIRES)|' \
		-e 's|@ADDITIONAL_LIBS@|$(ADDITIONAL_LIBS)|' \
		-e 's|=$(PREFIX)|=$${prefix}|' \
		-e 's|@PREFIX@|$(PREFIX)|' $< > $@

$(SRC_DIR)/parser.c: grammar.js
	$(TS) generate --no-bindings

install: all
	install -d '$(DESTDIR)$(INCLUDEDIR)'/tree_sitter '$(DESTDIR)$(PCLIBDIR)' '$(DESTDIR)$(LIBDIR)'
	install -m644 bindings/c/$(LANGUAGE_NAME).h '$(DESTDIR)$(INCLUDEDIR)'/tree_sitter/$(LANGUAGE_NAME).h
	install -m644 $(LANGUAGE_NAME).pc '$(DESTDIR)$(PCLIBDIR)'/$(LANGUAGE_NAME).pc
	install -m644 lib$(LANGUAGE_NAME).a '$(DESTDIR)$(LIBDIR)'/lib$(LANGUAGE_NAME).a
	install -m755 lib$(LANGUAGE_NAME).$(SOEXT) '$(DESTDIR)$(LIBDIR)'/lib$(LANGUAGE_NAME).$(SOEXTVER)
	ln -sf lib$(LANGUAGE_NAME).$(SOEXTVER) '$(DESTDIR)$(LIBDIR)'/lib$(LANGUAGE_NAME).$(SOEXTVER_MAJOR)
	ln -sf lib$(LANGUAGE_NAME).$(SOEXTVER_MAJOR) '$(DESTDIR)$(LIBDIR)'/lib$(LANGUAGE_NAME).$(SOEXT)

uninstall:
	$(RM) '$(DESTDIR)$(LIBDIR)'/lib$(LANGUAGE_NAME).a \
		'$(DESTDIR)$(LIBDIR)'/lib$(LANGUAGE_NAME).$(SOEXTVER) \
		'$(DESTDIR)$(LIBDIR)'/lib$(LANGUAGE_NAME).$(SOEXTVER_MAJOR) \
		'$(DESTDIR)$(LIBDIR)'/lib$(LANGUAGE_NAME).$(SOEXT) \
		'$(DESTDIR)$(INCLUDEDIR)'/tree_sitter/$(LANGUAGE_NAME).h \
		'$(DESTDIR)$(PCLIBDIR)'/$(LANGUAGE_NAME).pc

clean:
	$(RM) $(OBJS) $(LANGUAGE_NAME).pc lib$(LANGUAGE_NAME).a lib$(LANGUAGE_NAME).$(SOEXT)

test:
	$(TS) test

.PHONY: all install uninstall clean test
