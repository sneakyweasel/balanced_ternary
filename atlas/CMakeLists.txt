cmake_minimum_required(VERSION 3.24)
project(juggler_atlas LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Safe default before enable_language. Replaced by sm_120 on CUDA 12.8+.
set(CMAKE_CUDA_ARCHITECTURES "75-virtual")

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/cpp)

include(CheckLanguage)
check_language(CUDA)
if(CMAKE_CUDA_COMPILER)
    enable_language(CUDA)
    set(CMAKE_CUDA_STANDARD 20)
    set(JUGGLER_ATLAS_HAVE_CUDA 1)
    if(CMAKE_CUDA_COMPILER_VERSION VERSION_GREATER_EQUAL "12.8")
        set(JA_CUDA_ARCH "120")
    else()
        set(JA_CUDA_ARCH "75-virtual")
    endif()
    message(STATUS "juggler_atlas: CUDA ${CMAKE_CUDA_COMPILER_VERSION}, arch ${JA_CUDA_ARCH}")
else()
    set(JUGGLER_ATLAS_HAVE_CUDA 0)
    set(JA_CUDA_ARCH "")
    message(STATUS "juggler_atlas: CUDA toolkit not found; CPU census only")
endif()

add_library(juggler_atlas_cpu STATIC
    cpp/census.cpp
    cpp/harvest.cpp
)

add_executable(juggler-atlas-census
    cpp/main.cpp
)
target_link_libraries(juggler-atlas-census PRIVATE juggler_atlas_cpu)

if(JUGGLER_ATLAS_HAVE_CUDA)
    target_sources(juggler-atlas-census PRIVATE
        cuda/trajectory_kernel.cu
        cuda/harvest_kernel.cu
    )
    target_compile_definitions(juggler-atlas-census PRIVATE JUGGLER_ATLAS_CUDA=1)
    set_target_properties(juggler-atlas-census PROPERTIES
        CUDA_ARCHITECTURES "${JA_CUDA_ARCH}"
        CUDA_SEPARABLE_COMPILATION OFF
    )
endif()

add_executable(juggler-atlas-tests
    tests/test_runner.cpp
    tests/test_packed_word.cpp
    tests/test_juggler_map.cpp
    tests/test_census.cpp
    tests/test_harvest.cpp
)
target_include_directories(juggler-atlas-tests PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/tests)
target_link_libraries(juggler-atlas-tests PRIVATE juggler_atlas_cpu)

enable_testing()
add_test(NAME juggler_atlas_cpu_tests COMMAND juggler-atlas-tests)
