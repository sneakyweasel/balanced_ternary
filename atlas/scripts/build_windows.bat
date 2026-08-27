@echo off
setlocal EnableDelayedExpansion
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" || exit /b 1

if not defined CUDA_PATH (
  set "CUDA_ROOT=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA"
  for /d %%D in ("%CUDA_ROOT%\v*") do set "CUDA_PATH=%%D"
)
if not exist "%CUDA_PATH%\bin\nvcc.exe" (
  echo CUDA nvcc not found. Set CUDA_PATH or install CUDA 12.8+.
  exit /b 1
)
set "PATH=%CUDA_PATH%\bin;%PATH%"
echo Using CUDA_PATH=%CUDA_PATH%

set "CMAKE=C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe"
set "NINJA=C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\IDE\CommonExtensions\Microsoft\CMake\Ninja\ninja.exe"
set "NVCC=%CUDA_PATH%\bin\nvcc.exe"
set "NVCC_CMAKE=%NVCC:\=/%"

cd /d "%~dp0..\.."
"%CMAKE%" -S atlas -B atlas/build -G Ninja -DCMAKE_MAKE_PROGRAM="%NINJA%" -DCMAKE_CUDA_COMPILER="%NVCC_CMAKE%"
if errorlevel 1 exit /b 1
"%CMAKE%" --build atlas/build
if errorlevel 1 exit /b 1
atlas\build\juggler-atlas-tests.exe
exit /b %ERRORLEVEL%
