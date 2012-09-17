@echo off
rem figure out where we are
for %%I in ( %0\..\.. ) do set WORKDIR=%%~fI

set PY_MAJ=2
if not "%1" == "" set PY_MAJ=%1
set PY_MIN=5
if not "%2" == "" set PY_MIN=%2
set BUILD_TYPE=Release
if not "%3" == "" set BUILD_TYPE=%3
if not "%4" == "" set SVN_VER_MAJ_MIN=%4
if "%SVN_VER_MAJ_MIN%" == "" set /p SVN_VER_MAJ_MIN=Build Version:
if "%SVN_VER_MAJ_MIN%" == "" goto :eof

rem Save CWD
pushd .

rem in development the version info can be found
rem otherwise the builder will have run it already
if "%PY_MIN%" == "4" set COMPILER=msvc71
if "%PY_MIN%" == "5" set COMPILER=msvc71
if "%PY_MIN%" == "6" set COMPILER=msvc71

if exist ..\..\ReleaseEngineering\win32-%COMPILER%\software-versions-%SVN_VER_MAJ_MIN%.cmd (
    pushd ..\..\ReleaseEngineering\win32-%COMPILER%
    call software-versions-%SVN_VER_MAJ_MIN%.cmd off
    popd
    )

set PYCXX=%WORKDIR%\Import\pycxx-%PYCXX_VER%
set OPENSSL=%TARGET%\openssl-%OPENSSL_VER%
set SUBVERSION=%TARGET%\subversion-%SVN_VER%
set APR=%SUBVERSION%
set PY=c:\python%PY_MAJ%%PY_MIN%
set PYLIB=python%PY_MAJ%%PY_MIN%
set PYTHONPATH=%WORKDIR%\Source
set PYTHON=%PY%\python.exe
set wc_SVNVERSION=L:\BuildRoot\Win32-MSVC71-1.4.6\subversion-1.4.6\Release\bin\svnversion.exe

rem Need python and SVN on the path
PATH %PY%;%SUBVERSION%\%BUILD_TYPE%\bin;%PATH%

rem prove the python version selected
python -c "import sys;print 'Info: Python Version',sys.version"

rem restore original CWD
popd
