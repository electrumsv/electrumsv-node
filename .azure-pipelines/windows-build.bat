echo on

call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Enterprise\VC\Auxiliary\Build\vcvars64.bat"

set VCPKG_ROOT=%VCPKG_INSTALLATION_ROOT%
set BITCOIN_SV_REVISION=bugfix/cmake-windows-build
set BITCOIN_SV_REPO=https://github.com/electrumsv/bitcoin-sv

git clone --depth=1 --branch %BITCOIN_SV_REVISION% %BITCOIN_SV_REPO%

pushd bitcoin-sv
mkdir build
cd build

REM warning C4146: unary minus operator applied to unsigned type, result still unsigned
REM warning C4244: 'return': conversion from 'int64_t' to 'double', possible loss of data
REM warning C4267: 'function': conversion from 'size_t' to 'uint32_t', possible loss of data
REM warning C4805: '|': unsafe mix of type 'uint32_t' and type 'bool' in operation

%VCPKG_ROOT%\vcpkg.exe install "@%vcpkgInstallParamFile%"
cmake -DCMAKE_TOOLCHAIN_FILE=%VCPKG_ROOT%\scripts\buildsystems\vcpkg.cmake  -G "Visual Studio 16 2019" -Ax64 -DVCPKG_TARGET_TRIPLET=x64-windows-static -DCMAKE_BUILD_TYPE=Release -DBUILD_BITCOIN_WALLET=OFF -DBUILD_BITCOIN_BENCH=OFF -DUNIVALUE_BUILD_TESTS=OFF -DLEVELDB_BUILD_TESTS=OFF ..
msbuild BitcoinSV.sln /p:Configuration=Release /p:Platform="x64" /nowarn:"C4244,C4267,C4805,C4146"

popd
