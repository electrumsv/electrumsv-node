REM Unless echo is disabled for the vswhere loop, it prints every command.
echo off

REM %1 - path to checkout and build Bitcoin SV in.

set VSINSTALL_PATH=
set VSWHERE_PATH=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe
for /f "usebackq tokens=1* delims=: " %%i in (`"%VSWHERE_PATH%" -latest -requires Microsoft.Component.MSBuild`) do (
  if /i "%%i"=="installationPath" set VSINSTALL_PATH=%%j
)
if "%VSINSTALL_PATH%" EQU "" (
  exit /b 1
)

REM Re-enable echo for the rest of the script.
echo on
if "%vcpkg.arch%" EQU "x86" (
  set VCPKG_CMAKE_ARCH=Win32
  call "%VSINSTALL_PATH%\VC\Auxiliary\Build\vcvars32.bat"
) else if "%vcpkg.arch%" EQU "x64" (
  set VCPKG_CMAKE_ARCH=x64
  call "%VSINSTALL_PATH%\VC\Auxiliary\Build\vcvars64.bat"
) else (
  echo VC architecture unrecognised.
  exit /b 1
)

echo on
set VCPKG_ROOT=%VCPKG_INSTALLATION_ROOT%
set BITCOIN_SV_REVISION=bugfix/cmake-windows-build-1.0.13
set BITCOIN_SV_REPO=https://github.com/electrumsv/bitcoin-sv

git clone --depth=1 --branch %BITCOIN_SV_REVISION% %BITCOIN_SV_REPO% %1

pushd %1
mkdir build
cd build

REM warning C4146: unary minus operator applied to unsigned type, result still unsigned
REM warning C4244: 'return': conversion from 'int64_t' to 'double', possible loss of data
REM warning C4267: 'function': conversion from 'size_t' to 'uint32_t', possible loss of data
REM warning C4309: 'argument': truncation of constant value
REM warning C4805: '|': unsafe mix of type 'uint32_t' and type 'bool' in operation
REM warning C4834: discarding return value of function with 'nodiscard' attribute
REM warning C4996: 'fopen': This function or variable may be unsafe. Consider using fopen_s instead.

REM -DBUILD_BITCOIN_WALLET=OFF
REM These change the build from MT_StaticRelease to MD_DynamicRelease, and result in linker errors with Boost and more. But this is how we would generate pdbs.
REM -DCMAKE_CXX_FLAGS_RELEASE="/Zi" -DCMAKE_SHARED_LINKER_FLAGS_RELEASE="/DEBUG /OPT:REF /OPT:ICF"

%VCPKG_ROOT%\vcpkg.exe install "@%vcpkgInstallParamPath%\%vcpkg.arch%-windows-static.txt"
REM https://cmake.org/cmake/help/latest/generator/Visual%20Studio%2016%202019.html
cmake --version
REM There's some problem with cmake where it does not stick to the given Windows SDK version when finding SHLWAPI, and instead looks at the latest (Windows 11) SDK path to find those.
REM We override those explicitly by forcing explicit selection of the correct files.
cmake -DCMAKE_TOOLCHAIN_FILE=%VCPKG_ROOT%\scripts\buildsystems\vcpkg.cmake  -G "Visual Studio 17 2022" -A %VCPKG_CMAKE_ARCH% -DVCPKG_TARGET_TRIPLET=%vcpkg.arch%-windows-static -DCMAKE_BUILD_TYPE=Release -DCMAKE_SYSTEM_VERSION="10.0.22000.0" -DBUILD_BITCOIN_BENCH=OFF -DBUILD_BITCOIN_ZMQ=ON -DUNIVALUE_BUILD_TESTS=OFF -DLEVELDB_BUILD_TESTS=OFF -DSHLWAPI_INCLUDE_DIR="C:\Program Files (x86)\Windows Kits\10\Include\10.0.22000.0\um" -DSHLWAPI_LIBRARY="C:\Program Files (x86)\Windows Kits\10\Lib\10.0.22000.0\um\x64\ShLwApi.Lib" ..
if not exist "BitcoinSV.sln" (
  exit /b 1
)
msbuild BitcoinSV.sln /p:Configuration=Release /p:Platform="%VCPKG_CMAKE_ARCH%" /nowarn:"C4146,C4244,C4309,C4267,C4805,C4834,C4996"

popd
