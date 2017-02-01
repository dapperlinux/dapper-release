# dapper-release

##About
The Dapper Release package contains version information for the Dapper Linux distribution. It also contains system service overrides that create the workstation version of Dapper Linux.

Dapper-Release is based on the generic-release package.


##Building
To build this package, first install an RPM development chain:

```bash
$ sudo dnf install fedora-packager fedora-review

```

Next, setup rpmbuild directories with

```bash
$ rpmdev-setuptree
```
And place the file dapper-release.spec in the SPECS directory, and all the rest of the files in the SOURCES directory like so:
```bash
$ mv dapper-release.spec ~/rpmbuild/SPECS/
$ mv * ~/rpmbuild/SOURCES/
```

and finally, you can build RPMs and SRPMs with:
```bash
$ cd ~/rpmbuild/SPECS
$ rpmbuild -ba dapper-release.spec
```


