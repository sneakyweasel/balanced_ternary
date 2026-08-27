@echo off
setlocal EnableDelayedExpansion
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" || exit /b 1

if defined CUDA_PATH if exist "!CUDA_PATH!\bin\nvcc.exe" goto :cuda_ok
if defined CUDA_HOME if exist "!CUDA_HOME!\bin\nvcc.exe" (
  set "CUDA_PATH=!CUDA_HOME!"
  goto :cuda_ok
)
set "CUDA_ROOT=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA"
set "CUDA_PATH="
for /f "delims=" %%D in ('dir /b /ad /o-n "!CUDA_ROOT!\v*" 2^>nul') do (
  if exist "!CUDA_ROOT!\%%D\bin\nvcc.exe" (
    set "CUDA_PATH=!CUDA_ROOT!\%%D"
    goto :cuda_ok
  )
)
echo CUDA nvcc not found. Set CUDA_PATH or install CUDA 12.8+.
exit /b 1

:cuda_ok
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
