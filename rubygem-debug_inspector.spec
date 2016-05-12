%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from debug_inspector-0.0.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name debug_inspector

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.0.2
Release: 6%{?dist}
Summary: A Ruby wrapper for the MRI 2.0 debug_inspector API
Group: Development/Languages
License: MIT
URL: https://github.com/banister/debug_inspector
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

Requires:      %{?scl_prefix_ruby}ruby(release)
Requires:      %{?scl_prefix_ruby}ruby(rubygems)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby-devel
Provides:      %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
A Ruby wrapper for the MRI 2.0 debug_inspector API.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%build
# Create the gem as gem install only works on a gem file
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/

chmod -x %{buildroot}%{gem_dir}/gems/%{gem_name}-%{version}/Rakefile

%check
%{?scl:scl enable %{scl} - << \EOF}
set -e
pushd .%{gem_instdir}
# No upstream test suite available :/ but we can do some smoke test :)
ruby -Ilib:$(dirs +1)%{gem_extdir_mri} - << \EOR | grep '#<Class:RubyVM::DebugInspector>'
  require 'debug_inspector'

  # Open debug context
  # Passed `dc' is only active in a block
  RubyVM::DebugInspector.open { |dc|
    # backtrace locations (returns an array of Thread::Backtrace::Location objects)
    locs = dc.backtrace_locations

    # class of i-th caller frame
    p dc.frame_class(0)
  }
EOR
popd
%{?scl:EOF}

%files
%doc %{gem_instdir}/README.md
%dir %{gem_instdir}
%{gem_libdir}
%{gem_extdir_mri}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Rakefile
%{gem_instdir}/debug_inspector.gemspec

%changelog
* Wed Apr 06 2016 Pavel Valena <pvalena@redhat.com> - 0.0.2-6
- Add scl macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 07 2016 Vít Ondruch <vondruch@redhat.com> - 0.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 23 2015 Vít Ondruch <vondruch@redhat.com> - 0.0.2-2
- Update to recent guidelines + review fixes.

* Mon May 06 2013 Anuj More - 0.0.2-1
- Initial package
